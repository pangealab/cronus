# Local Imports
from cronus import properties
from cronus import profile

# Repo Imports
import logging
import configparser

# Set Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    print("Called Incident...")