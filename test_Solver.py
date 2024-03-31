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
        self.assertIsInstance(result, list)
        for assignment in result:
            self.assertIsInstance(assignment, tuple)
            self.assertEqual(len(assignment), 2)
            self.assertIsInstance(assignment[0], str)
            self.assertIsInstance(assignment[1], str)

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

if __name__ == '__main__':
    unittest.main()