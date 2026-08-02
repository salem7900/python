#!/usr/bin/env python3
import random
from typing import Generator

PLAYER_NAMES: tuple[str, ...] = ("Alice", "Bob", "Charlie", "Dylan")

ACTIONS: tuple[str, ...] = (
    "run", "eat", "sleep", "grab", "move",
    "climb", "swim", "release", "use",
)


def gen_event() -> Generator[tuple[str, str], None, None]:
    while True:
        name = random.choice(PLAYER_NAMES)
        action = random.choice(ACTIONS)
        yield name, action


def consume_event(
    ten_events: list[tuple[str, str]]
) -> Generator[tuple[str, str], None, None]:
    while len(ten_events) > 0:
        index = random.randint(0, len(ten_events) - 1)
        event = ten_events[index]
        del ten_events[index]
        yield event


def main() -> None:
    print("=== Game Data Stream Processor ===")
    events = gen_event()
    for i in range(1000):
        name, action = next(events)
        print(f"Event {i}: Player {name} did action {action}")

    ten_events: list[tuple[str, str]] = []
    for i in range(10):
        ten_events.append(next(events))
    print(f"Built list of 10 events: {ten_events}")

    for event in consume_event(ten_events):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {ten_events}")


if __name__ == "__main__":
    main()
