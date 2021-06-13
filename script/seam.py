import pygame
from pygame.locals import *
pygame.init()

from script import group, tile, palette, font, animation, player, score, sound, levels

seam = group.geometry[0]+48*7

level = None
level_index = None
black_screen = False


class Killer_Queen(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((1, 720))
        self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = (seam-group.geometry[0]+48)*-1, 0

    def Eliminate(self):
        for sprite in group.all_sprites:
            if sprite.rect.x <= self.rect.x:
                sprite.kill()

seam_Kill = Killer_Queen()


def Set_Data(level_data=None, level_index_data=None):
    global level, level_index
    if level_data != None:
        level = level_data
        for player in group.player_sprites:
            player.re_appear_index = 0

    if level_index_data != None:
        level_index = level_index_data


def Load(xi):
    global seam, x_index_normal_seam, x_index_background_seam, level_solid, level_background, x_seam, black_screen, bg
    level_data = level[level_index]
    palette.index, palette.special_index = level_data[0][0], level_data[0][1]
    level_solid      = level_data[1]
    level_background = level_data[2]
    group.can_scroll, group.auto_scroll = level_data[3][0], level_data[3][1]
    if level_data[4] != None and xi==0:
        score.time = level_data[4]

    sound.main_theme = level_data[5]
    sound.load(sound.main_theme[sound.index])

    for player in group.player_sprites:
        if not black_screen and not player.invincibility_power:
            sound.play(-1)

    group.background_color = level_data[6]

    x_seam = seam

    x_index_normal_seam = seam+(xi*48)
    #x_index_background_seam = seam+(xi*48)

    # background --------------------------------
    x_index_background = xi
    y_index_background = 0

    x_pos   = 0
    y_pos   = 0
    for row in level_background:
        for data in row:          
            try:
                tile.Generate_Tile( (x_pos, y_pos), row[x_index_background]  )
            except:
                x_index_background -= int( int(x_index_background/48)*48)
                tile.Generate_Tile( (x_pos, y_pos), row[x_index_background]  )
            x_pos += 48
            x_index_background += 1

            if x_pos > seam:
                x_pos = 0
                x_index_background_seam = int(x_index_background*48)-48
                x_index_background = xi
                break          
        x_pos   = 0
        x_index_background = xi
        y_pos += 48

    # Normal ------------------------------
    x_index_normal = xi
    y_index_normal = 0

    x_pos   = 0
    y_pos   = 0
    for row in level_solid:
        for data in row:
            try:
                tile.Generate_Tile( (x_pos, y_pos), row[x_index_normal]  )
            except:
                pass
            x_pos += 48
            x_index_normal += 1

            if x_pos > seam:
                x_pos = 0
                x_index_normal = xi
                break    
        x_pos   = 0
        x_index_normal = xi
        y_pos += 48

    #print(x_index_background_seam)


def Clear():
    for sprite in group.all_sprites:
        if not isinstance(sprite, font.Font) and not isinstance(sprite, animation.Coin_Display_Animation) and not isinstance(sprite, animation.Animation_Player) and not isinstance(sprite, player.Player) and not isinstance(sprite, animation.Animation_Pipe) and not isinstance(sprite, tile.Seam_Tile):
            sprite.kill()


def Seam(delta_time):
    global seam, x_seam, x_index_background_seam, x_index_normal_seam
    if x_seam < seam-48:
        x_seam += 48

        # Background -------------------------------------------------------------------------
        y_index_background = 0
        y_seam = 0
        for n in range(0, len(level_background)):
            try:
                tile.Generate_Tile( (x_seam, y_seam), level_background[y_index_background][int(x_index_background_seam/3/16)]  )

            except:
                x_index_background_seam -= 2304
                tile.Generate_Tile( (x_seam, y_seam), level_background[y_index_background][int(x_index_background_seam/3/16)]  )

            y_seam += 48
            y_index_background += 1

        # Solid ----------------------------------------------------------------------------
        y_index_normal = 0
        y_seam = 0
        for n in range(0, len(level_solid)):
            try:
                if  level_solid[y_index_normal][int(x_index_normal_seam/3/16)][0:2].lower() != "10":
                    tile.Generate_Tile( (x_seam, y_seam), level_solid[y_index_normal][int(x_index_normal_seam/3/16)]  )

            except:
                pass
            y_seam += 48
            y_index_normal += 1

        seam_Kill.Eliminate()

"""
def Scroll(player_s, delta_time):
    global x_seam, x_index_background_seam, x_index_normal_seam, group.can_scroll
    if group.can_scroll:
        if player_s.rect.x >= group.geometry[0]/3+48 and (int( player_s.right_velocity *group.time*delta_time) + int( player_s.left_velocity *group.time*delta_time) + int( player_s.platform_velocity_x *group.time*delta_time) ) >= 0:
            group.is_scroll = True
            

        else:
            group.is_scroll = False


        if group.is_scroll:
            if group.auto_scroll:
                right_val    = 3
                left_val     = 0
                platform_val = 0

            else:
                if group.is_scroll:
                    right_val    = int( player_s.right_velocity *group.time*delta_time)
                    left_val     = int( player_s.left_velocity *group.time*delta_time)
                    platform_val = int( player_s.platform_velocity_x *group.time*delta_time)

            x_index_normal_seam += right_val
            x_index_normal_seam += left_val
            x_index_normal_seam += platform_val

            x_index_background_seam += right_val
            x_index_background_seam += left_val
            x_index_background_seam += platform_val

            x_seam += right_val*-1
            x_seam += left_val*-1
            x_seam += platform_val*-1


            for sprite in group.all_sprites:
                if not isinstance(sprite, font.Font) and not isinstance(sprite, animation.Coin_Display_Animation):
                    sprite.rect.x += right_val*-1
                    sprite.rect.x += left_val*-1
                    sprite.rect.x += platform_val*-1
"""

def Scroll(player_s, delta_time):
    global x_seam, x_index_background_seam, x_index_normal_seam
    if group.can_scroll and not group.stop:
        if group.auto_scroll:
            group.is_scroll = True
            right_val    = player_s.walk_vel
            left_val     = 0
            platform_val = 0

        if not group.auto_scroll:
            if player_s.rect.x >= group.geometry[0]/3+81 and (int( player_s.right_velocity *group.time*delta_time) + int( player_s.left_velocity *group.time*delta_time) + int( player_s.platform_velocity_x *group.time*delta_time) ) >= 0:
                group.is_scroll = True
                right_val    = int( player_s.right_velocity *group.time*delta_time)
                left_val     = int( player_s.left_velocity *group.time*delta_time)
                platform_val = int( player_s.platform_velocity_x *group.time*delta_time) 

            else:
                group.is_scroll = False
                right_val    = 0
                left_val     = 0
                platform_val = 0

        if group.is_scroll:
            x_index_normal_seam += right_val
            x_index_normal_seam += left_val
            x_index_normal_seam += platform_val

            x_index_background_seam += right_val
            x_index_background_seam += left_val
            x_index_background_seam += platform_val

            x_seam += right_val*-1
            x_seam += left_val*-1
            x_seam += platform_val*-1


            for sprite in group.all_sprites:
                if not isinstance(sprite, font.Font) and not isinstance(sprite, animation.Coin_Display_Animation) and not isinstance(sprite, tile.Teleporter_Static):
                    sprite.rect.x += right_val*-1
                    sprite.rect.x += left_val*-1
                    sprite.rect.x += platform_val*-1


class Black_Screen(pygame.sprite.Sprite):
    def __init__(self):
        global black_screen
        super().__init__()
        sound.index = 0
        tile.tile_frame = 0
        animation.enemy_frame = 0
        animation.hammer_frame = 0

        group.stop = True
        black_screen = True
        self.game_over = False
        for player in group.player_sprites:
            self.player = player
        self.player.animation.set_visibility(False)
        self.image = pygame.Surface( ((*group.geometry), ) )
        self.rect = self.image.get_rect()
        self.time = group.Chronometer(4)
        self._layer = 4

        font.Kill_Identifier("screen")

        if score.lives > 0:
            font.Generate_Message("world {}-{}".format(levels.world+1, levels.level+1), int(group.geometry[0]/2-120), 216, (255, 255, 255), "screen")
            for player in group.player_sprites:
                if player.name == "luigi":
                    font.Generate_Message("=", int(group.geometry[0]/2-96), 291, (255, 255, 255), "screen")

                else:
                    font.Generate_Message("|", int(group.geometry[0]/2-96), 291, (255, 255, 255), "screen")

            font.Generate_Message("*  {}".format(score.lives), int(group.geometry[0]/2-24)  , 312, (255, 255, 255), "screen" )

                    
        else:
            self.game_over = True
            group.game_over = True
            self.time = group.Chronometer(6)
            font.Generate_Message("game over", int(group.geometry[0]/2-120), 312, (255, 255, 255), "screen")
            sound.game_over_sound.stop()
            sound.game_over_sound.play()

            #group.write_data( (  "0", "3" ), (2, 3) )

            levels.level = 0
            score.lives  = 3
            

    def update(self, delta_time):
        global black_screen
        if self.time.time_over():
            if not self.game_over:
                sound.play(-1)
            font.Kill_Identifier("screen")
            group.stop = False
            black_screen = False
            self.player.animation.set_visibility(True)
            self.kill()

