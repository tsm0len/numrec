from sklearn.datasets import load_digits 
import matplotlib.pyplot as plt
from json import loads, dumps
from random import uniform
from subprocess import call
import numpy

loaded_digits = load_digits()

DIGITS = loaded_digits.images #type:ignore
TARGETS = loaded_digits.target #type:ignore
DATA_NUMBER: int = len(DIGITS)//2
PARENTS_NUMBER: int = 2
WEIGHTS_SET_NUMBER: int = 10
MAX_DIFFERENCE: float = 0.3


def show_number(number: int) -> None:
    plt.matshow(DIGITS[number], cmap="gray_r") # skala szarości odwrócona
    plt.title(f"Target: {TARGETS[number]}")
    plt.show()

def sorted_dict_values(d: dict) -> list[int]:
    return (sorted(d, key = lambda x: d[x], reverse=True))

def import_weights(weight_set: int) -> list[list[list[list[int]]]]:
    with open(f"weights/weights{weight_set}.json", "r") as f:
        weights: list = loads(f.read())
    return weights

def export_weights(weights:list, weight_set: int) -> None:
    with open(f"weights/weights{weight_set}.json", "w") as f:
        f.write(dumps(weights, indent=4))

def export_stats(stats):
    with open("stats.json", "w") as f:
        f.write(dumps(stats, indent=4))

 
def guess(digit_index:int, weights:list[list[list[list[int]]]]) -> list[dict[int, float]|int]:

    digit = {i:j for i, j in enumerate(
        [x for y in DIGITS[digit_index].tolist() for x in y]
    )} # 2D array -> 1D dict
# {0: 0.0, 1: 0.0, 2: 5.0, ..., 63: 0.0}

    values: list[dict] = [digit, {}, {}, {}]
    
    for layer_index, layer in enumerate(weights):
        for neuron_index, neuron in enumerate(layer):
            for weight_index, weight in enumerate(neuron):
                values[layer_index + 1][weight_index] = round(values[layer_index + 1].get(weight_index, 1) + (values[layer_index][neuron_index] * weight[0] + weight[1]), 5)

    output = sorted_dict_values(values[3])[0]
    target = int(TARGETS[digit_index])

    return [output, target]


def selection(data_range:int) -> dict[int, int]:
    
    results = {i:0 for i in range(10)}
    
    for weight_set in range(10):
        weights = import_weights(weight_set)
        
        for digit in range(data_range):
            output, target = guess(digit, weights)

            if output == target:
                results[weight_set] += 1
                
    return results # type:ignore

def gen_new(weights:list, d:float = MAX_DIFFERENCE) -> list:
    output = weights.copy()
    for layer_index, layer in enumerate(weights):
        for neuron_index, neuron in enumerate(layer):
            for weight_index, weight in enumerate(neuron):
                output[layer_index][neuron_index][weight_index][0] += uniform(-d, d)
                output[layer_index][neuron_index][weight_index][1] += uniform(-d, d)
                
    return output

def evolve(parents: list[int]) -> None:
    parents_weights = []
    
    for parent in parents:
        parents_weights.append(import_weights(parent))

    for i in range(len(parents_weights)):
        export_weights(parents_weights[i], i)
    
    for i in range(len(parents_weights), WEIGHTS_SET_NUMBER):
        export_weights(gen_new(parents_weights[i%PARENTS_NUMBER]), i)

                    

if __name__ == "__main__":
    call("cls", shell=True)
    # show_number(4)
    for iteration in range(10000):
        
        results = selection(DATA_NUMBER)
        print(f"{iteration = }")
        print(f"{results = }\nsurvived = {sorted_dict_values(results)[:PARENTS_NUMBER]}")

        percentage = {i:round(p/DATA_NUMBER*100, 6) for i, p in results.items()}
        
        print(f"top percentage = {percentage[sorted_dict_values(percentage)[0]]}")
        print(f"average percentage = {round(sum(percentage.values())/10, 6)}\n")
        export_stats(percentage)

        evolve(sorted_dict_values(results)[:PARENTS_NUMBER])
    # call("shutdown /s /t 1", shell=True)