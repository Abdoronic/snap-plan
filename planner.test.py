from ortools.sat.python import cp_model

from planner.solver import plan_floor
from planner.io.parser import parse_floor
from planner.io.visualizer import visualize_floor

import time


def main():

    start_time = time.time()

    floor = parse_floor('inputs/floor_input_1.json')
    after_parse_time = time.time()
    print('Parsed in ' + str(after_parse_time - start_time) + ' seconds')

    status, solutions = plan_floor(floor)
    after_solve_time = time.time()

    ALLOWED_STATUSES = [
        cp_model.OPTIMAL,
        cp_model.FEASIBLE
    ]
    DISALLOWED_STATUSES = [
        cp_model.UNKNOWN,
        cp_model.MODEL_INVALID,
        cp_model.INFEASIBLE
    ]

    print(status)
    if (status not in ALLOWED_STATUSES):
        print('Failed to solve in ' +
              str(after_solve_time - after_parse_time) + ' seconds')
        end_time = time.time()
        print('Terminated in ' + str(end_time - start_time) + ' seconds')
        return

    print('Solved in ' + str(after_solve_time - after_parse_time) + ' seconds')

    visualize_floor(solutions[0])
    after_visualize_time = time.time()
    print('Visualized in ' + str(after_visualize_time - after_solve_time) + ' seconds')

    end_time = time.time()
    print('Terminated in ' + str(end_time - start_time) + ' seconds')


if __name__ == "__main__":
    main()
