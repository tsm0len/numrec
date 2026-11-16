from learn import guess, DIGITS, TARGETS
from learn import sorted_dict_keys_by_values, import_weights, export_stats, timer
from json import dumps

DATA_COUNT: int = len(DIGITS)*1//2
WEIGHTS_PATH = "weights_2"
WEIGHT_NUMBER = 0
# WEIGHT_NUMBER = int(input("> "))
@timer
def analyse() -> dict:
    print(f"Analysing {WEIGHTS_PATH}...")
    stats = {int(i):{"correct":0, "wrong":0, "mistaken":0, "guessed":{i:0 for i in range(10)}} for i in range(10)}
    
    for index in range(DATA_COUNT):
        output, target = guess(index, import_weights(WEIGHT_NUMBER, WEIGHTS_PATH))
        if output == target:
            stats[target]["correct"] += 1
        else:
            stats[target]["wrong"] += 1
            stats[output]["mistaken"] += 1
        stats[target]["guessed"][output] += 1
    print("Done")
    return stats
if __name__=="__main__":
    stats = analyse()
    # print(dumps(stats, indent=1))
    export_stats({"weights_patn":WEIGHTS_PATH, "weight_set":WEIGHT_NUMBER, "stats":stats}, "stats")