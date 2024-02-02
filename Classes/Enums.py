from enum import Enum

class State(Enum):
    Closed = 0
    Open = 1
    Marked = 2

class Directions(Enum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3