from logalyzer.parser_formats import get_format
from logalyzer.models import LogRecord


def parse_line(line: str, format_name: str) -> LogRecord:
    fmt = get_format(format_name)
    return fmt.parse_line(line)
