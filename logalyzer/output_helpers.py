from logalyzer.stats import GlobalStats
from logalyzer.models import HTTPMethod


def print_global_stats(global_stats: GlobalStats) -> None:
    print('=' * 16)
    if global_stats.first_timestamp and global_stats.last_timestamp:
        print(
            f"\nTotal Requests: {global_stats.total_requests}\n"
            f"Time Range: {global_stats.first_timestamp:%Y-%m-%d %H:%M:%S)} -> "
            f"{global_stats.last_timestamp:%Y-%m-%d %H:%M:%S}\n"
            f"Total Megabytes Sent: {global_stats.total_bytes / 1_000_000:.2f} MB\n"
        )


def print_by_status(by_status: dict[int, int]) -> None:
    print('='*16)
    print('\nStatus Codes: ')
    codes = sorted(by_status.items(), key=lambda item: item[0])
    for code, count in codes:
        if 100 <= code < 200:
            category = "Informational"
        elif 200 <= code < 300:
            category = "Success"
        elif 300 <= code < 400:
            category = "Redirect"
        elif 400 <= code < 500:
            category = "Client Error"
        else:
            category = "Server Error"

        print(f"\t{category} - {code}: {count}")


def print_by_method(by_method: dict[HTTPMethod, int]) -> None:
    print('\n' + ('=' * 16))
    print('\nHTTP Methods: ')
    for method, count in by_method.items():
        print(f'\n\tMethod {method.value}: {count}')


def print_top_paths(paths: list[tuple[str, int]], top_paths: int = 3) -> None:
    print('\n' + ('=' * 16))
    print('\nTop Paths:')
    counter = 0
    for path, count in paths:
        print(f'\n\tPath - {path}: {count}')
        counter += 1
        if counter >= top_paths:
            break


def print_top_error_paths(error_paths: list[tuple[str, int]], top_paths: int = 3) -> None:
    print('\n' + ('=' * 16))
    print('\nTop Error Paths:')
    counter = 0
    for path in error_paths:
        print(f'\n\tPath - {path[0]}: {path[1]}')
        counter += 1
        if counter >= 3:
            break
