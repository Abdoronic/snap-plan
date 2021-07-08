# Snap Plan

A Residential buildings functional plan designer.

![Example generated floor layout](https://i.imgur.com/CVj0aji.png)

## Build and Run

Snap Plan requires [Python](https://www.python.org/) and [OR-Tools](https://developers.google.com/optimization) to run.

Also, it requires [Plotly](https://pypi.org/project/plotly/) for visualizations.

Examples on how to use Snap Plan can be found in both `test_bench.ipynb` notebook and `planner.test.py`. The results of the running the `test_bench` notebook can be found in the `test_bench_results.pdf` file.

Note: Visualizing a floor plan from a Python file will open a browser window with the functional layout of the floor.

## Structure

* `inputs/`: Example inputs to test the solver.
* `planner/`:
  * `constrainers/`: A collection of constrainers modules, each responsible for enforcing a certain set of constraints.
  * `io/`: IO related modules for parsing, converting and visualizing floor plans. More details about the IO format can be found in the directory's readme.
  * `models/`: containing an OOP structure of the floor, apartment, floor-level module, and other relevant modules used by the solver.
  * `solution_handler.py`: Responsible of handling intermediate solutions.
  * `solver.py`: The entry point of the Snap Plan solver.
* `planner.test.py`: Example for using Snap Plan in a Python file.
* `test_bench.ipynb`: A notebook file with multiple test runs and examples of Snap Plan.
