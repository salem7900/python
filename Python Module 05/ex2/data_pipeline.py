#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Any, Protocol


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._storage: list[tuple[int, str]] = []
        self._rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        ...

    @abstractmethod
    def ingest(self, data: Any) -> None:
        ...

    def output(self) -> tuple[int, str]:
        if not self._storage:
            raise IndexError("No data available to output")
        return self._storage.pop(0)

    def _store(self, value: str) -> None:
        self._storage.append((self._rank, value))
        self._rank += 1

    @property
    def total_processed(self) -> int:
        return self._rank

    @property
    def remaining(self) -> int:
        return len(self._storage)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return len(data) > 0 and all(
                isinstance(item, (int, float)) for item in data
            )
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._store(str(item))
        else:
            self._store(str(data))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return len(data) > 0 and all(
                isinstance(item, str) for item in data
            )
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._store(item)
        else:
            self._store(data)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return self._is_valid_entry(data)
        if isinstance(data, list):
            return len(data) > 0 and all(
                isinstance(item, dict) and self._is_valid_entry(item)
                for item in data
            )
        return False

    @staticmethod
    def _is_valid_entry(entry: dict[Any, Any]) -> bool:
        return len(entry) > 0 and all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in entry.items()
        )

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        entries = data if isinstance(data, list) else [data]
        for entry in entries:
            self._store(": ".join(entry.values()))


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        values = ",".join(value for _, value in data)
        print(f"CSV Output: {values}")


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pairs = ", ".join(
            f'"item_{rank}": "{value}"' for rank, value in data
        )
        print(f"JSON Output: {{{pairs}}}")


class DataStream:
    def __init__(self) -> None:
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    break
            else:
                print(
                    "DataStream error - Can't process element in "
                    f"stream: {element}"
                )

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._processors:
            collected: list[tuple[int, str]] = []
            for _ in range(nb):
                try:
                    collected.append(proc.output())
                except IndexError:
                    break
            if collected:
                plugin.process_output(collected)

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        for proc in self._processors:
            name = self._display_name(proc)
            print(
                f"{name}: total {proc.total_processed} items "
                f"processed, remaining {proc.remaining} on processor"
            )

    @staticmethod
    def _display_name(proc: DataProcessor) -> str:
        suffix = "Processor"
        class_name = type(proc).__name__
        if class_name.endswith(suffix):
            return f"{class_name[:-len(suffix)]} {suffix}"
        return class_name


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===\n")

    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Processors")
    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()
    stream.register_processor(numeric)
    stream.register_processor(text)
    stream.register_processor(log)

    batch1: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected",
            },
        ],
        42,
        ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {batch1}")
    stream.process_stream(batch1)
    stream.print_processors_stats()

    csv_plugin = CSVExportPlugin()
    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, csv_plugin)
    stream.print_processors_stats()

    batch2: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {
                "log_level": "ERROR",
                "log_message": "500 server crash",
            },
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"\nSend another batch of data: {batch2}")
    stream.process_stream(batch2)
    stream.print_processors_stats()

    json_plugin = JSONExportPlugin()
    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, json_plugin)
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
