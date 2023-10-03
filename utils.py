from constants import *
import random

def generate_grid():
    num_linhas = 10
    num_colunas = 10
    matriz = [[0] * num_colunas for _ in range(num_linhas)]

    barcos = [(5, 1), (4, 2), (3, 2), (2, 3)]
    barcos.sort(reverse=True)

    for tamanho, quantidade in barcos:
        for _ in range(quantidade):
            while True:
                direcao = random.choice(["horizontal", "vertical"])
                x = random.randint(0, num_linhas - 1)
                y = random.randint(0, num_colunas - 1)

                space_okay = True
                position_okay = True

                for i in range(tamanho):
                    if direcao == "horizontal":
                        if y + i > num_colunas - 1 or matriz[x][y + i] != 0:
                            position_okay = False
                            break
                    else:
                        if x + i > num_linhas - 1 or matriz[x + i][y] != 0:
                            position_okay = False
                            break
                    for j in range(-1, 2):
                        for k in range(-1, 2):
                            if 0 <= x + i + j < num_linhas and 0 <= y + i + k < num_colunas:
                                if matriz[x + i + j][y + i + k] != 0:
                                    space_okay = False
                                    break
                
                if position_okay and space_okay:
                    for i in range(tamanho):
                        if direcao == "horizontal":
                            matriz[x][y + i] = tamanho
                        else:
                            matriz[x + i][y] = tamanho
                    break
                
                continue
    return matriz

def check_left_top(grid, i, j, size):

    if(i > 0 and grid[i-1][j] == size):
        return True
    if(j > 0 and grid[i][j-1] == size):
        return True
    
def check_right(grid, i, j, size):
    if(j < 10 - 1 and grid[i][j+1] == size):
        return True
    
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