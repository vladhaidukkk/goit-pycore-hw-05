import re
import sys
from collections import Counter
from datetime import date, datetime, time
from enum import StrEnum
from pathlib import Path
from typing import NamedTuple


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class Log(NamedTuple):
    date: date
    time: time
    level: LogLevel
    message: str


def parse_log_line(line: str) -> Log:
    # Step 1: Log line preparation
    line = line.strip()

    # Step 2: Find log entities
    timestamp_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
    level_pattern = "|".join(level.value for level in LogLevel)
    match = re.match(rf"({timestamp_pattern}) ({level_pattern}) (.+)", line)

    # Step 3: Extract log entities
    timestamp = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
    level = match.group(2)
    message = match.group(3)

    # Step 4: Construct & return log record
    return Log(
        date=timestamp.date,
        time=timestamp.time,
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
        logs = filter_logs_by_level(logs, level_arg) if level_arg else logs
        log_counts = count_logs_by_level(logs)
        display_log_counts(log_counts)
    except FileNotFoundError:
        print(f"File '{path_arg}' was not found")
    except IsADirectoryError:
        print(f"File is exected, not a directory: '{path_arg}'")
    except UnicodeError:
        print(f"File '{path_arg}' is not encoded as '{encoding}'")


if __name__ == "__main__":
    main()
