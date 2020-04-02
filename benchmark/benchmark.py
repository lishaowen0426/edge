

class Benchmark(object):

    def __init__(self, cmd, name, metric,image ='ubuntu'):
        '''

        :param image: docker image name
        :param cmd:  cmd to run when after logging in to the container
        :param metric: use this word to look for the final result,  "metric: some number"
        '''

        self._cmd = cmd
        self._image = image
        self._name = name
        self._metric = metric


    def getImage(self):
        return self._image


    def getCommand(self):
        return self._cmd

    def getName(self):
        return self._name

    def setContainerID(self, id):
        self._id = id

    def getContainerID(self):
        return self._id

    def parseResult(self, result):
        raise NotImplementedError
