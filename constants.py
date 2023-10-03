import pygame

pygame.mixer.init()

WINDOW_WIDTH = 720
WINDOW_HEIGHT = 450

GRID_WIDTH = 342
GRID_HEIGHT = 342

TILE_SIZE = 32

SHIP_POS_X = 244
SHIP_POS_Y = 216

OCEAN_GRID_X = 397
OCEAN_GRID_Y = 85
RADAR_GRID_X = 43
RADAR_GRID_POS = (RADAR_GRID_X, OCEAN_GRID_Y)

NUM_SHOOTS = 3

ADDRESS = 'localhost'
PORT = 1234

SHIP_SIZE = [2,3,3,4,5]
SHOOT_TYPES = ['radar_water', 'radar_ship', 'ocean_water', 'ocean_ship']

ship_spritesheet = pygame.image.load('assets/BattleShipSheet_final.png')
token_spritesheet = pygame.image.load('assets/Tokens.png')
titleScreen = pygame.image.load('assets/titleScreen.png')
ocean_map = pygame.image.load('assets/oceangrid_final.png')
radar_map = pygame.image.load('assets/radargrid_final.png')

gameSounds = {
    'play' : pygame.mixer.Sound('assets/play.wav'),
    'ship_shoot' : pygame.mixer.Sound('assets/explosion_metal.wav'),
    'water_shoot' : pygame.mixer.Sound('assets/splash.wav')
}

# Load the sprites from the spritesheets
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
