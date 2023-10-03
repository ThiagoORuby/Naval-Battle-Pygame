from constants import *
from utils import generate_grid

def check_winner(grid, mask):
    for i in range(10):
        for j in range(10):
            if grid[i][j] != 0:
                if grid[i][j] + mask[i][j] == grid[i][j]:
                    return False
                
    return True

class Player:
    
    def __init__(self):
        self.grid = []
        self.mask = []
        self.init_grid_and_mask()

    def init_grid_and_mask(self):
        
        self.grid = generate_grid()
        self.mask = [[0 for _ in range(10)] for _ in range(10)]

class Game:
    
    def __init__(self, id):
        self.id = id
        self.ready = False
        self.battle_count = 0
        self.players = [None, None]
        self.shoots = [None, None]
        self.shoot_count = 0
        self.current_player_id = None

    def connected(self):
        return self.ready

    def get_player_shoot(self, player):
        return self.shoots[player]
    
    def shoot(self, player, pos):
        self.shoots[player] = pos
        self.shoot_count+=1
        player2 = self.players[1 - player]
        col, row = [int(val) for val in pos.split(',')]

        if not player2.mask[row][col]:
            if player2.grid[row][col]:
                player2.mask[row][col] = 1
                gameSounds['ship_shoot'].stop()
                gameSounds['ship_shoot'].set_volume(0.03)
                gameSounds['ship_shoot'].play()
            else:
                player2.mask[row][col] = -1
                gameSounds['water_shoot'].stop()
                gameSounds['water_shoot'].set_volume(0.04)
                gameSounds['water_shoot'].play()
        if self.shoot_count == 30:
            self.update_current_player()
            self.shoot_count = 0

    def winner(self):
        player1 = self.players[0]
        player2 = self.players[1]

        p1_winner = check_winner(player2.grid, player2.mask)
        p2_winner = check_winner(player1.grid, player1.mask)

        if p1_winner:
            return 0
        
        if p2_winner:
            return 1
        
        
        return -1
    
    def reset(self):
        self.shoots = [None, None]
        self.shoot_count = 0
        self.battle_count += 1
        for player in self.players:
            player.init_grid_and_mask()
        
        self.update_current_player()

    def __repr__(self) -> str:
        return f"Game(id:{self.id}, ready: {self.ready})"

    def update_current_player(self):
        self.current_player_id = int(not self.current_player_id)