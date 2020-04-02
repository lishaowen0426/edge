import sys
sys.path.append('../')

from utils.ssh import SSHSession
from utils.docker import Docker
from logger import log
import time
from benchmark.redis_benchmark import RedisBenchmark
from monitor.sar_monitor import SarMonitor
from utils.tools import  isError


class Node (object):

    def __init__(self, username, host, passwd, port = 22, pkey = None):
        '''

        :param username:
        :param host: ip address or DNS hostname
        :param passwd:
        :param port:
        :param pkey:
        '''

        self.ssh_session = SSHSession(username = username, hostname = host, passwd = passwd, port = port, pkey = pkey)
        self.ssh_session.connect()
        self.os = self.ssh_session.getOS()

        # push the reporter file


        self.docker = Docker(self.ssh_session,self.os)

        if not self.docker.checkDocker():
            self.docker.installDocker()



    def getSSHSession(self):
        return self.ssh_session


    def addTask(self,task):
        self.docker.addTask(task)


    def pull(self,name):
        '''

        Pull the benchmark image from the docker repo
        '''
        self.docker.pull(name)

    def launch(self,name):
        '''

        Launch the benchmark container
        '''
        self.docker.launch(name)

    def run(self,name,background = True):
        self.docker.run(name,background= background)









if __name__ == '__main__':


    redis = RedisBenchmark(cmd = '/usr/local/bin/redis-benchmark -t set -q -l ', metric='SET' )


    node = Node('ubuntu')
    node.addTask(redis)


    node.pull(redis.getName())
    node.launch(redis.getName())
    node.run(redis.getName(),background=True)

    time.sleep(2)





