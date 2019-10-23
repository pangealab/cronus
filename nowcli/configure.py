import configparser
from os.path import expanduser

def main():
    print("Called Configure...")
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'key1': 'value1',
        'key2': 'value2',
        'key3': 'value3'}
    config['newyorkdemo01'] = {}
    topsecret = config['newyorkdemo01']
    topsecret['url'] = 'https://newyorkdemo01.service-now.com'     # mutates the parser
    topsecret['username'] = 'devops'
    topsecret['password'] = 'changeit'
    home = expanduser("~")
    with open(home+'/.now/credentials', 'w') as configfile:
        config.write(configfile)