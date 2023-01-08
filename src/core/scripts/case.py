import re
from functools import partial

_snake_1 = partial(re.compile(r'(.)((?<![^A-Za-z])[A-Z][a-z]+)').sub, r'\1_\2')
_snake_2 = partial(re.compile(r'([a-z0-9])([A-Z])').sub, r'\1_\2')


def snake_case(string: str, delimeter: str = '_') -> str:
    """Преобразование строки в snake case."""
    case = _snake_2(_snake_1(string)).casefold()
    if delimeter != '_':
        case = case.replace('_', delimeter)
    return case
