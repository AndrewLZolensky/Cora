from typing import Union, List, Set

class AtomicProposition():
    def __init__(self, proposition: str):
        self.proposition = proposition
    def __str__(self) -> str:
        return "(" + self.proposition + ")"
    def __eq__(self, other) -> bool:
        if isinstance(other, AtomicProposition):
            return other.proposition == self.proposition
        return False
    def __hash__(self):
        return hash(self.proposition)

class Conjunction():
    def __init__(self, left_conjunct: AtomicProposition, right_conjunct: AtomicProposition):
        self.left_conjunct = left_conjunct
        self.right_conjunct = right_conjunct
    def __str__(self) -> str:
        return "[" + self.left_conjunct.__str__() + " & " + self.right_conjunct.__str__() + "]"
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Conjunction):
            if (self.left_conjunct == __o.left_conjunct) and (self.right_conjunct == __o.right_conjunct):
                return True
            if (self.left_conjunct == __o.right_conjunct) and (self.right_conjunct == __o.left_conjunct):
                return True
        return False
    def __hash__(self):
        return hash(frozenset([self.left_conjunct, self.right_conjunct]))
        
class HornClause():
    def __init__(self, antecedent: Union[AtomicProposition, Conjunction], consequent: AtomicProposition):
        self.antecedent = antecedent
        self.consequent = consequent
    def __str__(self) -> str:
        return self.antecedent.__str__() + " -> " + self.consequent.__str__()
    def __hash__(self):
        return hash((self.antecedent, self.consequent))
    
class Reasoner():
    
    def __init__(self, implications: Set[HornClause], initial_knowledge_base: Set[AtomicProposition]):
        self.implications = implications
        self.initial_knowledge_base = initial_knowledge_base
        self.knowledge_base = initial_knowledge_base.copy()
        
    def __str__(self):
        temp = "\n" + "-"*80 + "\n" + "Implications:" + "\n" + "-"*80 + "\n"
        for implication in self.implications:
            temp += "\n" + implication.__str__()
        temp += "\n\n" + "-"*80 + "\n" + "Knowledge Base:" + "\n" + "-"*80 + "\n"
        for fact in self.knowledge_base:
            temp += "\n" + fact.__str__()
        return temp + "\n" + "-"*80 + "\n"
    
    def query_satisfied_by_knowledge_base(self, query: Union[AtomicProposition, Conjunction]) -> bool:
        if isinstance(query, AtomicProposition):
            for atom in self.knowledge_base:
                if query == atom:
                    return True
        if isinstance(query, Conjunction):
            satisfied_left_conjunct = False
            satisfied_right_conjunct = False
            for atom in self.knowledge_base:
                if query.left_conjunct == atom:
                    satisfied_left_conjunct = True
                if query.right_conjunct == atom:
                    satisfied_right_conjunct = True
                if satisfied_left_conjunct and satisfied_right_conjunct:
                    return True
        return False
    
    def forward_chain(self, query: AtomicProposition) -> bool:
        working_implications = self.implications.copy()
        num_cycles = 0
        num_new_facts = 0
        while True:
            if (self.query_satisfied_by_knowledge_base(query=query)):
                #print(f"process completed in {num_cycles} cycles")
                #print(f"added {num_new_facts} facts")
                return True
            num_cycles += 1
            initial_num_facts = len(self.knowledge_base)
            for implication in working_implications.copy():
                thing_to_satisfy = implication.antecedent
                satisfied = self.query_satisfied_by_knowledge_base(thing_to_satisfy)
                if satisfied:
                    self.knowledge_base.add(implication.consequent)
                    working_implications.remove(implication)
                    #print(f"cycle {num_cycles} added {implication.consequent}")
                    num_new_facts += 1
            if (len(self.knowledge_base) == initial_num_facts):
                break
        #print(f"process completed in {num_cycles} cycles")
        #print(f"added {num_new_facts} facts")
        return False
    
    def backward_chain(self, query: Union[AtomicProposition, Conjunction]):
        
        if (self.query_satisfied_by_knowledge_base(query=query)):
                return True
        if isinstance(query, AtomicProposition):
            for implication in self.implications:
                if (implication.consequent == query):
                    if self.backward_chain(implication.antecedent):
                        return True
        elif isinstance(query, Conjunction):
            for implication in self.implications:
                if (implication.consequent == query.left_conjunct):
                    if self.backward_chain(implication.antecedent) and self.backward_chain(query.right_conjunct):
                        return True
                elif (implication.consequent == query.right_conjunct):
                    if self.backward_chain(implication.antecedent) and self.backward_chain(query.left_conjunct):
                        return True
                    
        return False
     

if __name__ == "__main__":                   
    # propositions
    propA = "timmy is cool"
    propB = "timmy is friendly"
    propC = "timmy is motivated"
    propD = "timmy is successful"
    propE = "timmy is happy"

    # atomize
    atomA = AtomicProposition(proposition=propA)
    atomB = AtomicProposition(proposition=propB)
    atomC = AtomicProposition(proposition=propC)
    atomD = AtomicProposition(proposition=propD)
    atomE = AtomicProposition(proposition=propE)

    # create horn clauses
    hornAB = HornClause(atomA, atomB)
    conjunctionBC = Conjunction(atomB, atomC)
    hornBCD = HornClause(conjunctionBC, atomD)
    hornDE = HornClause(atomD, atomE)

    # should be able to prove query
    implications = {hornAB, hornBCD, hornDE}
    initial_knowledge_base = {atomA, atomC}
    query = atomE

    # create reasoner to prove query
    logos = Reasoner(implications=implications, initial_knowledge_base=initial_knowledge_base)
    print(logos.backward_chain(atomE))