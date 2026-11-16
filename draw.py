import turtle
import matplotlib.pyplot as plt
from learn import sorted_dict_keys_by_values, import_weights

WEIGHTS_PATH = "weights_2/"
WIDTH, HEIGHT = 400, 400
image_2d = [[0 for _ in range(8)] for _ in range(8)]


def show_number(number:list) -> None:
    plt.matshow(number, cmap="gray_r") # inverted gray scale
    plt.show()

def setup() -> tuple[turtle.Turtle, turtle._Screen]:
    screen = turtle.Screen()
    screen.setup(width=WIDTH+100, height=HEIGHT+100)
    screen.title("NumRec")

    screen.colormode(255)
    t = turtle.Turtle(shape="circle", visible=True)
    t.speed(0)
    t.shapesize(2)
    t.fillcolor("#FF0000")
    t.pensize(60)
    return t, screen

def cap(value: int, min: int, max: int) -> int:
    """Caps value between min and max

    Args:
        value (int): Number to cap
        min (int): Minimum value
        max (int): Maximum value

    Returns:
        int: Capped value
    """
    if value < min:
        return min
    if value > max:
        return max
    return value

def l_btn(x, y):
    drawing(x, y, 1)
    draw_to_list(x, y, 1)
def r_btn(x, y):
    drawing(x, y, 3)
    draw_to_list(x, y, 3)
def m_btn(x, y):
    # drawing(x, y, 2)
    # draw_to_list(x, y, 2)
    show_number(image_2d)
    
def draw_to_list(x: int, y:int, btn:int) -> None:
    """Converts drawing to list

    Args:
        x (int): Cursor's x value on canvas
        y (int): Cursor's y value on canvas
        btn (int): Mouse button (1-left, 2-middle, 3-right)
    """
    global image_2d
    DRAW_THICKNESS = 6
    DRAW_OVERFLOW = 1
    x = int(4 + cap(x, -200, 200)//50)
    y = int(3.5 - cap(y, -200, 200)//50)

    screen.title(str(guess(image_2d, import_weights(0, WEIGHTS_PATH))))

    if btn == 1:
        image_2d[y][x] = cap(image_2d[y][x]+DRAW_THICKNESS, 0, 16)
        for cord in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            image_2d[cap(y+cord[1], 0, 7)][cap(x+cord[0], 0, 7)] = cap(image_2d[cap(y+cord[1], 0, 7)][cap(x+cord[0], 0, 7)]+DRAW_OVERFLOW, 0, 16)
    elif btn == 3:
        # image_2d[y][x] = cap_value(image_2d[y][x]-4, 0, 16)
        image_2d[y][x] = 0
        for cord in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            image_2d[cap(y+cord[1], 0, 7)][cap(x+cord[0], 0, 7)] = cap(image_2d[cap(y+cord[1], 0, 7)][cap(x+cord[0], 0, 7)]-5, 0, 16)

def drawing(x, y, btn) -> None:

    x = cap(x, -200, 200)
    y = cap(y, -200, 200)
    if btn == 2:
        t.penup()
    else:
        t.pendown()       
        if btn == 1:
            color = "#000000"
        else:
            color = "#FFFFFF"
        t.pencolor(color)
    
    t.goto(x, y)

def guess(image:list[list[int]], weights:list[list[list[list[int]]]]) -> int:
    """Guesses number based on drawing

    Args:
        image (list[list[int]]): 8x8 image list
        weights (list[list[list[list[int]]]]):  Weights
        
    Returns:
        int: Guessed digit (0-9)
    """
    digit = {i:x for i, x in enumerate([x for y in image for x in y])}
    
    values: list[dict] = [digit, {}, {}, {}]
    
    for layer_index, layer in enumerate(weights):
        for neuron_index, neuron in enumerate(layer):
            for weight_index, weight in enumerate(neuron):
                values[layer_index + 1][weight_index] = round(
                    values[layer_index + 1].get(weight_index, 1) + 
                    (values[layer_index][neuron_index] * weight[0] + weight[1]), 6
                )
    output = sorted_dict_keys_by_values(values[3])[0]

    return output

if __name__ == "__main__":
    t, screen = setup()

    t.ondrag(l_btn, btn=1)
    t.onclick(m_btn, btn=2)
    t.ondrag(r_btn, btn=3)

    
    turtle.mainloop()
