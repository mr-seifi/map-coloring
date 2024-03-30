from collections import deque
from typing import Callable, List, Tuple


class CSP(object):
    def __init__(self, *args, **kwargs):
        self.variables = {}
        self.constraints = []
        self.unassigned_var = []

        self.var_constraints = {}

    def add_constraint(self, constraint_func, variables):
        self.constraints.append([constraint_func, *variables])
        try:
            self.var_constraints[variables[0]].append(
                (constraint_func, variables[1]))
        except:
            self.var_constraints[variables[0]] = [
                (constraint_func, variables[1])]

        try:
            self.var_constraints[variables[1]].append(
                (constraint_func, variables[0]))
        except:
            self.var_constraints[variables[1]] = [
                (constraint_func, variables[0])]

    def add_variable(self, variable, domain):
        self.variables[variable] = domain




