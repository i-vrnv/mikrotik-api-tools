import socket

from api_tools.api import ApiRos


class MtDevice(object):
    """
    This class contain information about device
    """
    def __init__(self, host, port, username, password):
        """
        :param apiros: instance of ApiROS class
        """

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, 8728))

        # Create apiros instance
        self.apiros = ApiRos(sock)
        self.apiros.login(username, password)

        self.identity = self.get_identity()
        info = self.get_info()
        self.factory_firmware = info['factory-firmware']
        self.firmware_type = info['firmware-type']
        self.routerboard = info['routerboard']
        self.serial_number = info['serial-number']
        self.upgrade_firmware = info['upgrade-firmware']
        self.model = info['model']
        self.current_firmware = info['current-firmware']

    def __del__(self):
        if self.sock:
            self.sock.close()

    def get_identity(self):
        """
        Get device identity
        :return: Mikrotik identity
        """
        info = self.apiros.execute(["/system/identity/print"])
        return info['name']

    def get_info(self):
        """
        Get information about device
        :return: dictionary
        """
        info = self.apiros.execute(["/system/routerboard/print"])
        return info

    def execute(self, command):
        return self.apiros.execute(command)

