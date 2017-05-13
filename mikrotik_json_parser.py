import json
import socket
import select
import sys

from mikrotik_api import ApiRos


def parse_config_file():
    with open('config.json') as json_data_file:
        conf = json.load(json_data_file)
        for i in conf.iteritems():
            yield i


def connection_test():
    devices = parse_config_file()
    for dev in devices:
        x = dev[1]['host']

        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((x, 8728))

        # Create apiros instance
        apiros = ApiRos(sock)
        apiros.login(dev[1]['user'], dev[1]['passwd'])

        output = apiros.execute(["/system/package/update/print"])
        print output

    sock.close()

if __name__ == '__main__':
    connection_test()