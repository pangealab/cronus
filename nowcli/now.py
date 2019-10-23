#!/usr/bin/python3
# -*- coding: utf-8 -*-

__version__ = "1.0.0"

import logging
import argparse
import requests
import urllib3

# Local Modules
import configure

def main():
    configure.main()

# Top Level Parser
parser = argparse.ArgumentParser(description="ServiceNow (NOW) Command Line Interface (CLI)", prog='now')
# parser.add_argument('configure', type=str, help='configure options')
# parser.add_argument('-p','--profile', type=str, help='profile')
# parser.add_argument('-x','--socks5', action='store_true', help='use SOCKS5 proxy on localhost port 5555')
# parser.add_argument('-v','--version', action='version', version=__version__)

commands_parser = parser.add_subparsers(help='commands')

# IM Parser
im_parser = commands_parser.add_parser('im', help='incident management')
im_parser.add_argument('create-incident', help='create an incident')

# EM Parser
em_parser = commands_parser.add_parser('em', help='event management')
em_parser.add_argument('create-event', help='create an event')

# Parse Arguments
args = parser.parse_args()

# Set the entry point
if __name__ == '__main__':
	main()