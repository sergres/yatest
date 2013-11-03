from dateutil import parser
from datetime import datetime

import dateutil.parser
from itertools import chain
import re

# http://stackoverflow.com/questions/6562148/python-finding-date-in-a-string/6562492#6562492
# Add more strings that confuse the parser in the list
UNINTERESTING = set(chain(dateutil.parser.parserinfo.JUMP,
                          dateutil.parser.parserinfo.PERTAIN,
                          ['a']))

def _get_date(tokens):
    for end in xrange(len(tokens), 0, -1):
        region = tokens[:end]
        if all(token.isspace() or token in UNINTERESTING
               for token in region):
            continue
        text = ''.join(region)
        try:
            date = dateutil.parser.parse(text)
            return end, date
        except ValueError:
            pass

def find_dates(text, max_tokens=50, allow_overlapping=False):
    tokens = filter(None, re.split(r'(\S+|\W+)', text))
    skip_dates_ending_before = 0
    for start in xrange(len(tokens)):
        region = tokens[start:start + max_tokens]
        result = _get_date(region)
        if result is not None:
            end, date = result
            if allow_overlapping or end > skip_dates_ending_before:
                skip_dates_ending_before = end
                yield date


LEVELS = ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

class LogFile:
    """one instance per log file"""
    file = None
    path = None
    log_level = None
    log_levels = []
    log_record = None

    def __init__(self, log_path, log_level):
        self.path = log_path
        try:
            self.file = open(self.path)
        except Exception, e:
            raise e

        if log_level in LEVELS:
            self.log_level = log_level

            # calculate log levels, which are ok
            log_level_acceptable = False
            for level in LEVELS:
                if level == self.log_level:
                    log_level_acceptable = True
                if log_level_acceptable:
                    self.log_levels.append(level) # e.g. ['WARNING', 'ERROR', 'CRITICAL']

        else:
            #never will work, because we have same check in run.py
            print log_level + " - invalid log level value. "
            exit(-1)
        self.getLogRecord()

    def check_log_level(self, str):
        for l in self.log_levels:
            if l.lower().find(str.lower()):
                return True
        return False


    def getLogRecord(self):
        self.log_record = LogRecord(self.file)
        return self.log_record

    def GetCurrTimeStamp(self):
        return self.log_record.GetTimeStamp()

    def isEmpty(self):
        return self.log_record.is_empty


class LogRecord:
    """contains one log record"""
    fp = None
    lines = None
    timestamp = None
    is_empty = False

    def __init__(self, fp):
        self.fp = fp
        self.lines = self.fp.readline()
        #print self.lines[0:30]
        # assume date is in first 20 chars
        self.timestamp = self.parse(self.lines)
        if '' == self.lines:
            self.is_empty = True
            return

        #handle multiline log records
        while True:
            file_pos = self.fp.tell()
            next_line = self.fp.readline()
            if '' == next_line:
                self.is_empty = True
                return

            #print self.parse(next_line[0:20]), next_line,
            if self.parse(next_line[0:20]):

                # print next_line, self.parse(next_line[0:20]),
                #this line has datetime string, let leave it for nex logRecord
                self.fp.seek(file_pos)
                return
            else:
                #after check - add to current log record
                # print 'second line'
                # print next_line,
                self.lines += next_line

    def GetTimeStamp(self):
        return self.timestamp

    def __str__(self):
        return self.lines

    def parse(self, str):
        for date in find_dates(str, allow_overlapping=False):
            return date
        return False

