from constants import *
import random

# Create a new ship on a grid
def createShip(size, grid):
    while True:
        i = random.randint(0, 9)
        j = random.randint(0, 9)
        direction = random.choice(["horizontal", "vertical"])
        
        if direction == "horizontal":
            finalI = i
            finalJ = j + size - 1
            if finalJ > 9:
                continue
        else:
            finalI = i + size - 1
            finalJ = j
            if finalI > 9:
                continue
        
        collision = False
        for x in range(i, finalI + 1):
            for y in range(j, finalJ + 1):
                if grid[x][y] > 0:
                    collision = True
                    break
            if collision:
                break
        
        if not collision and not adjacentShip(grid, i, j, finalI, finalJ):
            for x in range(i, finalI + 1):
                for y in range(j, finalJ + 1):
                    grid[x][y] = size
            break

# check if has an adjacent ship
def adjacentShip(grid, i, j, finalI, finalJ):
    for x in range(i - 1, finalI + 2):
        for y in range(j - 1, finalJ + 2):
            if 0 <= x < 10 and 0 <= y < 10 and grid[x][y] > 0:
                return True
    return False

# Generate a Battleship Grid
def generate_grid():
    grid = [[0] * 10 for _ in range(10)]

    ships = [(5, 1), (4, 2), (3, 2), (2, 3)]

    for size, qnt in ships:
        for _ in range(qnt):
            createShip(size, grid)
    
    return grid


def check_left_top(grid, i, j, size):

    if(i > 0 and grid[i-1][j] == size):
        return True
    if(j > 0 and grid[i][j-1] == size):
        return True
    
def check_right(grid, i, j, size):
    if(j < 10 - 1 and grid[i][j+1] == size):
        return True
    
# Draw the Grid on the screen
def draw_grid(window, grid):
    for i in range(10):
        for j in range(10):
            size = grid[i][j]
            
            if size == 0 or check_left_top(grid, i, j, size):
                continue

            if check_right(grid, i, j, size):
                window.blit(horizontal_ships[size], (OCEAN_GRID_X + j*TILE_SIZE - j,
                                                     OCEAN_GRID_Y + i*TILE_SIZE - i))
            else:
                window.blit(vertical_ships[size], (OCEAN_GRID_X + j*TILE_SIZE - j,
                                                     OCEAN_GRID_Y + i*TILE_SIZE - i))

# Draw the radar mask    
def draw_radar_mask(window, mask):
    for i in range(10):
        for j in range(10):
            kind = mask[i][j]

            if kind == 1:
                window.blit(tokens['radar_ship'], (RADAR_GRID_X + j*TILE_SIZE - j,
                                                     OCEAN_GRID_Y + i*TILE_SIZE - i))
            elif kind == -1:
                window.blit(tokens['radar_water'], (RADAR_GRID_X + j*TILE_SIZE - j,
                                                     OCEAN_GRID_Y + i*TILE_SIZE - i))

# Draw the ocean mask
def draw_ocean_mask(window, mask):
    for i in range(10):
        for j in range(10):
            kind = mask[i][j]

            if kind == 1:
                window.blit(tokens['ocean_ship'], (OCEAN_GRID_X + j*TILE_SIZE - j,
                                                     OCEAN_GRID_Y + i*TILE_SIZE - i))
            elif kind == -1:
                window.blit(tokens['ocean_water'], (OCEAN_GRID_X + j*TILE_SIZE - j,
                                                     OCEAN_GRID_Y + i*TILE_SIZE - i))