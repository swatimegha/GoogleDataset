from enum import Enum
import datetime
import json
import logging
from logging.config import dictConfig

class Level(Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'

class Logger:
    def __init__(self, name: str):
        self.level = logging.DEBUG
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(self.level)

    def debug(self, message: str):
        self.__logger.debug(message)

    def info(self, message: str):
        self.__logger.info(message)

    def warn(self, message: str):
        self.__logger.warning(message)

    def error(self, message: str):
        self.__logger.error(message)

    def trace(self, message: str):
        self.__logger.log(logging.NOTSET, message)


class NliServiceException(Exception):
    def __init__(self, level: Level, name: str, message: str):
        self.time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%M')
        self.level = level.value
        self.name = name
        self.text = message

    def to_json(self):
        return json.dumps(self.__dict__, indent = 4)

    def log(self) -> str:
        return f'[{self.time}] {self.level} from {self.name}: {self.text}'


class Trace:
    def __init__(self):
        self.__level = logging.DEBUG
        self.__sources = {}
    
    def getLogger(self, source_name: str) -> Logger:
        source = self.__sources.get(source_name)
        if source == None:
            source = Logger(source_name)
            if source.level == None:
                source.level = self.__level
            self.__sources[source_name] = source
        return source


trace = Trace()