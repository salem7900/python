#!/usr/bin/env python3
from abc import ABC, abstractmethod
from typing import Optional


class HealCapability(ABC):
    @abstractmethod
    def heal(self, target: Optional["HealCapability"] = None) -> str:
        ...


class TransformCapability(ABC):
    @abstractmethod
    def transform(self) -> str:
        ...

    @abstractmethod
    def revert(self) -> str:
        ...
