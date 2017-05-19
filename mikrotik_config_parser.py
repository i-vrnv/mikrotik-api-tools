import ConfigParser

from mikrotik_device import MtDevice


class Config(object):

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('config.ini')

    def get_general(self):
        general = {'debug': self.config.get('general', 'debug')}
        return general

    def get_ftp(self):
        ftp = {'host': self.config.get('ftp', 'host'),
               'port': self.config.get('ftp', 'port'),
               'username': self.config.get('ftp', 'username'),
               'password': self.config.get('ftp', 'password')}
        return ftp

    def get_devices(self):
        for section in self.config.sections():
            if section != 'general' and section != 'ftp':
                device = {'host': self.config.get(section, 'host'),
                          'username': self.config.get(section, 'username'),
                          'password': self.config.get(section, 'password'),
                          'dst-path': self.config.get(section, 'path')}
                # Return generator
                yield device
