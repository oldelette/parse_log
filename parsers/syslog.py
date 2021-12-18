from parsers.type import ParseModule as OurModule

class ParseModule(OurModule):
    def __init__(self, options=[]):
        """Initialize the syslog (standard timestamp) parsing module"""
        self.name = 'syslog'
        self.desc = 'syslog (standard timestamp) parsing module'
        self.format_regex = \
                '^([A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+([^\[\] ]+)\[?(\d*)\]?: (.*)'
        self.fields = ['date_stamp', 'log_source', 'source_process',
                'source_pid', 'message']
        self.backup_format_regex = None
        self.backup_fields = []
        self.tzone = None
        self.datestamp_type = 'standard'
