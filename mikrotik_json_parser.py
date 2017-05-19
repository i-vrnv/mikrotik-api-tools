import json
import socket
import select
import sys

from mikrotik_api import ApiRos
from mikrotik_config_parser import Config


def parse_config_file():
    with open('config.json') as json_data_file:
        conf = json.load(json_data_file)
        for i in conf.iteritems():
            # Return generator
            yield i

if __name__ == '__main__':
    connection_test()
