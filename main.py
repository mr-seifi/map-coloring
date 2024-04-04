import argparse
from enum import Enum
from CSP import CSP
from Solver import Solver
from map_generator import generate_borders_by_continent
from graphics import draw
import random

class Continent(Enum):
    asia = "Asia"
    africa = "Africa"
    america = "America"
    europe = "Europe"

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
        help="Map must be: [Asia, Africa, America, Europe]",
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
    parser.add_argument(
        "-ND",
        "--Neighbourhood-distance",
        type=int,
        default=1,
        help="The value determines the threshold for neighboring regions' similarity in color, with a default of 1 ensuring adjacent regions have distinct colors; increasing it, for instance to 2, extends this dissimilarity to the neighbors of neighbors."
    )
    args = parser.parse_args()
    borders = generate_borders_by_continent(continent=str(args.map), neighbor_threshold=args.Neighbourhood_distance)
    # print(borders)
    random.seed(10)
    def generate_color():
        r = random.random()
        g = random.random()
        b = random.random()
        return (r, g, b)

    colors = [generate_color() for _ in range(100)]
    result = None
    colors_count = 4
    while(result==None):
        print(f'Algorithm starts with {colors_count} colors')
        color_list = colors[:colors_count]
        csp = CSP()
        for country, neighbors in borders.items():
            csp.add_variable(country, color_list)
            for neighbor in neighbors:
                csp.add_constraint(lambda a, b: a != b, [country, neighbor])

        solver = Solver(csp, domain_heuristics=args.lcv, 
                        variable_heuristics=args.mrv, 
                        AC_3=args.arc_consistency)
        result = solver.backtrack_solver()
        colors_count += 1


    # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ constraints $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # print(csp.constraints)

    # print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ variables $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    # csp.add_variable('A', ['red', 'green', 'blue'])
    # csp.add_variable('B', ['red', 'green'])
    # csp.add_variable('C', ['red', 'green', 'blue'])
    # csp.add_constraint(lambda a, b: a != b, ['A', 'B'])
    # csp.add_constraint(lambda a, c: a != c, ['A', 'C'])
    # csp.add_constraint(lambda b, c: b != c, ['B', 'C'])


    # solver = Solver(csp, domain_heuristics=args.lcv, 
    #                 variable_heuristics=args.mrv, 
    #                 AC_3=args.arc_consistency)
    # result = solver.backtrack_solver()
    print("Assignment Number :",solver.csp.assignments_number)
    print("solution :",solver.csp.assignments)

    draw(solution=result, continent=str(args.map), assignments_number=solver.csp.assignments_number)
    

if __name__ == '__main__':
    main()