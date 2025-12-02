from abc import ABC, abstractmethod
from logalyzer.exceptions import LogParserError, FormatNotFound
from logalyzer.models import LogRecord, HTTPMethod
import datetime as dt
import re


class LogFormat(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Short key / identifier for this log format."""
        raise NotImplementedError

    @property
    @abstractmethod
    def pattern(self) -> re.Pattern[str]:
        """Compiled regular expression for this log format."""
        raise NotImplementedError

    @abstractmethod
    def parse_line(self, log_line: str) -> LogRecord:
        """Parse a single log line into a LogRecord, or raise LogParserError."""
        raise NotImplementedError


class ApacheCombinedFormat(LogFormat):
    def __init__(self) -> None:
        self._pattern: re.Pattern[str] = re.compile(
            r'(?P<ip>(?:\d{1,3}\.){3}\d{1,3})\s+'
            r'(?P<ident>\S+)\s+'
            r'(?P<authuser>\S+)\s+'
            r'\[(?P<timestamp>\d{1,2}/\w+/\d{4}:\d{2}:\d{2}:\d{2}\s+\+\d{4})\]\s+'
            r'"(?P<method>[A-Z]+)\s+(?P<path>\S+)\s+(?P<protocol>HTTP/\d\.\d)"\s+'
            r'(?P<status>\d{3})\s+'
            r'(?P<size>\d+|-)\s+'
            r'"(?P<referer>[^"]*)"\s+'
            r'"(?P<user_agent>[^"]*)"'
        )

    @property
    def name(self) -> str:
        return "apache_combined"

    @property
    def pattern(self) -> re.Pattern[str]:
        return self._pattern

    def parse_line(self, log_line: str) -> LogRecord:
        match = self.pattern.match(log_line)
        if not match:
            raise LogParserError(
                f"Log line does not match {self.name} format: {log_line!r}"
            )

        ip_str = match.group("ip")
        ts_str = match.group("timestamp")
        method_str = match.group("method")
        path_str = match.group("path")
        status_str = match.group("status")
        size_str = match.group("size")

        # timestamp conversion to datetime
        try:
            timestamp = dt.datetime.strptime(ts_str, "%d/%b/%Y:%H:%M:%S %z")
        except ValueError as exc:
            raise LogParserError(f"Invalid timestamp {ts_str!r}")

        # method conversion to HTTPMethod Enum
        try:
            method = HTTPMethod[method_str]
        except KeyError as exc:
            raise LogParserError(f"Unsupported HTTP method {method_str!r}")

        # status conversion to integer
        status = int(status_str)

        # size conversion to integer | None
        size: int | None
        if size_str == "-":
            size = None
        else:
            size = int(size_str)

        return LogRecord(
            ip=ip_str,
            timestamp=timestamp,
            method=method,
            path=path_str,
            status=status,
            size=size,
            raw=log_line.rstrip("\n"),
        )


FORMAT_REGISTRY: dict[str, LogFormat] = {
    "apache_combined": ApacheCombinedFormat(),
}


def get_format(name: str) -> LogFormat:
    try:
        return FORMAT_REGISTRY[name]
    except KeyError as exc:
        raise FormatNotFound('Format not found in registry', 404)
