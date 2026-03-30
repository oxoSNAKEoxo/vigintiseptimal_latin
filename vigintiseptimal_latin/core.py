from fractions import Fraction

ALPHABET = ['°','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
BASE = 27
DECIMAL_PRECISION = 10
SEPARATOR = '.'


# ── Conversion ──────────────────────────────────────────────

def letters_to_number(word: str) -> Fraction:
    """Convert a vigintiseptimal latin word to a decimal Fraction.

    Each letter has a value: °=0, a=1, b=2, ..., z=26.
    The word is read as a base-27 number (most significant digit on the left).
    Supports decimals with '.' separator (e.g. "a.cd").
    """
    if not word:
        raise ValueError("Empty input.")

    parts = word.split(SEPARATOR)
    if len(parts) > 2:
        raise ValueError(f"Multiple separators '{SEPARATOR}' found in '{word}'.")

    if not parts[0]:
        raise ValueError(f"Missing integer part in '{word}'.")

    if len(parts) == 2 and not parts[1]:
        raise ValueError(f"Trailing separator in '{word}'.")

    result = Fraction(0)
    for letter in parts[0]:
        if letter not in ALPHABET:
            raise ValueError(f"Invalid character: '{letter}'. Use only a-z and °.")
        result = result * BASE + ALPHABET.index(letter)

    if len(parts) == 2:
        for i, letter in enumerate(parts[1], start=1):
            if letter not in ALPHABET:
                raise ValueError(f"Invalid character: '{letter}'. Use only a-z and °.")
            result += Fraction(ALPHABET.index(letter), BASE ** i)

    return result


def number_to_letters(n: Fraction) -> str:
    """Convert a decimal Fraction to a vigintiseptimal latin word.

    Inverse of letters_to_number.
    Non-terminating fractions are truncated to DECIMAL_PRECISION digits.
    """
    if n < 0:
        raise ValueError("Negative numbers are not supported.")

    integer = int(n)
    fractional = n - integer

    if integer == 0:
        integer_part = '°'
    else:
        digits = []
        e = integer
        while e > 0:
            e, remainder = divmod(e, BASE)
            digits.append(ALPHABET[remainder])
        integer_part = ''.join(reversed(digits))

    if fractional == 0:
        return integer_part

    decimals = []
    for _ in range(DECIMAL_PRECISION):
        fractional *= BASE
        digit = int(fractional)
        decimals.append(ALPHABET[digit])
        fractional -= digit
        if fractional == 0:
            break

    while decimals and decimals[-1] == '°':
        decimals.pop()

    if decimals:
        return integer_part + SEPARATOR + ''.join(decimals)
    return integer_part


# French aliases
lettres_vers_nombre = letters_to_number
nombre_vers_lettres = number_to_letters
PRECISION_DECIMALES = DECIMAL_PRECISION
SEPARATEUR = SEPARATOR


# ── Tokenizer ───────────────────────────────────────────────

def tokenize(expression: str):
    """Tokenize 'aa.rd+b^c' into [Fraction, '+', Fraction, '^', Fraction]."""
    tokens = []
    i = 0
    while i < len(expression):
        ch = expression[i]
        if ch in '+-*/%^()':
            tokens.append(ch)
            i += 1
        elif ch in ALPHABET or ch == SEPARATOR:
            word = ''
            while i < len(expression) and (expression[i] in ALPHABET or expression[i] == SEPARATOR):
                word += expression[i]
                i += 1
            tokens.append(letters_to_number(word))
        else:
            raise ValueError(f"Unexpected character: '{ch}'.")
    return tokens


# ── Parser (recursive descent with precedence) ─────────────
#
#   expression = term (('+' | '-') term)*
#   term       = power (('*' | '/' | '%') power)*
#   power      = atom ('^' power)?                ← right-associative
#   atom       = number | '(' expression ')'

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def expression(self):
        left = self.term()
        while self.peek() in ('+', '-'):
            op = self.consume()
            right = self.term()
            if op == '+':
                left = left + right
            else:
                left = left - right
        return left

    def term(self):
        left = self.power()
        while self.peek() in ('*', '/', '%'):
            op = self.consume()
            right = self.power()
            if op == '*':
                left = left * right
            elif op == '/':
                if right == 0:
                    raise ValueError("Division by zero.")
                left = left / right
            else:
                if right == 0:
                    raise ValueError("Modulo by zero.")
                left = left % right
        return left

    def power(self):
        base = self.atom()
        if self.peek() == '^':
            self.consume()
            exponent = self.power()  # right-associative
            if exponent.denominator != 1:
                raise ValueError("Non-integer exponents are not supported.")
            return base ** int(exponent)
        return base

    def atom(self):
        token = self.peek()
        if token == '(':
            self.consume()
            result = self.expression()
            if self.peek() != ')':
                raise ValueError("Missing closing parenthesis ')'.")
            self.consume()
            return result
        if isinstance(token, Fraction):
            self.consume()
            return token
        raise ValueError(f"Expected value, found: '{token}'.")


# ── Main function ──────────────────────────────────────────

def vigintiseptimal_latin(expression: str) -> str:
    """Evaluate an expression in Vigintiseptimal Latin (base 27, latin alphabet).

    A numeral system using the 26 letters of the latin alphabet (a=1 to z=26)
    and the ° symbol as zero.

    Supports: +, -, *, /, %, ^ (power), parentheses.
    Precedence: ^ > *, /, % > +, -

    Examples:
        vigintiseptimal_latin("a+b")       → "c"
        vigintiseptimal_latin("a+b*c")     → "g"       (b*c first)
        vigintiseptimal_latin("(a+b)*c")   → "i"       (a+b first)
        vigintiseptimal_latin("c^c")       → "a°"      (3^3 = 27)
        vigintiseptimal_latin("d/b")       → "b"       (4/2 = 2)
    """
    expression = expression.strip().lower().replace(' ', '')
    tokens = tokenize(expression)
    parser = Parser(tokens)
    result = parser.expression()

    if parser.pos < len(parser.tokens):
        raise ValueError(f"Unexpected tokens after expression: '{parser.tokens[parser.pos]}'.")

    return number_to_letters(result)


# Aliases
vigintiseptimal = vigintiseptimal_latin
calc = vigintiseptimal_latin
cal = vigintiseptimal_latin


def main():
    import sys
    if len(sys.argv) > 1:
        print(vigintiseptimal_latin(' '.join(sys.argv[1:])))
    else:
        print(vigintiseptimal_latin(input()))


if __name__ == '__main__':
    main()
