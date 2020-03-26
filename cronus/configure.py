# Local Imports
from cronus import properties

# Repo Imports
import configparser
import logging
import os
import sys

# Set Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(args):

    path_exists = os.path.exists(properties.NOW_PATH)
    file_exists = os.path.isfile(properties.NOW_CONFIG)

    if not path_exists:
        print ("Called create path...")
        create_path()

    if not file_exists:
        init_config()
    
    if args.get:
        get_config(args)
        exit()

    if args.set:
        set_config(args)
        exit()

    edit_config(args)

def init_config():

    # Initialize the parser with defaults
    config = configparser.ConfigParser(
    defaults={'table_api':'/api/now/table',
              'cmdb_api':'/api/x_snc_labs_atlas/v1/register/services',
              'em_api':'/api/x_snc_labs_atlas/v1/create/event'
               })
    with open(properties.NOW_CONFIG, 'w') as configfile:
        config.write(configfile)

def edit_config(args):

    # Get Config Parser
    config = configparser.ConfigParser()
    config.read(properties.NOW_CONFIG)

    # Edit the DEFAULT section if no PROFILE provided
    if not args.profile:
        defaults = config.defaults()
        # Run through the STANDARD options
        for key in properties.OPTION_NAMES:
            if key in defaults:
                # Overwrite with user input
                new_value = input(key + " [" + defaults[key] + "]: ")
                if new_value:
                    defaults[key]=new_value
        with open(properties.NOW_CONFIG, 'w') as configfile:
            config.write(configfile)
    else:
        # Edit the PROFILE section if it exists
        if config.has_section(args.profile):
            items = config[args.profile]
            # Run through the STANDARD options
            for key in properties.OPTION_NAMES:
                if key in items:
                    # Overwrite with user input
                    new_value = input(key + " [" + items[key] + "]: ")
                    if new_value:
                        items[key]=new_value
            with open(properties.NOW_CONFIG, 'w') as configfile:
                config.write(configfile)
        # Create the PROFILE section if it does not exists
        else:
            config.add_section(args.profile)
            items = config[args.profile]
            # Run through the STANDARD options
            for key in properties.OPTION_NAMES:
                if key in items:
                    # Overwrite with user input
                    new_value = input(key + " [" + items[key] + "]: ")
                    if new_value:
                        items[key]=new_value
                # Create new options
                else:
                    value = input(key + " []: ")
                    items[key]=value
            with open(properties.NOW_CONFIG, 'w') as configfile:
                config.write(configfile)

def get_config(args):

    # Get Config Parser
    config = configparser.ConfigParser()
    config.read(properties.NOW_CONFIG)
   
    # Get Section
    section = args.get.split(".",1)[0]

    # Make DEFAULT section Uppercase
    if section == 'default':
        section = section.upper()

    # Get Key and Value
    key = args.get.split(".",1)[1]
    value = config.get(section,key)

    # Print Result
    print(key + " [" + value + "]")

def set_config(args):

    # Get Config Parser
    config = configparser.ConfigParser()
    config.read(properties.NOW_CONFIG)

    # Get Section
    section = args.set.split(".",1)[0]

    # Make DEFAULT section Uppercase
    if section == 'default':
        section = section.upper()

    # Create Section if not present
    if not config.has_section(section):
        config.add_section(section)

    # Get Key and Value
    keyvalue = args.set.split(".",1)[1]
    key = keyvalue.split("=",1)[0]
    value = keyvalue.split("=",1)[1]

    # Set Config
    config.set(section, key, value)

    # Save Config
    with open(properties.NOW_CONFIG, 'w') as configfile:
                config.write(configfile)

    # Print Result
    print(key + " [" + value + "]")

def create_path():  
    os.makedirs(properties.NOW_PATH, exist_ok = True)