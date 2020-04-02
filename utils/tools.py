def isError(stderr):
    return stderr.read().decode('utf-8') != ''


def readOut( stdout):
    return stdout.read().decode('utf-8')