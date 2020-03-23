#!/usr/bin/python3
# -*- coding: utf-8 -*-

__version__ = "1.0.1"

# Local Imports
from cronus import configure
from cronus import cmdb
from cronus import event
from cronus import incident
from cronus import properties

# Repo Imports
import os
import sys
import logging
import argparse
import requests
import urllib3

def main():
    if args.cmd == "configure":
        configure.main(args)
    elif args.cmd == "cmdb":
	    cmdb.main(args)        
    elif args.cmd == "im":
	    incident.main(args)
    elif args.cmd == "em":
	    event.main(args)
    else:
        exit()
    
# Top Level Parser
parser = argparse.ArgumentParser(description="ServiceNow (NOW) Command Line Interface (CLI)", prog='now')
parser.add_argument('-p','--profile', type=str, help='profile')
parser.add_argument('-d','--data', type=str, help='payload')
parser.add_argument('-x','--socks5', type=str, help='use SOCKS5 proxy on localhost port 5555')
parser.add_argument('-v','--version', action='version', version=__version__)

# Commands Parser
commands_parser = parser.add_subparsers(help='commands', dest='cmd')

# Configure Parser
configure_parser = commands_parser.add_parser('configure', help='configure profile')

# CMDB Parser
cmdb_parser = commands_parser.add_parser('cmdb', help='cmdb')
cmdb_parser.add_argument('register-services', help='register services')

# IM Parser
im_parser = commands_parser.add_parser('im', help='incident management')
im_parser.add_argument('get-incidents', help='get incidents')
im_parser.add_argument('update-incident', help='update incident')

# EM Parser
em_parser = commands_parser.add_parser('em', help='event management')
em_parser.add_argument('get-events', help='get events')

# Parse Arguments
args = parser.parse_args()

# Set the entry point
if __name__ == '__main__':
	main()