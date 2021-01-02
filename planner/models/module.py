from ortools.sat.python import cp_model

from typing import Tuple


class Module:
    def __init__(self):
        self.variables: Tuple[
            cp_model.IntVar,
            cp_model.IntVar,
            cp_model.IntVar,
            cp_model.IntVar
        ] = None
        self.width_variable: cp_model.IntVar = None
        self.length_variable: cp_model.IntVar = None
        self.area_variable: cp_model.IntVar = None
