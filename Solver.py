from collections import deque
from typing import Callable, List, Tuple
from CSP import CSP


class Solver(object):

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


    def backtrack_solver(self) -> List[Tuple[str, str]]:
        """
        Backtracking algorithm to solve the constraint satisfaction problem (CSP).

        Returns:
            List[Tuple[str, str]]: A list of variable-value assignments that satisfy all constraints.
        """

        if self.csp.is_complete():
            return self.csp.assignments

        variable = self.select_unassigned_variable()

        for value in self.ordered_domain_value(variable):
            if self.csp.is_consistent(variable, value):
                removed_values_from_domain = []
                for other_value in self.csp.variables[variable]:
                    if other_value != value:
                        removed_values_from_domain.append((variable, other_value))
              
                self.csp.assign(variable, value)
                
                if self.AC_3 is True:
                    if self.apply_AC3() is not None:
                        removed_values_from_domain.extend(self.apply_AC3())
                
                result = self.backtrack_solver()
                if result is not None:
                    return result
                self.csp.unassign(removed_values_from_domain, variable)

        return None

    def select_unassigned_variable(self) -> str:
        """
        Selects an unassigned variable using the MRV heuristic.

        Returns:
            str: The selected unassigned variable.
        """
        if self.variable_heuristic:
            return self.MRV()
        return self.csp.unassigned_var[0]

    def ordered_domain_value(self, variable: str) -> List[str]:
        """
        Returns a list of domain values for the given variable in a specific order.

        Args:
            variable (str): The name of the variable.

        Returns:
            List[str]: A list of domain values for the variable in a specific order.
        """
        # Function implementation goes here
        if self.domain_heuristic:
            return self.LCV(variable)
        return self.csp.variables[variable]

        

    def arc_reduce(self, x, y, consistent) -> List[str]:
        """
        Reduce the domain of variable x based on the constraints between x and y.

        Parameters:
        - x: The first variable.
        - y: The second variable.
        - consistent: A function that checks the consistency between two values.

        Returns:
        - The reduced domain of variable x if the domain is reduced, None otherwise.
        """
        if y not in self.csp.variables or x not in self.csp.variables:
            return None
        new_domain = [i for i in self.csp.variables[x] if any(consistent(i, j) for j in self.csp.variables[y])]
        if len(new_domain) != len(self.csp.variables[x]):
            return new_domain
        return None

    def apply_AC3(self) -> List[Tuple[str, str]]:
        """
        Applies the AC3 algorithm to reduce the domains of variables in the CSP.

        Returns:
            A list of tuples representing the removed values from the domain of variables.
        """
        queue = deque(constraint for constraint in self.csp.constraints)
        removed_values_from_domain = []
        while queue:
            constraint_func, x, y = queue.popleft()
            new_domain = self.arc_reduce(x, y, constraint_func)
            if new_domain is not None:
                removed_values_from_domain.extend((x, j) for j in self.csp.variables[x] if j not in new_domain)
                self.csp.variables[x] = new_domain
                if len(new_domain) == 0:
                    return None
                else:
                    for func, z in self.csp.var_constraints[x]:
                        if z != y:
                            queue.append((func, z, x))

        return removed_values_from_domain

    def MRV(self) -> str:
        """
        Selects the variable with the Minimum Remaining Values (MRV) heuristic.

        Returns:
            str: The variable with the fewest remaining values.
        """
        min_values = float('inf')
        selected_variable = None

        for variable in self.csp.unassigned_var:
            if len(self.csp.variables[variable]) < min_values:
                min_values = len(self.csp.variables[variable])
                selected_variable = variable

        return selected_variable

    def LCV(self, variable: str) -> List[str]:
        """
        Orders the values of a variable based on the Least Constraining Value (LCV) heuristic.

        Args:
            variable (str): The variable for which to order the values.

        Returns:
            List[str]: A list of values sorted based on the number of constraints they impose.
        """
        values = self.csp.variables[variable]
        constraints_count = []

        for value in values:
            count = 0
            for constraint_func, other_variable in self.csp.var_constraints[variable]:
                if other_variable in self.csp.variables and value in self.csp.variables[other_variable]:
                    count += 1
            constraints_count.append((value, count))

        constraints_count.sort(key=lambda x: x[1])

        return [value for value, _ in constraints_count]
