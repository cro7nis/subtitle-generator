import logging
from loguru import logger
import sys
from service.configs import settings
from gunicorn.glogging import Logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # find caller from where originated the logged message
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class DebugInterceptHandler(logging.Handler):
    def emit(self, record):
        # get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # find caller from where originated the logged message
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log('DEBUG', record.getMessage())


class StubbedGunicornLogger(Logger):
    def setup(self, cfg):
        handler = logging.NullHandler()
        self.error_logger = logging.getLogger("gunicorn.error")
        self.error_logger.addHandler(handler)
        self.access_logger = logging.getLogger("gunicorn.access")
        self.access_logger.addHandler(handler)
        self.error_logger.setLevel(settings.logging.level)
        self.access_logger.setLevel(settings.logging.level)


def configure_logger(level,
                     format,
                     loggers_to_loguru=None):
    logger.remove()  # remove initial loguru logger to add one with custom configs
    # Add gunicorn and uvicorn logs to loguru loggers,
    # adapted from https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/
    intercept_handler = InterceptHandler()  # Create a handler to redirect specific logs to loguru logger
    intercept_handler_debug = DebugInterceptHandler()
    # To view available loggers use logging.root.manager.loggerDict.keys()
    if loggers_to_loguru is not None:
        for logger_name in loggers_to_loguru:
            if 'nemo' in logger_name:
                logging.getLogger(logger_name).handlers = [
                    intercept_handler_debug]  # redirect logs from python logger to loguru
            else:
                logging.getLogger(logger_name).handlers = [
                    intercept_handler]  # redirect logs from python logger to loguru

    logger.configure(extra={"classname": "None"})

    logger.add(sys.stderr, format=format, filter=None, level=level, backtrace=True,
               diagnose=True)

    return logger


logger = configure_logger(**settings.logging)
