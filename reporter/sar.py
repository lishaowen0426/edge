
import subprocess
from time import sleep, time


def cmd(cmd):
    p = subprocess.Popen(cmd, stdout= subprocess.PIPE, stderr=subprocess.STDOUT,
                                 shell=True)

    return p



class SarReporter(object):

    def __init__(self, dbhost, passwd , port = 6379,myhost = None):
        '''

        :param myhost: for identify this machine
        :param dbhost: for redis connection
        :param passwd:
        :param port:
        '''

        cmd('echo Y|sudo apt-get install sysstat')
        cmd('echo Y| sudo apt-get install python-pip')
        cmd('echo Y | sudo pip install redis')


        import redis

        self.myhost = '106.53.181.173'

        self.db = redis.Redis(host = dbhost, password=passwd, port = port)



        self.mem = 'sudo sar -r 1 1| grep \'^[[:digit:]].*[[:digit:]]$\' |awk \'{print $5}\'' # %memused
        self.cpu = 'sudo sar -u 1 1| grep \'^[[:digit:]].*[[:digit:]]$\'|awk \'{print 100 - $8}\'' # 100 - %idle
        self.io =  'sudo sar -u 1 1| grep \'^[[:digit:]].*[[:digit:]]$\'|awk \'{print $6}\''  # %iowait
        self.net = 'ping -q 106.53.181.173   -c 1 | grep \'ms$\' | grep -o -E \'[0-9]+\\.[0-9]+\''





    def collect_and_upload(self, delay):

        sleep(delay)

        mem = float(subprocess.Popen(self.mem, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             shell=True).communicate()[0].rstrip())
        cpu = float(subprocess.Popen(self.cpu, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               shell=True).communicate()[0].rstrip())
        io = float(subprocess.Popen(self.io, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               shell=True).communicate()[0].rstrip())
        net = float(subprocess.Popen(self.net, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               shell=True).communicate()[0].split()[0])

        perf = 'mem:{mem} cpu:{cpu} io:{io} net:{net}'.format(
            mem = mem, cpu = cpu, io = io, net = net
        )
        data = {perf:time()}


        print(data)

        self.db.zadd(self.myhost,data)






    def run(self,delay):

        while 1:
            self.collect_and_upload(delay = delay)



if __name__ == '__main__':


    sar = SarReporter(dbhost='106.52.248.140', passwd='19950426')
    sar.run(2)