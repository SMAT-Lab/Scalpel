def actual_data_test_basics_static():
    static_infer = ["<builtin>.len", "random.choices"]
    return static_infer


def actual_data_test_basics_dynamic():
    dynamic_infer = [
        "<builtin>.len",
        "random.Random.choices",
    ]
    return dynamic_infer


def actual_data_test_nested_func_calls_static():
    static_infer = ["ex_b.factorial.inner_factorial", "ex_b.factorial"]
    return static_infer


def actual_data_test_func_inside_func_calls_static():
    static_infer = [
        "ex_c.sum_list_items.do_the_sum",
        "ex_c.sum_list_items.do_the_sum.do_core_computations",
        "ex_c.sum_list_items",
    ]
    return static_infer
