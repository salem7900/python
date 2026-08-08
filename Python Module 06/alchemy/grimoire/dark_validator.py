#!/usr/bin/env python3
from .dark_spellbook import dark_spell_allowed_ingredients

def validate_ingredients(ingredients: str) -> str:
    valid = dark_spell_allowed_ingredients()
    lowercase = ingredients.lower()

    is_valid = any(
        ingredient.lower() in lowercase
        for ingredient in valid
    )

    status = "VALID" if is_valid else "INVALID"
    return f"{ingredients} - {status}"