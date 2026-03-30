# Vigintiseptimal Latin

A base-27 numeral system using the 26 letters of the latin alphabet and the ° symbol as zero.

| Symbol | ° | a | b | c | d | e | f | g | h | i | j | k | l | m | n | o | p | q | r | s | t | u | v | w | x | y | z |
|--------|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Value  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10| 11| 12| 13| 14| 15| 16| 17| 18| 19| 20| 21| 22| 23| 24| 25| 26|

## Installation

```bash
pip install vigintiseptimal-latin
```

## Usage

### Python

```python
from vigintiseptimal_latin import calc

calc("a+b")        # "c"       (1 + 2 = 3)
calc("a+b*c")      # "g"       (1 + 2*3 = 7, precedence)
calc("(a+b)*c")    # "i"       ((1+2)*3 = 9, parentheses)
calc("c^c")        # "a°"      (3^3 = 27)
calc("d/b")        # "b"       (4 / 2 = 2)
calc("g%c")        # "a"       (7 % 3 = 1)
calc("a.n+b.n")    # "d.a"     (decimals)
```

### Conversion functions

```python
from vigintiseptimal_latin import letters_to_number, number_to_letters

letters_to_number("abc")      # Fraction(786)    (1*27² + 2*27 + 3)
number_to_letters(786)         # "abc"
letters_to_number("a.i")      # Fraction(4, 3)   (1 + 9/27 = 4/3)
```

### Command line

```bash
vigintiseptimal "a+b*c"
# g
```

## Operators

| Operator | Description    | Example          | Result |
|----------|----------------|------------------|--------|
| `+`      | Addition       | `a+b`            | `c`    |
| `-`      | Subtraction    | `c-a`            | `b`    |
| `*`      | Multiplication | `b*c`            | `f`    |
| `/`      | Division       | `d/b`            | `b`    |
| `%`      | Modulo         | `g%c`            | `a`    |
| `^`      | Power          | `c^c`            | `a°`   |
| `()`     | Parentheses    | `(a+b)*c`        | `i`    |

Precedence: `^` > `*`, `/`, `%` > `+`, `-`

## Precision

Calculations use Python's `Fraction` for exact arithmetic — no floating-point errors.

Only fractions whose denominator is a power of 3 terminate in base 27 (since 27 = 3³). Non-terminating fractions are displayed truncated to 10 digits by default.

| Fraction | Base 10    | Base 27        | Terminates? |
|----------|------------|----------------|-------------|
| 1/3      | 0.333...   | °.i            | Yes (9/27)  |
| 1/9      | 0.111...   | °.c            | Yes (3/27)  |
| 1/2      | 0.5        | °.mmmmmm...    | No          |

## License

MIT
