import random as rand
import time
import os

DEAD_SPACE = " "
ALIVE_SPACE = "X"
BORDER = "#"


def generate_random_board(x: int, y: int) -> list:
    return [
        [
            DEAD_SPACE if rand.randint(0, 1) == 1 else ALIVE_SPACE
            for _ in range(y)
        ]
        for _ in range(x)
    ]


def print_board(board: list):
    if len(BORDER) != 1:
        raise ValueError("No border")

    print(BORDER * (len(board[0]) + 2))
    for row in board:
        print(BORDER + "".join(row) + BORDER)
    print(BORDER * (len(board[0]) + 2))


def update_board(board: list):
    def get_num_neighbors(x: int, y: int):
        num = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i <= len(board) - 1 and 0 <= j <= len(board[0]) - 1:
                    if board[i][j] == ALIVE_SPACE:
                        num += 1
        return num - (1 if board[x][y] == ALIVE_SPACE else 0)

    # returns whether a cell should be alive the next turn
    def cell_state(x: int, y: int) -> bool:
        num_neighbors = get_num_neighbors(x, y)

        if board[x][y] == ALIVE_SPACE:
            overpopulated = num_neighbors >= 4
            underpopulated = num_neighbors <= 1
            death = overpopulated or underpopulated

            return not death
        else:
            return num_neighbors == 3

    new_board = [[DEAD_SPACE] * len(board[0]) for i in range(len(board))]

    for x, row in enumerate(board):
        for y, cell in enumerate(row):
            new_board[x][y] = ALIVE_SPACE if cell_state(x, y) else DEAD_SPACE

    return new_board


width, height = map(
    int,
    input(
        "What board size would you like"
        + "(input as 2 numbers with a space in between): "
    ).split(),
)

board = generate_random_board(width, height)

update_rate = 1 / int(input("How many times should it update per second: "))

prev_prev_board = []
prev_board = []

while board != prev_board and board != prev_prev_board:
    prev_prev_board = prev_board
    prev_board = board
    print_board(board)
    board = update_board(board)
    time.sleep(update_rate)
    os.system("clear")

print_board(board)

print(
    "the board died"
    if board == prev_board
    else "the board got stuck in a infinite loop"
)
