import pygame
from pygame.locals import *
pygame.init()



all_sprites = pygame.sprite.LayeredUpdates()
font_sprites = pygame.sprite.Group()
tile_sprites = pygame.sprite.Group()
background_sprites = pygame.sprite.Group()
stair_sprites = pygame.sprite.Group()
pipe_sprites  = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()
mario_fireball_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
death_sprites = pygame.sprite.Group()
player_sprites = pygame.sprite.Group()
object_sprites = pygame.sprite.Group()
animation_sprites = pygame.sprite.Group()

time = 60

texture = "resources/sprite/"

stop = False
is_scroll = False
auto_scroll = False
can_scroll = True

game_over = False

reset_warning = 0


def init():
    global tile_sheet, font_sheet, enemy_n_bosses_sheet, items_objects_sheet, player_sheet, castle_sheet, coin_display_animation, peach_sheet, poster_sprites
    tile_sheet = pygame.image.load(texture + "NES - Super Mario Bros - Tileset.png" ).convert()
    font_sheet = pygame.image.load(texture + "NES - Super Mario Bros - Font.png").convert_alpha()
    enemy_n_bosses_sheet = pygame.image.load(texture + "NES - Super Mario Bros - Enemies & Bosses.png").convert()
    items_objects_sheet  = pygame.image.load(texture + "NES - Super Mario Bros - Items Objects and NPCs.png").convert()
    player_sheet = pygame.image.load(texture + "NES - Super Mario Bros - Mario & Luigi.png" ).convert()
    castle_sheet = pygame.image.load(texture + "NES - Super Mario Bros - Castle.png" ).convert()
    peach_sheet  = pygame.image.load(texture + "Peach_Princess.png")
    poster_sprites = pygame.image.load(texture + "NES - Super Mario Bros - Title Screen.png").convert_alpha()

     
tile_w = 16
tile_h = 15


def get_geometry_scale():
    geometry = pygame.display.list_modes()[0]
    geometry = (  int(  (geometry[1]/tile_h)*tile_w  )   , geometry[1] )
    return geometry


def get_geometry_sub_scale():
    geometry = pygame.display.list_modes()[3]
    geometry = (  int(  (geometry[1]/tile_h)*tile_w  )   , geometry[1] )
    return geometry


geometry = ( (16*tile_w)*3 , ( (16*tile_h) * 3 ) )

geometry_sub = get_geometry_sub_scale()
geometry_full = get_geometry_scale()

geometry_scale = geometry_sub


gravity_in_up_WATHER   = .16
gravity_in_down_WATHER = .20

gravity_in_up_GRASS   = .32
gravity_in_down_GRASS = 1.5

color_key = (0, 0, 0)


blue_sky = (118, 134, 255)
black    = (0, 0, 0)
wather   = (66, 66, 255)

background_color = blue_sky


def get_data():
    data_open = open("data.txt")
    data_f = list()
    for data in data_open:
        data_f.append(data.replace("\n", ""))
    data_open.close()

    return data_f

def write_data(*args):
    data_open = get_data()

    for n in range(0, len(data_open)):
        data_open[n] += "\n"

    data_write = open("data.txt", "w")

    for n in range(0, len(args[0])):
        data_open[args[1][n]] = args[0][n] + "\n"
    data_open = "".join(data_open)
    data_write.write(data_open)
    data_write.close()


class Chronometer_Continuous():
    def __init__(self, time):
        super().__init__()
        self.time = time
        self.init_time = time
        self.decreasing_reazon = -0.06
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60
        
    def time_over(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            
            self.time += self.decreasing_reazon
            
        if self.time <= 0:
            return True

    def reset(self, time=False):
        if not time:
            self.time = self.init_time

        else:
            self.time = time
            self.init_time = time

    def play(self):
        self.decreasing_reazon = -0.06

    def stop(self):
        self.decreasing_reazon = 0


class Chronometer(pygame.sprite.Sprite):
    def __init__(self, time):
        super().__init__()
        self.time = time
        self.init_time = time
        self.decreasing_reazon = -0.6
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 600
        
    def time_over(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            
            self.time += self.decreasing_reazon
            
        if self.time <= 0:
            return True

        else:
            return False

    def reset(self, time=False):
        if not time:
            self.time = self.init_time

        else:
            self.time = time
            self.init_time = time

    def play(self):
        self.decreasing_reazon = -6

    def stop(self):
        self.decreasing_reazon = 0