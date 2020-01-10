# Local Imports
from cronus import properties
from cronus import profile

# Repo Imports
import logging
import configparser
import requests
import json

# Set Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(args):

    print("Called CMDB...")

    # Get Profile Props
    props = profile.get_props(args.profile)

    # Build Request
    headers = properties.HEADERS
    data = open(args.data,'rb')
    url = props["server"]+props["cmdb_api"]
    username = props["username"]
    password = props["password"]
    r = requests.post(url, headers=headers, data=data, auth=(username,password),timeout=60)
    print(r.json())