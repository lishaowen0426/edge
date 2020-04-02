

import re


if __name__ == '__main__':

    s = 'SET: -44583.23 requests per second'
    regx = re.findall('[-+]?([0-9]*\.[0-9]+|[0-9]+)',s)
    print(regx)