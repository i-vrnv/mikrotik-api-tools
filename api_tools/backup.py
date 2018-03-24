import socket
import time

from api_tools.device import Device
from api_tools.ini_parser import Config


def backup():
    # Get data from config
    general = Config().get_general()

    ftp = Config().get_ftp()
    devices = Config().get_devices()

    for dev in devices:

        device = Device(dev['host'], 8728, dev['username'], dev['password'])

        # Get date
        now = time.strftime("%d-%m-%Y")
        # Get hostname
        dev_identity = device.execute(["/system/identity/print"])['name']

        # Set fullname
        backup_fullname = "{0}-{1}".format(dev_identity, now)

        # Create backup file
        device.execute(["/system/backup/save",
                        "=dont-encrypt=yes",
                        "=name={0}".format(backup_fullname)])

        # Sleep while device working
        time.sleep(1)

        # Upload backup to ftp
        device.execute(["/tool/fetch",
                        "=upload=yes",
                        "=address={0}".format(ftp['host']),
                        "=port={0}".format(ftp['port']),
                        "=user={0}".format(ftp['username']),
                        "=password={0}".format(ftp['password']),
                        "=mode=ftp",
                        "=src-path={0}.backup".format(backup_fullname),
                        "=dst-path={0}/{1}.backup".format(dev['dst-path'], backup_fullname)])

        # Sleep while device working
        time.sleep(1)

        # Remove backup file
        device.execute(["/file/remove",
                        "=numbers={0}.backup".format(backup_fullname)])

        # Close socket
        # device.close()


if __name__ == '__main__':
    backup()
