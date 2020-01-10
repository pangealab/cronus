# Local Imports
from cronus import properties

# Repo Imports
import profile
import logging
import configparser

# Set Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    print("Called Event ...")