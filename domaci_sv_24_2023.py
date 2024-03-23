# OVE TRI METODE ĆE BITI POZIVANE KROZ AUTOMATSKE TESTOVE. NEMOJTE MENJATI NAZIV, PARAMETRE I POVRATNU VREDNOST.
# Dozvoljeno je implementirati dodatne, pomoćne metode, ali isključivo u okviru ovog modula.

from functools import total_ordering

from tokenizer import tokenize


class UnmatchingParentheses(Exception):
    pass


""" @total_ordering
class Priority:
    def __init__(self, operator,  value, associativity):
        self.operator = operator
        self.value = value
        self.associativity = associativity

    def  __lt__(self, other):
        if not isinstance(other, Priority):
            raise TypeError("Cannot compare instances of 'Priority' and '{0}'".format(type(other).__name__))
        return (self.value < other.value)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Priority):
            raise TypeError("Cannot compare instances of 'Priority' and '{0}'".format(type(other).__name__))
        return self.value == other.value """


operators = {
    "(": (0, None, None),
    ")": (0, None, None),
    "+": (1, "left", 2),
    "-": (1, "left", 2),
    "_": (1, "left", 1),
    "*": (2, "left", 2),
    "/": (2, "left", 2),
    "^": (3, "right", 2),
}


def numify(l):
    return [float(item) for item in l]


def apply(operator, *args):
    args = numify(args)

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
    stack = []
    result = []
    unary_flag = True
    infix = tokenize(expression)
    for item in infix:
        try:
            operator = operators[item]
        except KeyError:
            result.append(item)
            continue

        if item == "(":
            stack.append(item)
            unary_flag = True
            continue
        elif item == ")":
            while True:
                try:
                    top = stack[-1]
                except IndexError:
                    raise ValueError("Nedovoljan broj otvorenih zagrada")
                if top == "(":
                    stack.pop()
                    break
                else:
                    stack.pop()
                    result.append(top)
        elif unary_flag and item == "-":
            unary_flag = False
            stack.append("_")

        else:
            while stack and (
                (operators[stack[-1]][0] > operator[0])
                or (operators[stack[-1]][0] == operator[0] and operator[1] == "left")
            ):

                result.append(stack.pop())
            stack.append(item)

    while stack:
        result.append(stack.pop())

    if "(" in result:
        raise UnmatchingParentheses
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
    stack = []

    for item in token_list:
        try:
            operator = operators[item]
        except KeyError:
            stack.append(item)
            continue

        operands = []
        for i in range(operator[2]):
            operands.append(stack.pop())
        stack.append(apply(item, *operands))

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


exp = "(-6.11 - (-74)) * 2 ^ 2 ^ 3 - 2 ^ ((1 / 2)"

print(infix_to_postfix(exp))
print(calculate_infix(exp))
