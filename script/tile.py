import pygame, random
from pygame.locals import *
pygame.init()

from script import group, physic, animation, palette, obj, score, enemy, seam, sound, font, levels

tile_frame = 0 # tiene que ser global porque todos los tiles siempre tienen el mismo frame
tile_last_update = pygame.time.get_ticks()
tile_frame_rate = 100

"""
    x y

    tipo
    texturas
    parametros especiales
"""

def Global_Tile_Frame():
    global tile_frame, tile_last_update, tile_frame_rate
    if not group.stop:
        now = pygame.time.get_ticks()
        if now - tile_last_update > tile_frame_rate:           
            tile_last_update = now
            tile_frame += 1

            if tile_frame >= 8:
                tile_frame = 0


def Super_Generate( coor, tp, special_parameter_1 ): # Corregir la funcion y a todos los enemigos en levels.py !!!!!
    x, y = coor[0], coor[1]
    if special_parameter_1 == 1:
        Generate_Tile((x, y), tp+"0000")
        Generate_Tile((x-48, y), tp+"0000")

    if special_parameter_1 == 2:
        Generate_Tile((x, y), tp+"1000")
        Generate_Tile((x-48, y), tp+"0000")

    if special_parameter_1 == 3:
        Generate_Tile((x, y), tp+"0000")
        Generate_Tile((x-96, y), tp+"0000")

    if special_parameter_1 == 4:
        Generate_Tile((x, y), tp+"1000")
        Generate_Tile((x-96, y), tp+"0000")

    if special_parameter_1 == 5:
        Generate_Tile((x, y), tp+"0000")
        Generate_Tile((x-144, y), tp+"0000")


    if special_parameter_1 == 6:
        Generate_Tile((x, y), tp+"0000")
        Generate_Tile((x-48, y), tp+"0000")
        Generate_Tile((x-96, y), tp+"0000")

    if special_parameter_1 == 7:
        Generate_Tile((x, y), tp+"0000")
        Generate_Tile((x-96, y), tp+"1000")
        Generate_Tile((x-144, y), tp+"0000")

    if special_parameter_1 == 8:
        Generate_Tile((x, y), tp+"0000")
        Generate_Tile((x-96, y), tp+"0000")
        Generate_Tile((x-192, y), tp+"0000")

    if special_parameter_1 == 9:
        Generate_Tile((x, y), tp+"0000")
        Generate_Tile((x-144, y), tp+"1000")
        Generate_Tile((x-240, y), tp+"0000")

    if special_parameter_1 == 10:
        Generate_Tile((x, y), tp+"0000")
        Generate_Tile((x-144, y), tp+"0000")
        Generate_Tile((x-288, y), tp+"0000")


def Generate_Tile(screen_pos, param):
    x = screen_pos[0]
    y = screen_pos[1]

    type_of_tile = physic.convert_2(param[0:2])  #physic.convert(param[0]) + physic.convert(param[1])
    texture = [ physic.convert(param[2]), physic.convert(param[3]) ]
    if not isinstance(texture[0], bool):
        texture[0] *= 16

    if not isinstance(texture[1], bool):
        texture[1] *= 16

    texture = tuple(texture)

    special_parameter_1 = physic.convert(param[4])
    special_parameter_2 = physic.convert(param[5])
    """
        print("x:", x)
        print("y:", y)

        print("type_of_tile:", type_of_tile)
        print("texture:", texture)
        print("special_parameter_1:", special_parameter_1)
        print("special_parameter_2:", special_parameter_2)
    """

    if type_of_tile == 0:
        pass

    if type_of_tile == 1:
        tile_obj = Solid_Tile(x, y, texture)
        group.all_sprites.add(tile_obj)
        group.tile_sprites.add(tile_obj)

    if type_of_tile == 2:
        tile_obj = Sub_Solid_Tile(x, y, texture)
        group.all_sprites.add(tile_obj)
        group.tile_sprites.add(tile_obj)

    if type_of_tile == 3:
        tile_obj = No_Solid_Tile(x, y, texture)
        group.all_sprites.add(tile_obj)
        group.background_sprites.add(tile_obj)

    if type_of_tile == 4:
        tile_obj = Break_Tile(x, y, texture)
        group.all_sprites.add(tile_obj)
        group.tile_sprites.add(tile_obj)

    if type_of_tile == 5:
        if isinstance(texture[0], bool):
            texture = False
        tile_obj = Gift_Tile(x, y, texture, special_parameter_1, special_parameter_2)
        group.all_sprites.add(tile_obj)
        group.tile_sprites.add(tile_obj)

    if type_of_tile == 6:
        tile_obj = Coin(x, y)
        group.all_sprites.add(tile_obj)
        group.coin_sprites.add(tile_obj)

    if type_of_tile == 7:
        tile_obj = Axe(x, y)
        group.all_sprites.add(tile_obj)
        group.background_sprites.add(tile_obj)

    if type_of_tile == 8:
        tile_obj = Bullet_Tile(x, y)
        group.all_sprites.add(tile_obj)
        group.tile_sprites.add(tile_obj)

    if type_of_tile == 9:
        tile_obj = Spinning_Fire_Balls_Tile(x, y, texture, special_parameter_1, special_parameter_2)
        group.all_sprites.add(tile_obj)
        group.tile_sprites.add(tile_obj)

    if type_of_tile == 10:
        tile_obj = Jumping_Board_Tile(x, y)
        group.all_sprites.add(tile_obj)
        group.tile_sprites.add(tile_obj)

    if type_of_tile == 11:
        tile_obj = Platform(x, y, texture, special_parameter_1, special_parameter_2)
        group.all_sprites.add(tile_obj)
        group.tile_sprites.add(tile_obj)

    if type_of_tile == 12:
        tile_obj = Double_Platform(x, y, texture, None)
        group.all_sprites.add(tile_obj)
        group.tile_sprites.add(tile_obj)

    if type_of_tile == 13:
        pass

    if type_of_tile == 14:
        tile_obj = Pipe_2(x, y, texture, special_parameter_1, special_parameter_2)
        group.all_sprites.add(tile_obj)
        group.pipe_sprites.add(tile_obj)

    if type_of_tile == 15:
        tile_obj = Vine_2(x, y)
        group.all_sprites.add(tile_obj)
        group.tile_sprites.add(tile_obj)

    if type_of_tile == 16:
        texture = physic.convert_2( param[2:4]   )

        tile_obj = Teleporter_Static(x, y, texture, special_parameter_1)
        group.all_sprites.add(tile_obj)
        group.tile_sprites.add(tile_obj)

    if type_of_tile == 17:
        tile_obj = Teleporter_Move(x, y, texture, special_parameter_1, special_parameter_2)
        group.all_sprites.add(tile_obj)
        group.tile_sprites.add(tile_obj)

    if type_of_tile == 18:
        pole = Pole(x, y)
        group.all_sprites.add(pole)
        group.stair_sprites.add(pole)

    if type_of_tile == 19:
        tile_obj = Flag_From_Pole(x, y)
        group.all_sprites.add(tile_obj)
        group.background_sprites.add(tile_obj)

    if type_of_tile == 20:
        tile_obj = Castle_Tile(x, y, texture)
        group.all_sprites.add(tile_obj)
        group.background_sprites.add(tile_obj)

    if type_of_tile == 21:
        pass

    if type_of_tile == 22:
        tile_obj = Triple_Tile(x, y)
        group.all_sprites.add(tile_obj)
        group.background_sprites.add(tile_obj)

    if type_of_tile == 23:
        tile_obj = Block_Scroll_Tile(x, y)
        group.all_sprites.add(tile_obj)
        group.background_sprites.add(tile_obj)



    # Player ------------------------------------------------------------------------
    if type_of_tile == 27:
        middle_alignment = int(texture[0]/16)
        y_alignment      = texture[1]
        player_physic    = special_parameter_1

        for player in group.player_sprites:
            player.not_damage_time.time = 0
            player.auto_mode = bool(int(special_parameter_2))
            if middle_alignment == 0:
                alignment_val = 0

            if middle_alignment == 1:
                alignment_val = +27

            if middle_alignment == 2:
                alignment_val = -27


            player.rect.x = x+alignment_val
            if y_alignment:
                player.rect.top = y

            if not y_alignment:
                player.rect.bottom = y+48

            player.set_physic(bool(player_physic))

            player.left_velocity   = 0
            player.right_velocity  = 0
            if not player.wather:
                if y_alignment:
                    player.bottom_velocity = player.fall_vel

                else:
                    player.bottom_velocity = 1

    # NPC ---------------------------------------------------------------------------
    if type_of_tile == 28:
        npc = Toad(x, y)
        group.all_sprites.add(npc)
        group.tile_sprites.add(npc)

    if type_of_tile == 29:
        npc = Peach_Princess(x, y)
        group.all_sprites.add(npc)
        group.tile_sprites.add(npc)


    old_x = x
    if texture[0]/16 == 0:
        x = x

    if texture[0]/16 == 1:
        x += 27

    if texture[0]/16 == 2:
        x += -27

    # Enemigos ----------------------------------------------------------------------
    if type_of_tile == 30: # 130000
        if special_parameter_1 == 0:
            en = enemy.Goomba(x, y)
            group.all_sprites.add(en)
            group.enemy_sprites.add(en)

        else:
            Super_Generate((x, y), "13", special_parameter_1)


    if type_of_tile == 31:
        if special_parameter_1 == 0:
            en = enemy.Koopa_Paratroopa_Green(x, y)
            group.all_sprites.add(en)
            group.enemy_sprites.add(en)

        else:
            Super_Generate((x, y), "14", special_parameter_1)

    if type_of_tile == 32:
        if special_parameter_1 == 0:
            en = enemy.Koopa_Troopa_Green(x, y)
            group.all_sprites.add(en)
            group.enemy_sprites.add(en)

        else:
            Super_Generate((x, y), "15", special_parameter_1)

    if type_of_tile == 33:
        if special_parameter_1 == 0:
            en = enemy.Koopa_Paratroopa_Red(x, y)
            group.all_sprites.add(en)
            group.enemy_sprites.add(en)

        else:
            Super_Generate((x, y), "16", special_parameter_1 )

    if type_of_tile == 34:
        if special_parameter_1 == 0:
            en = enemy.Koopa_Troopa_Red(x, y)
            group.all_sprites.add(en) 
            group.enemy_sprites.add(en)

        else:
            Super_Generate((x, y), "17", special_parameter_1)

    if type_of_tile == 35:
        if special_parameter_1 == 0:
            en = enemy.Buzzy_Beetle(x, y)
            group.all_sprites.add(en)
            group.enemy_sprites.add(en)

        else:
            Super_Generate((x, y), "18", special_parameter_1)

    if type_of_tile == 36:
        if special_parameter_1 == 0:
            en = enemy.Spiny(x, y)
            group.all_sprites.add(en)
            group.enemy_sprites.add(en)

        else:
            Super_Generate((x, y), "19", special_parameter_1)

    if type_of_tile == 37: # 1a0000
        en = enemy.Lakitu(x, y)
        group.all_sprites.add(en)
        group.enemy_sprites.add(en)

    if type_of_tile == 38:
        en = enemy.Bullet_Bill(x, y)
        group.all_sprites.add(en)
        group.enemy_sprites.add(en)

    if type_of_tile == 39:
        en = enemy.Pirana_Plant_Green(x, y, special_parameter_1)
        group.all_sprites.add(en)
        group.enemy_sprites.add(en)

    if type_of_tile == 40:
        en = enemy.Hammer_Brother(x, y)
        group.all_sprites.add(en)
        group.enemy_sprites.add(en)

    if type_of_tile == 41:
        en = enemy.Bloober(x, y)
        group.all_sprites.add(en)
        group.enemy_sprites.add(en)

    if type_of_tile == 42:
        en = enemy.Cheep_Cheep_Wather(x, y, special_parameter_1)
        group.all_sprites.add(en)
        group.enemy_sprites.add(en)

    if type_of_tile == 43:
        en = enemy.Cheep_Cheep_Grass(x, y)
        group.all_sprites.add(en)
        group.enemy_sprites.add(en)

    if type_of_tile == 44:
        en = enemy.Podoboo(x, y, special_parameter_1)
        group.all_sprites.add(en)
        group.enemy_sprites.add(en)
    
    if type_of_tile == 45:
        en = enemy.Bowser_Fire(x, y, special_parameter_1)
        group.all_sprites.add(en)
        group.enemy_sprites.add(en)

    x = old_x

    if type_of_tile == 46:
        en = enemy.Bowser(x, y, texture, None, special_parameter_2)
        group.all_sprites.add(en)
        group.enemy_sprites.add(en)


    # Otros bloques -----------------------------------------------------

    if type_of_tile == 82:
        tile_obj = Spiny_Tile(x, y)
        group.all_sprites.add(tile_obj)
        group.tile_sprites.add(tile_obj)


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((48, 48))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self._layer = 2

        self.top_collide = True
        self.bottom_collide = True
        self.left_collide = True
        self.right_collide = True

        self.can_rebound = False
        self.is_rebound  = False

        self.breakable   = False
        self.is_break    = False

        self.coin        = False
        self.vine        = False

        self.jump_board  = False

        self.platform    = False
        self.double_platform = False

        self.pipe        = False

        self.teleporter  = False
        self.pole        = False

        self.killer      = False   

        self.spiny       = False

        self.palette = palette.palette_2
        self.index = palette.index
        

    def set_color_palette(self):
        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace( self.palette[0][0], self.palette[self.index][0] ) 
        self.image_pixel_array.replace( self.palette[0][1], self.palette[self.index][1] )
        self.image_pixel_array.replace( self.palette[0][2], self.palette[self.index][2] )
        self.image_pixel_array.replace( self.palette[0][3], self.palette[self.index][3] ) 
        self.image_pixel_array.replace( self.palette[0][4], self.palette[self.index][4] )
        self.image_pixel_array.replace( self.palette[0][5], self.palette[self.index][5] )
        #self.image_pixel_array.replace( self.palette[0][6], self.palette[self.index][6] )
        self.image_pixel_array.replace( self.palette[0][7], self.palette[self.index][7] )


    def bump(self):
        sound.bump_sound.stop()
        sound.bump_sound.play()


    def breakblock(self):
        sound.breakblock_sound.stop()
        sound.breakblock_sound.play()


class Solid_Tile(Tile):
    def __init__(self, x, y, texture):
        super().__init__(x, y)
        if texture[1] > 31 and texture[1] < 64:
            self.palette = palette.special_palette
            self.index = palette.special_index

        if texture[1] > 63 or texture == (48, 0):
            self.palette = palette.palette_3

        if texture == (96, 32):
            Generate_Tile((x, y+48), "035100" )

        self.sheet = group.tile_sheet.copy()
        self.sheet.set_clip(pygame.Rect(texture[0], texture[1], 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey(group.color_key)
        self.set_color_palette()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y


class No_Solid_Tile(Tile):
    def __init__(self, x, y, texture):
        super().__init__(x, y)
        if texture[1] > 31 and texture[1] < 64:
            self.palette = palette.special_palette
            self.index = palette.special_index

        if texture[1] > 63:
            self.palette = palette.palette_3

        if texture == (80, 16) and y <= 624:
            Generate_Tile((x, y+48), "035100" )



        self.sheet = group.tile_sheet.copy()
        self.sheet.set_clip(pygame.Rect(texture + (16, 16)))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.set_color_palette()

        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self._layer = 0

        self.top_collide = False
        self.left_collide = False
        self.bottom_collide = False
        self.right_collide = False


class Sub_Solid_Tile(Tile):
    def __init__(self, x, y, texture):
        super().__init__(x, y)
        if texture[1] > 31 and texture[1] < 64:
            self.palette = palette.special_palette
            self.index = palette.special_index

        if texture[1] > 63:
            self.palette = palette.palette_3

        self.sheet = group.tile_sheet.copy()
        self.sheet.set_clip(pygame.Rect(texture+(16, 16)))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.set_color_palette()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.left_collide = False
        self.right_collide = False
        self.bottom_collide = False


class Castle_Tile(Tile):
    def __init__(self, x, y, texture):
        super().__init__(x, y)
        self.is_top = False
        if texture[0] == 0:
            self.is_top = True
            wh = ( 0, 0, 80, 80)
            self.tile_obj = Solid_Tile(x-96, y+48, (400, 64))
            group.all_sprites.add(self.tile_obj)
            group.tile_sprites.add(self.tile_obj)

        if texture[0] == 16:
            wh = ( 80, 0, 80, 96)

        if texture[0] == 32:
            wh = ( 160, 0, 64, 96)

        self.sheet = group.castle_sheet.copy()
        self.sheet.set_clip(pygame.Rect(wh))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.set_color_palette()

        self.image = pygame.transform.scale(self.image, (wh[2]*3, wh[3]*3))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x+(wh[2]*-3)+48, y

        self.top_collide = False
        self.left_collide = False
        self.bottom_collide = False
        self.right_collide = False

        self.can_rev = True
        self.time = 0
        self.count_fireworks = 0
        self.time_to_drop = group.Chronometer_Continuous(.5)

        for player in group.player_sprites:
            self.player = player


    def controll_fire_works(self):
        if self.can_rev:
            if self.player.auto_mode:
                self.time = str(int(score.time))

                if self.time[-1] == "6":
                    self.count_fireworks = 6
                    #score.time_to_continue.time = 3

                elif self.time[-1] == "3":
                    self.count_fireworks = 3
                    #score.time_to_continue.time = 1.5
                    self.time_to_drop.time += .5

                elif self.time[-1] == "1":
                    self.count_fireworks = 1
                    #score.time_to_continue.time = .5
                    self.time_to_drop.time += 1

                else:
                    self.count_fireworks = 0


                if self.rect.x == 96:
                    self.count_fireworks = 0

                self.can_rev = False


    def controll_flag(self, delta_time):
        if score.time <= 0:
            if not self.tile_obj.rect.y <= self.rect.y-48 and not bool(int(pygame.mixer.get_busy())):
                self.tile_obj.rect.y += ( -2*group.time*delta_time )

            else:
                if self.count_fireworks > 0:
                    if self.time_to_drop.time_over():
                        self.time_to_drop.reset()
                        group.all_sprites.add(obj.Fireworks(random.randrange(0, 720, 48), random.randrange(96, 288, 48)))
                        self.count_fireworks -= 1


    def update(self, delta_time):
        if self.is_top:
            self.controll_flag(delta_time)
            self.controll_fire_works()
                

class Break_Tile(Tile):
    def __init__(self, x, y, texture):
        super().__init__(x, y)
        self.texture = texture

        self.set_visibility(True)
        
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self.breakable = True


    def rebound(self):
        self.bump()
        self.can_rebound = False
        self.is_rebound = True
        self.set_visibility(False)
        rebound_animation = Rebound_Tile(self, self.texture)
        group.all_sprites.add(rebound_animation)
        group.tile_sprites.add(rebound_animation)


    def set_visibility(self, val_bool):
        if val_bool:
            self.can_rebound = True
            self.is_rebound  = False
            self.sheet = group.tile_sheet.copy()
            self.sheet.set_clip(pygame.Rect(self.texture[0], self.texture[1], 16, 16))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.image.set_colorkey(group.color_key)
            self.set_color_palette()
            self.image = pygame.transform.scale(self.image, (48, 48))

        if not val_bool:
            self.image = pygame.Surface((48, 48))
            self.image.fill((0, 0, 0))
            self.image.set_colorkey((0, 0, 0))

            
    def break_tile(self):
        score.score += 50
        self.breakblock() # Sonido
        self.can_rebound = False
        self.is_rebound  = True
        self.breakable   = False
        self.is_break    = True
        self.set_visibility(False)
        rebound_animation = Rebound_Tile(self, (288, 16), True)
        group.all_sprites.add(rebound_animation)
        group.tile_sprites.add(rebound_animation)

        break_brick = animation.Break_Tile_Explosion(self)


class Gift_Tile(Tile):
    def __init__(self, x, y, texture, gift, quantity):
        super().__init__(x, y)
        self.texture = texture
        if not self.texture:
            self.palette = palette.palette_3
            self.sprite_states = ((384, 0), (384, 0), (384, 0), (384, 0), (400, 0), (416, 0), (416, 0), (400, 0))

        else:
            self.sprite_states = ( (self.texture[0], self.texture[1]),  )


        self.sheet = group.tile_sheet.copy()

        if not self.texture:
            self.sheet.set_clip(pygame.Rect( self.sprite_states[tile_frame] + (16, 16) )) 
        else:
            self.sheet.set_clip(pygame.Rect( self.sprite_states[0] + (16, 16) ))

        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey(group.color_key)
        self.set_color_palette()
        self.image = pygame.transform.scale(self.image, (48, 48))

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self.visibility = True
        self.gift = gift
        self.hit_quantity = 0
        self.quantity = quantity

        self.level_index = self.quantity

        if self.gift == 4:
            self.quantity = 1

        self.can_rebound = True


    def set_visibility(self, val_bool):
        self.visibility = val_bool
        if val_bool:
            self.drop_gift()


    def drop_gift(self):
        if self.gift == 0: # Moneda
            sound.coin_sound.stop()
            sound.coin_sound.play()

            coin = animation.Coin_jump_animation(self.rect.x, self.rect.y-48)
            group.all_sprites.add(coin)
            group.death_sprites.add(coin)

            score.coin  += 1
            score.score += 200

        if self.gift == 1:
            for player in group.player_sprites:
                if not player.size:
                    magic_mushroom = obj.Magic_Mushroom(self)
                    group.all_sprites.add(magic_mushroom)
                    group.object_sprites.add(magic_mushroom)
                else:
                    fire_flower = obj.Fire_Flower(self)
                    group.all_sprites.add(fire_flower)
                    group.object_sprites.add(fire_flower)

        if self.gift == 2:
            one_up_mushroom = obj.One_Up_Mushroom(self)
            group.all_sprites.add(one_up_mushroom)
            group.object_sprites.add(one_up_mushroom)

        if self.gift == 3:
            star_man = obj.Starman(self)
            group.all_sprites.add(star_man)
            group.object_sprites.add(star_man)

        if self.gift == 4:
            sound.vine_sound.stop()
            sound.vine_sound.play()
            vine = Vine(self.rect.x, self.rect.y, (368, 64), self, -144)
            """
            vine.top_collide = True
            vine.left_collide = True
            vine.right_collide = True
            vine.bottom_collide = True
            """
            group.all_sprites.add(vine)
            group.stair_sprites.add(vine)

        if self.gift == 5:
            poison_mushroom = obj.Poison_Mushroom(self)
            group.all_sprites.add(poison_mushroom)
            group.object_sprites.add(poison_mushroom)


    def rebound(self):
        self.bump()
        self.can_rebound = False
        self.is_rebound  = True
        self.set_visibility(False)
        self.hit_quantity += 1

        #if not self.texture:
        ti_text = (432, 0)

        #else:
        #    ti_text = (self.sprite_states[0][0], self.sprite_states[0][1]  )

        rebound_animation = Rebound_Tile(self, (ti_text[0], ti_text[1], 16, 16))
        group.all_sprites.add(rebound_animation)
        group.tile_sprites.add(rebound_animation)


    def update(self, delta_time):
        if self.visibility:
            if not self.hit_quantity >= self.quantity:
                self.can_rebound = True
                self.is_rebound  = False
                if not self.texture:
                    self.sheet.set_clip(pygame.Rect( self.sprite_states[tile_frame] + (16, 16) )) 
                else:
                    self.sheet.set_clip(pygame.Rect( self.sprite_states[0] + (16, 16) ))
                self.image = self.sheet.subsurface(self.sheet.get_clip())
                self.image.set_colorkey(group.color_key)
                self.image = pygame.transform.scale(self.image, (48, 48))

            else:
                self.is_rebound  = False
                self.can_rebound = False
                self.sheet.set_clip(pygame.Rect(432, 0, 16, 16)) 
                self.image = self.sheet.subsurface(self.sheet.get_clip())
                self.image.set_colorkey(group.color_key)
                self.image = pygame.transform.scale(self.image, (48, 48))

        else:
            self.image = pygame.Surface((48, 48))
            self.image.fill((0, 0, 0))
            self.image.set_colorkey((0, 0, 0))


class Rebound_Tile(Tile):
    def __init__(self, sprite_object, texture, dokill=False):
        self.sprite_object = sprite_object
        self.dokill = dokill
        super().__init__(self.sprite_object.rect.x, self.sprite_object.rect.y)
        self.palette = self.sprite_object.palette
        self.sheet = group.tile_sheet.copy()
        self.sheet.set_clip(pygame.Rect(texture[0], texture[1], 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey(group.color_key)
        self.set_color_palette()
        self.image = pygame.transform.scale(self.image, (48, 48))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.sprite_object.rect.x, self.sprite_object.rect.y

        self.bottom_velocity = -8
        self.gravity = 0

        
        self._layer = 2
    

    def update(self, delta_time):
        if not group.stop:
            self.rect.x = self.sprite_object.rect.x

            coin_collide = pygame.sprite.spritecollide(self, group.coin_sprites, True)
            for coin in coin_collide:
                sound.coin_sound.stop()
                sound.coin_sound.play()

                coin = animation.Coin_jump_animation(self.rect.x, self.rect.y-48)
                group.all_sprites.add(coin)
                group.death_sprites.add(coin)

                score.coin  += 1
                score.score += 200

            if self.bottom_velocity < 0:
                self.gravity = group.gravity_in_down_GRASS
                self.left_collide = False
                self.right_collide = False

            if self.bottom_velocity >= 0:
                self.gravity = group.gravity_in_down_GRASS
                self.left_collide = True
                self.right_collide = True
            
            self.bottom_velocity = physic.Accelearted_Linear_Movement(self.bottom_velocity, delta_time, 12, self.gravity, -.01, True)

            self.rect.y += self.bottom_velocity

            if self.rect.bottom+3 >= self.sprite_object.rect.bottom:
                group.all_sprites.change_layer(self, 1)

            if self.rect.bottom > self.sprite_object.rect.bottom:
                self.sprite_object.set_visibility(True)
                self.kill()
                if self.dokill:
                    self.sprite_object.kill()      


class Vine(Tile):
    def __init__(self, x, y, texture, sprite_object, collide_on_top):
        super().__init__(x, y)
        self.palette = palette.palette_1
        self.sprite_object = sprite_object
        self.vine = False
        self.sheet = group.tile_sheet.copy()

        self.sheet.set_clip(pygame.Rect(texture+(16, 16)))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.set_color_palette()

        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self._layer = self.sprite_object._layer -1

        self.top_collide = False
        self.left_collide = False
        self.bottom_collide = False
        self.right_collide = False

        self.y_velocity = -3

        self.collide_on_top = collide_on_top

        self.can_add = True
        try:
            self.level_index = self.sprite_object.level_index

        except:
            self.level_index = 0


    def travel(self):
        if tuple(self.sheet.get_clip())[0:2] == (368, 64):
            for player in group.player_sprites:
                if player.rect.bottom <= -46 and player.handle_mode == 1:
                    seam.Clear()
                    seam.Set_Data(None, self.level_index)
                    seam.Load(0)


    def update(self, delta_time):
        if not group.stop:
            self.travel()
            if not self.rect.y <= self.collide_on_top:
                self.rect.y += int(self.y_velocity*group.time*delta_time)
            if self.can_add:
                if self.rect.bottom <= self.sprite_object.rect.top:
                    self.can_add = False
                    group.all_sprites.change_layer(self, self.sprite_object._layer)
                    vine = Vine(self.rect.x, self.rect.bottom, (368, 80), self.sprite_object, self.collide_on_top+48)
                    group.all_sprites.add(vine)
                    group.stair_sprites.add(vine)


class Vine_2(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.left_collide = False
        self.right_collide = False
        self.top_collide   = False
        self.bottom_collide  = False

        sound.vine_sound.stop()
        sound.vine_sound.play()
        vine = Vine(self.rect.x, self.rect.y, (368, 64), self, 432)

        vine.top_collide = True
        vine.left_collide = True
        vine.right_collide = True
        vine.bottom_collide = True
        
        group.all_sprites.add(vine)
        group.tile_sprites.add(vine)


class Pole(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.pole = True
        self.palette = palette.special_palette
        self.index   = palette.special_index

        self.sheet = group.tile_sheet.copy()
        self.sheet.set_clip(pygame.Rect(256, 48, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.set_color_palette()

        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self.top_collide = False
        self.left_collide = False
        self.bottom_collide = False
        self.right_collide = False

        self._layer = 1


class Flag_From_Pole(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.palette = palette.palette_1

        self.sheet = group.tile_sheet.copy()
        self.sheet.set_clip(pygame.Rect(384, 80, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.set_color_palette()

        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x+24, y

        self.top_collide = False
        self.left_collide = False
        self.bottom_collide = False
        self.right_collide = False

        self.walk_vel = 5

        self.can_play = True


    def go_down(self, delta_time):
        for player in group.player_sprites:
            if player.handle_mode == 1 and player.auto_mode:
                if self.can_play:
                    self.can_play = False
                    sound.stop()
                    pygame.mixer.stop()
                    sound.flag_pole_sound.stop()
                    sound.flag_pole_sound.play()
                    player.invincibility_power = False
                    player.invincibility_time.reset()
                    sound.star_man_theme.stop()

                    if player.rect.y >= (48*11):
                        p = "100"

                    elif player.rect.y >= (48*10):
                        p = "200"

                    elif player.rect.y >= (48*9):
                        p = "400"

                    elif player.rect.y >= (48*8):
                        p = "500"

                    elif player.rect.y >= (48*7):
                        p = "800"

                    elif player.rect.y >= (48*6):
                        p = "1000"
                    
                    elif player.rect.y >= (48*5):
                        p = "2000"

                    elif player.rect.y >= (48*4):
                        p = "4000"

                    else:
                        p = "5000"

                    font.Generate_S_Point(p, self.rect.x+64, 552, "flag_point")
                    score.score += int(p)

                if self.rect.y < 516:
                    self.rect.y += int(self.walk_vel*group.time*delta_time)

                else:
                    if not player.animation.direction_x:
                        player.animation.direction_x = True
                        sound.stage_clear.stop()
                        sound.stage_clear.play()

                    if player.animation.direction_x:
                        add_time = .05
                        player.key_d_time += add_time*group.time*delta_time


    def go_up(self, delta_time):
        for letter in group.font_sprites:
            if letter.identifier == "flag_point":
                if letter.rect.y >= 144:
                    letter.rect.y -= int(self.walk_vel*group.time*delta_time)


    def update(self, delta_time):
        self.go_down(delta_time)
        self.go_up(delta_time)


class Bullet_Tile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sheet = group.tile_sheet.copy()
        self.sheet.set_clip(pygame.Rect(144, 0, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey(group.color_key)
        self.set_color_palette()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self.drop_time = group.Chronometer(3)


    def drop_bullet(self):
        if self.drop_time.time_over():
            self.drop_time.reset()
            bullet = enemy.Bullet_Bill(self.rect.x, self.rect.y+3)
            group.all_sprites.add(bullet)
            group.enemy_sprites.add(bullet)
            group.all_sprites.change_layer(bullet.animation, self._layer-1)


    def update(self, delta_time):
        if not group.stop:
            self.drop_bullet()


class Spinning_Fire_Balls_Tile(Tile):  # ( angulo, direcccion  )   ( 3, # ), (f, !)
    def __init__(self, x, y, texture, angle, direction):
        super().__init__(x, y)
        if texture[1] > 31 and texture[1] < 64:
            self.palette = palette.special_palette
            self.index = palette.special_index

        if texture[1] > 63 or texture == (48, 0):
            self.palette = palette.palette_3
        self.sheet = group.tile_sheet.copy()
        self.sheet.set_clip(pygame.Rect(texture[0], texture[1], 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey(group.color_key)
        self.set_color_palette()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        angle *= 20

        spinnnig_fire_ball = enemy.Spinning_Fire_Ball(self, 0, angle, direction)
        group.all_sprites.add(spinnnig_fire_ball)
        group.enemy_sprites.add(spinnnig_fire_ball)

        spinnnig_fire_ball = enemy.Spinning_Fire_Ball(self, 24, angle, direction)
        group.all_sprites.add(spinnnig_fire_ball)
        group.enemy_sprites.add(spinnnig_fire_ball)

        spinnnig_fire_ball = enemy.Spinning_Fire_Ball(self, 48, angle, direction)
        group.all_sprites.add(spinnnig_fire_ball)
        group.enemy_sprites.add(spinnnig_fire_ball)

        spinnnig_fire_ball = enemy.Spinning_Fire_Ball(self, 72, angle, direction)
        group.all_sprites.add(spinnnig_fire_ball)
        group.enemy_sprites.add(spinnnig_fire_ball)

        spinnnig_fire_ball = enemy.Spinning_Fire_Ball(self, 96, angle, direction)
        group.all_sprites.add(spinnnig_fire_ball)
        group.enemy_sprites.add(spinnnig_fire_ball)

        spinnnig_fire_ball = enemy.Spinning_Fire_Ball(self, 120, angle, direction)
        group.all_sprites.add(spinnnig_fire_ball)
        group.enemy_sprites.add(spinnnig_fire_ball)


class Jumping_Board_Tile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.jump_board = True
        self.can_jump   = True
        self.palette = palette.palette_1
        self.sprite_states = ((176, 64, 16, 32), (192, 73, 16, 23), (208, 80, 16, 16), (192, 73, 16, 23))
        self.frame = 0


        self.sheet = group.tile_sheet.copy()
        self.sheet.set_clip(pygame.Rect(self.sprite_states[self.frame]))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey(group.color_key)
        self.set_color_palette()
        self.image = pygame.transform.scale(self.image, ( self.sprite_states[self.frame][2]*3 , self.sprite_states[self.frame][3]*3))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self.init_bottom = self.rect.bottom

        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60


    def jump(self):
        self.can_jump = False


    def animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            if not self.can_jump:
                self.frame += 1

            if self.frame >= len(self.sprite_states):
                self.frame = 0
                self.can_jump = True

            else:
                x = self.rect.x
                self.sheet.set_clip(pygame.Rect(self.sprite_states[self.frame]))
                self.image = self.sheet.subsurface(self.sheet.get_clip())
                self.image.set_colorkey(group.color_key)
                self.set_color_palette()
                self.image = pygame.transform.scale(self.image, ( self.sprite_states[self.frame][2]*3 , self.sprite_states[self.frame][3]*3))
                self.rect = self.image.get_rect()
                self.rect.x, self.rect.bottom = x, self.init_bottom


    def update(self, delta_time):
        if not group.stop:
            self.animation()


class Platform(Tile):
    def __init__(self, x, y, texture, width, direction): # 85
        super().__init__(x, y)
        self.platform = True
        self.texture = texture
        self.direction = direction
        self.image = pygame.Surface(( width*48 , 24))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.walk_vel = 3
        self.x_velocity = 0
        self.y_velocity = 0

        self.top_y    = 0
        self.bottom_y = 0

        self.left_x  = 0
        self.right_x = 0

        self.tile_obj = No_Solid_Tile(x, y, (288, 16))
        group.all_sprites.add(self.tile_obj)
        group.background_sprites.add(self.tile_obj)

        self.mul_val = 1

        if direction == 0:
            self.x_velocity = self.walk_vel

        if direction == 1:
            self.x_velocity = self.walk_vel*-1

        if direction == 2:
            self.y_velocity = self.walk_vel
            self.right_collide = False
            self.left_collide  = False

        if direction == 3:
            self.y_velocity = self.walk_vel*-1
            self.right_collide = False
            self.left_collide  = False

        if direction == 4:
            self.top_y = self.rect.y
            self.bottom_y = self.top_y +(48*8)

            self.y_velocity = self.walk_vel
            self.right_collide = False
            self.left_collide  = False

        if direction == 5:
            self.walk_vel = 2
            self.mul_val = 5
            self.left_x  = self.tile_obj.rect.x
            self.right_x = self.left_x + (48*self.mul_val)

        if direction == 6:
            self.mul_val = 7
            self.left_x  = self.tile_obj.rect.x
            self.right_x = self.left_x + (48*self.mul_val)

        if direction == 7:
            self.walk_vel = 2
            self.mul_val = 3
            self.left_x  = self.tile_obj.rect.x
            self.right_x = self.left_x + (48*self.mul_val)


        for n in range(0, width):
            animation = Platform_Animation(self, n*48)
            group.all_sprites.add(animation)
            group.background_sprites.add(animation)


    def special_controll(self):
        if self.direction == 4:
            if self.rect.y <= self.top_y:
                self.y_velocity = self.walk_vel

            if self.rect.y >= self.bottom_y:
                self.y_velocity = self.walk_vel*-1

        if self.direction == 5 or self.direction == 6 or self.direction == 7:
            self.left_x  = self.tile_obj.rect.x
            self.right_x = self.left_x + (48*self.mul_val)


            if self.rect.x <= self.left_x:
                self.x_velocity = self.walk_vel

            if self.rect.x >= self.right_x:
                self.x_velocity = self.walk_vel*-1
        

    def update(self, delta_time):
        if not group.stop:
            self.special_controll()
            self.rect.x += int(self.x_velocity*group.time*delta_time)
            self.rect.y += int(self.y_velocity*group.time*delta_time)

            if self.rect.top > group.geometry[1]:
                self.rect.bottom = 0

            if self.rect.bottom < 0:
                self.rect.top = group.geometry[1]


class Double_Platform(Tile):
    def __init__(self, x, y, distance, sprite_object=None):
        super().__init__(x, y)
        self.platform = True
        self.double_platform = True
        self.can_roll = True
        self.is_player_up = False
        self.texture = (128, 80)
        self.image = pygame.Surface(( 3*48 , 24))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.y_velocity = 0
        self.x_velocity = 0

        self.walk_vel = 4

        for player in group.player_sprites:
            self.player = player

        self.sprite_object = sprite_object

        if self.sprite_object == None:
            tile_obj = Double_Platform(self.rect.x+(distance[0]*3), self.rect.y+(distance[1]*3), distance, self)
            group.all_sprites.add(tile_obj)
            group.tile_sprites.add(tile_obj)
            self.sprite_object = tile_obj

        for n in range(0, 3):
            animation = Platform_Animation(self, n*48)
            group.all_sprites.add(animation)
            group.background_sprites.add(animation)

        tile_obj = Rope(self)
        group.all_sprites.add(tile_obj)
        group.background_sprites.add(tile_obj)        


    def manage_velocity(self, delta_time):
        if self.player.rect.bottom+3 >= self.rect.top and self.player.rect.top < self.rect.bottom:
            if self.player.rect.left >= self.rect.left and self.player.rect.right <= self.rect.right:
                self.y_velocity = self.walk_vel
                self.is_player_up = True

        else:
            self.y_velocity = 0
            self.is_player_up = False


    def manage_movement(self, delta_time):
        if self.can_roll and self.sprite_object.can_roll:
            self.rect.y += int(self.y_velocity*group.time*delta_time)

        if self.rect.y <= 144 and not self.is_player_up:
            self.rect.y = 144
            self.can_roll = False

        else:
            self.can_roll = True


    def manage_sprite_object(self, delta_time):
        if self.can_roll and self.sprite_object.can_roll:
            self.sprite_object.rect.y += int(self.y_velocity*group.time*delta_time)*-1


    def update(self, delta_time):
        if not group.stop:
            self.manage_velocity(delta_time)
            self.manage_movement(delta_time)
            self.manage_sprite_object(delta_time)


class Platform_Animation(Tile):
    def __init__(self, sprite_object, relative_x):
        super().__init__(0, 0)
        self.sprite_object = sprite_object
        self.relative_x = relative_x
        self.sheet = group.tile_sheet.copy()
        self.sheet.set_clip(pygame.Rect(  self.sprite_object.texture + (16, 8)  ))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (48, 24))

        self.rect = self.image.get_rect()
        self.position()

        self.top_collide = False
        self.left_collide = False
        self.bottom_collide = False
        self.right_collide = False
        

    def position(self):
        self.rect.x = self.sprite_object.rect.x + self.relative_x
        self.rect.y = self.sprite_object.rect.y


    def update(self, delta_time):
        self.position()


class Rope(Tile):
    def __init__(self, sprite_object):
        super().__init__(0, 0)
        self.sprite_object = sprite_object
        self.sheet = group.tile_sheet.copy()
        self.sheet.set_clip(pygame.Rect(96, 16, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.set_color_palette()

        self.image = pygame.transform.scale(self.image, (48, self.sprite_object.rect.y-141 ))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = self.sprite_object.rect.x+(self.sprite_object.image.get_width()/3), 144

        self.top_collide = False
        self.left_collide = False
        self.bottom_collide = False
        self.right_collide = False


    def update(self, delta_time):
        self.sheet.set_clip(pygame.Rect(96, 16, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        try:
            self.image = pygame.transform.scale(self.image, (48, self.sprite_object.rect.y-141  ))
        except:
            pass
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = self.sprite_object.rect.x+(self.sprite_object.image.get_width()/3), 144


class Pipe(Tile):
    def __init__(self, x, y, texture, identifier, level_index):
        super().__init__(x, y)
        if texture[1]:
            self.pipe = True

        self.identifier = identifier
        self.level_index = level_index

        self.palette = palette.special_palette
        self.index = palette.special_index

        

        self.sheet = group.tile_sheet.copy()
        if texture[0] != 48:
            self.sheet.set_clip(pygame.Rect(texture[0], 32, 16, 16))
        else:
            self.sheet.set_clip(pygame.Rect(32, 48, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey(group.color_key)
        self.set_color_palette()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y


    def teleport(self):
        seam.Clear()
        seam.Set_Data(None, self.level_index)
        x = 0
        for row in seam.level[seam.level_index][1]:
            x = 0
            for data in row:
                if data[0:2] == "0d" and physic.convert(data[4]) == self.identifier+1:
                    seam.Load(x-2)
                    
                    break
                x += 1


class Pipe_2(Tile):
    def __init__(self, x, y, direction, identifier, level_index ):
        super().__init__(x, y)
        self.image = pygame.Surface((3, 3))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        
        self.pipe = True

        self.identifier = identifier
        self.level_index = level_index

        self.direction_1 = int(direction[0]/16)
        self.direction_2 = int(direction[1]/16)

        self.position()

        self.left_collide    = False
        self.right_collide   = False
        self.top_collide     = False
        self.bottom_collide  = False

        self.find = False


    def position(self):
        """
        if self.direction_1 == 0 or self.direction_1 == 1:
            self.rect.x += 3
        """
        pass

        if self.direction_1 == 0:
            self.rect.y += 45

        if self.direction_1 == 2:
            self.rect.x += 45
            self.rect.y += 45

        if self.direction_1 == 3:
            self.rect.x -= 45
            self.rect.y += 45


    def travel(self):
        seam.Clear()
        seam.Set_Data(None, self.level_index)
        x = 0
        for row in seam.level[seam.level_index][1]:
            x = 0
            for data in row:
                if data[0:2] == "0d" and physic.convert(data[4]) == self.identifier:
                    seam.Load(x-2)
                    self.find = True
                    
                    break
                x += 1

        if not self.find:
            seam.Load(0)


class Teleporter_Static(Tile):
    def __init__(self, x, y, x_index, level_index):
        super().__init__(x, y)
        self.teleporter = True
        self.image = pygame.Surface((group.geometry[0], 48))
        self.image.fill((0, 0, 0))

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self.x_index = x_index
        self.level_index = level_index


    def teleport(self):
        seam.Clear()
        seam.Set_Data(None, self.level_index)
        seam.Load(self.x_index-2)


class Teleporter_Move(Tile):
    def __init__(self, x, y, texture, level, level_index):
        super().__init__(x, y)
        self.image = pygame.Surface((48, 48))
        self.image.fill((0, 0, 255))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x+45, y

        self.top_collide = False
        self.left_collide = False
        self.bottom_collide = False
        self.right_collide = False

        self.level = level
        self.level_index = level_index

    def teleport(self):
        levels.level += 1

        if levels.level >= 5:
            levels.world += 1
            levels.level = 1

        seam.Clear()
        group.all_sprites.add(seam.Black_Screen())
        seam.Set_Data(levels.world_array[levels.world][levels.level], 0)
        seam.Load(0)

    def update(self, delta_time):
        self.teleport()


class Killer_Player_Tile(Tile):
    def __init__(self, x, y):
        super().__init__(0, 0)
        self.killer = True
        self.image = pygame.Surface((group.geometry[0], 48))
        self.image.fill((0, 0, 255))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y


class Spiny_Tile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.spiny = True
        self.sheet = group.tile_sheet.copy()
        self.sheet.set_clip(pygame.Rect(416, 80, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey(group.color_key)
        self.set_color_palette()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y


class Axe(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.palette = palette.palette_3
        self.sprite_states = (432, 432, 432, 432, 448, 464, 464, 448)
        self.sheet = group.tile_sheet.copy()

        self.sheet.set_clip(pygame.Rect(self.sprite_states[tile_frame], 16, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey(group.color_key)
        self.set_color_palette()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self.top_collide = False
        self.left_collide = False
        self.bottom_collide = False
        self.right_collide = False

        self.can_collide = True
        self.can_kill = False
        self.tile_list = list()
        self.kill_index = 0

        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100


    def The_Rect_X(self, x):
        return x.rect.x


    def The_Rect_Y(self, y):
        return y.rect.y*-1


    def manage_player_collide(self):
        if self.can_collide:
            player_collide = pygame.sprite.spritecollide(self, group.player_sprites, False)
            for player in player_collide:
                if player.rect.center[0] >= self.rect.left and player.rect.center[0] <= self.rect.right:
                    for tile in group.tile_sprites:
                        try:                
                            if tuple( tile.sheet.get_clip() )[0:2] == (192, 32) or tuple( tile.sheet.get_clip() )[0:2] == (64, 64):
                                self.tile_list.append(tile)
                        except:
                            pass
                    for tile in group.background_sprites:
                        try:                
                            if tuple( tile.sheet.get_clip() )[0:2] == (192, 32) or tuple( tile.sheet.get_clip() )[0:2] == (64, 64):
                                self.tile_list.append(tile)
                        except:
                            pass

                    
                    self.tile_list.sort(key=self.The_Rect_Y)
                    self.tile_list.sort(key=self.The_Rect_X)
                    self.kill_index = len(self.tile_list)-1
                    self.can_collide = False
                    self.can_kill = True
                    group.stop = True


    def kill_tiles(self):
        now = pygame.time.get_ticks()
        if now  - self.last_update > self.frame_rate:
            self.last_update = now
            if self.can_kill:
                if self.kill_index <= -1:
                    
                    for player in group.player_sprites:
                        player.auto_mode = True

                    group.stop = False
                    group.can_scroll = True
                    group.auto_scroll = True

                    pygame.mixer.stop()
                    sound.stop()

                    bow = False

                    for enemy_ in group.enemy_sprites:
                        if isinstance(enemy_, enemy.Bowser):
                            bow = True


                    if bow:
                        sound.world_clear_sound_bowser.stop()
                        sound.world_clear_sound_bowser.play()

                    else:
                        sound.world_clear_sound_simple.stop()
                        sound.world_clear_sound_simple.play()

                    self.kill()

                else:
                    sound.breakblock_sound.stop()
                    sound.breakblock_sound.play()
                    self.tile_list[self.kill_index].kill()
                    self.kill_index -= 1


    def animation(self):
        self.sheet.set_clip(pygame.Rect(self.sprite_states[tile_frame], 16, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey(group.color_key)
        self.image = pygame.transform.scale(self.image, (48, 48))


    def block_scroll(self):
        if self.rect.x <= group.geometry[0]-96 and not self.can_kill:
            group.can_scroll = False


    def update(self, delta_time):
        if not group.stop:
            self.animation()

        self.block_scroll()
        self.manage_player_collide()
        self.kill_tiles()
        

class Coin(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.palette = palette.palette_3
        self.coin = True
        self.sprite_states = (384, 384, 384, 384, 400, 416, 416, 400)

        self.sheet = group.tile_sheet.copy()

        self.sheet.set_clip(pygame.Rect(self.sprite_states[tile_frame], 16, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey(group.color_key)
        self.set_color_palette()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self.top_collide = False
        self.left_collide = False
        self.bottom_collide = False
        self.right_collide = False

    def update(self, delta_time):
        self.sheet.set_clip(pygame.Rect(self.sprite_states[tile_frame], 16, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey(group.color_key)
        self.image = pygame.transform.scale(self.image, (48, 48))


class Triple_Tile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.Surface((48, 114))
        self.image.fill((118, 134, 255))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self._layer = 0


class Block_Scroll_Tile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self, delta_time):
        if self.rect.x <= group.geometry[0]-48:
            group.can_scroll = False


class Seam_Tile(Tile):
    def __init__(self, y):
        super().__init__(0, 0)

        self.image = pygame.Surface((48, 48))
        self.image.fill((0, 0, 255))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = seam.seam+48, y

        self._layer = 2

        self.x = self.rect.x

    def update(self, delta_time):
        self.rect.x = seam.x_seam+48


class Toad(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.sheet = group.items_objects_sheet.copy()
        self.sheet.set_clip(pygame.Rect(0, 135, 19, 33))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (57, 99))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x-9, y

        self._layer = 3
        self.can_display_message = False
        self.rev = False

        self.count = 0

        self.message_1 = ("thank you!", int(group.geometry[0]/2)-120, 216, (255, 255, 255), "screen")
        self.message_2 = (          "", int(group.geometry[0]/2)-120, 216, (255, 255, 255), "screen")

        self.time_to_display = group.Chronometer(2)
        self.time_to_display.time = 0

        self.time_to_change = group.Chronometer(2)

        for player in group.player_sprites:
            self.player = player


    def display_message(self):
        if self.can_display_message and not group.can_scroll:
            if self.time_to_display.time_over():
                self.count += 1
                font.Generate_Message(*self.message_1)
                font.Generate_Message(*self.message_2)

                self.message_1 = ("but our princess is in", int(group.geometry[0]/2)-264, 288, (255, 255, 255), "screen")
                self.message_2 = ("another castle!"       , int(group.geometry[0]/2)-264, 336, (255, 255, 255), "screen")

                self.time_to_display.reset()

                if self.count >= 2:
                    self.can_display_message = False


    def block_scroll(self):
        if self.rect.x <= group.geometry[0]-384-9:
            group.auto_scroll = False
            group.can_scroll  = False

            if not bool(int(pygame.mixer.get_busy())) and self.time_to_change.time_over():
                levels.level += 1

                if levels.level >= 4:
                    levels.world += 1
                    levels.level = 0

                seam.Clear()
                group.all_sprites.add(seam.Black_Screen())
                seam.Set_Data(levels.world_array[levels.world][levels.level], 0)
                seam.Load(0)


    def update(self, delta_time):
        if not group.stop:
            if self.player.auto_mode and self.player.right_collision[0] and not self.rev:
                self.can_display_message = True
                self.rev = True

            self.display_message()
            self.block_scroll()
                

class Peach_Princess(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.can_display_message = False
        self.can_play_music      = True

        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150

        self.normal_states = (125, 8, 16, 24)
        self.speak_states  = (109, 8, 16, 24)
        self.walk_states   = ( 93, 8, 16, 24)

        self.sprite_states = [ self.normal_states, self.normal_states  ]

        self.sheet = group.peach_sheet.copy()
        self.controll_states()
        self.animation()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y+27

        self._layer = 3
        
        self.rev = False
        self.count = 0

        self.message_1 = ("thank you!", int(group.geometry[0]/2)-120, 216, (255, 255, 255), "screen")
        self.message_2 = (          "", int(group.geometry[0]/2)-120, 216, (255, 255, 255), "screen")

        self.time_to_display = group.Chronometer(2)
        self.time_to_display.time = 0

        self.time_to_change = group.Chronometer(2)

        for player in group.player_sprites:
            self.player = player


    def display_message(self):
        if self.can_display_message and not group.can_scroll:
            if self.time_to_display.time_over():
                self.count += 1
                font.Generate_Message(*self.message_1)
                font.Generate_Message(*self.message_2)

                #self.message_1 = ("but our princess is in", int(group.geometry[0]/2)-264, 288, (255, 255, 255), "screen")
                self.message_1 = ("i hope that you really  ", int(group.geometry[0]/2)-264, 288, (255, 255, 255), "screen")
                #self.message_2 = ("another castle!"       , int(group.geometry[0]/2)-264, 336, (255, 255, 255), "screen")
                self.message_2 = ("enjoyed this fan made .D"      , int(group.geometry[0]/2)-264, 336, (255, 255, 255), "screen")
            
                self.time_to_display.reset()

                if self.count >= 2:
                    self.can_display_message = False
                    font.Generate_Message("                      . "      , int(group.geometry[0]/2)-264, 318, (255, 255, 255), "screen" )
                    

    def block_scroll(self):
        if self.rect.x <= group.geometry[0]-384-9:
            group.auto_scroll = False
            group.can_scroll  = False

            if not bool(int(pygame.mixer.get_busy())) and self.time_to_change.time_over():
                """
                levels.level += 1

                if levels.level >= 4:
                    levels.world += 1
                    levels.level = 0

                seam.Clear()
                group.all_sprites.add(seam.Black_Screen())
                seam.Set_Data(levels.world_array[levels.world][levels.level], 0)
                seam.Load(0)
                """
                if self.can_play_music:
                    sound.end_sound.stop()
                    sound.end_sound.play(-1)
                    self.can_play_music = False


    def controll_states(self):
        if self.can_display_message and not group.can_scroll:
            self.sprite_states[1] = self.speak_states

        elif not self.can_play_music:
            self.sprite_states[1] = self.normal_states


    def animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now

            self.frame += 1
            if self.frame >= len(self.sprite_states):
                self.frame = 0

        self.sheet.set_clip(pygame.Rect(  self.sprite_states[self.frame] ))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (48, 72))


    def update(self, delta_time):
        if not group.stop:
            self.controll_states()
            self.animation()
            if self.player.auto_mode and self.player.right_collision[0] and not self.rev:
                self.can_display_message = True
                self.rev = True

            self.display_message()
            self.block_scroll()
                
