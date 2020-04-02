import sys
sys.path.append('../')


import paramiko
from logger import log


class SSHSession(object):

    def __init__(self, username, hostname, passwd, port = 22, pkey = None):
        '''

        :param username:
        :param host:
        :param passwd:
        :param pkey:  an optional private key to use for authentication
        '''
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._hostname = hostname
        self._passwd = passwd
        self._username = username
        self._port = port
        self._pkey = pkey

    def connect(self):

        try:
            self._ssh.connect( hostname= self._hostname, port=self._port, username=self._username,
                           password= self._passwd, pkey= self._pkey, timeout=20)

            self._channel = self._ssh.invoke_shell()

        except:
            log.warning('Failed to connect to {user}@{host}'.format(user= self._username, host=self._hostname))
            self._ssh.close()

    def close(self):

        self._ssh.close()
        self._channel.close()


    def getOS(self):
        _,stdout,_ = self.exec_command('uname -a | grep -i ubuntu')
        if stdout.read().decode('utf-8') == '':
            self._os = 'centos'
        else:
            self._os = 'ubuntu'

        return self._os




    def exec_command(self, cmd, timeout = None):
        return self._ssh.exec_command(cmd, timeout=timeout, get_pty=True)

    def exec_command_stdout(self, cmd, timeout = None):
        _, stdout, _ = self._ssh.exec_command(cmd, timeout = timeout, get_pty=True)
        return stdout.read().decode('utf-8')



if __name__ == '__main__':


    docker = '/usr/local/bin/docker '

    ssh = SSHSession(username= 'ubuntu', hostname='106.53.181.173',passwd='19950426Li')
    ssh.connect()
    stdin, stdout, stderr = ssh.exec_command('pgrep asd')
    #os = ssh.getOS()
    #print(os)

    print(stdout.read().decode('utf-8') == '')
    #print(stderr.read().decode('utf-8'))
    ssh.close()