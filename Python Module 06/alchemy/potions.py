#!/usr/bin/env python3
import elements
from .elements import create_earth, create_air


def healing_potion() -> str:
    return (
        f"Healing potion brewed with "
        f"'{create_earth()}' and '{create_air()}'"
    )


def strength_potion() -> str:
    return (
        f"Strength potion brewed with "
        f"'{elements.create_fire()}' and '{elements.create_water()}'"
    )
