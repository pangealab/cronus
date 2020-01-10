# Local Imports
from cronus import properties

# Repo Imports
import configparser
import logging

# Set Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_props(profile):

    config = configparser.ConfigParser()
    config.read(properties.NOW_CONFIG)

    # Return the DEFAULT section if no PROFILE provided
    if not profile:
        defaults = config.defaults()
        return defaults
    else:
        # Return the PROFILE section if it exists
        if config.has_section(profile):
            items = config[profile]
            return items
        # Create the PROFILE section if it does not exists
        else:
            defaults = config.defaults()
            return defaults