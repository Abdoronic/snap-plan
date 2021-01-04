from ortools.sat.python import cp_model


def base_reify(condition: cp_model.Constraint, not_condition: cp_model.Constraint, model: cp_model.CpModel) -> cp_model.IntVar:
    b = model.NewBoolVar('')

    # Implement b == condition.
    model.Add(condition).OnlyEnforceIf(b)
    model.Add(not_condition).OnlyEnforceIf(b.Not())

    return b


def not_reify(a_var, model: cp_model.CpModel) -> cp_model.IntVar:
    return base_reify(
        a_var == 0,
        a_var != 0,
        model
    )


def and_reify(var_list: list, model: cp_model.CpModel) -> cp_model.IntVar:
    var_sum = sum(var_list)
    var_len = len(var_list)
    return base_reify(
        var_sum == var_len,
        var_sum != var_len,
        model
    )


def or_reify(var_list: list, model: cp_model.CpModel) -> cp_model.IntVar:
    var_sum = sum(var_list)
    return base_reify(
        var_sum >= 1,
        var_sum < 1,
        model
    )


def xor_reify(var_list: list, model: cp_model.CpModel) -> cp_model.IntVar:
    var_sum = sum(var_list)
    return base_reify(
        var_sum == 1,
        var_sum != 1,
        model
    )


def eq_tuple_reify(var_tuple: tuple, other_var_tuple: tuple, model: cp_model.CpModel) -> cp_model.IntVar:
    positional_equalities = [
        base_reify(
            var_tuple[i] == other_var_tuple[i],
            var_tuple[i] != other_var_tuple[i],
            model
        ) for i in range(len(var_tuple))
    ]
    return and_reify(positional_equalities, model)


def eq_var_reify(var: cp_model.IntVar, other_var: cp_model.IntVar, model: cp_model.CpModel) -> cp_model.IntVar:
    return base_reify(
        var == other_var,
        var != other_var,
        model
    )


def fail_reify(model: cp_model.CpModel) -> cp_model.IntVar:
    b = model.NewBoolVar('')
    model.Add(b == 0)
    return b
