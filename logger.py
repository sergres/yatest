from dateutil.parser import parse

LEVELS = ['DEBUG', 'WARN', 'ERROR', 'CRITICALL', 'NOTICE']

class LogFile:
    """one instance per log file"""
    file = None
    path = None
    log_level = None
    log_record = None
    is_empty = False

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
        return self.is_empty


class LogRecord:
    """contains one log record"""
    fp = None
    lines = None
    timestamp = None
    def __init__(self, fp):
        self.fp = fp
        self.lines = fp.readline()
        #handle time stamp
        print self.lines[0:20]
        #self.timestamp = parse(self._fix_string(self.lines), fuzzy=True)
        self.timestamp = parse(self.lines[0:20], fuzzy=True)
        print self.timestamp
        if '' == self.lines:
            return
        #handle multiline log records
        next_line = fp.readline()
        while next_line[0] in ' ':
            self.lines += next_line
            next_line = fp.readline()

    def _fix_string(self, log_line):
        #TODO
        log_line = log_line.replace('mac-shchypas', 'macshchypas')
        return log_line

    def GetTimeStamp(self):
        return self.timestamp

    def __unicode__(self):
        return self.lines
