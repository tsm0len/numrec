from typing import Any, Callable

from sklearn.datasets import load_digits 
import matplotlib.pyplot as plt
from json import loads, dumps
from random import uniform
from subprocess import call
from time import time

loaded_digits = load_digits()
DIGITS = loaded_digits.images #type:ignore
TARGETS = loaded_digits.target #type:ignore
# 1797 total digits
DATA_COUNT: int = len(DIGITS)*1//2
PARENTS_COUNT: int = 3
WEIGHTS_SET_COUNT: int = 15
# MAX_DIFFERENCE: float = 0.2
MAX_DIFFERENCE: float = 0.2
WEIGHTS_PATH: str = "weights_7"

def timer(func) -> Callable[..., Any]:
    """Decorator measuring functions worktime"""
    def f(*args, **kwargs) -> Any:
        t1: float = time()
        r: function = func(*args, **kwargs)
        t2: float = time()
        print(f"{func.__name__}() done in {round(t2 - t1, 5)}s")
        return r
    return f

def show_number(number_index:int) -> None:
    """Plots 8x8 number image in grayscale

    Args:
        number (int): Number index from sklearn.datasets library
    """
    plt.matshow(DIGITS[number_index], cmap="gray_r") # inverted gray scale
    plt.title(f"Target: {TARGETS[number_index]}")
    plt.show()

def sorted_dict_keys_by_values(d:dict) -> list[int]:
    """Returns dictionary keys sorted by values

    Args:
        d (dict): Unsorted dictionary

    Returns:
        list[int]: Sorted dictionary keys
    """
    return (sorted(d, key = lambda x: d[x], reverse=True))

def import_weights(weight_set:int, path:str=WEIGHTS_PATH) -> list[list[list[list[int]]]]:
    """Imports weights from .json files from given directory

    Args:
        weight_set (int): weights{weights_set} parameter
        path (str, optional): Weights directory path. Defaults to WEIGHTS_PATH.

    Returns:
        list[list[list[list[int]]]]: List of weights
    """
    with open(f"{path}/weights{weight_set}.json", "r") as f:
        weights: list = loads(f.read())
    return weights

def export_weights(weights:list, weight_set: int, path:str=WEIGHTS_PATH) -> None:
    """Exports weights to .json files to given directory

    Args:
        weights (list): List of weights
        weight_set (int): File name index 
        path (str, optional): Weights directory path. Defaults to WEIGHTS_PATH.
    """
    with open(f"{path}/weights{weight_set}.json", "w") as f:
        f.write(dumps(weights, 
                    #   indent=4
                      ))
        # f.write(dumps(weights))

def export_stats(stats:dict, path:str=WEIGHTS_PATH) -> None:
    """Exports guess stats to .json file to given directory

    Args:
        stats (dict): Dictionary with guess stats
        path (str, optional): Stats directory path. Defaults to WEIGHTS_PATH.
    """
    with open(f"{path}/stats.json", "w") as f:
        f.write(dumps(stats, 
                      indent=4
                      ))

def guess(digit_index:int, weights:list[list[list[list[int]]]]) -> tuple[int, int]:
    """Guesses digit on 8x8 image from sklearn.datasets library

    Args:
        digit_index (int): Image index from sklearn.datasets library
        weights (list[list[list[list[int]]]]): List of weights

    Returns:
        tuple[int, int]: Returns (output, target)
    """
    digit = {i:j for i, j in enumerate(
        [x for y in DIGITS[digit_index].tolist() for x in y]
    )} # 2D array -> 1D dict
# {0: 0.0, 1: 0.0, 2: 5.0, ..., 63: 0.0}

    values: list[dict] = [digit, {}, {}, {}]
    
    for layer_index, layer in enumerate(weights):
        for neuron_index, neuron in enumerate(layer):
            for weight_index, weight in enumerate(neuron):
                values[layer_index + 1][weight_index] = round(
                    values[layer_index + 1].get(weight_index, 1) + 
                    (values[layer_index][neuron_index] * weight[0] + weight[1]), 6
                )

    output = sorted_dict_keys_by_values(values[3])[0]
    target = int(TARGETS[digit_index])

    return output, target

@timer
def get_performance(data_range:int) -> dict[int, int]:
    """Returns list of each weight set performance

    Args:
        data_range (int): Range of tested images

    Returns:
        dict[int, int]: Returns dictionary with performance
    """
    results = {i:0 for i in range(WEIGHTS_SET_COUNT)}
    
    for weight_set in range(WEIGHTS_SET_COUNT):
        weights = import_weights(weight_set)
        
        for digit in range(data_range):
            output, target = guess(digit, weights)

            if output == target:
                results[weight_set] += 1
                
    return results # type:ignore

def gen_new(weights:list, d:float = MAX_DIFFERENCE) -> list:
    """Generates new weight set based on given weights by adding small random number in range [-d, d]

    Args:
        weights (list): Previous weight set
        d (float, optional): Max added/subtracted value. Defaults to MAX_DIFFERENCE.

    Returns:
        list: New set of weights
    """
    output = weights.copy()
    for layer_index, layer in enumerate(weights):
        for neuron_index, neuron in enumerate(layer):
            for weight_index, weight in enumerate(neuron):
                output[layer_index][neuron_index][weight_index][0] = round(
                    output[layer_index][neuron_index][weight_index][0] + uniform(-d, d), 6
                    )
                output[layer_index][neuron_index][weight_index][1] = round(
                    output[layer_index][neuron_index][weight_index][1] + uniform(-3*d, 3*d), 6
                    )
                
    return output

@timer
def replace_weights(parents:list[int]) -> None:
    """Replaces old weights by new genereted using gen_new() function

    Args:
        parents (list[int]): Original weights' indexes
    """
    parents_weights = []
    
    for parent in parents:
        parents_weights.append(import_weights(parent))

    for i in range(len(parents_weights)):
        export_weights(parents_weights[i], i)
    
    for i in range(len(parents_weights), WEIGHTS_SET_COUNT):
        export_weights(gen_new(parents_weights[i%PARENTS_COUNT]), i)

                    

if __name__ == "__main__":
    call("cls", shell=True)
    # show_number(0)
    # print(len(DIGITS))
    for iteration in range(10000):
        
        results = get_performance(DATA_COUNT)
        percentage = {i:round(p/DATA_COUNT*100, 5) for i, p in results.items()}

        print(f"results = {results} (per {DATA_COUNT})")
        print(f"survived = {sorted_dict_keys_by_values(results)[:PARENTS_COUNT]}")
        
        print(f"top percentage = {percentage[sorted_dict_keys_by_values(percentage)[0]]}")
        print(f"average percentage = {round(sum(percentage.values())/WEIGHTS_SET_COUNT, 5)}\n")
        print(f"iteratnion = {iteration}\n")
        
        export_stats(percentage)
        replace_weights(sorted_dict_keys_by_values(results)[:PARENTS_COUNT])
        
    # call("shutdown /s /t 1", shell=True)