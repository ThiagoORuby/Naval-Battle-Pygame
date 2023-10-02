def grid_to_matrix():
    matrix = []
    with open('grid.txt', 'r') as f:
        for row in f:
            el = [int(num) for num in row.split()]
            matrix.append(el)
    
    return matrix

class Player:
    
    def __init__(self):
        self.grid = []
        self.mask = []
        self.init_grid_and_mask()

    def init_grid_and_mask(self):
        
        self.grid = grid_to_matrix()
        self.mask = [[0 for _ in range(10)] for _ in range(10)]

class Game:
    
    def __init__(self, id):
        self.id = id
        self.ready = False
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
            else:
                player2.mask[row][col] = -1
        if self.shoot_count == 3:
            self.update_current_player()
            self.shoot_count = 0

    def __repr__(self) -> str:
        return f"Game(id:{self.id}, ready: {self.ready})"

    def update_current_player(self):
        self.current_player_id = int(not self.current_player_id)