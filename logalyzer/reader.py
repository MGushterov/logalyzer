from os import PathLike
from typing import Iterator, Iterable
from logalyzer.exceptions import LogParserError
from logalyzer.models import LogRecord
from logalyzer.parser import parse_line
from queue import Queue
from threading import Thread

PathType = str | PathLike[str]


def iter_lines(path: PathType) -> Iterator[str]:
    """Yield lines from a file lazily, without trailing newline."""
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")


def iter_records(path: PathType, format_name: str, strict: bool) -> Iterator[LogRecord]:
    """Yield LogRecord objects parsed from a single log file.

        Raises:
            FileNotFoundError, LogParserError"""
    for line in iter_lines(path):
        try:
            yield parse_line(line, format_name)
        except LogParserError as exc:
            if strict:
                print(exc)

            continue


def iter_records_multi_sequential(paths: Iterable[PathType], format_name: str, strict: bool) -> Iterator[LogRecord]:
    """Yield LogRecord objects from multiple log files, sequentially."""
    for path in paths:
        yield from iter_records(path, format_name, strict)


_SENTINEL = object()


def _worker(path: str, format_name: str, strict: bool, queue: Queue):
    """Read one file and push LogRecord objects into the queue."""
    try:
        for record in iter_records(path, format_name, strict):
            queue.put(record)
    finally:
        queue.put(_SENTINEL)  # signal: "this worker is done"


def iter_records_multi_parallel(paths: Iterable[str], format_name: str, strict: bool = False, workers: int = 4) \
        -> Iterator[LogRecord]:
    queue: Queue = Queue(maxsize=2000)

    threads = []
    for path in paths:
        t = Thread(target=_worker, args=(path, format_name, strict, queue), daemon=True)
        t.start()
        threads.append(t)

    alive_workers = len(threads)

    while alive_workers > 0:
        item = queue.get()

        if item is _SENTINEL:
            alive_workers -= 1
            continue

        yield item
