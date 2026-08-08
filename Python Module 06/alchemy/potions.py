#!/usr/bin/env python3
import elements
from .elements import create_earth, create_air

def healing_potion() -> str:
    return f"Healing potion brewed with '{create_air()}' and '{create_earth()}'"

def strength_potion() -> str:
    return f"Strength potion brewed with '{elements.create_water()}' and '{elements.create_fire()}'"
