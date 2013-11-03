#!/usr/bin/env python
import argparse
LEVELS = ['DEBUG', 'WARN', 'ERROR', 'CRITICALL', 'NOTICE']
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l',
                        '--level',
                        choices=LEVELS,
                        help="log level filter",
                        )
    args = parser.parse_args()
    print args
