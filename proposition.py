from typing import Set, Union, Tuple
from abc import ABC, abstractmethod

class Term(ABC):
    
    """Basic Term Class: subclassed by Constant, Variable, and GroundedFunction
    """
    
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    @abstractmethod
    def __eq__(self, other) -> bool:
        pass
    
    @abstractmethod
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
        if isinstance(other, Variable):
            return other.symbol == self.symbol
        return False
    
    def __hash__(self) -> int:
        return hash((type(self), self.symbol))
    
class Function:
    
    """Function with a symbol, name, arity, and argument roles (ix to role)
    """
    
    def __init__(self, symbol: str, name: str, arity: int = 0, *, roles: Tuple[str] = ()):
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
    
    def __init__(self, function: Function, *, arguments: Tuple[Term] = ()):
        for arg in arguments:
            if not isinstance(arg, Term):
                raise TypeError(f"Argument {arg} is not a Term.")
        if len(arguments) != function.arity:
            raise ValueError(f"Grounded Function expects {function.arity} arguments, but received {len(arguments)} instead.")
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
    
    def __init__(self, symbol: str, name: str, arity: int = 0, *, roles: Tuple[str] = ()):
        if arity != len(roles) and len(roles) != 0:
            raise ValueError(f"Predicate '{symbol}' expects {arity} arguments, got {len(roles)} roles.")
        self.symbol = symbol
        self.name = name
        self.arity = arity
        self.roles = roles
        
    def __str__(self) -> str:
        return f"Predicate - symbol: {self.symbol}, name: {self.name}, arity: {self.arity}, roles: {self.roles}"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Predicate):
            return (self.symbol == other.symbol) and (self.name == other.name)
        return False
    
    def __hash__(self) -> int:
        return hash((type(self), self.symbol, self.name))
    
class AtomicProposition(ABC):
    
    """Basic Atomic Proposition Class: subclassed by PredicateExpression
    """
    
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    @abstractmethod
    def __eq__(self, other) -> bool:
        pass
    
    @abstractmethod
    def __hash__(self) -> int:
        pass
    
    @abstractmethod
    def evaluate(self, world):
        pass

class PredicateExpression(AtomicProposition):
    
    """Predicate Expression with aa predicate and arguments whose index maps to their role
    """
    
    def __init__(self, predicate: Predicate, *, arguments: Tuple[Term] = ()):
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
        
    def __eq__(self, other) -> bool:
        if isinstance(other, PredicateExpression):
            return (self.predicate == other.predicate) and (self.arguments == other.arguments)
        return False
    
    def __hash__(self) -> int:
        return hash((type(self), self.predicate, self.arguments))
    
    def evaluate(self, world) -> bool:
        if self not in world:
            raise ValueError(f"Atomic Proposition {self.__str__()} does not have an assigned truth value in world.")
        return world[self]

class ComplexProposition(ABC):
    
    """Basic Complex Proposition Type: subclassed by Negation and BinaryProposition
    """

    @abstractmethod
    def __str__(self) -> str:
        pass
    
    @abstractmethod
    def __eq__(self, other) -> bool:
        pass
    
    @abstractmethod
    def __hash__(self) -> int:
        pass
    
    @abstractmethod
    def evaluate(self, world) -> bool:
        pass

class Negation(ComplexProposition):
    
    """Negation class with proposiiton argument
    """
    
    def __init__(self, proposition: Union[AtomicProposition, ComplexProposition]):
        self.proposition = proposition
        
    def __str__(self) -> str:
        if isinstance(self.proposition, AtomicProposition) or isinstance(self.proposition, Negation):
            return f"¬{self.proposition}"
        return f"¬({self.proposition})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Negation):
            return self.proposition == other.proposition
        return False
    
    def __hash__(self) -> int:
        return hash((type(self), self.proposition))
    
    def evaluate(self, world) -> bool:
        return not self.proposition.evaluate(world)

class BinaryProposition(ComplexProposition):
    
    """Basic Binary Proposition Class: subclassed by Conjunction, Disjunction, Implication, and Biconditional
    """
    
    def __init__(self, left: Union[AtomicProposition, ComplexProposition], right: Union[AtomicProposition, ComplexProposition]):
        self.left = left
        self.right = right
        
    def __eq__(self, other) -> bool:
        if isinstance(other, type(self)):
            return (self.left == other.left) and (self.right == other.right)
        return False
    
    def __hash__(self) -> int:
        return hash((type(self), self.left, self.right))
    
    def evaluate(self, world) -> bool:
        pass

class Conjunction(BinaryProposition):
    
    """Conjunction class with left and right proposition arguments
    """
    
    def __str__(self) -> str:
        return f"({self.left} ∧ {self.right})"
    
    def evaluate(self, world) -> bool:
        return self.left.evaluate(world) and self.right.evaluate(world)

class Disjunction(BinaryProposition):
    
    """Disjunction class with left and right proposition arguments
    """
    
    def __str__(self) -> str:
        return f"({self.left} ∨ {self.right})"
    
    def evaluate(self, world) -> bool:
        return self.left.evaluate(world) or self.right.evaluate(world)

class Implication(BinaryProposition):
    
    """Implication class with left and right proposition arguments
    """
    
    def __str__(self) -> str:
        return f"({self.left} → {self.right})"
    
    def evaluate(self, world) -> bool:
        return ((not self.left.evaluate(world)) or self.right.evaluate(world))

class Biconditional(BinaryProposition):
    
    """Biconditional class with left and right proposition arguments
    """
    
    def __str__(self) -> str:
        return f"({self.left} ↔ {self.right})"
    
    def evaluate(self, world) -> bool:
        return self.left.evaluate(world) == self.right.evaluate(world)
     
if __name__ == "__main__":
    
    # Constants and Variables
    a = Constant('a', 'Alice')
    b = Constant('b', 'Bob')
    x = Variable('x')

    # Functions
    father = Function(symbol='F', name='FatherOf', arity=1, roles=('child',))
    father_of_a = GroundedFunction(function=father, arguments=(a,))

    # Predicates
    parent = Predicate(symbol='P', name='ParentOf', arity=2, roles=('parent', 'child'))

    # Predicate Expressions
    parent_expr = PredicateExpression(predicate=parent, arguments=(father_of_a, b))

    # World with truth assignments
    world = {
        parent_expr: True
    }

    # Evaluate Atomic Proposition
    print(f"{parent_expr} evaluates to {parent_expr.evaluate(world)}")  # Should print True

    # Negation
    negation = Negation(proposition=parent_expr)
    print(f"{negation} evaluates to {negation.evaluate(world)}")  # Should print False

    # Conjunction
    another_parent_expr = PredicateExpression(predicate=parent, arguments = (b, a))
    conjunction = Conjunction(left=parent_expr, right=another_parent_expr)
    world[another_parent_expr] = True
    print(f"{conjunction} evaluates to {conjunction.evaluate(world)}")  # Should print False