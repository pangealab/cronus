#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "1.0.0"

import logging
import argparse
import requests
import urllib3
from tabulate import tabulate

def main():
    print("TODO")

# Set the top-level parser
parser = argparse.ArgumentParser(description="audit a servicenow instance and produce a markdown report")
parser.add_argument('-v','--version', action='version', version=__version__)
parser.add_argument('-s','--server', type=str, help='server')
parser.add_argument('-t','--type', type=str, choices={'scripts','groups','group-roles','sys-user-roles','users'}, help='script audit report')
parser.add_argument('-u','--user', type=str, help='username')
parser.add_argument('-p','--pwd', type=str, help='password')
parser.add_argument('-x','--socks5', action='store_true', help='Use SOCKS5 proxy on localhost port 5555')
args = parser.parse_args()

# Set the entry point
if __name__ == '__main__':
	main()