
class LogsHandler(object):

    def __init__(self, device):
        self.device = device

    def print_logs(self):
        for log_line in self.device.execute(['/log/print']):
            print("ID: {0} - Time: {1} - Topics: {2} - Message: {3}".format(log_line['.id'], log_line['time'], log_line['topics'], log_line['message']))
