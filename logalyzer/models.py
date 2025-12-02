from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class HTTPMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    PATCH = 'PATCH'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'


class StatusClass(Enum):
    INFORMATIONAL = 'INFORMATIONAL'
    SUCCESS = 'SUCCESS'
    REDIRECTION = 'REDIRECTION'
    CLIENT_ERROR = 'CLIENT_ERROR'
    SERVER_ERROR = 'SERVER_ERROR'


@dataclass(frozen=True)
class LogRecord:
    ip: str
    timestamp: datetime
    method: HTTPMethod
    path: str
    status: int
    size: int | None
    raw: str

    def is_error(self) -> bool:
        return True if self.status >= 400 else False

    @property
    def status_class(self) -> StatusClass | None:
        if 100 <= self.status < 200:
            return StatusClass.INFORMATIONAL
        elif 200 <= self.status < 300:
            return StatusClass.SUCCESS
        elif 300 <= self.status < 400:
            return StatusClass.REDIRECTION
        elif 400 <= self.status < 500:
            return StatusClass.CLIENT_ERROR
        elif 500 <= self.status < 600:
            return StatusClass.SERVER_ERROR
        else:
            return None

