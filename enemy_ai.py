import pygame
import random
import copy

from battleship import BattleShip

ai_last_good_pos = (-1, -1)

def ai_place_ships(board, board_size, ships):
    for ship in ships:
        while(True):
            pos = (random.randint(0, board_size[0]-1), random.randint(0, board_size[1]-1) )
            ship.rotate_clockwise()
            if(board.add_ship(2, ship, pos)):
                break

def ai_take_a_shot(board):
    if(ai_last_good_pos == (-1, -1)):
        return ( random.randint(0, board.size[0]-1), random.randint(0, board.size[1]-1) )