
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


class LogRecord:
    """contains one log record"""
    fp = None
    lines = None
    def __init__(self, fp):
        self.fp = fp
        self.lines = fp.readline()

    def GetTimeStamp(self):
        return 'TODO: ' +  self.lines
