import pygame
import copy

from battleship import BattleShip
from battleship import BSOrientation

from draw_wizard import draw_board_bottom
from draw_wizard import draw_board_top
from draw_wizard import draw_both_boards_only

class Board:
    def __init__(self, size):
        self.size = size
        
        self.p1_ships = []
        self.p1_board = []
        
        self.p2_ships = []
        self.p2_board = []
        
        for _ in range(size[1]):
            row = []
            for _ in range(size[0]):
                row.append(None)
            self.p1_board.append(row)
            
        self.p2_board = copy.deepcopy(self.p1_board)
    
    def draw_bottom(self, screen, delta):
        return draw_board_bottom(screen, self.size, self.p1_board, self.p1_ships, delta)
    
    def draw_top(self, screen):
        return draw_board_top(screen, self.size, self.p2_board, self.p2_ships)
    
    def draw_both_for_animation(self, screen, y):
        draw_both_boards_only(screen, y, self.size)
    
    def add_ship(self, player, ship, pos):
        coords = ship.get_all_coords(pos)
        for coord in coords:
            if coord[0] < 0 or coord[0] >= self.size[0] or coord[1] < 0 or coord[1] >= self.size[1]:
                return False
        
        adjacent_coords = []
        for coord in coords:
            adjacent_coords.append( copy.copy(coord) )
            if(coord[0] > 0):
                adjacent_coords.append( (coord[0]-1, coord[1]) )
            if(coord[0] < self.size[0]-1):
                adjacent_coords.append( (coord[0]+1, coord[1]) )
            if(coord[1] > 0):
                adjacent_coords.append( (coord[0], coord[1]-1) )
            if(coord[1] < self.size[1]-1):
                adjacent_coords.append( (coord[0], coord[1]+1) )
        
        
        if(player == 1):
            
            for coord in adjacent_coords:
                if self.p1_board[coord[1]][coord[0]] != None:
                    return False
            
            self.p1_ships.append((pos, ship))
            num = len(self.p1_ships)-1
            for coord in coords:
                self.p1_board[coord[1]][coord[0]] = num
                
        elif(player == 2):
            
            for coord in adjacent_coords:
                if self.p2_board[coord[1]][coord[0]] != None:
                    return False
                
            self.p2_ships.append((pos, ship))
            num = len(self.p2_ships)-1
            for coord in coords:
                self.p2_board[coord[1]][coord[0]] = num
        
        return True
                
    def shoot_at_p1(self, pos):
        val = self.p1_board[pos[1]][pos[0]]
        if val == None:
            self.p1_board[pos[1]][pos[0]] = -1
            return False
        elif val >= 0:
            coords = self.p1_ships[val][1].get_all_coords( self.p1_ships[val][0] )
            for i in range(len(coords)):
                if coords[i] == pos:
                    self.p1_ships[val][1].set_segment_on_fire(i, True)
        return True
                    
    def shoot_at_p2(self, pos):
        val = self.p2_board[pos[1]][pos[0]]
        if val == None:
            self.p2_board[pos[1]][pos[0]] = -1
            return False
        elif val >= 0:
            coords = self.p2_ships[val][1].get_all_coords( self.p2_ships[val][0] )
            for i in range(len(coords)):
                if coords[i] == pos:
                    self.p2_ships[val][1].set_segment_on_fire(i, True)
        return True