from planner.constrainers.utils import base_reify, or_reify
from ortools.sat.python import cp_model

from planner.models.module import Module

from typing import List


def constraint_module(module: Module, model: cp_model.CpModel):
    (xs, xe, ys, ye) = module.variables

    width = module.width_variable
    length = module.length_variable
    area = module.area_variable

    model.Add(xs < xe)
    model.Add(ys < ye)
    model.Add(xe - xs == width)
    model.Add(ye - ys == length)
    model.AddMultiplicationEquality(area, [width, length])


def constraint_slim_modules(modules: List[Module], model: cp_model.CpModel):
    for module in modules:
        constraint_module(module, model)

        is_width_slim = base_reify(
            module.width_variable == 1,
            module.width_variable != 1,
            model
        )

        is_length_slim = base_reify(
            module.length_variable == 1,
            module.length_variable != 1,
            model
        )

        is_slim = or_reify([is_width_slim, is_length_slim], model)

        model.Add(is_slim == 1)

