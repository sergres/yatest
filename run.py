#!/usr/bin/env python
import argparse
import os.path
from logger import LogFile, LEVELS
from datetime import datetime

def is_valid_file(parser, arg):
    if not os.path.isfile(arg):
       parser.error("%s - is not a file, or does not exist!"%arg)
    else:
       return arg


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l',
                        '--level',
                        choices=LEVELS,
                        help="log level filter",
                        default='NOTSET'
                        )

    parser.add_argument('logfiles',
                        nargs='+',
                        help='enter path of log file[s]',
                        type=lambda x: is_valid_file(parser,x))

    args = parser.parse_args()
    logfiles = []
    for log in args.logfiles:
        # print log
        # print args.level
        logfiles.append(LogFile(log_path=log, log_level=args.level))

    while len(logfiles):
        dt = datetime.now()
        #here we will put log record with minmum datetime
        min_log = None
        for log_file in logfiles:
            if log_file.GetCurrTimeStamp() <= dt:
                dt = log_file.GetCurrTimeStamp()
                min_log = log_file
        print min_log.getLogRecord(),
        # print min_log.GetCurrTimeStamp(), min_log.path
        if min_log.isEmpty():
            logfiles.pop(logfiles.index(min_log))
            # print " file is empty"






