import re
import sys
from collections import Counter
from enum import StrEnum
from pathlib import Path
from typing import NamedTuple


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Log(NamedTuple):
    date: str
    time: str
    level: LogLevel
    message: str


def parse_log_line(line: str) -> Log:
    # Step 1: Log line preparation
    line = line.strip()

    # Step 2: Find log entities
    date_pattern = r"\d{4}-\d{2}-\d{2}"
    time_pattern = r"\d{2}:\d{2}:\d{2}"
    level_pattern = "|".join(level.value for level in LogLevel)
    match = re.match(rf"({date_pattern}) ({time_pattern}) ({level_pattern}) (.+)", line)

    # Step 3: Extract log entities
    raw_date = match.group(1)
    raw_time = match.group(2)
    level = match.group(3)
    message = match.group(4)

    # Step 4: Construct & return log record
    return Log(
        date=raw_date,
        time=raw_time,
        level=level,
        message=message,
    )


def load_logs(file_path: str | Path, *, encoding: str = "utf-8") -> list[Log]:
    with open(file_path, encoding=encoding) as logs_file:
        return [parse_log_line(log_line) for log_line in logs_file]


def filter_logs_by_level(logs: list[Log], level: LogLevel) -> list[Log]:
    return [log for log in logs if log.level == level]


def count_logs_by_level(logs: list[Log]) -> dict[LogLevel, int]:
    return dict(Counter(log.level for log in logs))


def display_log_counts(counts: dict[LogLevel, int]) -> None:
    level_title = "Рівень логування"
    level_width = len(level_title)

    count_title = "Кількість"
    count_width = len(count_title)

    print(f"{level_title} | {count_title}")
    print(f"{'-' * level_width}-|-{'-' * count_width}")
    for level, count in counts.items():
        print(f"{level:<{level_width}} | {count:<{count_width}}")


def main():
    args = iter(sys.argv[1:])

    path_arg = next(args, None)
    if not path_arg:
        print("Missing required argument: path/to/logfile.log")
        sys.exit(1)

    level_arg = next(args, None)
    if level_arg:
        level_arg = level_arg.upper()
        if level_arg not in LogLevel:
            valid_levels = ", ".join(f"'{level.value}'" for level in LogLevel)
            print(f"Unsupported log level '{level_arg}', choose from: {valid_levels}")
            sys.exit(1)

    encoding = "utf-8"
    try:
        logs = load_logs(path_arg, encoding=encoding)
        log_counts = count_logs_by_level(logs)
        display_log_counts(log_counts)

        if level_arg:
            print(f"\nДеталі логів для рівня '{level_arg}':")
            for log in filter_logs_by_level(logs, level_arg):
                print(f"{log.date} {log.time} - {log.message}")
    except FileNotFoundError:
        print(f"File '{path_arg}' was not found")
    except IsADirectoryError:
        print(f"File is exected, not a directory: '{path_arg}'")
    except UnicodeError:
        print(f"File '{path_arg}' is not encoded as '{encoding}'")


if __name__ == "__main__":
    main()
