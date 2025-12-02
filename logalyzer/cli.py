from argparse import ArgumentParser
from logalyzer.reader import iter_records, iter_records_multi_sequential, iter_records_multi_parallel
from logalyzer.stats import compute_stats
from logalyzer.output_helpers import (print_global_stats, print_by_status, print_by_method, print_top_paths,
                                      print_top_error_paths)


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog='Logalyzer',
        description='simple, fast, memory-efficient log analyzer'.title()
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    stats_subparser = subparsers.add_parser('stats', help='Get stats for logs')
    stats_subparser.add_argument('paths', nargs='+', help='Specify path(s) to log file(s)')
    stats_subparser.add_argument('-f', '--format', dest='format', default='apache_combined', help=('''
        Specify desired format from:
        [ apache_combined (default)]
        '''))
    stats_subparser.add_argument('--strict', dest='strict',
                                 action='store_true',
                                 help='When strict, raises exception whenever line could not be parsed')
    stats_subparser.add_argument('--parallel', dest='parallel', action='store_true',
                                 help='Parallel processing')
    stats_subparser.add_argument('--top-paths', dest='top_paths', type=int, default=3,
                                 help='Get N amount of top visited paths; default is 3')

    parse_parser = subparsers.add_parser('parse')
    parse_parser.add_argument('path')
    parse_parser.add_argument('--format', default='apache_combined')

    return parser


def handle_stats(args):
    if len(args.paths) == 1:
        records = iter_records(args.paths[0], args.format, args.strict)
    elif args.parallel:
        records = iter_records_multi_parallel(args.paths, args.format, args.strict)
    else:
        records = iter_records_multi_sequential(args.paths, args.format, args.strict)

    stats = compute_stats(records, args.top_paths)
    print_global_stats(stats.global_stats)
    print_by_status(stats.by_status)
    print_by_method(stats.by_method)
    print_top_paths(stats.top_paths, args.top_paths)
    print_top_error_paths(stats.top_error_paths, args.top_paths)


def handle_parse(args):
    print(args)
    for record in iter_records(args.path, args.format):
        print(record)
