
from benchmark.benchmark import Benchmark
import re

class RedisBenchmark(Benchmark):

    def __init__(self, cmd, metric,name = 'redis',image = 'redis'):
        super().__init__(cmd = cmd, name=name,image=image,metric=metric)


    def parseResult(self, output):

        all_results = output.splitlines() # all_results shoule be like ['SET: 43333.34', 'SET: 43240.02', 'SET: 43233.89 requests per second']
                                          # we only need the requests per second terms
        regx = re.compile('(.*)requests per second')
        result = [r for r in all_results if regx.match(r)]
        result = re.findall('[-+]?([0-9]*\.[0-9]+|[0-9]+)',result[0])

        self.result = {self._metric:float(result[0])}
        print(self.result)
