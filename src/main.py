from world import *
from lexer import Token, TokenType, Lexer
import sys

def main():
    fname = sys.argv[1]
    source = open(fname, 'r')
    lexer = Lexer(source.read())

    lexer.read_tokens()

    print(lexer.tokens)


    # Z = Term("Z", [])
    # S = lambda A: Term("S", [A])
    #
    # N1 = S(Z)
    # N2 = S(N1)
    # N3 = S(N2)
    #
    # a = Generic("a")
    # b = Generic("b")
    #
    # add = Transform("add", [])
    #
    # add.case(Case(
    #     [a, Z],
    #     a,
    # ))
    #
    # add.case(Case(
    #     [a, S(b)],
    #     Call(add, [S(a), b])
    # ))
    #
    # mult = Transform("mult", [])
    #
    # mult.case(Case(
    #     [a, Z],
    #     Z
    # ))
    #
    # mult.case(Case(
    #     [a, S(b)],
    #     add(a, mult(a, b))
    # ))
    #
    # print(mult.apply([N3, N2]))
    #
    # true = Term("T", [])
    # false = Term("F", [])
    #
    # bool_or = Transform("or", [
    #     Case([a, false], false),
    #     Case([false, a], false),
    #     Case([true, true], true)
    # ])
    #
    # print(bool_or.apply([false, true]))

if __name__ == "__main__":
    main()
