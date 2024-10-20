from typing import Set

class Term:
    """Basic Term Class: subclassed by Constant, Variable, and GroundedFunction
    """
    def __init__(self):
        pass
    def __str__(self) -> str:
        pass
    def __eq__(self, other) -> bool:
        pass
    def __hash__(self) -> int:
        pass

class Constant(Term):
    """Constant with a symbol and a name
    """
    def __init__(self, symbol: str, name: str = None):
        self.symbol = symbol
        self.name = name
    def __str__(self) -> str:
        return self.symbol
    def __eq__(self, other) -> bool:
        if isinstance(other, Constant):
            return (other.symbol == self.symbol) and (other.name == self.name)
        return False
    def __hash__(self) -> int:
        return hash((type(self), self.symbol, self.name))

class Variable(Term):
    """Variable with a symbol
    """
    def __init__(self, symbol: str):
        self.symbol = symbol
    def __str__(self) -> str:
        return self.symbol
    def __eq__(self, other) -> bool:
        if isinstance(other, Constant):
            return other.symbol == self.symbol
        return False
    def __hash__(self) -> int:
        return hash((type(self), self.symbol))
    
class Function():
    """Function with a symbol, name, arity, and argument roles (ix to role)
    """
    def __init__(self, symbol: str, name: str, arity: int = 0, *roles: str):
        if arity != len(roles) and len(roles) != 0:
            raise ValueError(f"Function '{symbol}' expects {arity} arguments, got {len(roles)} roles.")
        self.symbol = symbol
        self.name = name
        self.arity = arity
        self.roles = roles
    def __str__(self) -> str:
        return f"Function - symbol: {self.symbol}, name: {self.name}, arity: {self.arity}, roles: {self.roles}"
    def __eq__(self, other) -> bool:
        if isinstance(other, Function):
            return (self.symbol == other.symbol) and (self.name == other.name)
        return False
    def __hash__(self) -> int:
        return hash((type(self), self.symbol, self.name))

class GroundedFunction(Term):
    """Grounded Function with a function and arguments whose index maps to their role
    """
    def __init__(self, function: Function, *arguments: Term):
        for arg in arguments:
            if not isinstance(arg, Term):
                raise TypeError(f"Argument {arg} is not a Term.")
        if len(arguments) != function.arity:
            raise ValueError(f"Grounded Function expects {function.arity} arguments, but recieved {len(arguments)} instead.")
        self.function = function
        self.arguments = arguments
    def __str__(self) -> str:
        if self.arguments:
            return f"{self.function.symbol}({', '.join(str(arg) for arg in self.arguments)})"
        else:
            return self.function.symbol
    def __eq__(self, other) -> bool:
        if isinstance(other, GroundedFunction):
            return (self.function == other.function) and (self.arguments == other.arguments)
        return False
    def __hash__(self) -> int:
        return hash((type(self), self.function, self.arguments))

class Predicate:
    """Predicate with a symbol, name, arity, and argument roles (ix to role)
    """
    def __init__(self, symbol: str, name: str, arity: int = 0, *roles: str):
        if arity != len(roles) and len(roles) != 0:
            raise ValueError(f"Predicate '{symbol}' expects {arity} arguments, got {len(roles)} roles.")
        self.symbol = symbol
        self.name = name
        self.arity = arity
        self.roles = roles
    def __str__(self) -> str:
        return f"Predicate - symbol: {self.symbol}, name: {self.name}, arity: {self.arity}, roles: {self.roles}"
    def __eq__(self, other) -> bool:
        if isinstance(other, Function):
            return (self.symbol == other.symbol) and (self.name == other.name)
        return False
    def __hash__(self) -> int:
        return hash((type(self), self.symbol, self.name))
    
class AtomicProposition:
    """Basic Atomic Proposition Class: subclassed by PredicateExpression
    """
    def __init__(self):
        pass
    def __str__(self) -> str:
        pass
    def __eq__(self, other) -> bool:
        pass
    def __hash__(self) -> int:
        pass

class PredicateExpression(AtomicProposition):
    """Predicate Expression with aa predicate and arguments whose index maps to their role
    """
    def __init__(self, predicate: Predicate, *arguments: Term):
        if predicate.arity != len(arguments):
            raise ValueError(f"Predicate '{predicate.symbol}' expects {predicate.arity} arguments, got {len(arguments)}.")
        for arg in arguments:
            if not isinstance(arg, Term):
                raise TypeError(f"Argument {arg} is not a Term.")
        self.predicate = predicate
        self.arguments = arguments
        self.truth_value = None
    def __str__(self) -> str:
        if self.arguments:
            return f"{self.predicate.symbol}({', '.join(str(arg) for arg in self.arguments)})"
        else:
            return self.predicate.symbol
    def assign_truth_value(self, truth_value: bool):
        self.truth_value = truth_value
    def __eq__(self, other) -> bool:
        if isinstance(other, PredicateExpression):
            return (self.predicate == other.predicate) and (self.arguments == other.arguments)
        return False
    def __hash__(self) -> int:
        return hash((type(self), self.predicate, self.arguments))

class ComplexProposition:
    """Basic Complex Propositon Type: subclassed by Negation and BinaryProposition
    """
    def __init__(self):
        pass
    def __str__(self) -> str:
        pass
    def __eq__(self, other) -> bool:
        pass
    def __hash__(self) -> int:
        pass
    def evaluate(self, world) -> bool:
        pass
    def get_atoms(self) -> Set[AtomicProposition]:
        pass

class Negation(ComplexProposition):
    """Negation class with proposiiton argument
    """
    def __init__(self, proposition):
        self.proposition = proposition
    def __str__(self) -> str:
        if isinstance(self.proposition, AtomicProposition) or isinstance(self.proposition, Negation):
            return f"¬{self.proposition}"
        return f"¬({self.proposition})"

class BinaryProposition(ComplexProposition):
    """Basic Binary Proposition Class: subclassed by Conjunction, Disjunction, Implication, and Biconditional
    """
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Conjunction(BinaryProposition):
    """Conjunction class with left and right proposition arguments
    """
    def __str__(self) -> str:
        return f"({self.left} ∧ {self.right})"

class Disjunction(BinaryProposition):
    """Disjunction class with left and right proposition arguments
    """
    def __str__(self) -> str:
        return f"({self.left} ∨ {self.right})"

class Implication(BinaryProposition):
    """Implication class with left and right proposition arguments
    """
    def __str__(self) -> str:
        return f"({self.left} → {self.right})"

class Biconditional(BinaryProposition):
    """Biconditional class with left and right proposition arguments
    """
    def __str__(self) -> str:
        return f"({self.left} ↔ {self.right})"
     
if __name__ == "__main__":
    
    dr_const = Constant("d1", "doctor 1")
    pat_const = Constant("p1", "patient 1")
    cond_const = Constant("c1", "condition 1")
    dx_pred = Predicate("D", "diagnosis", 3, "doctor", "patient", "condition")
    dx_sent_A = PredicateExpression(dx_pred, dr_const, pat_const, cond_const)
    
    dr_const = Constant("d2", "doctor 2")
    pat_const = Constant("p2", "patient 2")
    cond_const = Constant("c1", "condition 1")
    dx_sent_B = PredicateExpression(dx_pred, dr_const, pat_const, cond_const)
    
    conj = Conjunction(dx_sent_A, dx_sent_B)
    neg = Negation(conj)
    print(neg)