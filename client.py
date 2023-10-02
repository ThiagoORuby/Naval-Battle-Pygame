import pygame
from network import Network
from constants import *
from components import *
import pickle
from math import floor
pygame.font.init()

pygame.init()
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Client")

ship_spritesheet = pygame.image.load('assets/BattleShipSheet_final.png')
token_spritesheet = pygame.image.load('assets/Tokens.png')
ocean_map = pygame.image.load('assets/oceangrid_final.png')
radar_map = pygame.image.load('assets/radargrid_final.png')

row = 0
col = 0
h_row = SHIP_POS_Y
h_col = SHIP_POS_X
vertical_ships = dict()
horizontal_ships = dict()
for size in SHIP_SIZE:
    sprite_v = ship_spritesheet.subsurface(
        pygame.Rect(
            col,
            row,
            TILE_SIZE,
            TILE_SIZE*size - (size - 1)
        )
    )
    sprite_h = ship_spritesheet.subsurface(
        pygame.Rect(
            h_col,
            h_row,
            TILE_SIZE*size - (size - 1),
            TILE_SIZE
        )
    ) 
    vertical_ships[size] = sprite_v
    horizontal_ships[size] = sprite_h
    col += (TILE_SIZE + 6)
    h_row += (TILE_SIZE + 6)

tokens = dict()
col = 0
for kind in SHOOT_TYPES:
    sprite = token_spritesheet.subsurface(
        pygame.Rect(
            col,
            0,
            TILE_SIZE,
            TILE_SIZE
        )
    )
    tokens[kind] = sprite
    col += TILE_SIZE

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


def redrawWindow(win, game, p):
    win.fill((0,0,50))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (WINDOW_WIDTH/2 - text.get_width()/2, WINDOW_HEIGHT/2 - text.get_height()/2))
    else:
        win.blit(radar_map, (12,54))
        win.blit(ocean_map, (12*2 + 342,54))

        draw_grid(win, game.players[p].grid)

        if game.current_player_id == p:
            font = pygame.font.SysFont("comicsans", 60)
            text = font.render("Your Round", 1, (0, 255,255))
            win.blit(text, (200, 10))

        draw_ocean_mask(win, game.players[p].mask)
        draw_radar_mask(win, game.players[1 - p].mask)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if RADAR_GRID_X < pos[0] < RADAR_GRID_X + GRID_WIDTH - TILE_SIZE and \
                    OCEAN_GRID_Y < pos[1] < OCEAN_GRID_Y + GRID_HEIGHT - TILE_SIZE:
                    pos_grid = [floor(abs(pos[i] - RADAR_GRID_POS[i])//(TILE_SIZE - 1)) for i in range(2)]
                    data = f"{pos_grid[0]},{pos_grid[1]}"
                    if game.current_player_id == player and game.connected():
                        n.send(data)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((0,0,50))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()
