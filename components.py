from constants import *
from utils import generate_grid

# Check if a player lost the game
def check_loser(player):
    for i in range(10):
        for j in range(10):
            if player.grid[i][j] != 0:
                if player.grid[i][j] + player.mask[i][j] == player.grid[i][j]:
                    return False
                
    return True

class Player:

    """Class that represents a Player
    """
    
    def __init__(self):
        self.grid = []
        self.mask = []
        self.init_grid_and_mask()

    def init_grid_and_mask(self):
        """Create a new random grid and reset the mask
        """
        
        self.grid = generate_grid()
        self.mask = [[0 for _ in range(10)] for _ in range(10)]

class Game:

    
    def __init__(self, id):
        """Class that represents a Game

        Args:
            id (int): The Game Session id
        """
        self.id = id
        self.ready = False
        self.battle_count = 0
        self.players = [None, None]
        self.shoots = [None, None]
        self.shoot_count = 0
        self.current_player_id = None

    def connected(self):
        """Check if the game's ready

        Returns:
            bool: Ready status
        """
        return self.ready
    
    def shoot(self, player_id, pos):
        """Execute a shoot from a player

        Args:
            player_id (int): Id of the player
            pos (List(int)): Grid position
        """
        self.shoots[player_id] = pos
        self.shoot_count+=1
        player2 = self.players[1 - player_id]
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
        if self.shoot_count == NUM_SHOOTS:
            self.update_current_player()
            self.shoot_count = 0

    def winner(self):
        """Returns the winner player id

        Returns:
            int: winner player id or -1
        """
        player1 = self.players[0]
        player2 = self.players[1]

        p1_winner = check_loser(player2)
        p2_winner = check_loser(player1)

        if p1_winner:
            return 0
        
        if p2_winner:
            return 1
        
        
        return -1
    
    def reset(self):
        """Reset the game session
        """
        self.shoots = [None, None]
        self.shoot_count = 0
        self.battle_count += 1
        for player in self.players:
            player.init_grid_and_mask()
        
        self.update_current_player()

    def __repr__(self) -> str:
        return f"Game(id:{self.id}, ready: {self.ready})"

    def update_current_player(self):
        """Update the current player
        """
        self.current_player_id = int(not self.current_player_id)