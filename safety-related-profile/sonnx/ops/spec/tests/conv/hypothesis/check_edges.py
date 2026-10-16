import json
import itertools



def check_edges(data):
    with open("generated_data.json", "r") as f:
        data = json.load(f)
        check_dx0_result = check_individual_variables("dx0", data["dx0"], data["min_dx0"], data["max_dx0"])
        check_dx1_result = check_individual_variables("dx1", data["dx1"], data["min_dx1"], data["max_dx1"])
        check_x_spatial_axis_result = check_spatial_axis("x_spatial_axis", data["x_spatial_axis"], data["x_spatial_axis_min"], data["x_spatial_axis_max"])
        check_dw0_result = check_individual_variables("dw0", data["dw0"], data["min_dw0"], data["max_dw0"])
        # Irrelevant see dw1 because they are the same as dx1, X [C2]
        check_w_spatial_axis_result = check_spatial_axis("w_spatial_axis",data["w_spatial_axis"], data["w_spatial_axis_min"], data["w_spatial_axis_max"])
        #Irrelevant see db0 because they are the same as dw0, B [C1]
        strides_result = check_2d_variables("strides", data["strides"], data["strides_min"], data["strides_max"])
        auto_pad_result = check_auto_pad(data["auto_pad"])
        pads_result = check_pads(data["pads"], data["pads_min"], data["pads_max"])
        dilations_result = check_2d_variables("dilations", data["dilations"], data["dilation_min"], data["dilation_max"])
        #Irrelevant check kernel shape it would be the same as w_spatial_axis
        return all([check_dx0_result, check_dx1_result, check_x_spatial_axis_result, strides_result, check_dw0_result, auto_pad_result, pads_result, dilations_result, check_w_spatial_axis_result])


"""
Check individual variable analysis
"""
def check_individual_variables(variable_name, variable_analysis, min, max):    
    corner_cases = [min, max]
    corner_cases_test = all(corner_case in variable_analysis for corner_case in corner_cases)

    has_mean_case_mean = any(d for d in variable_analysis if d > min and d < max)
    has_out_of_bounds = not(any(d for d in variable_analysis if d < min or d > max))

    print(f"Individual variable analysis: {variable_name}")
    if not corner_cases_test:
        for corner_case in corner_cases:
            if corner_case not in variable_analysis:
                print(f"    - Missing corner case: {corner_case}")
    if not has_mean_case_mean:
        print(f"  - Missing mean case")
    if not has_out_of_bounds:
        print(f"  - Found out of bounds values")

    return all([corner_cases_test, has_mean_case_mean, has_out_of_bounds])


"""
Check spatial_axis contains all corner cases
"""
def check_spatial_axis(testcase_name, spatial_axis, min_spatial_axis, max_spatial_axis):

    corner_cases = generate_corner_cases(min_spatial_axis, max_spatial_axis)
    corner_cases_test = all(corner_case in spatial_axis for corner_case in corner_cases)
    has_edge_case_lower = has_edge_case(spatial_axis, 0, min_spatial_axis, min_spatial_axis, max_spatial_axis)
    has_edge_case_higher = has_edge_case(spatial_axis, 0, max_spatial_axis, min_spatial_axis, max_spatial_axis)
    has_edge_case_lower_1 = has_edge_case(spatial_axis, 1, min_spatial_axis, min_spatial_axis, max_spatial_axis)
    has_edge_case_higher_1 = has_edge_case(spatial_axis, 1, max_spatial_axis, min_spatial_axis, max_spatial_axis)
    has_mean_case_mean = has_mean_case(spatial_axis, min_spatial_axis, max_spatial_axis)

    print(f"{testcase_name} analysis:")
    if not corner_cases_test:
        for corner_case in corner_cases:
            if corner_case not in spatial_axis:
                print(f"    - Missing corner case: {corner_case}")
    if not has_edge_case_lower:
        print(f"  - Missing edge case lower in dimension 0")
    if not has_edge_case_higher:
        print(f"  - Missing edge case higher in dimension 0")
    if not has_edge_case_lower_1:
        print(f"  - Missing edge case lower in dimension 1")
    if not has_edge_case_higher_1:
        print(f"  - Missing edge case higher in dimension 1")
    if not has_mean_case_mean:
        print(f"  - Missing mean case")


    return all([corner_cases_test, has_edge_case_lower, has_edge_case_higher, has_edge_case_lower_1, has_edge_case_higher_1, has_mean_case_mean])

"""
Check pads contains all corner cases
"""
def check_pads(pads, min_pads, max_pads):
    #Dont check cases where auto_pad is different from NOTSET
    pads = [pad for pad in pads if len(pad) == 4] 
    
    corner_cases_combinations = [list(t) for t in itertools.product([min_pads, max_pads], repeat=4)]
    corner_cases_test = all(corner_case in pads for corner_case in corner_cases_combinations)
    if not corner_cases_test:
        print(f"pads analysis:")
        for corner_case in corner_cases_combinations:
            if corner_case not in pads:
                print(f"    - Missing corner case: {corner_case}")

    mean = 'A'
    edge_cases_combinations = [list(t) for t in itertools.product([min_pads, max_pads, mean], repeat=4) if mean in t]
    edge_cases_tests = pads_wildcard(edge_cases_combinations, pads, mean, min_pads, max_pads)
    if not edge_cases_tests:
        for edge_case in edge_cases_combinations:
            if not any(match_wildcard(edge_case, pad, mean, min_pads, max_pads) for pad in pads):
                print(f"    - Missing edge case with wildcard: {edge_case}")

    return all([corner_cases_test, edge_cases_tests])

"""
Check strides contains all corner cases
"""

def check_2d_variables(variable_name, variable_value, min_strides, max_strides):
    
    corner_cases = generate_corner_cases(min_strides, max_strides)
    corner_cases_test = all(corner_case in variable_value for corner_case in corner_cases)

    # Check for lines
    has_mean_case_mean_lines = any(
        d for d in variable_value if len(d) > 0 and d[0] > min_strides and d[0] < max_strides
    )
    has_out_of_bounds_lines = not(any(
        d for d in variable_value if len(d) > 0 and (d[0] < min_strides or d[0] > max_strides)
    ))
    
    # Edge cases
    has_edge_case_lower = has_edge_case(variable_value, 0, min_strides, min_strides, max_strides)
    has_edge_case_higher = has_edge_case(variable_value, 0, max_strides, min_strides, max_strides)

    #Check for columns
    has_mean_case_mean_columns = any(
        d for d in variable_value if len(d) > 1 and d[1] > min_strides and d[1] < max_strides
    )
    has_out_of_bounds_columns = not(any(
        d for d in variable_value if len(d) > 1 and (d[1] < min_strides or d[1] > max_strides)
    ))

    # Edge cases
    has_edge_case_lower_1 = has_edge_case(variable_value, 1, min_strides, min_strides, max_strides)
    has_edge_case_higher_1 = has_edge_case(variable_value, 1, max_strides, min_strides, max_strides)

    print(f"{variable_name} analysis:")
    if not corner_cases_test:
        for corner_case in corner_cases:
            if corner_case not in variable_value:
                print(f"    - Missing corner case: {corner_case}")
    if not has_mean_case_mean_lines:
        print(f"  - Missing mean case in lines")
    if not has_out_of_bounds_lines:
        print(f"  - Found out of bounds values in lines")
    if not has_mean_case_mean_columns:
        print(f"  - Missing mean case in columns")
    if not has_out_of_bounds_columns:
        print(f"  - Found out of bounds values in columns")
    if not has_edge_case_lower:
        print(f"  - Missing edge case lower in dimension 0")
    if not has_edge_case_higher:
        print(f"  - Missing edge case higher in dimension 0")
    if not has_edge_case_lower_1:
        print(f"  - Missing edge case lower in dimension 1")
    if not has_edge_case_higher_1:
        print(f"  - Missing edge case higher in dimension 1")

    return all([corner_cases_test, has_mean_case_mean_lines, has_out_of_bounds_lines, has_mean_case_mean_columns, has_out_of_bounds_columns, has_edge_case_lower, has_edge_case_higher, has_edge_case_lower_1, has_edge_case_higher_1])


"""
Check auto_pad contains all values
"""
def check_auto_pad(auto_pad):
    possible_values = ['SAME_UPPER', 'SAME_LOWER', 'NOTSET', 'VALID']
    auto_pad_test = all(value in auto_pad for value in possible_values)
    auto_pad_out_of_bounds = not any(value not in possible_values for value in auto_pad)

    print(f"auto_pad analysis:")
    if not auto_pad_test:
        for value in possible_values:
            if value not in auto_pad:
                print(f"    - Missing value: {value}")
    if not auto_pad_out_of_bounds:
        print(f"  - Found out of bounds values")

    return all([auto_pad_test, auto_pad_out_of_bounds])

"""
Generate corner cases for x_spatial_axis
"""
def generate_corner_cases(min_x_spatial_axis, max_x_spatial_axis):
    return [
        [x1, x2]
        for x1 in (min_x_spatial_axis, max_x_spatial_axis)
        for x2 in (min_x_spatial_axis, max_x_spatial_axis)
    ]


"""
Auxiliary functions to help generate edges and corner cases
"""
def has_edge_case(x_spatial_axis, dim_idx, edge_value, min_value, max_value):
    return any(
        edge_case 
        for edge_case in x_spatial_axis
        if len(edge_case) > 0 and edge_case[dim_idx] == edge_value 
        and all(
            edge_case[i] != min_value and edge_case[i] != max_value
            for i in range(len(edge_case)) if i != dim_idx
        )
    )

def has_mean_case(x_spatial_axis, min_value, max_value):
    return any(
        edge_case
        for edge_case in x_spatial_axis
        if all(v != min_value and v != max_value for v in edge_case)
    )


def match_wildcard(edge_case, pad, wildcard_value, min_value, max_value):
    for ec, p in zip(edge_case, pad):
        if ec != wildcard_value:
            if ec != p:
                return False
        else:
            if p == min_value or p == max_value:
                return False
    return True


def pads_wildcard(edge_cases, pads, wildcard_value, min_value, max_value):
    for edge_case in edge_cases:
        if not any(match_wildcard(edge_case, pad, wildcard_value, min_value, max_value) for pad in pads):
            return False
    return True

print(check_edges("generated_data.json"))