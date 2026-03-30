"""Vigintiseptimal Latin — a base-27 numeral system using the latin alphabet."""

from .core import (
    vigintiseptimal_latin,
    vigintiseptimal,
    calc,
    cal,
    letters_to_number,
    number_to_letters,
    lettres_vers_nombre,
    nombre_vers_lettres,
    ALPHABET,
    BASE,
    DECIMAL_PRECISION,
    PRECISION_DECIMALES,
)

__version__ = "1.0.0"
__all__ = [
    "vigintiseptimal_latin",
    "vigintiseptimal",
    "calc",
    "cal",
    "letters_to_number",
    "number_to_letters",
    "lettres_vers_nombre",
    "nombre_vers_lettres",
    "ALPHABET",
    "BASE",
    "DECIMAL_PRECISION",
    "PRECISION_DECIMALES",
]
