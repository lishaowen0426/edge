import sys
sys.path.append('../')

import time

from logger import log
from utils.tools import isError,readOut

from benchmark.benchmark import Benchmark

class Docker(object):

    def __init__(self, ssh_session, os):
        '''

        :param ssh_session:
        :param os:
        '''

        self.ssh = ssh_session
        self.os = os
        self.tasks = {}


    def checkDocker(self):
        '''
        check whether Docker is installed, and if it is, verify it as well

        '''

        if self.os == 'ubuntu':
            if self.ssh.exec_command_stdout('which docker') == '':
                log.error('Docker is not installed')
                return False

            _, _,stderr = self.ssh.exec_command('sudo docker run hello-world')

            if stderr.read().decode('utf-8') != '':
                log.error('Docker verification failed')
                return False
            else:
                log.warning('Docker has been successfully verified...')
                return True

        elif self.os == 'centos':
            raise NotImplementedError

    def installDocker(self):
        raise NotImplementedError


    def addTask(self, task):

        assert task, 'Please provide the benchmark to docker'
        self.tasks[task.getName()] = task


    def pull(self,name):

        img = self.tasks[name].getImage()

        if self.os == 'ubuntu':
            if self.ssh.exec_command_stdout('sudo docker image ls | grep {image}'.format(image=img)) == '':
                _,stdout,stderr = self.ssh.exec_command('sudo docker pull {image}'.format(img))
                if stderr.read().decode('utf-8') != '':
                    log.error('Cannot pull the image from docker repo')

        elif self.os == 'centos':
            raise NotImplementedError

        log.warning('Image has been successfully pulled from the docker repo')


    def launch(self,name):
        img = self.tasks[name].getImage()


        if self.os == 'ubuntu':

            self.ssh.exec_command('sudo docker stop {image}'.format(image = img))
            self.ssh.exec_command('sudo docker rm {image}'.format(image=img)) # the container might be running, anyway
                                                                              # remove it for safe
            self.ssh.exec_command('sudo docker system prune')
            time.sleep(1)

            _,stdout,stderr = self.ssh.exec_command('sudo docker run --rm -d --name {name} {image}'.format(
                name = img, image = img
            ))
            if isError(stderr):

                log.error('Launch the container {name} failed'.format(name = img))
                return
            id = readOut(stdout)
            self.tasks[name].setContainerID(id)
            log.warning('Container {name} has been launched with id {id}'.format(name = img, id = id ))
        elif self.os == 'centos':
            raise NotImplementedError



    def run(self,name,background):

        cmd = self.tasks[name].getCommand()
        id = self.tasks[name].getContainerID()

        if self.os == 'ubuntu':

            if background:
                self.ssh.exec_command('sudo docker exec -i -t -d {id}  {cmd}'.format(
                    id=id[0:10], cmd=cmd)) #-i: keep stdin open  -t:allocate psedo-TTY  -d: detach
            else:

                _, stdout, stderr = self.ssh.exec_command('sudo docker exec -i -t {id}  {cmd}'.format(
                id = id[0:10], cmd = cmd))

                str = readOut(stdout)
                self.tasks[name].parseResult(str)


        elif self.os == 'centos':
            raise NotImplementedError
