#!/usr/bin/env python
# coding: utf-8

# In[55]:


#!python
#cython: language_level=3
import cplex
import numpy as np

#might not be necessary
class Custom_Node():
    def __init__(self, name):
        self.name = name

class Custom_Edge():
    def __init__(self,node1,node2):
        self.node1 = node1
        self.node2 = node2
    def identify(self):
        print(f'Connecting {node1.name} to {node2.name}')

#-------------------------
def vertex_cover(vertices, edges):
    prob = cplex.Cplex()
    prob.set_problem_name("Minimum Vertex Cover")
    prob.set_problem_type(cplex.Cplex.problem_type.LP)
    prob.objective.set_sense(prob.objective.sense.minimize)

    names = [vertice for vertice in vertices]

    # Objective (linear) weights
    w_obj = np.repeat(1, len(names)).tolist()
    # Lower bounds. Since these are all zero, we could simply not pass them in as
    # all zeroes is the default.
    low_bnd = np.repeat(0, len(names)).tolist()
    # Upper bounds. The default here would be cplex.infinity, or 1e+20.
    upr_bnd = np.repeat(1, len(names)).tolist()
    prob.variables.add(names=names, obj=w_obj, lb=low_bnd, ub=upr_bnd)
    all_int = [(var, prob.variables.type.integer) for var in names]
    prob.variables.set_types(all_int)

    constraints = []
    for edge in edges:
        constraints.append([[edge[0],edge[1]], [1,1]])
    print(constraints)
    # Constraint names
    constraint_names = ["".join(x[0]) for x in constraints]
    print(constraint_names)
    # Each edge must have at least one vertex
    rhs = [1] * len(constraints)
    print(rhs)
    # We need to enter the senses of the constraints. That is, we need to tell Cplex
    # whether each constrains should be treated as an upper-limit (≤, denoted "L"
    # for less-than), a lower limit (≥, denoted "G" for greater than) or an equality
    # (=, denoted "E" for equality)
    constraint_senses = ["G"] * len(constraints)

    # And add the constraints
    prob.linear_constraints.add(names=constraint_names,
                                lin_expr=constraints,
                                senses=constraint_senses,
                                rhs=rhs)
    # Solve the problem
    print("Problem Type: %s" % prob.problem_type[prob.get_problem_type()])
    prob.solve()
    print("Solution result is: %s" % prob.solution.get_status_string())
    print(prob.solution.get_values())

def run():
    r"""
    Example Undirected Graph:
          g
        /   \
      /       \
    a --- b --- e
    | \   |   / |
    |   \ |  /  |
    c --- d --- f
    """
    prob = cplex.Cplex()
    prob.set_problem_name("Minimum Vertex Cover")

    # PROBLEM TYPE OPTIONS
    # =============================
    # Cplex.problem_type.LP
    # Cplex.problem_type.MILP
    # Cplex.problem_type.fixed_MILP
    # Cplex.problem_type.QP
    # Cplex.problem_type.MIQP
    # Cplex.problem_type.fixed_MIQP
    # Cplex.problem_type.QCP
    # Cplex.problem_type.MIQCP
    # =============================
    prob.set_problem_type(cplex.Cplex.problem_type.LP)

    # We want to find a maximum of our objective function
    prob.objective.set_sense(prob.objective.sense.minimize)

    # Variable Names
    names = ["a", "b", "c", "d", "e", "f", "g"]

    # Objective (linear) weights
    w_obj = [1, 1, 1, 1, 1, 1, 1]
    # Lower bounds. Since these are all zero, we could simply not pass them in as
    # all zeroes is the default.
    low_bnd = [0, 0, 0, 0, 0, 0, 0]
    # Upper bounds. The default here would be cplex.infinity, or 1e+20.
    upr_bnd = [1, 1, 1, 1, 1, 1, 1]
    prob.variables.add(names=names, obj=w_obj, lb=low_bnd, ub=upr_bnd)

    # How to set the variable types
    # Must be AFTER adding the variablers
    #
    # Option #1: Single variable name (or number) with type
    # prob.variables.set_types("0", prob.variables.type.continuous)
    # Option #2: List of tuples in the form (var_name, type)
    # prob.variables.set_types([("1", prob.variables.type.integer), \
    #                           ("2", prob.variables.type.binary), \
    #                           ("3", prob.variables.type.semi_continuous), \
    #                           ("4", prob.variables.type.semi_integer)])
    #
    # Vertex cover requires only integers
    all_int = [(var, prob.variables.type.integer) for var in names]
    prob.variables.set_types(all_int)

    constraints = []
    # Edge ab
    constraints.append([["a", "b"], [1, 1]])
    # Edge ac
    constraints.append([["a", "c"], [1, 1]])
    # Edge ad
    constraints.append([["a", "d"], [1, 1]])
    constraints.append([["a", "g"], [1, 1]])
    constraints.append([["b", "d"], [1, 1]])
    constraints.append([["b", "e"], [1, 1]])
    constraints.append([["c", "d"], [1, 1]])
    constraints.append([["d", "e"], [1, 1]])
    constraints.append([["d", "f"], [1, 1]])
    constraints.append([["e", "g"], [1, 1]])
    constraints.append([["f", "e"], [1, 1]])

    # Constraint names
    constraint_names = ["".join(x[0]) for x in constraints]

    # Each edge must have at least one vertex
    rhs = [1] * len(constraints)

    # We need to enter the senses of the constraints. That is, we need to tell Cplex
    # whether each constrains should be treated as an upper-limit (≤, denoted "L"
    # for less-than), a lower limit (≥, denoted "G" for greater than) or an equality
    # (=, denoted "E" for equality)
    constraint_senses = ["G"] * len(constraints)

    # And add the constraints
    prob.linear_constraints.add(names=constraint_names,
                                lin_expr=constraints,
                                senses=constraint_senses,
                                rhs=rhs)
    # Solve the problem
    print("Problem Type: %s" % prob.problem_type[prob.get_problem_type()])
    prob.solve()
    print("Solution result is: %s" % prob.solution.get_status_string())
    print(prob.solution.get_values())

#example run
vertex_cover(
    ["A","B","C"],
    [("A","B"), ("A","C"), ("B", "C")]
)
