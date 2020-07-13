# Local Imports
from cronus import properties
from cronus import profile

# Repo Imports
import logging
import configparser
import requests
import time
import json
from halo import Halo
import polling2


# Set Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

debugFlag = False
user = ''
pwd = ''
instanceUrl = ''
spinner = ''

#https://github.com/manrajgrover/halo
def respDebug(tag, response):
    if(debugFlag):
        print(tag+' Status:', response.status_code, ' Headers:', response.headers, ' Response:', response.json());


def _makeCreateCatalogCall(catalogName, templateURL):
    # Set the request parameters, change 1234 to snc
    url = instanceUrl + '/api/1234/cpg_for_now_cli/createCatalog'

    # Set proper headers
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    payload = {
        'templateName': catalogName,
        'templateURL': templateURL
    }

    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd),
                             headers=headers, data=json.dumps(payload))
    # Check for HTTP codes other than 200
    respDebug('_createCatalog', response)
    if response.status_code != 200:
        print('Error!! Status:', response.status_code, 'Headers:',
              response.headers, 'Error Response:', response.json())
        raise Exception('Failure to create catalog');


#get status by looking up the created cataog, assumes name is unique
def _getCatalogCreationStatus(catalogName):
    # Set the request parameters
    data = _getCatalogDetails(catalogName);
    if ('result' in data and len(data['result']) > 0 and data['result'][0]['name'] == catalogName):
        #print('Found catalog:' + catalogName)
        return data['result'][0]['sys_id']

    return ''


def _getCatalogDetails(catalogName):
    # Set the request parameters
    url = instanceUrl + '/api/now/table/sn_cmp_bp_cat_item?sysparm_query=name%3D'+catalogName + \
          '%5Eactive%3Dtrue&sysparm_fields=sys_id%2Cname%2Cactive%2Cblue_print&sysparm_limit=1'

    # Set proper headers
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers)

    # Check for HTTP codes other than 200
    respDebug('_getCreatedCatalog', response)
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:',
              response.headers, 'Error Response:', response.json())
        return ''

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    return data;


def _makeOrderCatalogCall(catalogId, payload):
    print("Ordering catalog")
    # Set the request parameters
    url = instanceUrl + '/api/now/cmp_catalog_api/submitrequest?cat_id='+catalogId

    # Set proper headers
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    # Do the HTTP request
    response = requests.post(url, auth=(user, pwd),
                             headers=headers, data=payload)

    # Check for HTTP codes other than 200
    respDebug('_orderCatalog', response)
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:',
              response.headers, 'Error Response:', response.json())
        raise Exception('Failure to create catalog');

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    return data['number']


def _getCatalogOrderStatus(orderNumber):
    # Set the request parameters
    url = instanceUrl + '/api/now/cmp_catalog_api/status?req_item=' + orderNumber

    # Set proper headers
    headers = {"Content-Type": "application/json",
               "Accept": "application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers)

    # Check for HTTP codes other than 200
    respDebug('_getCatalogOrderStatus', response)
    if response.status_code != 200:
        return 'Waiting'

    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    status = data['state']

    if (str(status) == 'Closed Complete' or 'Complete' in str(status)):
        return 'Success'

    if (str(status) == 'Error'):
       return 'Failed'

    if(data and data['stage'] and data['stage'] == 'Task Created for User'):

        print('Failed to create order, please check the system');
        return 'Failed'

    return 'Waiting'

# this has been replaced with polling util
# def createCatalog(catalogName, armTemplateURL):
#     _createCatalog(catalogName, armTemplateURL)
#     count = 1
#     while count < 500:
#         print('..', end =" ");
#         catalogId = _getCreatedCatalog(catalogName)
#         if catalogId == '':
#             count += 1
#             time.sleep(15)
#         elif catalogId:
#             print('Catalog creation is successful, catalogId:'+catalogId)
#             return catalogId
#     return ''

def createCatalog(catalogName, armTemplateURL):
    spinner = Halo('Creating catalog '+catalogName);
    spinner.start();
    try:
        _makeCreateCatalogCall(catalogName, armTemplateURL)
        spinner.success('Catalog '+catalogName+' created')
    except Exception:
        spinner.fail('Failed to create catalog '+catalogName)
        return;

    spinner.start('Activating catalog '+catalogName);
    try:
        catalogId = polling2.poll(
            lambda: _getCatalogCreationStatus(catalogName),
            check_success= lambda cat_id: cat_id and len(str(cat_id).strip()) > 0,
            step=10,
            max_tries=500,
            log=logging.DEBUG)

        if len(str(catalogId).strip()):
            spinner.success('Successfully activated catalog '+ catalogName);
    except Exception:
        spinner.fail('Failed to activate the catalog '+catalogName);
        return;


def orderCatalog(catalogName, catalogId, orderData):
    spinner = Halo('Ordering catalog '+catalogName);
    spinner.start();

    try:
        orderNumber = _makeOrderCatalogCall(catalogId, orderData)
        if orderNumber:
            spinner.succeed('Order submitted for catalog '+catalogName+' and order number is:'+orderNumber);
    except Exception:
        spinner.fail('Failed to submit order for catalog '+catalogName);
        return;

    spinner.start('Processing order, with order number:'+orderNumber);

    try:
        result = polling2.poll(
            lambda: _getCatalogOrderStatus(orderNumber),
            check_success= lambda status: status == 'Success',
            step=10,
            max_tries=500,
            log=logging.DEBUG)
    except Exception:
        spinner.fail('Failed to provision stack, order failed:'+orderNumber);
        return;

    if result:
        spinner.succeed('Order completed and stack is provisioned successfully');
    else:
        spinner.fail('Failed to provision stack, order failed:'+orderNumber);

def raise_(ex):
    raise ex

# this has been replaced with polling util
# def orderCatalog(catalogId, orderData):
#     global spinner
#     orderNumber = _makeOrderCatalogCall(catalogId, orderData)
#     print('Order placed, orderId:'+orderNumber);
#     count = 1
#     while count < 500:
#         print('..', end =" ");
#         status = _getOrderStatus(orderNumber)
#         if(status == 'Success'):
#             spinner.succeed('Stack creation is successful')
#             print('Stack creation is successful')
#             break;
#         elif(status == 'Failed'):
#             spinner.fail("Failed to create order, please check the system")
#             print('Failed to create order, please check the system');
#             break;
#         print ('..', end =" ");
#         time.sleep(15)
#         count += 1

def check():
    spinner = Halo('Creating catalog');
    spinner.start();
    time.sleep(3);
    spinner.succeed('Create request accepted')
    spinner.start('Activating')
    time.sleep(3);
    spinner.succeed('Activated succesfully')


def main(args):
    global debugFlag;
    global  spinner

    if args.debug:
        debugFlag = True;

    if debugFlag:
        print("Called Cpg..., args:"+str(args))

    # Get Profile Props
    props = profile.get_props(args.profile)

    # Build Request
    #headers = properties.HEADERS

    global instanceUrl
    global user
    global pwd

    instanceUrl = props["server"]
    user = props["username"]
    pwd = props["password"]

    if args.action == 'create-catalog':
        start_time = time.time()
        with open(args.data) as f:
            payload = json.load(f)

        templateURL = payload['template_url']
        catalogName = payload['catalog_name']
        catalogId = createCatalog(catalogName, templateURL)

        print('Catalog created successfully. Catalog Id:', str(catalogId))
        if debugFlag:
            print("Time taken: --- %s seconds ---" % (time.time() - start_time))

    elif args.action == 'order-catalog':
        r = Timer();

        start_time = time.time()
        with open(args.data) as f:
            payload = json.load(f)

        catalogId = ''
        if 'catalog_id' in payload:
            catalogId = payload['catalog_id']

        payloadData = payload['order_data']

        if 'catalog_name' in payload:
            catalogName = payload['catalog_name']

            if catalogName and len(catalogName.strip())>0:
                catalogDetails = _getCatalogDetails(catalogName);
                if catalogDetails['result'] and len(catalogDetails['result']) > 0 and catalogDetails['result'][0]['sys_id']:
                    catalogId = catalogDetails['result'][0]['sys_id']

        try:
            orderCatalog(catalogName , catalogId, json.dumps(payloadData))
            spinner.succeed('Stack created successfully')
        except Exception:
            spinner.fail('Catalog order failed')

        if debugFlag:
            print("Time taken: --- %s seconds ---" % (time.time() - start_time))

    elif args.action == 'check':
        check()