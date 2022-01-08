import random
from typing import List, Dict
import json # only for debugging

BOARD_WIDTH = 11
BOARD_HEIGHT = 11

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""

def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """
    my_neck = my_body[1]  # The segment of body right after the head is the 'neck'

    if my_neck["x"] < my_head["x"]:  # my neck is left of my head
        possible_moves.remove("left")
    elif my_neck["x"] > my_head["x"]:  # my neck is right of my head
        possible_moves.remove("right")
    elif my_neck["y"] < my_head["y"]:  # my neck is below my head
        possible_moves.remove("down")
    elif my_neck["y"] > my_head["y"]:  # my neck is above my head
        possible_moves.remove("up")

    return possible_moves

def get_head_pos(head: Dict[str, int], move: str) -> dict:
    if move == 'left':
        return {'x':head['x']-1, 'y':head['y']  }
    if move == 'right':
        return {'x':head['x']+1, 'y':head['y']  }
    if move == 'up':
        return {'x':head['x']  , 'y':head['y']+1}
    if move == 'down':
        return {'x':head['x']  , 'y':head['y']-1}

def in_bounds(pos) -> bool:
    return pos['x'] >= 0 and pos['x'] < BOARD_WIDTH and pos['y'] >= 0 and pos['y'] < BOARD_HEIGHT

def suicide_move(body: List[dict], move: str) -> bool:
    if get_head_pos(body[0], move) in body[1:]:
        return True
    return False

def offensive(snakes: List[dict], mysnake: dict, move: str) -> bool:
    for snake in snakes:
        if snake['id'] == mysnake['id']:
            continue

        next_head_pos = get_head_pos(mysnake['head'], move)
        if next_head_pos in snake['body'][1:]:
            return True
        if next_head_pos == snake['head'] and mysnake['length'] <= snake['length']:
            return True

    return False

def random_move():
    return random.choice(['up', 'down', 'left', 'right'])

def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    global BOARD_HEIGHT, BOARD_WIDTH

    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]  # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves = ["up", "down", "left", "right"]

    # Don't allow your Battlesnake to move back in on it's own neck
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)

    BOARD_HEIGHT = data['board']['height']
    BOARD_WIDTH = data['board']['width']
    print(f'>>> board size = {BOARD_WIDTH} x {BOARD_HEIGHT}')

    # don't let the Battlesnake pick a move that would hit its own body or
    # goes out of bounds or attack another battlesnake
    bad_moves = set()
    for move in possible_moves:
        if suicide_move(data['you']['body'], move):
            bad_moves.add(move)
            continue
        if not in_bounds(get_head_pos(data['you']['head'], move)):
            bad_moves.add(move)
            continue
        if offensive(data['board']['snakes'], data['you'], move):
            bad_moves.add(move)
            continue

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    for move in bad_moves:
        possible_moves.remove(move)

    if len(possible_moves) == 0:
        move = random_move()
    else:
        move = random.choice(possible_moves)
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move
