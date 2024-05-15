import logging.handlers
import traceback
from enum import Enum

class LogLevel(Enum):
    """
    Repair States Enumerator.
    """
    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING
    error = logging.ERROR
    critical = logging.CRITICAL

def CreateLogger(str_Session, int_LogLevel, str_LogFormat, str_DateFormat):
    """
    The main function of the script,
    log_format = '%(asctime)s - %(levelname)s - [%(name)s]: %(message)s'
    str_DateFormat = '%H:%M:%S'
    :return: none.
    :rtype: none.
    """
    try:
        obj_logger = logging.getLogger(str_Session)
        obj_logger.setLevel(int_LogLevel)

        # remove all default handlers
        for handler in obj_logger.handlers:
            obj_logger.removeHandler(handler)

        # create console handler and set level to debug
        console_handle = logging.StreamHandler()
        console_handle.setLevel(int_LogLevel)

        # create formatter
        formatter = logging.Formatter(str_LogFormat, str_DateFormat)
        console_handle.setFormatter(formatter)

        # now add new handler to logger
        obj_logger.addHandler(console_handle)
        return obj_logger

    except Exception as e:
        lines = traceback.format_exception(type(e), e, e.__traceback__)
        obj_logger.debug(''.join(lines))
        obj_logger.critical('CreateLogger Error: ' + str(e) + ' - Line: ' + str(e.__traceback__.tb_lineno))
        exit()