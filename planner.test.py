from planner.io.parser import parse_floor
from planner.io.visualizer import visualize_floor
from planner.solver import plan_floor

floor = parse_floor('inputs/floor_input_2.json')

status, solver = plan_floor(floor)

visualize_floor(floor, solver)
