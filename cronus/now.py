#!/usr/bin/python3
# -*- coding: utf-8 -*-

__version__ = "1.0.0"

import logging
import argparse
import requests
import urllib3

import cronus.configure as configure
import cronus.event as event
import cronus.incident as incident

def main():
    if args.cmd == "configure":
        configure.main(args)
    elif args.cmd == "im":
	    incident.main()
    elif args.cmd == "em":
	    event.main()
    else:
        exit()
    
# Top Level Parser
parser = argparse.ArgumentParser(description="ServiceNow (NOW) Command Line Interface (CLI)", prog='now')
parser.add_argument('-p','--profile', type=str, help='profile')
parser.add_argument('-x','--socks5', type=str, help='use SOCKS5 proxy on localhost port 5555')
parser.add_argument('-v','--version', action='version', version=__version__)

# Commands Parser
commands_parser = parser.add_subparsers(help='commands', dest='cmd')

# Configure Parser
im_parser = commands_parser.add_parser('configure', help='configure profile')

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