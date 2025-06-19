from world import *

def main():
    add = Transform("add", [])

    add.case(Case(
        [Generic("a"), Term("Z", [])],
        Generic("a"),
    ))

    add.case(Case(
        [Generic("a"), Term("S", [Generic("b")])],
        Call(add, [Term("S", [Generic("a")]), Generic("b")])
    ))

    Z = Term("Z", [])
    S = lambda A: Term("S", [A])

    N1 = S(Z)
    N2 = S(N1)
    N3 = S(N2)

    print(add.apply([N3, N2]))

if __name__ == "__main__":
    main()
