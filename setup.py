from json import dumps
from random import uniform


def setup_weights(ignore:list=[], amount=10):
    for index in range(amount):
        if index not in ignore:
            with open(f"weights/weights{index}.json", "w") as f:
                f.write(dumps(
        [ # calosc
            [ # i-0
                [ # i[0]
                    [round(uniform(-2, 2), 5), round(uniform(-5, 5), 5)] for _ in range(64) #do kazdego
                ] for _ in range(64) #z kazdego
            ],
            [ # 0-1
                [
                    [round(uniform(-2, 2), 5), round(uniform(-5, 5), 5)] for _ in range(64)
                ] for _ in range(64)
            ],
            [ # 1-o
                [
                    [round(uniform(-2, 2), 5), round(uniform(-5, 5), 5)] for _ in range(10)
                ] for _ in range(64)
            ]
        ],
    indent=4)
)


if __name__ == "__main__":
    setup_weights()