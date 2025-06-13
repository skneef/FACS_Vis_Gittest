import numpy as np
import pandas as pd
import scipy as sp
import warnings

warnings.simplefilter('ignore', category=RuntimeWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

def calculate_logicle(t, m, w, a, p, s):
    # This function is used to calculate the logicle value using given parameters
    # Define the equation as a function
    def equation(x):
        return (t * np.exp(-(m - w - a))) * (np.exp(x - w - a) - p ** 2 * np.exp(-(x - w - a) / p) + p ** 2 - 1) - s

    # noinspection PyTypeChecker
    def equation_low(x):
        return -(t * np.exp(-(m - w - a))) * (np.exp(w + a - x) - p ** 2 * np.exp(-(w + a - x) / p) + p ** 2 - 1) - s

    # Initial guess for x
    initial_guess = 0.0

    # Use fsolve to find the root
    logicle, = sp.optimize.fsolve(equation, initial_guess)
    logicle = logicle / np.log(10)

    if logicle < (w + a):
        logicle, = sp.optimize.fsolve(equation_low, initial_guess)
        logicle = logicle / np.log(10)

    return logicle

def calculate_parameters(T=(1<<18), M=4.5, r=100):
    # this function is for calculating the parameters to be used to calculate the logicle value. These parameters are based on the full population.
    # T (same as t) is the highest value or highest expected value in the population
    t = T
    # M represents the width of the image to be used
    m = M * np.log(10)
    # w represents the part that should be in linear scale and is calculated with r, the lowest value
    w = (M - np.log10(t / np.abs(r))) / 2

    def equation(x):
        return (2 * x * np.log(x)) / (x + 1) - w

    initial_guess = 2.0
    p, = sp.optimize.fsolve(equation, initial_guess)

    # a represents that part that should be negative in the scale
    a = 0

    a_log = calculate_logicle(t, m, w, a, p, r)
    zero_log = calculate_logicle(t, m, w, a, p, 0)

    if a_log < 0:
        a = abs(zero_log - a_log)

    return t, m, w, a, p

def axis_scale(t, m, w, a, p, min=None, max=None):
    # This function returns 3 scales, one with names for the larger ticks, one for the .5 ticks and one for the other ticks
    axis_scale = pd.DataFrame(columns=["Value", "Name", "Logicle"])

    value = (
            [-90000 + 10000 * n for n in range(9)] +
            [-9000 + 1000 * n for n in range(9)] +
            [-900 + 100 * n for n in range(9)] +
            [-90 + 10 * n for n in range(8)] +
            [0] +
            [20 + 10 * n for n in range(8)] +
            [100 + 100 * n for n in range(9)] +
            [1000 + 1000 * n for n in range(9)] +
            [10000 + 10000 * n for n in range(9)] +
            [100000 + 100000 * n for n in range(9)] +
            [1000000 + 1000000 * n for n in range(9)] +
            [10000000 + 10000000 * n for n in range(9)] +
            [100000000]
    )
    name = [
        "", "", "", "", "", "", "", "", "$-10^4$",
        "", "", "", "", "", "", "", "", "$-10^3$",
        "", "", "", "", "", "", "", "", "$-10^2$",
        "", "", "", "", "", "", "", "",
        "0",
        "", "", "", "", "", "", "", "",
        "$10^2$", "", "", "", "", "", "", "", "",
        "$10^3$", "", "", "", "", "", "", "", "",
        "$10^4$", "", "", "", "", "", "", "", "",
        "$10^5$", "", "", "", "", "", "", "", "",
        "$10^6$", "", "", "", "", "", "", "", "",
        "$10^7$", "", "", "", "", "", "", "", "",
        "$10^8$"
    ]

    axis_scale["Value"] = value
    axis_scale["Name"] = name

    for index, row in axis_scale.iterrows():
        s = row["Value"]
        x = calculate_logicle(t, m, w, a, p, s)
        axis_scale.loc[index, "Logicle"] = x

    zero = axis_scale[axis_scale["Name"] == "0"]
    three = axis_scale[axis_scale["Name"] == "$10^3$"]

    if min != None:
        if min <= 10:
            axis_scale = axis_scale[axis_scale["Value"] >= min].reset_index(drop=True)
        else:
            axis_scale = axis_scale[axis_scale["Value"] >= 20].reset_index(drop=True)
    if max != None:
        if max <= 100000:
            axis_scale = axis_scale[axis_scale["Value"] <= 100000].reset_index(drop=True)
        else:
            max_index = axis_scale[axis_scale["Value"] <= max].index[-1]
            axis_scale = axis_scale.iloc[:max_index + 2]

    if ~axis_scale["Name"].isin(["0"]).any():
        axis_scale = pd.concat([axis_scale, zero])
    if ~axis_scale["Name"].isin(["$10^3$"]).any():
        axis_scale = pd.concat([axis_scale, three])

    axis_scale = axis_scale.sort_values(["Value"]).reset_index(drop=True)
    axis_scale["Logicle"] = axis_scale["Logicle"].astype('float64')

    main_axis_scale = axis_scale[axis_scale["Name"] != ""]
    sec_axis_scale = axis_scale[axis_scale['Value'].astype("string").str.contains("5")]
    #sec_axis_scale["Name"] = sec_axis_scale["Name"].astype("float64")
    scale_index = list(main_axis_scale.index) + list(sec_axis_scale.index)
    ter_axis_scale = axis_scale[~axis_scale.index.isin(scale_index)]
    #ter_axis_scale["Name"] = ter_axis_scale["Name"].astype("float64")

    return main_axis_scale, sec_axis_scale, ter_axis_scale

