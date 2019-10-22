#!/usr/bin/env python
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
parser.add_argument('-p','--profile', type=str, help='profile')
parser.add_argument('-c','--configure', type=str, help='configure options')
parser.add_argument('-x','--socks5', action='store_true', help='use SOCKS5 proxy on localhost port 5555')
parser.add_argument('-v','--version', action='version', version=__version__)

# Commands Parser
subparsers = parser.add_subparsers(title='commands', description='Valid NOW CLI commands', help='command help')

# IM Command Parser
im_parser = subparsers.add_parser('im', description='Incident Management Command')

# EM Command Parser
em_parser = subparsers.add_parser('em', description='Event Management Command')

# Parse Arguments
args = parser.parse_args()

# Set the entry point
if __name__ == '__main__':
	main()