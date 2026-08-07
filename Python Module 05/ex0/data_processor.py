#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Any


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


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")

    print("Testing Numeric Processor...")
    numeric = NumericProcessor()
    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(
        f"Trying to validate input 'Hello': {numeric.validate('Hello')}"
    )
    print("Test invalid ingestion of string 'foo' without prior "
          "validation:")
    try:
        numeric.ingest("foo")
    except ValueError as error:
        print(f"Got exception: {error}")

    numeric_data: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {numeric_data}")
    numeric.ingest(numeric_data)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")

    print("\nTesting Text Processor...")
    text = TextProcessor()
    print(f"Trying to validate input '42': {text.validate(42)}")

    text_data = ["Hello", "Nexus", "World"]
    print(f"Processing data: {text_data}")
    text.ingest(text_data)
    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")

    print("\nTesting Log Processor...")
    log = LogProcessor()
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")

    log_data = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"},
    ]
    print(f"Processing data: {log_data}")
    log.ingest(log_data)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
