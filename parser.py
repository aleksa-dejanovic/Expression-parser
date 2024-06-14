from tokenizer import tokenize

from enum import Enum


class UnmatchingParentheses(Exception):
    pass


class FormatError(Exception):
    def __init__(self) -> None:
        super().__init__("Neispravan format izraza")


class State(Enum):
    BIN_OP = 1
    OPERAND = 2
    UN_OP = 3


class Stack:

    def __init__(self) -> None:
        self._stack = []

    def push(self, item):
        self._stack.insert(len(self._stack), item)

    def top(self):
        if not self._stack:
            return None
        return self._stack[len(self._stack) - 1]

    def pop(self):
        ret_val = self.top()
        self._stack = self._stack[:-1]
        return ret_val

    def __bool__(self):
        return bool(self._stack)


operators = {
    "(": (0, None, None),
    ")": (0, None, None),
    "+": (1, "left", 2),
    "-": (1, "left", 2),
    "*": (2, "left", 2),
    "/": (2, "left", 2),
    "_": (3, "left", 1),
    "^": (4, "right", 2),
}


def apply(operator, *args):

    if operator == "+":
        return args[0] + args[1]
    elif operator == "-":
        return args[1] - args[0]
    elif operator == "_":
        return -args[0]
    elif operator == "*":
        return args[0] * args[1]
    elif operator == "/":
        if args[0] == 0:
            raise ZeroDivisionError()
        else:
            return args[1] / args[0]
    elif operator == "^":
        return args[1] ** args[0]


def infix_to_postfix(expression):
    """Funkcija konvertuje izraz iz infiksne u postfiksnu notaciju

    Args:
        expression (string): Izraz koji se parsira. Izraz može da sadrži cifre, zagrade, znakove računskih operacija.
        U slučaju da postoji problem sa formatom ili sadržajem izraza, potrebno je baciti odgovarajući izuzetak.

    Returns:
        list: Lista tokena koji predstavljaju izraz expression zapisan u postfiksnoj notaciji.
    Primer:
        ulaz '6.11 – 74 * 2' se pretvara u izlaz [6.11, 74, 2, '*', '-']
    """
    if not isinstance(expression, str):
        raise TypeError("Izraz mora biti string")

    stack = Stack()
    result = []
    state = State.UN_OP
    infix = tokenize(expression)
    for item in infix:
        try:
            operator = operators[item]
        except KeyError:
            if state == State.BIN_OP:
                raise FormatError()
            result.append(float(item))
            state = State.BIN_OP
            continue

        if item == "(":
            stack.push(item)
            state = State.UN_OP
        elif item == ")" and state == State.BIN_OP:
            while True:
                try:
                    top = stack.top()
                except IndexError:
                    raise UnmatchingParentheses("Nedovoljan broj otvorenih zagrada")
                if top == "(":
                    stack.pop()
                    break
                else:
                    stack.pop()
                    result.append(top)

        elif item == "-" and state == State.UN_OP:
            stack.push("_")
            state = State.OPERAND
        elif item == "+" and state == State.UN_OP:
            state = State.OPERAND

        elif state == State.BIN_OP:
            while stack and (
                (operators[stack.top()][0] > operator[0])
                or (operators[stack.top()][0] == operator[0] and operator[1] == "left")
            ):

                result.append(stack.pop())
            stack.push(item)
            state = State.OPERAND
        else:
            raise FormatError()

    while stack:
        result.append(stack.pop())

    if "(" in result:
        raise UnmatchingParentheses("Nezatvorene zagrede")
    return result


def calculate_postfix(token_list):
    """Funkcija izračunava vrednost izraza zapisanog u postfiksnoj notaciji

    Args:
        token_list (list): Lista tokena koja reprezentuje izraz koji se izračunava. Izraz može da sadrži cifre, zagrade,
         znakove računskih operacija.
        U slučaju da postoji problem sa brojem parametara, potrebno je baciti odgovarajući izuzetak.

    Returns:
        result: Broj koji reprezentuje konačnu vrednost izraza

    Primer:
        Ulaz [6.11, 74, 2, '*', '-'] se pretvara u izlaz -141.89
    """

    if not isinstance(token_list, list):
        raise TypeError("Token list mora biti lista")

    stack = Stack()

    for item in token_list:
        try:
            operator = operators[item]
        except KeyError:
            stack.push(item)
            continue

        operands = []
        for i in range(operator[2]):
            operands.append(stack.pop())
        stack.push(apply(item, *operands))

    return stack.pop()


def calculate_infix(expression):
    """Funkcija izračunava vrednost izraza zapisanog u infiksnoj notaciji

    Args:
        expression (string): Izraz koji se parsira. Izraz može da sadrži cifre, zagrade, znakove računskih operacija.
        U slučaju da postoji problem sa formatom ili sadržajem izraza, potrebno je baciti odgovarajući izuzetak.

        U slučaju da postoji problem sa brojem parametara, potrebno je baciti odgovarajući izuzetak.


    Returns:
        result: Broj koji reprezentuje konačnu vrednost izraza

    Primer:
        Ulaz '6.11 – 74 * 2' se pretvara u izlaz -141.89
    """
    return calculate_postfix(infix_to_postfix(expression))
