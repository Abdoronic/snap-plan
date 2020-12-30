import uuid


def base_reify(condition, not_condition, model):
    b = model.NewBoolVar(str(uuid.uuid4()))

    # Implement b == condition.
    model.Add(condition).OnlyEnforceIf(b)
    model.Add(not_condition).OnlyEnforceIf(b.Not())

    return b


def not_reify(a_var, model):
    return base_reify(
        a_var == 0,
        a_var != 0,
        model
    )


def sum_vars(var_list):
    var_sum = 0
    for var in var_list:
        var_sum += var
    return var_sum


def and_reify(var_list, model):
    var_sum = sum_vars(var_list)
    var_len = len(var_list)
    return base_reify(
        var_sum == var_len,
        var_sum != var_len,
        model
    )


def or_reify(var_list, model):
    var_sum = sum_vars(var_list)
    return base_reify(
        var_sum >= 1,
        var_sum < 1,
        model
    )


def xor_reify(var_list, model):
    var_sum = sum_vars(var_list)
    return base_reify(
        var_sum == 1,
        var_sum != 1,
        model
    )


def eq_reify(var1, var2, model):
    return base_reify(
        var1 == var2,
        var2 != var2,
        model
    )


def add_if_then_else(unique_name, if_condition, else_condition, then_constraint, else_constraint, model):
    """Constrains that for model when the if_condition holds, then_constraint is enforced and that otherwise when else_condition holds, else_constraint is enforced. This creates a BoolVar to enforce the constraints, which is returned. Based on official code at https://github.com/google/or-tools/blob/master/ortools/sat/doc/channeling.md#if-then-else-expressions

    Parameters
    ----------
        unique_name: str
            Name to uniquely identify a generated BoolVar.
        if_condition: BoundedLinearExpression
            When satisfied, the then_constraint is enforced.
        else_condition: BoundedLinearExpression
            When satisfied, the else_constraint is enforced. This must be the logical negation of if_condition.
        then_constraint: BoundedLinearExpression
            Enforced when if_condition holds.
        else_constraint: BoundedLinearExpression
            Enforced when else_condition holds.
        model: CpModel
            Model to add the constraints to.

    Returns
    -------
        BoolVar
            BoolVar created to enforce the complex constraint.
    """

    # Declare intermediate boolean variable.
    b = model.NewBoolVar(unique_name)

    # Implement b == if_condition.
    model.Add(if_condition).OnlyEnforceIf(b)
    model.Add(else_condition).OnlyEnforceIf(b.Not())

    # Create two half-reified constraints.
    # First, b implies then_constraint.
    model.Add(then_constraint).OnlyEnforceIf(b)
    # Second, not(b) implies else_constraint.
    model.Add(else_constraint).OnlyEnforceIf(b.Not())

    return b
