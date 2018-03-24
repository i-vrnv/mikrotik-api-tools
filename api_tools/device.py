from api_tools.api import ApiRos
from api_tools.logs import LogsHandler


def get_value_by_key(data_list, key):
    name = ''
    for i in data_list:
        if key in i:
            name = i[key]
    return name


class Device(object):
    """
    This class contain information about device
    """

    def __init__(self, host, port, username, password):
        """
        :param apiros: instance of ApiROS class
        """
        self.device = ApiRos(host, port, username, password)
        self.identity = self.get_identity()

        info = self.get_info()
        self.factory_firmware = get_value_by_key(info, 'factory-firmware')
        self.firmware_type = get_value_by_key(info, 'firmware-type')
        self.routerboard = get_value_by_key(info, 'routerboard')
        self.serial_number = get_value_by_key(info, 'serial-number')
        self.upgrade_firmware = get_value_by_key(info, 'upgrade-firmware')
        self.model = get_value_by_key(info, 'model')
        self.current_firmware = get_value_by_key(info, 'current-firmware')

    def __del__(self):
        self.device.close()

    def get_identity(self):
        """
        Get device identity
        :return: Mikrotik identity
        """
        info = self.device.execute(["/system/identity/print"])
        return get_value_by_key(info, 'name')

    def get_info(self):
        """
        Get information about device
        :return: dictionary
        """
        info = self.device.execute(["/system/routerboard/print"])
        return info

    def update_info(self):
        info = self.get_info()
        self.factory_firmware = info['factory-firmware']
        self.firmware_type = info['firmware-type']
        self.routerboard = info['routerboard']
        self.serial_number = info['serial-number']
        self.upgrade_firmware = info['upgrade-firmware']
        self.model = info['model']
        self.current_firmware = info['current-firmware']

    def execute(self, command):
        return self.device.execute(command)

    def close(self):
        self.device.close()

    def print_logs(self):
        LogsHandler(self.device).print_logs()
