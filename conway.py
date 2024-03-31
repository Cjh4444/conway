import random as rand
import time
import os

DEAD_SPACE = " "
ALIVE_SPACE = "X"
BORDER = "#"


def generate_random_board(num_rows: int, num_cols: int) -> list:
    return [
        [
            DEAD_SPACE if rand.randint(0, 1) == 1 else ALIVE_SPACE
            for _ in range(num_cols)
        ]
        for _ in range(num_rows)
    ]


def print_board(board: list):
    if len(BORDER) != 1:
        raise ValueError("No border")

    print(BORDER * (len(board[0]) + 2))
    for row in board:
        print(BORDER + "".join(row) + BORDER)
    print(BORDER * (len(board[0]) + 2))


def update_board(board: list):
    def get_num_neighbors(row_coord: int, col_coord: int):
        return sum(
            board[row][col] == ALIVE_SPACE
            for col in range(col_coord - 1, col_coord + 2)
            for row in range(row_coord - 1, row_coord + 2)
            if 0 <= row < len(board)
            and 0 <= col < len(board[0])
            and (row_coord, col_coord) != (row, col)
        )

    # returns whether a cell should be alive the next turn
    def cell_state(row_coord: int, col_coord: int) -> bool:
        num_neighbors = get_num_neighbors(row_coord, col_coord)

        if board[row_coord][col_coord] == ALIVE_SPACE:
            overpopulated = num_neighbors >= 4
            underpopulated = num_neighbors <= 1
            death = overpopulated or underpopulated

            return not death
        else:
            return num_neighbors == 3

    new_board = [
        [
            ALIVE_SPACE if cell_state(row, col) else DEAD_SPACE
            for col in range(len(board[0]))
        ]
        for row in range(len(board))
    ]

    return new_board


def main():
    rows, columns = map(
        int,
        input(
            "What board size would you like?"
            + " (input as 2 numbers with a space in between): "
        ).split(),
    )

    board = generate_random_board(rows, columns)

    update_rate = 1 / int(
        input("How many times should it update per second: ")
    )

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

    print("board is dead" if board == prev_board else "permanent repetition")


if __name__ == "__main__":
    main()
