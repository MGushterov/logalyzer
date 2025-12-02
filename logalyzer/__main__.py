from logalyzer.cli import build_parser, handle_stats, handle_parse
import time


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "stats":
        start = time.perf_counter()
        handle_stats(args)
        end = time.perf_counter()
        print(f'EXECUTED IN: {round(end - start, 4)} seconds')
    elif args.command == "parse":
        handle_parse(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
