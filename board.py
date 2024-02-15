import pygame

from battleship import BattleShip
from battleship import BSOrientation

from draw_wizard import draw_board_bottom
from draw_wizard import draw_board_top

class Board:
    def __init__(self, size):
        self.size = size
        
        self.p1_ships = []
        self.p1_board = []
        
        self.p2_ships = []
        self.p2_board = []
        
        for _ in range(size[1]):
            row = []
            row2 = []
            for _ in range(size[0]):
                row.append(None)
                row2.append(None)
            self.p1_board.append(row)
            self.p2_board.append(row2)
    
    def draw_bottom(self, screen, delta):
        return draw_board_bottom(screen, self.size, self.p1_board, self.p1_ships, delta)
    
    def draw_top(self, screen):
        return draw_board_top(screen, self.size, self.p2_board, self.p2_ships)
    
    def add_ship(self, player, ship, pos):
        coords = ship.get_all_coords(pos)
        if(player == 1):
            self.p1_ships.append((pos, ship))
            num = len(self.p1_ships)-1
            for coord in coords:
                self.p1_board[coord[1]][coord[0]] = num
        if(player == 2):
            self.p2_ships.append((pos, ship))
            num = len(self.p2_ships)-1
            for coord in coords:
                self.p2_board[coord[1]][coord[0]] = num
                
    def shoot_at_p1(self, pos):
        val = self.p1_board[pos[1]][pos[0]]
        if val == None:
            self.p1_board[pos[1]][pos[0]] = -1
        elif val >= 0:
            coords = self.p1_ships[val][1].get_all_coords( self.p1_ships[val][0] )
            for i in range(len(coords)):
                if coords[i] == pos:
                    self.p1_ships[val][1].set_segment_on_fire(i, True)
                    
    def shoot_at_p2(self, pos):
        val = self.p2_board[pos[1]][pos[0]]
        if val == None:
            self.p2_board[pos[1]][pos[0]] = -1
        elif val >= 0:
            coords = self.p2_ships[val][1].get_all_coords( self.p2_ships[val][0] )
            for i in range(len(coords)):
                if coords[i] == pos:
                    self.p2_ships[val][1].set_segment_on_fire(i, True)