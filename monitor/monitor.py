
class Monitor(object):

    def __init__(self, name,executable, options):
        '''
        :param name: used to kill the monitor
        :param executable:
        :param options:

        to run the monitor: executable options, for example, top 1 3, where top is exe, 1 3 is options
        '''
        self.name = name
        self.executable = executable
        self.options = options


    def getExecutable(self):

        return self.executable

    def getOptions(self):

        return self.options

    def getName(self):

        return self.name





