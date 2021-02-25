import logging
import os


def mylogger(log_file_name):

    # create logger
    p = '/Users/jinghanma/Helium10/auto_jobs/logs'
    logging.basicConfig(filename=os.path.join(p, log_file_name),
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger


if __name__ == '__main__':
    pass
