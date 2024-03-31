import argparse
from enum import Enum
from CSP import CSP
from Solver import Solver
from map_generator import generate_borders_by_continent
from graphics import draw


class Continent(Enum):
    asia = "Asia"
    africa = "Africa"
    america = "America"
    europe = "Europe"
    ocenia = "Ocenia"

    def __str__(self):
        return self.value
    

def main():
    parser = argparse.ArgumentParser(
        prog="Map Coloring",
        description="Utilizing CSP to solve map coloring problem",
    )

    parser.add_argument(
        "-m",
        "--map",
        type=Continent,
        choices=list(Continent),
        help="Map must be: [Asia, Africa, America, Europe, Ocenia]",
    )
    parser.add_argument(
        "-lcv",
        "--lcv",
        action="store_true",
        help="Enable least constraint value (LCV) as a order-type optimizer"
    )
    parser.add_argument(
        "-mrv",
        "--mrv",
        action="store_true",
        help="Enable minimum remaining values (MRV) as a order-type optimizer"
    )
    parser.add_argument(
        "-ac3",
        "--arc-consistency",
        action="store_true",
        help="Enable arc consistency as a mechanism to eliminate the domain of variables achieving an optimized solution"
    )

    args = parser.parse_args()
    borders = generate_borders_by_continent(continent=str(args.map))
    # print(borders)
    csp = CSP()
    for country, neighbors in borders.items():
        csp.add_variable(country, ['red', 'green', 'blue', 'yellow'])
        for neighbor in neighbors:
            csp.add_constraint(lambda a, b: a != b, [country, neighbor])

    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ constraints $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print(csp.constraints)

    # print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ variables $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # csp.add_variable('A', ['red', 'green', 'blue'])
    # csp.add_variable('B', ['red', 'green'])
    # csp.add_variable('C', ['red', 'blue'])
    # csp.add_constraint(lambda a, b: a != b, ['A', 'B'])
    # csp.add_constraint(lambda a, c: a != c, ['A', 'C'])

    solver = Solver(csp, domain_heuristics=args.lcv, 
                    variable_heuristics=args.mrv, 
                    AC_3=args.arc_consistency)
    result = solver.backtrack_solver()
    print("Assignment Number :",solver.csp.assignments_number)

    draw(solution=result, continent=str(args.map), assignments_number=solver.csp.assignments_number)
    

if __name__ == '__main__':
    main()