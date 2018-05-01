#!/usr/bin/python2
import re, string

# L_FALSE = ""
# AXIOM   = ""

# NOT_LEFT  = ""
# NOT_RIGHT = ""

# AND_LEFT  = ""
# AND_RIGHT = ""

# OR_LEFT  = ""
# OR_RIGHT = ""

# ARROW_LEFT  = ""
# ARROW_RIGHT = ""

# ARROW_LEFT  = "((.*),)*((.*)->(.*?))(,(.*))*=>(.*)"
# ARROW_RIGHT = "(.*)=>((.*),)*(.*)->(.*)(,(.*))*"

FORMULA_REGEX = "^\(\((.*)\)(->|\^|v)\((.*)\)\)$"

class sNODE:
  
    def __init__(self, parent, left, right):
        self.parent = parent

        self.left = left
        if self.left == ['']:
            self.left = []

        self.right = right
        if self.right == ['']:
            self.right = []

        self.rule = None
        self.children = []

        self.valid = True
    
    def addChild(self, child):
        print "Adding child"
        self.children.append(child)
        
    def show(self):
        return "     {} => {} ..... {}".format(", ".join(self.left), ", ".join(self.right), self.rule)

def print_tree(node):
    
    output_string = []
    
    open_set = set()
    
    root = node
    open_set.add(node)

    upto = 0
    next_level = 1
    next_level_addon = 0
    current_level_string = ""
    
    while open_set != set():
      
        next_node = open_set.pop()

        current_level_string += next_node.show()

        for child in next_node.children:
            next_level_addon += 1
            open_set.add(child)

        upto += 1
        if next_level == upto:
            output_string.append(current_level_string)
            output_string.append("-"*50)
            next_level += next_level_addon
            next_level_addon = 0
            current_level_string = ""

    print "\n".join(output_string[::-1])

def get_matches(item):
    match = re.search(FORMULA_REGEX, item)
    if match:
        return match.groups()
    else:
        return False

        
def apply_rules(item, side, LHS, RHS):
    print "Applying rules to {}, {}, {}, {}".format(item, side, LHS, RHS)
    match = get_matches(item)
    if match:
        F, op, G = match
    else:
        if item.startswith("~"):
            if side == 0:
                return ("~ L", [(LHS, [item[1:]]+RHS)])
            else:
                return ("~ R", [([item[1:]]+LHS, RHS)])
        else:
            return None

    
    if op == "->":
        if side == 0:
            return ("-> L", [(LHS, [F]+RHS), ([G]+LHS, RHS)])
        else:
            ("-> R", [([F]+LHS, [G]+RHS)])
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
        
def check_valid(LHS, RHS):
    if "!" in LHS:
        return "!L"
    for item in LHS:
        if item in string.uppercase:
            if item in RHS:
                return "Ax"
    return None
  
def parse_formula(node):
  
    LHS = node.left
    RHS = node.right
    
    is_valid = check_valid(LHS, RHS)
    if is_valid:
        node.rule = is_valid
        return True
    
    for i in xrange(len(LHS)):
        item = LHS[i]
        result = apply_rules(item, 0, LHS[:i] + LHS[i+1:], RHS)
        if result is not None:
            node.rule = result[0]
            for left, right in result[1]:
                new_child = sNODE(node, left, right)
                node.addChild(new_child)
            return True
    
    for i in xrange(len(RHS)):
        item = RHS[i]
        result = apply_rules(item, 1, LHS, RHS[:i] + RHS[i+1:])
        if result is not None:
            node.rule = result[0]
            print result
            for left, right in result[1]:
                new_child = sNODE(node, left, right)
                node.addChild(new_child)
            return True

    # No more rules can be applied and is not valid
    return False

def parse_node(root, node):
    res = parse_formula(node)
    if res == False:
        root.valid = False
    print "Children"
    print node.children
    for child in node.children:
        parse_node(root, child)
    
def parse_tree(node):
    parse_node(node, node)

lhs_inp = raw_input(": ").split(",")
rhs_inp = raw_input(": ").split(",")

root_node = sNODE(None, lhs_inp, rhs_inp)

parse_tree(root_node)

print "PRINTING TREE"
print "-"*50
print_tree(root_node)
print root_node.valid