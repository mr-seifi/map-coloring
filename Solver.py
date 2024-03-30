from collections import deque
from typing import Callable, List, Tuple
from CSP import CSP


def Solver(object):

    def __init__(self, csp: CSP, domain_heuristics: bool = False, variable_heuristics: bool = False, AC_3: bool = False) -> None:
        """
        Initializes a Solver object.

        Args:
            csp (CSP): The Constraint Satisfaction Problem to be solved.
            domain_heuristics (bool, optional): Flag indicating whether to use domain heuristics. Defaults to False.
            variable_heuristics (bool, optional): Flag indicating whether to use variable heuristics. Defaults to False.
            AC_3 (bool, optional): Flag indicating whether to use the AC-3 algorithm. Defaults to False.
        """
        self.domain_heuristic = domain_heuristics
        self.variable_heuristic = variable_heuristics
        self.AC_3 = AC_3
        self.csp = csp
        self.queue = deque(constraint for constraint in csp.constraints)

    def backtrack_solvers(self):
        pass

    def arc_reduce(self, x, y, consistent) -> bool:
        """
        Reduce the domain of variable x based on the constraints between x and y.

        Parameters:
        - x: The first variable.
        - y: The second variable.
        - consistent: A function that checks the consistency between two values.

        Returns:
        - True if the domain of variable x is reduced, False otherwise.
        """
        new_domain = []
        for i in self.csp.variables[x]:
            flag = False
            for j in self.csp.variables[y]:
                if consistent(i, j):
                    flag = True
                    break
            if flag:
                new_domain.append(i)
        if len(new_domain) != len(self.csp.variables[x]):
            self.csp.variables[x] = new_domain
            return True
        return False

    def AC3(self) -> bool:
        """
        Applies the Arc Consistency 3 (AC3) algorithm to the constraint satisfaction problem (CSP).

        Returns:
            bool: True if the CSP is solvable, False otherwise.
        """
        queue = deque(constraint for constraint in self.csp.constraints)

        while queue:
            constraint_func, x, y = queue.popleft()
            if self.arc_reduce(x, y, constraint_func):
                if len(self.csp.variables[x]) == 0:
                    return False
                else:
                    for func, z in self.csp.var_constraints[x]:
                        if z != y:
                            queue.append((func, z, x))

        return True

    def MRV(self) -> str:
        """
        Selects the variable with the Minimum Remaining Values (MRV) heuristic.

        Returns:
            str: The variable with the fewest remaining values.
        """
        min_values = float('inf')
        selected_variable = None

        for variable in self.csp.variables:
            if len(self.csp.variables[variable]) < min_values:
                min_values = len(self.csp.variables[variable])
                selected_variable = variable

        return selected_variable

    def LCV(self, variable: str) -> List[Tuple[str, int]]:
        """
        Orders the values of a variable based on the Least Constraining Value (LCV) heuristic.

        Args:
            variable (str): The variable for which to order the values.

        Returns:
            List[Tuple[str, int]]: A list of tuples containing the value and the number of constraints it imposes.
        """
        values = self.csp.variables[variable]
        constraints_count = []

        for value in values:
            count = 0
            for constraint in self.csp.constraints:
                if variable in constraint[1] and value in self.csp.variables[constraint[2]]:
                    count += 1
            constraints_count.append((value, count))

        constraints_count.sort(key=lambda x: x[1])

        return constraints_count
