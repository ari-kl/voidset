from typing import List, Self, Dict

class Generic:
    name: str
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return f"<{self.name}>"

    def bind(self, term: 'Term') -> Dict[str, 'Term']:
        return { self.name: term }

    def sub(self, bindings: Dict[str, 'Term']) -> 'Term':
        return bindings[self.name]

    def matches(self, inputs: List['Term | Generic']) -> bool:
        return True

    def realize(self) -> 'Term':
        return Term("EMPTY", [])

class Term:
    struct: str
    args: List['Call | Term | Generic']

    def __init__(self, struct: str, args: List['Call | Term | Generic']) -> None:
        self.struct = struct
        self.args = args

    def __str__(self) -> str:
        if len(self.args) == 0:
            return self.struct
        else:
            return f"{self.struct}[{", ".join(map(str, self.args))}]"

    def bind(self, term: Self) -> Dict[str, Self]:
        bindings = {}

        if self.struct == term.struct:
            for (shape, real) in zip(self.args, term.args):
                if isinstance(shape, Generic):
                    bindings[shape.name] = real
                elif isinstance(shape, Term) and isinstance(real, Term):
                    bindings = bindings | shape.bind(real)

        return bindings

    def sub(self, bindings: Dict[str, 'Term']) -> 'Call | Term':
        subbed_args = []

        for arg in self.args:
            subbed_args.append(arg.sub(bindings))

        return type(self)(self.struct, subbed_args)

    def matches(self, inputs: List[Self | Generic]) -> bool:
        if len(self.args) != len(inputs):
            return False

        for (generic, real) in zip(self.args, inputs):
            if isinstance(generic, Term) and isinstance(real, Term):
                if generic.struct != real.struct:
                    return False
                else:
                    if not generic.matches(real.args):
                        return False

        return True

    def realize(self) -> Self:
        return type(self)(self.struct, [arg.realize() for arg in self.args])


class Case:
    inputs: List[Term | Generic]
    output: 'Call | Term | Generic'

    def __init__(self, inputs: List[Term | Generic], output: Term) -> None:
        self.inputs = inputs
        self.output = output

    def matches(self, inputs: List[Term]) -> bool:
        if len(self.inputs) != len(inputs):
            return False

        for (generic, real) in zip(self.inputs, inputs):
            if not generic.matches(real.args):
                return False

        return True

class Transform:
    name: str
    cases: List[Case]

    def __init__(self, name: str, cases: List[Case]) -> None:
        self.name = name
        self.cases = cases

    def case(self, case: Case):
        self.cases.append(case)

    def apply(self, terms: List[Term]) -> Term:
        for case in self.cases:
            if case.matches(terms):
                bindings = {}

                for (input, term) in zip(case.inputs, terms):
                    bindings = bindings | input.bind(term)

                subbed = case.output.sub(bindings)

                return subbed.realize()

class Call:
    name: Transform
    args: List[Self | Term | Generic]

    def __init__(self, name: Transform, args: List[Self | Term | Generic]) -> None:
        self.name = name
        self.args = args

    def sub(self, bindings: Dict[str, Term]) -> Self:
        new_args = []

        for arg in self.args:
            new_args.append(arg.sub(bindings))

        return type(self)(self.name, new_args)

    def realize(self) -> Term:
        return self.name.apply([arg.realize() for arg in self.args])
