from collections import deque


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

    def backtrack_solvers(self):
        pass



def Solver(object):

    def __init__(self, *args, **kwargs):
        self.domain_heuristic = kwargs['domain_heuristic']
        self.variable_heuristic = kwargs['variable_heuristic']
        self.AC_3 = kwargs['AC_3']

    def AC_3(self):
        def arc_reduce(x, y, consistent):
            new_domain = []
            for i in self.variables[x]:
                flag = False
                for j in self.variables[y]:
                    if consistent(i, j):
                        flag = True
                        break
                if flag:
                    new_domain.append(i)
            if len(new_domain) != len(self.variables[x]):
                self.variables[x] = new_domain
                return True
            return False

        queue = deque(constraint for constraint in self.constraints)

        while queue:
            constraint_func, x, y = queue.popleft()
            if arc_reduce(x, y, constraint_func):
                if len(self.variables[x]) == 0:
                    return False
                else:
                    for func, z in self.var_constraints[x]:
                        if z != y:
                            queue.append((func, z, x))

        return True
    
    def MRV():
        pass
    def LCV():
        pass
