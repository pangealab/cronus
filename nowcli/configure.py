import configparser
import logging
import os
import sys

# Set Vars
USER_HOME = os.path.expanduser("~")
NOW_DIR = ".now"
NOW_FILE = "credentials"
NOW_PATH = USER_HOME + "/" + NOW_DIR
NOW_CONFIG = NOW_PATH + "/" + NOW_FILE
NOW_DEFAULT = "DEFAULT"
OPTION_NAMES = ['api','http_headers','params','server','username','password']

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

    # Initialize the parser with defaults
    config = configparser.ConfigParser(
    defaults={'api':'"/api/now/table"',
              'http_headers':'{"Content-Type":"application/json","Accept":"application/json"}',
              'params':'"sysparm_limit=10000"',
               })
    with open(NOW_CONFIG, 'w') as configfile:
        config.write(configfile)               

def edit_config(args):

    config = configparser.ConfigParser()
    config.read(NOW_CONFIG)

    # Edit the DEFAULT section if no profile provided
    if not args.profile:
        defaults = config.defaults()
        for key in OPTION_NAMES:
            if key in defaults:
                new_value = input(key + " [" + defaults[key] + "]: ")
                if new_value:
                    defaults[key]=new_value
        with open(NOW_CONFIG, 'w') as configfile:
            config.write(configfile)
    else:
        if config.has_section(args.profile):
            items = config[args.profile]
            for key in OPTION_NAMES:
                if key in items:
                    new_value = input(key + " [" + items[key] + "]: ")
                    if new_value:
                        items[key]=new_value
            with open(NOW_CONFIG, 'w') as configfile:
                config.write(configfile)
        else:
            config.add_section(args.profile)
            items = config[args.profile]
            for key in OPTION_NAMES:
                if key in items:
                    new_value = input(key + " [" + items[key] + "]: ")
                    if new_value:
                        items[key]=new_value
                else:
                    value = input(key + " []: ")
                    items[key]=value
            with open(NOW_CONFIG, 'w') as configfile:
                config.write(configfile)            

def create_path():  
    os.makedirs(NOW_PATH, exist_ok = True)