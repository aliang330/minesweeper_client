from enum import Enum
import json
from typing import List

class Board:


    def __init__(self, board, x: int, y: int, bombs: int):
        self.x = x
        self.y = y
        self.bombs = bombs
        self.board = board
        self.create_square_board()
        print("hit")

    def create_square_board(self):
        square_board = []
        row = []

        for i in range(self.x):
            for j in range(self.y):
                square_dict = self.board[i][j]
                row.append(self.dicToSquare(square_dict))
            square_board.append(row)

        self.board = square_board

    def dicToSquare(self, square_dict):

        new_square = Square(square_dict["state"],
                            bool(square_dict["isFlag"]),
                            square_dict["adjacentBombs"]
                            )
        return new_square

    @staticmethod
    def from_json(json_string):
        json_dict = json.loads(json_string)
        return Board(**json_dict)

    def __str__(self):
        rep_string = ""
        for i in range(self.x):
            for j in range(self.y):
                square = self.board[i][j]
                if square.state == "UNTOUCHED":
                    rep_string += "- "
            rep_string += "\n"
        return rep_string

class Square:

    def __init__(self, state: str, is_flag: bool, adjacent_bombs: int):
        self.state = state
        self.is_flag = is_flag
        self.adjacent_bombs = adjacent_bombs


class SquareState(Enum):
    UNTOUCHED = 1
    DUG = 2
    MINE = 3


