from typing import Iterable, Iterator
from dataclasses import dataclass
from datetime import datetime
from logalyzer.models import StatusClass, HTTPMethod, LogRecord
from collections import defaultdict


@dataclass
class GlobalStats:
    total_requests: int
    first_timestamp: datetime | None
    last_timestamp: datetime | None
    total_bytes: int


@dataclass
class StatsResults:
    global_stats: GlobalStats
    by_status: dict[int, int]
    by_status_class: dict[StatusClass, int]
    by_method: dict[HTTPMethod, int]
    top_paths: list[tuple[str, int]]
    top_error_paths: list[tuple[str, int]]


def compute_stats(records: Iterator[LogRecord], top_paths_number: int = 3) -> StatsResults:
    total_requests = 0
    first_timestamp, last_timestamp = None, None
    total_bytes = 0
    by_status, by_status_class, by_method = defaultdict(int), defaultdict(int), defaultdict(int)
    path_counts, err_path_counts = defaultdict(int), defaultdict(int)

    for record in records:
        total_requests += 1
        if first_timestamp is None or record.timestamp < first_timestamp:
            first_timestamp = record.timestamp

        if last_timestamp is None or record.timestamp > last_timestamp:
            last_timestamp = record.timestamp

        if record.size is not None:
            total_bytes += record.size

        by_status[record.status] += 1
        by_status_class[record.status_class] += 1
        by_method[record.method] += 1

        path_counts[record.path] += 1
        if record.is_error():
            err_path_counts[record.path] += 1

    top_paths = sorted(
        path_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )[:top_paths_number + 1]

    top_error_paths = sorted(
        err_path_counts.items(),
        key=lambda item: item[1],
        reverse=True
    )[:top_paths_number + 1]

    return StatsResults(
        global_stats=GlobalStats(
            total_requests,
            first_timestamp,
            last_timestamp,
            total_bytes
        ),
        by_status=by_status,
        by_status_class=by_status_class,
        by_method=by_method,
        top_paths=top_paths,
        top_error_paths=top_error_paths
    )
