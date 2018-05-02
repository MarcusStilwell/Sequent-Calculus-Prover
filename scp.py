#!/usr/bin/python2
import re, string

# Regex for generic formula (doesn't work)
# FORMULA_REGEX = "^\(\((.*)\)(->|\^|v)\((.*)\)\)$"

# Regex for smallest formula possible (literal primitive literal)
SINGLE_FORMULA = "^\s*(~?[A-Z!])\s*(->|\^|v)\s*(~?[A-Z!])\s*$"

# Class representing a node
class sNODE:
  
    def __init__(self, parent, left, right):
        self.parent = parent

        # LHS
        self.left = left
        if self.left == ['']:
            self.left = []

        # RHS
        self.right = right
        if self.right == ['']:
            self.right = []

        # Rule applied
        self.rule = None

        # Children
        self.children = []

        # Used for the root, to specify whether valid
        self.valid = True
    
    def addChild(self, child):
        self.children.append(child)
        
    def show(self):
        return "     {} => {} ..... {}".format(", ".join(self.left), ", ".join(self.right), self.rule)

def print_tree(node):
    
    # Use bfs to go level by level
    output_string = []
    
    open_set = set()
    open_set.add(node)
    
    root = node

    # Use to keep track of level
    upto = 0
    next_level = 1
    next_level_addon = 0
    current_level_string = ""
    
    while open_set != set():
      
        next_node = open_set.pop()

        current_level_string += "       "*len(next_node.children) + next_node.show()

        for child in next_node.children:
            next_level_addon += 1
            open_set.add(child)

        upto += 1
        if next_level == upto:
            output_string.append(current_level_string)
            output_string.append("-"*100)
            next_level += next_level_addon 
            next_level_addon = 0
            current_level_string = ""

    print "\n".join(output_string[::-1])

# Check if brackets match
def check_brackets(formula):
    outer_count = 0
    char_count = 0
    for c in formula:
        char_count += 1
        if c == "(":
            outer_count += 1
        elif c == ")":
            outer_count -= 1
        if outer_count < 0:
            return False
    if outer_count != 0:
        return False
    return True

# Gets the next matching set of brackets
def get_next_bracket_match(item):
    if not item.startswith("("):
        return None
    outer_count = 0
    char_count = 0
    for c in item:
        char_count += 1
        if c == "(":
            outer_count += 1
        elif c == ")":
            outer_count -= 1
        if outer_count == 0:
            return char_count


def get_matches(item):

    # Make sure the item exists
    item = item.strip(" ")
    if item == "":
        return False

    orig_item = item

    # Remove outer brackets
    while get_next_bracket_match(item) == len(item):
        item = item[1:-1]
        item = item.strip(" ")

    # Attempt to match F op G
    match = re.search(SINGLE_FORMULA, item)
    if match:
        return match.groups()

    # Attempt to match (F) op (G)
    next_b = get_next_bracket_match(item)
    if next_b is not None:
        F = item[:next_b].strip(" ")
        item = item[next_b:].strip(" ")

        if item.startswith("->"):
            op = "->"
            item = item[2:].strip(" ")
        elif item.startswith("^"):
            op = "^"
            item = item[1:].strip(" ")
        elif item.startswith("v"):
            op = "v"
            item = item[1:].strip(" ")
        else:
            op = ""

        if op != "":
            next_b = get_next_bracket_match(item)
            if next_b is not None:
                G = item[:next_b].strip(" ")
                item = item[next_b:].strip(" ")

                if item == "":
                    return F, op, G

    item = orig_item

    # Attempt to match (F) op G
    next_b = get_next_bracket_match(item)
    if next_b is not None:
        F = item[:next_b].strip(" ")
        item = item[next_b:].strip(" ")

        if item.startswith("->"):
            op = "->"
            item = item[2:].strip(" ")
        elif item.startswith("^"):
            op = "^"
            item = item[1:].strip(" ")
        elif item.startswith("v"):
            op = "v"
            item = item[1:].strip(" ")
        else:
            op = ""


        if op != "":
            if check_brackets(item):
                G = item
                return F, op, G


    item = orig_item


    # Attempt to match F op (G)
    F = ""
    while item != "":
        if item.startswith("->"):
            op = "->"
            item = item[2:].strip(" ")
            break
        elif item.startswith("^"):
            op = "^"
            item = item[1:].strip(" ")
            break
        elif item.startswith("v"):
            op = "v"
            item = item[1:].strip(" ")
            break
        else:
            F += item[0]
            item = item[1:]

    next_b = get_next_bracket_match(item)
    if next_b is not None:
        G = item[:next_b].strip(" ")
        item = item[next_b:].strip(" ")

        if item == "":
            return F, op, G

    return False

        
def apply_rules(item, side, LHS, RHS):

    # Start with ~ rule
    if item.startswith("~"):
        if side == 0:
            return ("~ L", [(LHS, [item[1:]]+RHS)])
        else:
            return ("~ R", [([item[1:]]+LHS, RHS)])
    else:
        # Try get F op G
        match = get_matches(item)
        if match:
            F, op, G = match
        else:
            return None

    # Apply the rules, returning rule used and LHS/RHS
    if op == "->":
        if side == 0:
            return ("-> L", [(LHS, [F]+RHS), ([G]+LHS, RHS)])
        else:
            return ("-> R", [([F]+LHS, [G]+RHS)])
    if op == "^":
        if side == 0:
            return ("^ L", [([F]+[G]+LHS, RHS)])
        else:
            return ("^ R", [(LHS, [F]+RHS), (LHS, [G]+RHS)])
    if op == "v":
        if side ==0:
            return ("v L", [([F]+LHS, RHS), ([G]+LHS, RHS)])
        else:
            return ("v R", [(LHS, [F]+[G]+RHS)])
    
    return None

# Check if valid
def check_valid(LHS, RHS):
    if "!" in LHS:
        return "!L"
    for item in LHS:
        if item in string.uppercase:
            if item in RHS:
                return "Ax"
    return None

# Remove all brackets and whitespace in all items in LHS and RHS
def remove_brackets_whitespace(node):

    new_lhs = []
    for item in node.left:
        item = item.strip(" ")
        while get_next_bracket_match(item) == len(item):
            item = item[1:-1]
            item = item.strip(" ")
        new_lhs.append(item)


    new_rhs = []
    for item in node.right:
        item = item.strip(" ")
        while get_next_bracket_match(item) == len(item):
            item = item[1:-1]
            item = item.strip(" ")
        new_rhs.append(item)

    node.left = new_lhs
    node.right = new_rhs

# Find a rule to apply to a node
def parse_formula(node):

    # Remove brackets and whitespace first
    remove_brackets_whitespace(node)
    LHS = node.left
    RHS = node.right
    
    # Check if already valid
    is_valid = check_valid(LHS, RHS)
    if is_valid:
        node.rule = is_valid
        return True
    
    # Go through the LHS
    for i in xrange(len(LHS)):
        item = LHS[i]
        result = apply_rules(item, 0, LHS[:i] + LHS[i+1:], RHS)
        if result is not None:
            node.rule = result[0]
            for left, right in result[1]:
                new_child = sNODE(node, left, right)
                node.addChild(new_child)
            return True
    
    # Go through the RHS
    for i in xrange(len(RHS)):
        item = RHS[i]
        result = apply_rules(item, 1, LHS, RHS[:i] + RHS[i+1:])
        if result is not None:
            node.rule = result[0]
            for left, right in result[1]:
                new_child = sNODE(node, left, right)
                node.addChild(new_child)
            return True

    # No more rules can be applied and is not valid
    return False

# Parse a node
def parse_node(root, node):
    res = parse_formula(node)
    if res == False:
        root.valid = False
    for child in node.children:
        parse_node(root, child)
    
# Parse a tree (treats the node as the root)
def parse_tree(node):
    parse_node(node, node)

# Grab the input
lhs_inp = raw_input("Hypotheses: ").split(",")
rhs_inp = raw_input("Conclusion: ").split(",")

# Check the brackets match
if check_brackets(lhs_inp) and check_brackets(rhs_inp):

    # Create the tree
    root_node = sNODE(None, lhs_inp, rhs_inp)

    parse_tree(root_node)

    print "Printing tree"
    print_tree(root_node)
    print ""
    print "Valid: {}".format(root_node.valid)
else:
    print "Mismatched brackets"