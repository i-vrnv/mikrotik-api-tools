import socket
import time
import mikrotik_json_parser

from mikrotik_api import ApiRos


def backup():
    # Get data from config
    devices = mikrotik_json_parser.parse_config_file()
    for dev in devices:
        # Create socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((dev[1]['host'], 8728))
        # Create apiros instance
        apiros = ApiRos(sock)
        apiros.login(dev[1]['user'], dev[1]['passwd'])
        # Get hostname
        dev_identity = apiros.execute(["/system/identity/print"])['name']
        # Get date
        now = time.strftime("%d-%m-%Y");
        # /system backup save dont-encrypt=yes name={0}
        # TODO: Create command
        apiros.execute([""])
        # /tool fetch address={0} port={1} user={2} password={3}mode=ftp
        # src-path={5}.backup dst-path={4}/{5}.backup upload=yes
        # TODO: Create command
        apiros.execute([""])
        # /file remove {0}
        # TODO: Create command
        apiros.execute(["/file/remove/{0}".format()])

if __name__ == '__main__':
    backup()