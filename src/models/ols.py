import statsmodels.formula.api as smf


def build_formula(df, dependent_variable, treatment, control_variables):
    lhs = f"standardize({dependent_variable})"
    rhs = f"C(treatment, Treatment(reference='{treatment['reference']}'))"
    for control_variable in control_variables:
        if df[control_variable].dtype == object:
            rhs += f" + C({control_variable})"
        else:
            rhs += f" + standardize({control_variable})"
    return lhs + " ~ " + rhs


def fit_model(df, formula):
    return smf.ols(
        formula=formula,
        data=df[df.experiment_active == True],
    ).fit(cov_type="HAC", cov_kwds={"maxlags": 1})


def result_to_english(result, dependent_variable, treatment):
    coefficient_names = result.params.index.tolist()
    treatment_name = (
        f"Treatment(reference='{treatment['reference']}'))[T.{treatment['target']}]"
    )
    target_indices = [i for i, c in enumerate(coefficient_names) if treatment_name in c]
    assert len(target_indices) == 1
    idx = target_indices[0]
    effect = result.params[idx]
    p_value = result.pvalues[idx]
    lower = result.conf_int()[0][idx]
    upper = result.conf_int()[1][idx]
    stat_sig = (lower > 0) or (upper < 0)
    if stat_sig:
        s = f"{treatment['target'].capitalize()} had a "
        s += f"{abs(effect):.2f} standard deviation "
        if effect > 0:
            s += "increase "
        else:
            s += "decrease "
        s += f"on {dependent_variable.replace('_', ' ')} "
        s += f"relative to the {treatment['reference']} treatment "
        s += f"(p value={p_value:.3f})."
        return s

    return f"The effect on {dependent_variable.replace('_', ' ')} was not statistically signficant."
