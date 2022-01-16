import logging
from logging import handlers
from dataclasses import dataclass

# MYVAR = 'gavin'

@dataclass
class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.
    """
    myvar: str
    def filter(self, record):
        record.SERNUM = self.myvar
        # record.MYVAR = MYVAR
        return True

def init_log():
    logging.root.handler = []
    logging.root.setLevel(logging.DEBUG)

    # syslog settings
    sys_handler = logging.handlers.SysLogHandler("/dev/log")
    # sys_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sys_formatter = logging.Formatter('<Serial number:%(SERNUM)s> %(asctime)s - %(name)s - %(levelname)s - %(message)s')
    sys_handler.setFormatter(sys_formatter)
    logging.root.addHandler(sys_handler)

