import logging
from mylogging import init_log, ContextFilter
from dataclasses import dataclass


MYVAR = 'HP-010'

logger = logging.getLogger(__name__)
logger.addFilter(ContextFilter(MYVAR))

init_log()
logger.info("hello")