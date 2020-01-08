# Gobal Imports
import os
import sys

# Set Global Variables
USER_HOME = os.path.expanduser("~")
NOW_DIR = ".now"
NOW_FILE = "credentials"
NOW_PATH = USER_HOME + "/" + NOW_DIR
NOW_CONFIG = NOW_PATH + "/" + NOW_FILE
NOW_DEFAULT = "DEFAULT"
OPTION_NAMES = ['api','http_headers','params','server','username','password']