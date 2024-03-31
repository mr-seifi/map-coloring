
import unittest
from CSP import CSP
from Solver import Solver


class TestSolver(unittest.TestCase):

    def test_backtrack_solver(self):
        # Create a CSP object and add variables and constraints
        csp = CSP()
        csp.add_variable('A', ['red', 'green', 'blue'])
        csp.add_variable('B', ['red', 'green'])
        csp.add_variable('C', ['red', 'blue'])
        csp.add_constraint(lambda a, b: a != b, ['A', 'B'])
        csp.add_constraint(lambda a, c: a != c, ['A', 'C'])

        # Create a Solver object
        solver = Solver(csp)

        # Call the backtrack_solver method
        result = solver.backtrack_solver()

        # Assert that the result is not None
        self.assertIsNotNone(result)

        # Assert that the result is a list of variable-value assignments
        self.assertIsInstance(result, dict)
        for variable, value in result.items():
            self.assertIsInstance(variable, str)
            self.assertIsInstance(value, str)

    def test_select_unassigned_variable(self):
        # Create a CSP object and add variables
        csp = CSP()
        csp.add_variable('A', ['red', 'green', 'blue'])
        csp.add_variable('B', ['red', 'green'])
        csp.add_variable('C', ['red', 'blue'])

        # Create a Solver object
        solver = Solver(csp)

        # Call the select_unassigned_variable method
        variable = solver.select_unassigned_variable()

        # Assert that the variable is not None
        self.assertIsNotNone(variable)

        # Assert that the variable is a string
        self.assertIsInstance(variable, str)

        # Assert that the variable is unassigned
        self.assertFalse(csp.is_assigned(variable))

    def test_ordered_domain_value(self):
        # Create a CSP object and add variables
        csp = CSP()
        csp.add_variable('A', ['red', 'green', 'blue'])
        csp.add_variable('B', ['red', 'green'])
        csp.add_variable('C', ['red', 'blue'])

        # Create a Solver object
        solver = Solver(csp)

        # Call the ordered_domain_value method for variable 'A'
        ordered_values = solver.ordered_domain_value('A')

        # Assert that the ordered_values is not None
        self.assertIsNotNone(ordered_values)

        # Assert that the ordered_values is a list
        self.assertIsInstance(ordered_values, list)

        # Assert that the ordered_values is in a specific order
        expected_order = ['red', 'green', 'blue']
        self.assertEqual(ordered_values, expected_order)

    def test_arc_reduce(self):
        # Create a CSP object and add variables and constraints
        csp = CSP()
        csp.add_variable('A', ['red', 'green', 'blue'])
        csp.add_variable('B', ['red', 'green'])
        csp.add_variable('C', ['red', 'blue'])
        csp.add_constraint(lambda a, b: a != b, ['A', 'B'])
        csp.add_constraint(lambda a, c: a != c, ['A', 'C'])

        # Create a Solver object
        solver = Solver(csp)

        # Call the arc_reduce method
        reduced_domains = solver.arc_reduce('A', 'B', csp.are_consistent)

        # Assert that the reduced_domains is not None
        self.assertIsNotNone(reduced_domains)

        # Assert that the reduced_domains is a list
        self.assertIsInstance(reduced_domains, list)

        # Assert that the reduced_domains contains valid values
        for domain in reduced_domains:
            self.assertIsInstance(domain, str)

    def test_apply_AC3(self):
        # Create a CSP object and add variables and constraints
        csp = CSP()
        csp.add_variable('A', ['red', 'green', 'blue'])
        csp.add_variable('B', ['red', 'green'])
        csp.add_variable('C', ['red', 'blue'])
        csp.add_constraint(lambda a, b: a != b, ['A', 'B'])
        csp.add_constraint(lambda a, c: a != c, ['A', 'C'])

        # Create a Solver object
        solver = Solver(csp)

        # Call the apply_AC3 method
        result = solver.apply_AC3()

        # Assert that the result is not None
        self.assertIsNotNone(result)

        # Assert that the result is a list of variable-value assignments
        self.assertIsInstance(result, dict)
        for variable, value in result.items():
            self.assertIsInstance(variable, str)
            self.assertIsInstance(value, str)

    def test_MRV(self):
        # Create a CSP object and add variables
        csp = CSP()
        csp.add_variable('A', ['red', 'green', 'blue'])
        csp.add_variable('B', ['red', 'green'])
        csp.add_variable('C', ['red', 'blue'])

        # Create a Solver object
        solver = Solver(csp)

        # Call the MRV method
        variable = solver.MRV()

        # Assert that the variable is not None
        self.assertIsNotNone(variable)

        # Assert that the variable is a string
        self.assertIsInstance(variable, str)

    def test_LCV(self):
        # Create a CSP object and add variables
        csp = CSP()
        csp.add_variable('A', ['red', 'green', 'blue'])
        csp.add_variable('B', ['red', 'green'])
        csp.add_variable('C', ['red', 'blue'])

        # Create a Solver object
        solver = Solver(csp)

        # Call the LCV method for variable 'A'
        ordered_values = solver.LCV('A')

        # Assert that the ordered_values is not None
        self.assertIsNotNone(ordered_values)

        # Assert that the ordered_values is a list
        self.assertIsInstance(ordered_values, list)

        # Assert that the ordered_values contains valid values
        for value in ordered_values:
            self.assertIsInstance(value, str)



if __name__ == '__main__':
    unittest.main()