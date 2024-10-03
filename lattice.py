from typing import List, Dict, Set
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout
class ConceptLattice():
    def __init__(self, relation: Dict[str, Set[str]]):
        self.relation = relation
        self.entities = set(relation.keys())
        self.attributes = {attribute for attribute_list in relation.values() for attribute in attribute_list}
        self.inverted_relation = self.invert_relation()
        self.concepts = self.extract_concepts()
        
    def extract_concepts(self):
        intensions = list()
        curr_closure = set()
        while (curr_closure != self.attributes):
            curr_closure = self.next_closure(curr_closure)
            if(curr_closure == set()):
                return
            intensions.append(curr_closure)
        
        concepts = [{"id": i, "data": {"extension": self.up(intensions[i]), "intension": intensions[i]}} for i in range(len(intensions))]
        return concepts
    
    def child_subchild_graph(self):
        n = len(self.concepts)
        adjacency = [[0 for _ in range(n)] for _ in range(n)]  # 2D list to represent the graph
        
        for i, parent in enumerate(self.concepts):
            for j, child in enumerate(self.concepts):
                if i != j and parent['data']['intension'] < child['data']['intension']:
                    # Check if child has more attributes than the parent (subset relation)
                    if self.is_direct_child(parent, child):
                        adjacency[i][j] = 1  # Mark direct child relationship
                        
        self.plot_lattice(adjacency, verbose=True)
    
    def is_direct_child(self, parent, child):
        """Check if child is a direct child of parent."""
        parent_int = parent['data']['intension']
        child_int = child['data']['intension']
        
        # Step 1: Ensure the child is a superset of the parent
        if not parent_int < child_int:
            return False
        
        # Step 2: Ensure there is no intermediate concept
        for other_concept in self.concepts:
            other_int = other_concept['data']['intension']
            if parent_int < other_int < child_int:
                return False
        
        return True
        
    def plot_lattice(self, adjacency, verbose=False):
        """Plot the graph using NetworkX and Matplotlib with Graphviz layout."""
        # Create a directed graph
        G = nx.DiGraph()

        # Add nodes (concept IDs as labels using their intensions)
        for i, concept in enumerate(self.concepts):
            label = i
            if verbose:
                # Use the string representation of the intension set as the label
                if concept['data']['intension'] == self.attributes:
                    continue
                label_int = ', '.join(sorted(concept['data']['intension']))
                label_ext = ', '.join(sorted(concept['data']['extension']))
                label = label_int + "\n" + label_ext
            G.add_node(i, label=label)

        # Add edges based on adjacency matrix
        for i in range(len(adjacency)):
            for j in range(len(adjacency[i])):
                if adjacency[i][j] == 1:  # There's a relationship from concept i to concept j
                    G.add_edge(i, j)

        # Use Graphviz's 'dot' layout for hierarchical graphs
        pos = graphviz_layout(G, prog='dot')  # This will organize the nodes hierarchically
        labels = nx.get_node_attributes(G, 'label')

        # Draw the graph
        nx.draw_networkx(G, pos, with_labels=True, labels=labels, node_color='lightblue', 
            font_weight='normal', node_size=200, arrows=True, font_size=8)
        plt.title("Concept Lattice Child-Parent Relations (Hierarchical Layout)")
        plt.show()
       
    # compute the next closure in reverse lectic ordering 
    def next_closure(self, last_closure: Set[str]) -> Set[str]:
        curr_closure = last_closure.copy()
        for attribute in sorted(self.attributes, reverse=True):
            if attribute in curr_closure:
                curr_closure.remove(attribute)
            else:
                temp_closure = curr_closure.copy()
                temp_closure.add(attribute)
                candidate = self.closure_at(temp_closure)
                if candidate != curr_closure:
                    diff = candidate - curr_closure
                    lower_el = any(item < attribute for item in diff)
                    if not lower_el:
                        return candidate
    
    # invert dictionary of {entity: Set(attributes)} -> {aattribute: Set(entities)}
    def invert_relation(self) -> Dict[str, Set[str]]:
        inverted = dict()
        for entity in self.entities:
            for attribute in self.relation[entity]:
                if attribute in inverted:
                    inverted[attribute].add(entity)
                else:
                    inverted[attribute] = {entity}
        return inverted
     
    # compute the closure of a set of attributes
    # the set of all attributes shared by all objects having all attributes in attribute_subset               
    def closure_at(self, attribute_subset: Set[str]) -> Set[str]:
        shared_entities = self.up(attribute_subset)
        shared_attributes = self.down(shared_entities)
        return shared_attributes

    # compute the closure of a set of entities
    # the set of all entities having all attributes shared by the entities in entity_subset
    def closure_ent(self, entity_subset: Set[str]) -> Set[str]:
        shared_attributes = self.down(entity_subset)
        shared_entities = self.up(shared_attributes)
        return shared_entities
    
    def up(self, attribute_subset: Set[str]) -> Set[str]:
        # Initialize to include all entities if the attribute subset is not empty
        if not attribute_subset:
            return set()
        sharing_entities = set.intersection(*(self.inverted_relation[attribute] for attribute in attribute_subset if attribute in self.inverted_relation))
        return sharing_entities

    def down(self, entity_subset: Set[str]) -> Set[str]:
        # Initialize to include all attributes if the entity subset is not empty
        if not entity_subset:
            return self.attributes
        shared_attributes = set.intersection(*(self.relation[entity] for entity in entity_subset if entity in self.relation))
        return shared_attributes
    
    
if __name__ == "__main__":
    
    large_relation = {
        "apple": {"red", "sweet", "round", "fruit", "tree-grown"},
        "banana": {"yellow", "sweet", "curved", "fruit", "tropical"},
        "carrot": {"orange", "crunchy", "root", "vegetable", "underground"},
        "grape": {"purple", "sweet", "small", "fruit", "vine-grown"},
        "strawberry": {"red", "sweet", "small", "fruit", "soft"},
        "potato": {"brown", "starchy", "root", "vegetable", "underground"},
        "broccoli": {"green", "crunchy", "vegetable", "florets", "tree-like"},
        "watermelon": {"green", "sweet", "large", "fruit", "water-rich"},
        "lemon": {"yellow", "sour", "round", "citrus", "fruit"},
        "cherry": {"red", "sweet", "small", "fruit", "stone-fruit"},
        "tomato": {"red", "juicy", "round", "fruit", "vine-grown"},
        "onion": {"white", "pungent", "round", "vegetable", "layers"},
        "cucumber": {"green", "crunchy", "long", "vegetable", "water-rich"},
        "blueberry": {"blue", "sweet", "small", "fruit", "berry"},
        "mango": {"orange", "sweet", "tropical", "fruit", "stone-fruit"},
        "spinach": {"green", "leafy", "vegetable", "soft", "iron-rich"},
        "pineapple": {"brown", "tropical", "fruit", "spiky", "sweet"},
        "peach": {"orange", "sweet", "stone-fruit", "fuzzy", "juicy"},
        "garlic": {"white", "pungent", "clove", "vegetable", "underground"},
        "pear": {"green", "sweet", "fruit", "tree-grown", "juicy"},
        "pumpkin": {"orange", "round", "vegetable", "large", "squash"},
        "zucchini": {"green", "long", "vegetable", "soft", "summer-squash"},
        "avocado": {"green", "creamy", "fruit", "stone-fruit", "fat-rich"},
        "grapefruit": {"pink", "bitter", "citrus", "fruit", "large"},
        "kiwi": {"brown", "fuzzy", "small", "fruit", "tart"},
        "beetroot": {"purple", "earthy", "root", "vegetable", "underground"},
        "eggplant": {"purple", "soft", "vegetable", "long", "spongy"},
        "pepper": {"green", "spicy", "vegetable", "capsicum", "crunchy"},
        "plum": {"purple", "sweet", "fruit", "stone-fruit", "juicy"},
        "coconut": {"brown", "hard", "fruit", "tropical", "water-filled"},
        "lettuce": {"green", "leafy", "vegetable", "crunchy", "water-rich"},
        "raspberry": {"red", "tart", "small", "fruit", "berry"},
        "lime": {"green", "sour", "citrus", "small", "fruit"},
        "celery": {"green", "crunchy", "vegetable", "stalk", "water-rich"},
        "pomegranate": {"red", "sweet", "fruit", "seeds", "tart"},
        "papaya": {"orange", "tropical", "fruit", "sweet", "soft"},
        "cabbage": {"green", "leafy", "vegetable", "crunchy", "layers"},
        "blackberry": {"black", "sweet", "small", "fruit", "berry"},
        "radish": {"red", "spicy", "root", "vegetable", "crunchy"},
        "sweet potato": {"orange", "sweet", "root", "vegetable", "underground"},
        "corn": {"yellow", "sweet", "vegetable", "kernel", "starchy"},
        "peas": {"green", "small", "vegetable", "legume", "round"},
        "asparagus": {"green", "long", "vegetable", "spring", "tender"},
        "cantaloupe": {"orange", "sweet", "fruit", "melon", "water-rich"},
        "fig": {"purple", "sweet", "fruit", "soft", "tree-grown"},
        "dates": {"brown", "sweet", "fruit", "dry", "sticky"},
        "brussels sprouts": {"green", "small", "vegetable", "leafy", "crunchy"},
    }

    small_relation = {
        "apple": {"red", "sweet"},
        "banana": {"yellow", "curved"},
        "carrot": {"orange", "crunchy"},
        "grape": {"purple", "small"},
        "lemon": {"yellow", "sour"},
        "orange": {"orange", "citrus"},
        "potato": {"brown", "starchy"},
    }
    
    machine = ConceptLattice(small_relation)
    machine.child_subchild_graph()
    
