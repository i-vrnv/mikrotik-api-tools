class MtDevice(object):
    """
    This class contain information about device
    """
    def __init__(self, apiros):
        """
        :param apiros: instance of ApiROS class
        """
        self.apiros = apiros
        self.identity = self.get_identity()

        info = self.get_info()
        self.factory_firmware = info['factory-firmware']
        self.firmware_type = info['firmware-type']
        self.routerboard = info['routerboard']
        self.serial_number = info['serial-number']
        self.upgrade_firmware = info['upgrade-firmware']
        self.model = info['model']
        self.current_firmware = info['current-firmware']

    def get_identity(self):
        """
        Get device identity
        :return: Mikrotik identity
        """
        self.apiros.write_sentence(["/system/identity/print"])
        info = self.apiros.parse_out()
        return info['name']

    def get_info(self):
        self.apiros.write_sentence(["/system/routerboard/print"])
        info = self.apiros.parse_out()
        return info
