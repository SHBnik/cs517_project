#!python
#cython: language_level=3
import cplex
import numpy as np

def vertex_cover(vertices, edges):
    print(vertices)
    print(edges)
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
    #print("Problem Type: %s" % prob.problem_type[prob.get_problem_type()])
    prob.solve()
    #print("Solution result is: %s" % prob.solution.get_status_string())
    #print(prob.solution.get_values())
    vertexCovers = []
    solutions = prob.solution.get_values()
    for j in range(0,len(solutions)):
        if solutions[j] == 1:
            vertexCovers.append(vertices[j])
    return vertexCovers
