import logging

log = logging.getLogger('logger')

stream = logging.StreamHandler()
stream.setLevel(logging.WARNING)

file = logging.FileHandler(filename='../log/warnings')
file.setLevel(logging.ERROR)

log.addHandler(stream)
log.addHandler(file)

