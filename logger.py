from dateutil.parser import parse

LEVELS = ['DEBUG', 'WARN', 'ERROR', 'CRITICALL', 'NOTICE']

class LogFile:
    """one instance per log file"""
    file = None
    path = None
    log_level = None
    log_record = None

    def __init__(self, log_path, log_level):
        self.path = log_path
        try:
            self.file = open(self.path)
        except Exception, e:
            raise e
        if log_level in LEVELS:
            self.log_level = log_level
        else:
            #never will work, because we have same check in run.py
            print log_level + " - invalid log level value. "
            exit(-1)
        self.getLogRecord()

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
        self.timestamp = self.parse(self.lines[0:30])
        if '' == self.lines:
            self.is_empty = True
            return

        #handle multiline log records
        # while True:
        #     file_pos = self.fp.tell()
        #     nextg_line = self.fp.readline()
        #     try:
        #         parse(next_line[0:20], fuzzy=True)
        #         #this line has datetime string, let leave it for nex logRecord
        #         self.fp.seek(file_pos)
        #         return
        #     except :
        #         #after check - add to current log record
        #         self.lines += next_line

    def _fix_string(self, log_line):
        #TODO
        log_line = log_line.replace('mac-shchypas', 'macshchypas')
        return log_line

    def GetTimeStamp(self):
        return self.timestamp

    def __str__(self):
        return self.lines

    def parse(self, str):
        timestamp = None
        try:
            timestamp = parse(str[0:20], fuzzy=True)
        except:
            pass

        try:
            timestamp = parse(str, fuzzy=True)
        except:
            pass

        try:
            timestamp = parse(str, yearfirst=True, fuzzy=True)
        except:
            pass
        return timestamp
