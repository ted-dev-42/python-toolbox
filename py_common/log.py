import logging
import os
import sys


def init(tag, log_file=None, level=logging.INFO):

    log_pattern = '[{}]'.format(tag) + ' %(asctime)s [%(levelname)s] %(message)s [%(funcName)s: %(filename)s, %(lineno)d]'
    date_pattern = '%Y-%m-%d %H:%M:%S'
    # logging.basicConfig(level=logging.DEBUG,
    #                     format=format,
    #                     datefmt=datefmt,
    #                     filename=log_file,
    #                     filemode='w')
    #
    # consoleLogger=logging.StreamHandler(sys.stdout)
    # consoleLogger.setLevel(logging.INFO)
    # consoleLogger.setFormatter(logging.Formatter(format, datefmt))
    # logging.getLogger().addHandler(consoleLogger)

    log = logging.getLogger()
    log.setLevel(level)
    log_format = logging.Formatter(log_pattern, date_pattern)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(log_format)
    log.addHandler(sh)

    if log_file is not None:
        print(log_file)
        dir = os.path.dirname(log_file)
        if dir != '' and not os.path.exists(dir):
            os.makedirs(dir)

        fh = logging.FileHandler(log_file)
        fh.setFormatter(log_format)
        log.addHandler(fh)

