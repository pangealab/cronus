import configparser
import logging
import os

# Set Vars
USER_HOME = os.path.expanduser("~")
NOW_DIR = ".now"
NOW_FILE = "credentials"
NOW_PATH = USER_HOME + "/" + NOW_DIR
NOW_CONFIG = NOW_PATH + "/" + NOW_FILE
NOW_DEFAULT = "default"

# Set Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(args):

    path_exists = os.path.exists(NOW_PATH)
    file_exists = os.path.isfile(NOW_CONFIG)
    
    if not path_exists:
        create_path()

    if not file_exists:
        init_config()
    else:
        edit_config(args)

def init_config():
    config = configparser.ConfigParser()
    config[NOW_DEFAULT] = {
        'api': '"/api/now/table"',
        'http_headers': '{"Content-Type":"application/json","Accept":"application/json"}',
        'params': '"sysparm_limit=10000"'}
    with open(NOW_CONFIG, 'w') as configfile:
        config.write(configfile)

def edit_config(args):
    config = configparser.ConfigParser()
    config.read(NOW_CONFIG)

    if not args.profile:
        args.profile = NOW_DEFAULT

    if not config.has_section(args.profile):
        print(args.profile + " section does not exist")
    else:
        for key, value in config.items(args.profile):
            new_value = input(key + " [" + value + "]: ")
            if new_value:
                value = new_value
def create_path():
    os.makedirs(NOW_PATH, exist_ok = True)