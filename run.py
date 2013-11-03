#!/usr/bin/env python
import argparse
import os.path
from logger import LogFile, LEVELS


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
                        )

    parser.add_argument('logfiles',
                        nargs='+',
                        help='enter path of log file[s]',
                        type=lambda x: is_valid_file(parser,x))

    args = parser.parse_args()
    logfiles = []
    for log in args.logfiles:
        print log
        print args.level
        logfiles.append(LogFile(log_path=log, log_level=args.level))

    while len(logfiles):
        for log_file in logfiles:
            print log_file.GetCurrTimeStamp()
            if log_file.isEmpty():
                pass




