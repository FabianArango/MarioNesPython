import pygame
from pygame.locals import *
pygame.init()

from script import group, physic, palette, tile, font, sound, seam

enemy_frame = 0
enemy_last_update = pygame.time.get_ticks()
enemy_frame_rate = 150

hammer_frame = 0



def Global_Enemy_Frame():
    global enemy_frame, enemy_last_update, enemy_frame_rate, hammer_frame
    if not group.stop:
        now = pygame.time.get_ticks()
        if now - enemy_last_update > enemy_frame_rate:
            enemy_last_update = now
            enemy_frame += 1
            hammer_frame += 1
            if enemy_frame >= 2:
                enemy_frame = 0
            
            if hammer_frame >= 4:
                hammer_frame = 0

        
class Animation_Player(pygame.sprite.Sprite): #
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.sheet = group.player_sheet.copy()
        self.sheet.set_clip(pygame.Rect(80, 34, 16, 16)) 
        
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.data_iamge = ( (48, 48), 32, 16, 16)
        
        self.rect = self.image.get_rect()

        self.position()

        
        self._layer = 6

        self.direction_x = False
        self.can_drop_fireball = True

        self.visibility = True

        # states -----------------------------------------------------------
        self.static_states = ( 0, ) ###

        self.walk_states = ( 16,  32,  48, 32) ###

        self.skiding_states = ( 64, ) ###

        self.jump_states = ( 80, ) ###

        self.crouched_down_states = ( 96, ) ###

        self.static_climb_states = ( 112, ) ###

        self.climb_states = ( 112, 128 ) ###

        self.swim_states = ( 144, 160 ) ###

        self.swim_jump_states = ( 176, 192, 208, 224 ) ###

        self.fire_static_states = (256, ) ###

        self.fire_walk_states = ( 256, 272, 288, 272 ) ###

        self.fire_skiding_states = (304, )

        self.fire_jump_states = (320, ) ###

        self.resize()

        self.sprite_states = self.static_states

        # palette ----------------------------------------------------------------------
        self.mario_palette = (  ( (174,  47,  40), (231, 156,  33), (106, 107,   4) ), )
        self.luigi_palette = (  ( (255, 255, 255), (231, 156,  33), (36 , 151,   0) ), )

        

        #self.fire_palette  = (  ( (247, 214, 164), (231, 156,  33), (174,  47,  40) ), )
        self.fire_palette  = (  ( (255, 206, 198), (231, 156,  33), (174,  47,  40) ), )

        self.invincibility_palette = (  
                                ( palette.palette_1[palette.index][4], palette.palette_1[palette.index][5], palette.palette_1[palette.index][3] ),
                                ( palette.palette_2[palette.index][4], palette.palette_2[palette.index][5], palette.palette_2[palette.index][3] ), 
                                ( palette.palette_1[palette.index][2], palette.palette_1[palette.index][1], palette.palette_1[palette.index][0] ),
                                self.mario_palette[0] 
                             )

        self.no_visible_palette = (  ( (0,  0,  0), (0, 0, 0), (0, 0, 0) ), )

        self.damaged_palette    = ( self.no_visible_palette[0], self.no_visible_palette[0], self.mario_palette[0], self.mario_palette[0] )

        if self.sprite_object.name == "mario":
            self.paltte = self.mario_palette

        if self.sprite_object.name == "luigi":
            self.paltte = self.luigi_palette

        else:
            self.paltte = self.mario_palette

        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100

        self.color_frame = 0
        self.color_last_update = pygame.time.get_ticks()
        self.color_frame_rate = 80


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        """
        if not self.sprite_object.is_crouched_down:
            if self.sprite_object.size:
                self.rect.y = self.sprite_object.rect.y-6

            if not self.sprite_object.size:
                self.rect.y = self.sprite_object.rect.y-3

        else:
            self.rect.y = self.sprite_object.rect.y-51
        """
        self.rect.bottom = self.sprite_object.rect.bottom+3


    def direction_in_x_axis(self):
        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) < 0:
            self.direction_x = True

        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) > 0:
            self.direction_x = False


    def controll_color_palette(self):
        if self.sprite_object.invincibility_time.time <= 2.5:
            self.color_frame_rate = 130

        else:
            self.color_frame_rate = 80

        if self.visibility:
            if self.sprite_object.not_damage_time.time_over():
                if not self.sprite_object.invincibility_power:
                    if not self.sprite_object.fire_power:
                        if self.sprite_object.name == "mario":
                            self.paltte = self.mario_palette
                            self.damaged_palette    = ( self.no_visible_palette[0], self.no_visible_palette[0], self.mario_palette[0], self.mario_palette[0] )

                        if self.sprite_object.name == "luigi":
                            self.paltte = self.luigi_palette
                            self.damaged_palette    = ( self.no_visible_palette[0], self.no_visible_palette[0], self.luigi_palette[0], self.luigi_palette[0] )

                        else:
                            self.paltte = self.mario_palette

                    else:
                        self.paltte = self.fire_palette

                else:
                    self.invincibility_palette = (  
                                        ( palette.palette_1[palette.index][4], palette.palette_1[palette.index][5], palette.palette_1[palette.index][3] ),
                                        ( palette.palette_2[palette.index][4], palette.palette_2[palette.index][5], palette.palette_2[palette.index][3] ), 
                                        ( palette.palette_1[palette.index][2], palette.palette_1[palette.index][1], palette.palette_1[palette.index][0] ),
                                        self.mario_palette[0] 
                                    )
                    self.paltte = self.invincibility_palette

            else:
                self.paltte = self.damaged_palette

        else:
            self.paltte = self.no_visible_palette


    def controll_states(self):
        self.frame_rate = 90 - ( abs(int(self.sprite_object.left_velocity) + int(self.sprite_object.right_velocity) ) **2 )
        if self.sprite_object.handle_mode == 0:
            if not self.sprite_object.KEY_S:
                if self.sprite_object.bottom_collision[0]:
                    if int(self.sprite_object.left_velocity) == 0 and int(self.sprite_object.right_velocity) == 0:
                        if not self.sprite_object.fire_power:
                            self.sprite_states = self.static_states

                        else:
                            if self.can_drop_fireball and self.sprite_object.KEY_K:
                                self.sprite_states = self.fire_static_states

                            else:
                                self.sprite_states = self.static_states


                    if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) != 0:
                        if not self.direction_x:
                            if not bool( int(self.sprite_object.left_velocity) ) :
                                if not self.sprite_object.fire_power:
                                    self.sprite_states = self.walk_states
                                else:
                                    if self.can_drop_fireball and self.sprite_object.KEY_K:
                                        self.sprite_states = self.fire_walk_states

                                    else:
                                        self.sprite_states = self.walk_states
                                        
                            else:
                                if not bool( self.sprite_object.left_MAX_VEL  ):
                                    if not self.sprite_object.fire_power:
                                        self.sprite_states = self.walk_states

                                    else:
                                        if self.can_drop_fireball and self.sprite_object.KEY_K:
                                            self.sprite_states = self.fire_walk_states
                                            
                                        else:
                                            self.sprite_states = self.walk_states
                                    

                                else:
                                    self.sprite_states = self.skiding_states

                        if self.direction_x:
                            if not bool( int(self.sprite_object.right_velocity) ):
                                if not self.sprite_object.fire_power:
                                    self.sprite_states = self.walk_states

                                else:
                                    if self.can_drop_fireball and self.sprite_object.KEY_K:
                                        self.sprite_states = self.fire_walk_states

                                    else:
                                        self.sprite_states = self.walk_states

                            else:
                                if not bool( self.sprite_object.right_MAX_VEL  ):
                                    if not self.sprite_object.fire_power:
                                        self.sprite_states = self.walk_states

                                    else:
                                        if self.can_drop_fireball and self.sprite_object.KEY_K:
                                            self.sprite_states = self.fire_walk_states

                                        else:
                                            self.sprite_states = self.walk_states

                                else:
                                    self.sprite_states = self.skiding_states

                else:
                    if self.sprite_object.wather:
                        if self.sprite_object.KEY_L:
                            self.sprite_states = self.swim_jump_states

                        if not self.sprite_object.KEY_L:
                            self.sprite_states = self.swim_states

                    if not self.sprite_object.wather:
                        if not self.sprite_object.can_jump:
                            if not self.sprite_object.fire_power:
                                self.sprite_states = self.jump_states

                            else:
                                if self.can_drop_fireball and self.sprite_object.KEY_K:
                                    self.sprite_states = self.fire_jump_states

                                else:
                                    self.sprite_states = self.jump_states

            else:
                if self.sprite_object.wather:
                    if self.sprite_object.bottom_collision[0]:
                        self.sprite_states = self.crouched_down_states

                    if not self.sprite_object.bottom_collision[0]:
                        if self.sprite_object.KEY_L:
                            self.sprite_states = self.swim_jump_states

                        else:
                            self.sprite_states = self.swim_states

                if not self.sprite_object.wather:
                    self.sprite_states = self.crouched_down_states


        if self.sprite_object.handle_mode == 1:
            if int(self.sprite_object.top_velocity + self.sprite_object.bottom_velocity) != 0 and not self.sprite_object.auto_mode:
                self.sprite_states = self.climb_states
            else:
                self.sprite_states = self.static_climb_states


    def animation_rate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:           
            self.last_update = now
            self.frame += 1

            if not self.sprite_object.KEY_K:
                self.can_drop_fireball = True

            elif self.can_drop_fireball and self.sprite_object.KEY_K and bool(int(self.sprite_object.can_drop_fireball+.5)):
                self.can_drop_fireball = False

    
    def palette_rate(self):
        now = pygame.time.get_ticks()
        if now - self.color_last_update > self.color_frame_rate:
            self.color_last_update = now
            self.color_frame += 1
          

    def animation(self):
        if self.color_frame >= len(self.paltte):
            self.color_frame = 0

        if self.frame >= len(self.sprite_states):
            self.frame = 0
        
        self.sheet = group.player_sheet.copy()
        self.sheet.set_clip(pygame.Rect( self.sprite_states[self.frame],  self.data_iamge[1], self.data_iamge[2], self.data_iamge[3]  )) 
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0, 0))

        self.image_pixel_array = pygame.PixelArray(self.image)
        self.image_pixel_array.replace(self.mario_palette[0][0], self.paltte[self.color_frame][0])
        self.image_pixel_array.replace(self.mario_palette[0][1], self.paltte[self.color_frame][1])
        self.image_pixel_array.replace(self.mario_palette[0][2], self.paltte[self.color_frame][2])

        self.image = pygame.transform.scale(self.image, self.data_iamge[0])
        if self.sprite_states != self.skiding_states:
            self.image = pygame.transform.flip(self.image, self.direction_x, False)

        else:
            if self.direction_x:
                self.image = pygame.transform.flip(self.image, False, False)

            if not self.direction_x:
                self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.position()


    def resize(self, animation=True):
        if self.sprite_object.size:
            self.data_iamge = ( (48, 96), 0, 16, 32)

        if not self.sprite_object.size:
            self.data_iamge = ( (48, 48), 32, 16, 16)


    def set_visibility(self, val_bool):
        self.visibility = val_bool


    def update_animation(self):
        self.direction_in_x_axis()      
        self.controll_states()
        self.controll_color_palette()
        self.animation_rate()
        self.palette_rate()
        self.animation()


class Power_up_transformation(pygame.sprite.Sprite): #
    def __init__(self, sprite_object, power_up):
        super().__init__()
        self.sprite_object = sprite_object
        self.sprite_object.set_visibility(False)
        group.stop = True
        
        self.up_states = ( 
                                (0, 32, 16, 16), (240, 0, 16, 32), (0, 32, 16, 16), 
                                (240, 0, 16, 32), (0, 32, 16, 16), (240, 0, 16, 32), 
                                (0, 32, 16, 16), (0, 32, 16, 16), (0, 0, 16, 32), 
                                (0, 32, 16, 16), (0, 0, 16, 32)
                              )

        self.down_states = self.up_states[::-1]

        self.fire_states = list()

        s = (self.sprite_object.sprite_states[self.sprite_object.frame], self.sprite_object.data_iamge[1], self.sprite_object.data_iamge[2], self.sprite_object.data_iamge[3])

        for n in range(11):
            self.fire_states.append(s)
        
        if power_up == 0:
            self.sprite_states = self.up_states
            self.paltte = self.sprite_object.paltte

        if power_up == 1:
            self.sprite_states = self.down_states
            self.paltte = self.sprite_object.paltte

        if power_up == 2:
            self.sprite_states = self.fire_states 
            """
            self.paltte = list(self.sprite_object.invincibility_palette)
            self.paltte[3] = self.sprite_object.fire_palette[0]
            self.paltte = self.paltte[::-1]
            self.paltte = tuple(self.paltte)
            """
            self.paltte = (  
                                         ( palette.palette_1[palette.index][4], palette.palette_1[palette.index][5], palette.palette_1[palette.index][3] ),
                                         ( palette.palette_2[palette.index][4], palette.palette_2[palette.index][5], palette.palette_2[palette.index][3] ), 
                                         ( palette.palette_1[palette.index][2], palette.palette_1[palette.index][1], palette.palette_1[palette.index][0] ),
                                         ( (255, 206, 198), (231, 156,  33), (174,  47,  40) )
                                         )
            


        self.sheet = group.player_sheet.copy()
        self.sheet.set_clip(pygame.Rect(self.sprite_states[0]))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (self.sprite_states[0][2]*3, self.sprite_states[0][3]*3) )
        self.rect = self.image.get_rect()
        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom

        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 80

        self.color_frame = 0
        self.color_last_update = pygame.time.get_ticks()
        self.color_frame_rate = self.sprite_object.color_frame_rate

        self._layer = self.sprite_object._layer-2


    def animation_rate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1


    def palette_rate(self):
        now = pygame.time.get_ticks()
        if now - self.color_last_update > self.color_frame_rate:
            self.color_last_update = now
            self.color_frame += 1


    def animation(self):
        if self.frame >= len(self.sprite_states):
            self.sprite_object.set_visibility(True)
            group.stop = False
            self.kill()
    
        else:
            if self.color_frame >= len(self.paltte):
                self.color_frame = 0

            self.sheet = group.player_sheet.copy()
            self.sheet.set_clip(pygame.Rect(self.sprite_states[self.frame]))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.image.set_colorkey((0, 0, 0))
            self.image_pixel_array = pygame.PixelArray(self.image)
            self.image_pixel_array.replace(self.sprite_object.mario_palette[0][0], self.paltte[self.color_frame][0])
            self.image_pixel_array.replace(self.sprite_object.mario_palette[0][1], self.paltte[self.color_frame][1])
            self.image_pixel_array.replace(self.sprite_object.mario_palette[0][2], self.paltte[self.color_frame][2])
            self.image = pygame.transform.scale(self.image, (self.sprite_states[self.frame][2]*3, self.sprite_states[self.frame][3]*3) )
            self.image = pygame.transform.flip(self.image, self.sprite_object.direction_x, False)
            self.rect = self.image.get_rect()
            self.position()


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom


    def update(self, delta_time):
        self.animation_rate()
        self.palette_rate()
        self.animation()


class Animation_Pipe(pygame.sprite.Sprite): #
    def __init__(self, sprite_object, pipe):
        super().__init__()
        group.stop = True
        self.sprite_object = sprite_object
        self.sprite_object.animation.set_visibility(False)
        self.pipe = pipe
        self.stade = False
        """
        self.image = pygame.Surface((48, 96))
        self.image.fill((255, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        """
        
        self.sheet = group.player_sheet.copy()

        self.sheet.set_clip(pygame.Rect( (0, )+ self.sprite_object.animation.data_iamge[1:4]  ))
        self.image = self.sheet.subsurface( self.sheet.get_clip() )

        self.palette = self.sprite_object.animation.paltte

        self.image.set_colorkey((0, 0, 0))

        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace( (174,  47,  40), self.palette[self.sprite_object.animation.color_frame][0] )
        self.image_pixel_array.replace( (231, 156,  33), self.palette[self.sprite_object.animation.color_frame][1] )
        self.image_pixel_array.replace( (106, 107,   4), self.palette[self.sprite_object.animation.color_frame][2] )

        self.image = pygame.transform.scale( self.image, (self.sprite_object.animation.data_iamge[2]*3, self.sprite_object.animation.data_iamge[3]*3   )  )
        self.image = pygame.transform.flip(  self.image, self.sprite_object.animation.direction_x, False)

        self.rect = self.image.get_rect()

        self.walk_vel = 2
        self.set_velocity_1()

        self._layer = self.pipe._layer-1

        self.wait_time = group.Chronometer_Continuous(1.3)


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom+3


    def set_velocity_1(self):
        sound.pipe_sound.stop()
        sound.pipe_sound.play()
        self.position()
        if self.pipe.direction_1 == 0:
            self.x_vel = 0
            self.y_vel = self.walk_vel

        if self.pipe.direction_1 == 1:
            self.x_vel = 0
            self.y_vel = self.walk_vel*-1

        if self.pipe.direction_1 == 2:
            self.x_vel = self.walk_vel
            self.y_vel = 0

        if self.pipe.direction_1 == 3:
            self.x_vel = self.walk_vel*-1
            self.y_vel = 0


    def set_velocity_2(self):
        if not self.stade:
            sound.pipe_sound.stop()
            sound.pipe_sound.play()
            self.pipe.travel()
            self.position()
            
            if self.pipe.direction_2 == 0:
                self.rect.top = self.sprite_object.rect.bottom
                self.x_vel = 0
                self.y_vel = self.walk_vel*-1

            if self.pipe.direction_2 == 1:
                self.rect.bottom = self.sprite_object.rect.top
                self.x_vel = 0
                self.y_vel = self.walk_vel

            if self.pipe.direction_2 == 2:
                self.rect.left = self.sprite_object.rect.right
                self.x_vel = self.walk_vel*-1
                self.y_vel = 0

            if self.pipe.direction_2 == 3:
                self.rect.right = self.sprite_object.rect.left
                self.x_vel = self.walk_vel
                self.y_vel = 0

            if self.pipe.direction_2 == 4:
                sound.pipe_sound.stop()
                self.rect.right = self.sprite_object.rect.right
                self.x_vel = self.walk_vel
                self.y_vel = 0

            self.stade = True

        elif self.stade:
            group.stop = False
            self.sprite_object.animation.set_visibility(True)
            self.kill()


    def manage_movement(self, delta_time):
        self.rect.x += int(self.x_vel*group.time*delta_time)
        self.rect.y += int(self.y_vel*group.time*delta_time)

        if not self.stade:
            if self.rect.top > self.sprite_object.animation.rect.bottom or self.rect.bottom < self.sprite_object.animation.rect.top:
                self.x_vel = 0
                self.y_vel = 0
                if self.wait_time.time_over():
                    self.set_velocity_2()

            elif self.rect.left > self.sprite_object.animation.rect.right or self.rect.right < self.sprite_object.animation.rect.left:
                self.x_vel = 0
                self.y_vel = 0
                if self.wait_time.time_over():
                    self.set_velocity_2()

        else:
            if (self.rect.top < self.sprite_object.animation.rect.top and self.y_vel < 0 ) or (self.rect.bottom > self.sprite_object.animation.rect.bottom and self.y_vel > 0):
                self.set_velocity_2()
        
            elif (self.rect.left < self.sprite_object.animation.rect.left and self.x_vel < 0) or (self.rect.right > self.sprite_object.animation.rect.right and self.x_vel > 0):
                self.set_velocity_2()


    def animation(self):
        self.frame = self.sprite_object.animation.frame
        self.sheet.set_clip(pygame.Rect(  (self.sprite_object.animation.sprite_states[self.frame],  ) + self.sprite_object.animation.data_iamge[1:4]  ))
        self.image = self.sheet.subsurface( self.sheet.get_clip() )
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale( self.image, (self.sprite_object.animation.data_iamge[2]*3, self.sprite_object.animation.data_iamge[3]*3   )  )
        self.image = pygame.transform.flip(  self.image, self.sprite_object.animation.direction_x, False)


    def update(self, delta_time):
        self.manage_movement(delta_time)
        self.animation()


class Animation_Magic_Mushroom(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.sheet = group.items_objects_sheet.copy()
    
        self.sheet.set_clip(pygame.Rect(0, 16, 16, 16)) 
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (48, 48))

        self.rect = self.image.get_rect()
        self.rect.center = self.sprite_object.rect.center
        self.rect.y = self.sprite_object.rect.y

        self._layer = self.sprite_object.sprite_object._layer-1

    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.y = self.sprite_object.rect.y

    def update_animation(self):
        self.position()


class Animation_One_Up_Mushroom(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.sheet = group.items_objects_sheet.copy()
    
        self.sheet.set_clip(pygame.Rect(16, 16, 16, 16)) 
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.image_pixel_array = pygame.PixelArray(self.image)
        self.image_pixel_array.replace(palette.palette_1[0][3], palette.palette_1[palette.index][3])
        self.image_pixel_array.replace(palette.palette_1[0][4], palette.palette_1[palette.index][4])
        self.image_pixel_array.replace(palette.palette_1[0][5], palette.palette_1[palette.index][5])

        self.image = pygame.transform.scale(self.image, (48, 48))

        self.rect = self.image.get_rect()
        self.rect.center = self.sprite_object.rect.center
        self.rect.y = self.sprite_object.rect.y

        self._layer = self.sprite_object.sprite_object._layer-1

    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.y = self.sprite_object.rect.y

    def update_animation(self):
        self.position()


class Animation_Fire_Flower(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.sheet = group.items_objects_sheet.copy()
        self.sheet.set_clip(pygame.Rect(0, 32, 16, 16)) 
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace(palette.palette_1[0][0], palette.palette_1[palette.index][0])
        self.image_pixel_array.replace(palette.palette_1[0][1], palette.palette_1[palette.index][1])
        self.image_pixel_array.replace(palette.palette_1[0][2], palette.palette_1[palette.index][2])
        self.image_pixel_array.replace(palette.palette_1[0][3], palette.palette_1[palette.index][3])
        self.image_pixel_array.replace(palette.palette_1[0][4], palette.palette_1[palette.index][4])
        self.image_pixel_array.replace(palette.palette_1[0][5], palette.palette_1[palette.index][5])
    
        self.image = pygame.transform.scale(self.image, (48, 48))

        self.rect = self.image.get_rect()

        self.rect.center = self.sprite_object.rect.center
        self.rect.y = self.sprite_object.rect.y

        self._layer = self.sprite_object.sprite_object._layer-1

        self.sprite_states = (0, 16, 32, 48)

        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 80


    def animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1

            if self.frame >= len(self.sprite_states):
                self.frame = 0

            self.sheet.set_clip(pygame.Rect(self.sprite_states[self.frame], 32, 16, 16)) 
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.image.set_colorkey((0, 0, 0))
            self.image = pygame.transform.scale(self.image, (48, 48))


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.y = self.sprite_object.rect.y

    
    def update_animation(self):
        self.animation()
        self.position()


class Animation_Star_Man(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.sheet = group.items_objects_sheet.copy()

        self.sheet.set_clip(pygame.Rect(0, 48, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace(palette.palette_1[0][0], palette.palette_1[palette.index][0])
        self.image_pixel_array.replace(palette.palette_1[0][2], palette.palette_1[palette.index][2])
        self.image_pixel_array.replace(palette.palette_1[0][3], palette.palette_1[palette.index][3])
        self.image_pixel_array.replace(palette.palette_1[0][4], palette.palette_1[palette.index][4])

        self.image = pygame.transform.scale(self.image, (48, 48))

        self.rect = self.image.get_rect()

        self.rect.center = self.sprite_object.rect.center
        self.rect.y = self.sprite_object.rect.y

        self._layer = self.sprite_object.sprite_object._layer -1

        self.sprite_states = (0, 16, 32, 48)

        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 90

    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.y = self.sprite_object.rect.y


    def animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1

            if self.frame >= len(self.sprite_states):
                self.frame = 0

            self.sheet.set_clip(pygame.Rect(self.sprite_states[self.frame], 48, 16, 16))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.image.set_colorkey((0, 0, 0))
            self.image = pygame.transform.scale(self.image, (48, 48))

    def update_animation(self):
        self.position()
        self.animation()


class Animation_Poison_Mushroom(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.sheet = group.items_objects_sheet.copy()
    
        self.sheet.set_clip(pygame.Rect(32, 16, 16, 16)) 
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image_pixel_array = pygame.PixelArray(self.image)
        self.image_pixel_array.replace(palette.palette_1[0][0], palette.palette_1[palette.index][0])
        self.image_pixel_array.replace(palette.palette_1[0][1], palette.palette_1[palette.index][1])
        self.image_pixel_array.replace(palette.palette_1[0][2], palette.palette_1[palette.index][2])
        self.image = pygame.transform.scale(self.image, (48, 48))

        self.rect = self.image.get_rect()
        self.rect.center = self.sprite_object.rect.center
        self.rect.y = self.sprite_object.rect.y

        self._layer = self.sprite_object.sprite_object._layer-1

    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.y = self.sprite_object.rect.y

    def update_animation(self):
        self.position()


class Coin_jump_animation(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_states = (464, 480, 496, 512)
        self.sheet = group.tile_sheet.copy()

        self.sheet.set_clip(pygame.Rect(self.sprite_states[0], 0, 16, 16)) 
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (48, 48))
        
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self._layer = 3

        self.Y_Y = y

        self.bottom_velocity = -24
        self.gravity = group.gravity_in_down_GRASS


        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60


    def animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:           
            self.last_update = now
            self.frame += 1

            if self.frame >= len(self.sprite_states):
                self.frame = 0

            self.sheet.set_clip(pygame.Rect(self.sprite_states[self.frame], 0, 16, 16)) 
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.image.set_colorkey((0, 0, 0))
            self.image = pygame.transform.scale(self.image, (48, 48))


    def manage_velocity(self, delta_time):
        self.bottom_velocity = physic.Accelearted_Linear_Movement(self.bottom_velocity, delta_time, 12, self.gravity, .01, True)


    def update(self, delta_time):
        self.manage_velocity(delta_time)
        self.rect.y += int(self.bottom_velocity+group.time*delta_time)

        if self.rect.y > self.Y_Y:
            font.Generate_Point("200", self.rect.x+3, self.rect.y)
            self.kill()

        self.animation()


class Coin_Display_Animation(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_states = (0, 0, 0, 0, 8, 16, 16, 8)
        self.sheet = group.items_objects_sheet.copy()

        self.sheet.set_clip(pygame.Rect(self.sprite_states[tile.tile_frame], 112, 8, 8)) 
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace(palette.palette_3[0][0], palette.palette_3[palette.index][0])
        self.image_pixel_array.replace(palette.palette_3[0][1], palette.palette_3[palette.index][1])
        self.image_pixel_array.replace(palette.palette_3[0][2], palette.palette_3[palette.index][2])
        self.image = pygame.transform.scale(self.image, (24, 24))
        
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self._layer = 5


    def update(self, delta_time):
        self.sheet.set_clip(pygame.Rect(self.sprite_states[tile.tile_frame], 112, 8, 8)) 
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (24, 24))


class Death_Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_object, states, rate, *args):
        super().__init__()
        self.sprite_object = sprite_object
        self.sprite_states = states
        self.sheet = self.sprite_object.sheet.copy()

        self.sheet.set_clip(pygame.Rect(self.sprite_states[0]))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.image = pygame.transform.scale(self.image, (self.sprite_states[0][2]*3, self.sprite_states[0][3]*3))

        self.rect = self.image.get_rect()
        self.rect.center = args

        self._layer = 3

        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = rate


    def update(self, delta_time):
        if not group.stop:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame >= len(self.sprite_states):
                    self.kill()

                else:
                    self.sheet.set_clip(pygame.Rect(self.sprite_states[self.frame]))
                    self.image = self.sheet.subsurface(self.sheet.get_clip())
                    self.image.set_colorkey((0, 0, 0))
                    self.image = pygame.transform.scale(self.image, (self.sprite_states[self.frame][2]*3, self.sprite_states[self.frame][3]*3))


class Death_Jump(pygame.sprite.Sprite):
    def __init__(self, sprite_object, states, direction, force):
        super().__init__()
        self.sprite_states = states
        self.sprite_object = sprite_object
        self.direction = direction

        self.sheet = self.sprite_object.sheet.copy()
        self.sheet.set_clip(pygame.Rect(self.sprite_states)) 
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.image = pygame.transform.scale(self.image, (self.sprite_states[2]*3, self.sprite_states[3]*3))
        self.image = pygame.transform.flip(self.image, self.direction[0], self.direction[1])
        self.rect = self.image.get_rect()

        self.rect.center = self.sprite_object.rect.center

        self._layer = 3

        self.bottom_velocity = force
        self.gravity = 0

        self.gravity_in_down = group.gravity_in_down_GRASS
        self.gravity_in_up   = group.gravity_in_up_GRASS
 

        if self.direction[0]:
            self.x_velocity = -3

        if not self.direction[0]:
            self.x_velocity = 3

    def manage_velocity(self, delta_time):
        if self.bottom_velocity < 0:
            self.gravity = self.gravity_in_up

        if self.bottom_velocity >= 0:
            self.gravity = self.gravity_in_down

        self.bottom_velocity = physic.Accelearted_Linear_Movement(self.bottom_velocity, delta_time, 12, self.gravity, .01, True)

    def update(self, delta_time):
        if not group.stop:
            self.manage_velocity(delta_time)
            self.rect.x += int(self.x_velocity*group.time*delta_time)

            self.rect.y += int(self.bottom_velocity*group.time*delta_time)

            if self.rect.right < 0:
                self.kill()

            if self.rect.y > group.geometry[1]:
                self.kill()


class Player_Death_Jump(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        sound.player_die_sound.stop()
        sound.player_die_sound.play()

        group.stop = True
        self.sprite_object = sprite_object
        self.sprite_object.animation.set_visibility(False)
        self.sprite_states = (240, 32, 16, 16)

        self.sheet = self.sprite_object.animation.sheet.copy()
        self.sheet.set_clip(pygame.Rect(self.sprite_states)) 
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        if self.sprite_object.name == "luigi":
            self.image_pixel_array = pygame.PixelArray(self.image)
            self.image_pixel_array.replace(self.sprite_object.animation.mario_palette[0][0], self.sprite_object.animation.paltte[0][0])
            self.image_pixel_array.replace(self.sprite_object.animation.mario_palette[0][1], self.sprite_object.animation.paltte[0][1])
            self.image_pixel_array.replace(self.sprite_object.animation.mario_palette[0][2], self.sprite_object.animation.paltte[0][2])

        self.image = pygame.transform.scale(self.image, (self.sprite_states[2]*3, self.sprite_states[3]*3))
        self.rect = self.image.get_rect()

        self.rect.center = self.sprite_object.rect.center

        self._layer = 3

        self.bottom_velocity = -12
        self.gravity = 0

        self.gravity_in_down = group.gravity_in_down_GRASS
        self.gravity_in_up   = group.gravity_in_up_GRASS

        self.wait_time = group.Chronometer_Continuous(.6)
 
    def manage_velocity(self, delta_time):
        if self.wait_time.time_over():
            if self.bottom_velocity < 0:
                self.gravity = self.gravity_in_up

            if self.bottom_velocity > 0:
                self.gravity = self.gravity_in_down

            self.bottom_velocity = physic.Accelearted_Linear_Movement(self.bottom_velocity, delta_time, 12, self.gravity, -.01, True)

            self.rect.y += int(self.bottom_velocity*group.time*delta_time)

    def update(self, delta_time):
        self.manage_velocity(delta_time)
        if self.rect.y > group.geometry[1]+1152:
            group.stop = False
            self.sprite_object.animation.set_visibility(True)
            seam.Clear()
            group.all_sprites.add(seam.Black_Screen())
            seam.Set_Data(None, self.sprite_object.re_appear_index)
            seam.Load(0)
            self.kill()


class Break_Tile_Explosion(object):
    def __init__(self, sprite_object):
        self.sprite_object = sprite_object

        self.force = -12

        brick = Death_Jump(self.sprite_object, (448, 0, 8, 8), (False, False), self.force)
        group.all_sprites.add(brick)
        group.death_sprites.add(brick)

        brick = Death_Jump(self.sprite_object, (448, 0, 8, 8), (True, False), self.force)
        group.all_sprites.add(brick)
        group.death_sprites.add(brick)

        brick = Death_Jump(self.sprite_object, (448, 8, 8, 8), (False, True), self.force/2)
        group.all_sprites.add(brick)
        group.death_sprites.add(brick)

        brick = Death_Jump(self.sprite_object, (448, 8, 8, 8), (True, True), self.force/2)
        group.all_sprites.add(brick)
        group.death_sprites.add(brick)


class Bubble(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sheet = group.items_objects_sheet.copy()
        self.sheet.set_clip(pygame.Rect(38, 133, 4, 4))

        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.image = pygame.transform.scale(self.image, (12, 12))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self._layer = 3

        self.y_velocity = -2

    def update(self, delta_time):
        if not group.stop:
            self.rect.y += int(self.y_velocity*group.time*delta_time)

            if self.rect.y < 96:
                self.kill()


class Goomba_Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.palette = palette.palette_1

        self.sprite_states = (81, 97)

        self.sheet = group.enemy_n_bosses_sheet.copy()

        self.sheet.set_clip(pygame.Rect(81, 48, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace( self.palette[0][0], self.palette[palette.index][0] )
        self.image_pixel_array.replace( self.palette[0][1], self.palette[palette.index][1] )
        self.image_pixel_array.replace( self.palette[0][2], self.palette[palette.index][2] )

        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()

        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom+3

        self._layer = 3


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom+3

    
    def animation(self):
        self.sheet.set_clip(pygame.Rect((self.sprite_states[enemy_frame], 48, 16, 16)))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (48, 48))


    def update_animation(self):
        self.position()
        self.animation()


class Koopa_Troopa_Paratroopa_Green_Animartion(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.palette = palette.palette_1
        self.sprite_object = sprite_object

        self.walk_states = ((210, 32, 16, 32), (194, 32, 16, 32))
        self.fly_states  = ((178, 32, 16, 32), (162, 32, 16, 32))
        self.hide_states = ((130, 32, 16, 16), )
        self.round_states = ((130, 32, 16, 16), (114, 48, 16, 16), (130, 48, 16, 16), (146, 48, 16, 16) )
        self.i_want_to_break_free_states = ((114, 32, 16, 16), (130, 32, 16, 16))

        self.sprite_states = self.walk_states
        
        self.direction_x = False
        self.direction_y = False

        self.sheet = group.enemy_n_bosses_sheet.copy()
        self.sheet.set_clip(pygame.Rect(self.sprite_states[0]))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace( self.palette[0][3], self.palette[palette.index][3] )
        self.image_pixel_array.replace( self.palette[0][4], self.palette[palette.index][4] )
        self.image_pixel_array.replace( self.palette[0][5], self.palette[palette.index][5] )

        self.image = pygame.transform.scale(self.image, (self.sprite_states[0][2]*3, self.sprite_states[0][3]*3))
        self.rect = self.image.get_rect()

        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom+3

        self._layer = 3

        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        if not self.direction_y:
            self.rect.bottom = self.sprite_object.rect.bottom+3

        else:
            self.rect.bottom = self.sprite_object.rect.bottom+9


    def direction_in_x_axis(self):
        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) < 0:
            self.direction_x = True

        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) > 0:
            self.direction_x = False


    def controll_states(self):
        if not self.sprite_object.is_hide:
            self.frame_rate = 150
            if not self.sprite_object.can_fly:
                self.sprite_states = self.walk_states

            else:
                self.sprite_states = self.fly_states

        else:
            
            if not self.sprite_object.is_round:
                self.frame_rate = 150
                if self.sprite_object.hide_time.time < 1.5:
                    self.sprite_states = self.i_want_to_break_free_states

                else:
                    self.sprite_states = self.hide_states

            else:
                self.frame_rate = 60
                self.sprite_states = self.round_states


    def animation_rate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            

    def animation(self):
        if self.frame >= len(self.sprite_states):
            self.frame = 0

        if self.sprite_states == self.walk_states or self.sprite_states == self.fly_states:
            self.sheet.set_clip(pygame.Rect(self.sprite_states[enemy_frame]))

        else:
            self.sheet.set_clip(pygame.Rect(self.sprite_states[self.frame]))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (self.sprite_states[self.frame][2]*3, self.sprite_states[self.frame][3]*3))
        self.image = pygame.transform.flip(self.image, self.direction_x, self.direction_y)
        self.rect = self.image.get_rect()

        self.position()


    def update_animation(self):
        self.direction_in_x_axis()
        self.controll_states()
        self.animation_rate()
        self.animation()


class Koopa_Troopa_Paratroopa_Red_Animartion(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.palette = palette.palette_1
        self.sprite_object = sprite_object

        self.walk_states = ((210, 32, 16, 32), (194, 32, 16, 32))
        self.fly_states  = ((178, 32, 16, 32), (162, 32, 16, 32))
        self.hide_states = ((130, 32, 16, 16), )
        self.round_states = ((130, 32, 16, 16), (114, 48, 16, 16), (130, 48, 16, 16), (146, 48, 16, 16) )
        self.i_want_to_break_free_states = ((114, 32, 16, 16), (130, 32, 16, 16))

        self.sprite_states = self.walk_states
        
        self.direction_x = False
        self.direction_y = False

        self.sheet = group.enemy_n_bosses_sheet.copy()
        self.sheet.set_clip(pygame.Rect(self.sprite_states[0]))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace( self.palette[0][3], self.palette[0][3] )
        self.image_pixel_array.replace( self.palette[0][4], self.palette[0][6] )
        self.image_pixel_array.replace( self.palette[0][5], self.palette[0][5] )

        self.image = pygame.transform.scale(self.image, (self.sprite_states[0][2]*3, self.sprite_states[0][3]*3))
        self.rect = self.image.get_rect()

        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom+3

        self._layer = 3

        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        if not self.direction_y:
            self.rect.bottom = self.sprite_object.rect.bottom+3

        else:
            self.rect.bottom = self.sprite_object.rect.bottom+9


    def direction_in_x_axis(self):
        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) < 0:
            self.direction_x = True

        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) > 0:
            self.direction_x = False


    def controll_states(self):
        if not self.sprite_object.is_hide:
            self.frame_rate = 150
            if not self.sprite_object.can_fly:
                self.sprite_states = self.walk_states

            else:
                self.sprite_states = self.fly_states

        else:
            
            if not self.sprite_object.is_round:
                self.frame_rate = 150
                if self.sprite_object.hide_time.time < 1.5:
                    self.sprite_states = self.i_want_to_break_free_states

                else:
                    self.sprite_states = self.hide_states

            else:
                self.frame_rate = 60
                self.sprite_states = self.round_states


    def animation_rate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            

    def animation(self):
        if self.frame >= len(self.sprite_states):
            self.frame = 0

        if self.sprite_states == self.walk_states:
            self.sheet.set_clip(pygame.Rect(self.sprite_states[enemy_frame]))

        else:
            self.sheet.set_clip(pygame.Rect(self.sprite_states[self.frame]))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (self.sprite_states[self.frame][2]*3, self.sprite_states[self.frame][3]*3))
        self.image = pygame.transform.flip(self.image, self.direction_x, self.direction_y)
        self.rect = self.image.get_rect()

        self.position()


    def update_animation(self):
        self.direction_in_x_axis()
        self.controll_states()
        self.animation_rate()
        self.animation()


class Buzzy_Beetle_Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.palette = palette.palette_1
        self.sprite_object = sprite_object

        self.walk_states = ((179, 16, 16, 16), (163, 16, 16, 16))
        self.hide_states = ((147, 16, 16, 16), )
        self.round_states = ((147, 16, 16, 16), (147, 0, 16, 16), (163, 0, 16, 16), (179, 0, 16, 16) )

        self.sprite_states = self.walk_states
        
        self.direction_x = False
        self.direction_y = False

        self.sheet = group.enemy_n_bosses_sheet.copy()
        self.sheet.set_clip(pygame.Rect(self.sprite_states[0]))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace( self.palette[0][0], self.palette[palette.index][0] )
        self.image_pixel_array.replace( self.palette[0][1], self.palette[palette.index][1] )
        self.image_pixel_array.replace( self.palette[0][2], self.palette[palette.index][2] )

        self.image = pygame.transform.scale(self.image, (self.sprite_states[0][2]*3, self.sprite_states[0][3]*3))
        self.rect = self.image.get_rect()

        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom+3

        self._layer = 3

        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        if not self.direction_y:
            self.rect.bottom = self.sprite_object.rect.bottom+3

        else:
            self.rect.bottom = self.sprite_object.rect.bottom+9


    def direction_in_x_axis(self):
        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) < 0:
            self.direction_x = True

        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) > 0:
            self.direction_x = False


    def controll_states(self):
        if not self.sprite_object.is_hide:
            self.frame_rate = 150
            self.sprite_states = self.walk_states

        else:
            self.frame_rate = 60
            if not self.sprite_object.is_round:
                self.sprite_states = self.hide_states

            else:
                self.sprite_states = self.round_states


    def animation_rate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            

    def animation(self):
        if self.frame >= len(self.sprite_states):
            self.frame = 0

        if self.sprite_states == self.walk_states:
            self.sheet.set_clip(pygame.Rect(self.sprite_states[enemy_frame]))

        else:
            self.sheet.set_clip(pygame.Rect(self.sprite_states[self.frame]))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (self.sprite_states[self.frame][2]*3, self.sprite_states[self.frame][3]*3))
        self.image = pygame.transform.flip(self.image, self.direction_x, self.direction_y)
        self.rect = self.image.get_rect()

        self.position()


    def update_animation(self):
        self.direction_in_x_axis()
        self.controll_states()
        self.animation_rate()
        self.animation()


class Spiny_Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.palette = palette.palette_1
        self.sprite_object = sprite_object

        self.walk_states = ((212, 16, 16, 16), (196, 16, 16, 16))
        self.egg_states  = ((212, 0, 16, 16), (196, 0, 16, 16) )

        self.sprite_states = self.egg_states
        
        self.direction_x = False
        self.direction_y = False

        self.sheet = group.enemy_n_bosses_sheet.copy()
        self.sheet.set_clip(pygame.Rect(self.sprite_states[0]))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.image = pygame.transform.scale(self.image, (self.sprite_states[0][2]*3, self.sprite_states[0][3]*3))
        self.rect = self.image.get_rect()

        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom+3

        self._layer = 3


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        if not self.direction_y:
            self.rect.bottom = self.sprite_object.rect.bottom+3

        else:
            self.rect.bottom = self.sprite_object.rect.bottom+9


    def direction_in_x_axis(self):
        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) < 0:
            self.direction_x = True

        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) > 0:
            self.direction_x = False


    def controll_states(self):
        if self.sprite_object.touch_the_floor:
            self.sprite_states = self.walk_states

        else:
            self.sprite_states = self.egg_states


    def animation(self):
        self.sheet.set_clip(pygame.Rect(self.sprite_states[enemy_frame]))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (self.sprite_states[enemy_frame][2]*3, self.sprite_states[enemy_frame][3]*3))
        self.image = pygame.transform.flip(self.image, self.direction_x, self.direction_y)
        self.rect = self.image.get_rect()

        self.position()


    def update_animation(self):
        self.direction_in_x_axis()
        self.controll_states()
        self.animation()


class Lakitu_Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.normal_states = (294, 0, 16, 32)
        self.will_drop_states = (294, 32, 16, 32)

        self.sprite_states = self.normal_states
        self.direction_x = True

        self.sheet = group.enemy_n_bosses_sheet.copy()
        self.sheet.set_clip(pygame.Rect(self.sprite_states))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace(palette.palette_1[0][3], palette.palette_1[palette.index][3])
        self.image_pixel_array.replace(palette.palette_1[0][4], palette.palette_1[palette.index][4])
        self.image_pixel_array.replace(palette.palette_1[0][5], palette.palette_1[palette.index][5])

        self.image = pygame.transform.scale(self.image, (48, 96))
        self.image = pygame.transform.flip(self.image, self.direction_x, False)

        self.rect = self.image.get_rect()

        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom+3

        self._layer = 3


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom+3


    def direction_in_x_axis(self):
        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) < 0:
            self.direction_x = False

        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) > 0:
            self.direction_x = True


    def controll_states(self):
        if self.sprite_object.can_drop.time <= .5:
            self.sprite_states = self.will_drop_states

        else:
            self.sprite_states = self.normal_states


    def animation(self):
        self.sheet.set_clip(pygame.Rect(self.sprite_states))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (48, 96))
        self.image = pygame.transform.flip(self.image, self.direction_x, False)


    def update_animation(self):
        self.direction_in_x_axis()
        self.controll_states()
        self.animation()
        self.position()


class Bullet_Bill_Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.init_x = self.sprite_object.rect.x
        self.can_change = True

        self.direction_in_x_axis()
        self.sheet = group.enemy_n_bosses_sheet.copy()
        self.sheet.set_clip(pygame.Rect(130, 16, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace(palette.palette_1[0][0], palette.palette_1[palette.index][0])
        self.image_pixel_array.replace(palette.palette_1[0][1], palette.palette_1[palette.index][1])
        self.image_pixel_array.replace(palette.palette_1[0][2], palette.palette_1[palette.index][2])
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.image = pygame.transform.flip(self.image, self.direction_x, False)
        self.rect = self.image.get_rect()
        self._layer = 1
        self.position()


    def direction_in_x_axis(self):
        if self.sprite_object.right_velocity != 0:
            self.direction_x = False

        else:
            self.direction_x = True


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.top = self.sprite_object.rect.top-3


    def reset_layer(self):
        if self.can_change:
            if self.rect.x <= self.init_x-48 or self.rect.x >= self.init_x+48:
                self.can_change = False
                group.all_sprites.change_layer(self, 3)


    def update_animation(self):
        self.reset_layer()
        self.position()


class Pirana_Plant_Green_Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.sprite_states = (243, 227)
        self.sheet = group.enemy_n_bosses_sheet.copy()

        self.go = self.sprite_object.go

        self.sheet.set_clip(pygame.Rect(self.sprite_states[enemy_frame], 32, 16, 32))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace(palette.palette_1[0][3], palette.palette_1[palette.index][3])
        self.image_pixel_array.replace(palette.palette_1[0][4], palette.palette_1[palette.index][4])
        self.image_pixel_array.replace(palette.palette_1[0][5], palette.palette_1[palette.index][5])
        self.image = pygame.transform.scale(self.image, (48, 96))
        self.image = pygame.transform.flip(self.image, False, self.go)
        self.rect = self.image.get_rect()
        self.position()

        self._layer = 3

    def position(self):
        self.rect.center = self.sprite_object.rect.center
        if self.go:
            self.rect.top = self.sprite_object.rect.top-3

        if not self.go:
            self.rect.bottom = self.sprite_object.rect.bottom+3

    def animation(self):
        self.sheet.set_clip(pygame.Rect(self.sprite_states[enemy_frame], 32, 16, 32))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (48, 96))
        self.image = pygame.transform.flip(self.image, False, self.go)

    def update_animation(self):
        self.animation()
        self.position()


class Hammer_Brother_Aniamtion(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.palette = palette.palette_1
        self.index = palette.index
        self.can_display = True

        self.direction_in_x_axis()

        self.walk_states = (277, 261)
        self.hammer_states = (245, 229)
        self.sprite_states = self.walk_states

        self.attac_walk_vel = 1
        self.x_velocity = 0

        self.sheet = group.enemy_n_bosses_sheet.copy()

        self.sheet.set_clip(pygame.Rect(self.sprite_states[enemy_frame], 0, 16, 32))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace( self.palette[0][3], self.palette[palette.index][3] )
        self.image_pixel_array.replace( self.palette[0][4], self.palette[palette.index][4] )
        self.image_pixel_array.replace( self.palette[0][5], self.palette[palette.index][5] )

        self.image = pygame.transform.scale(self.image, (48, 96))
        self.image = pygame.transform.flip(self.image, self.direction_x, False)
        
        self.rect = self.image.get_rect()
        #self.rect.center = self.sprite_object.rect.center
        self.position(1.666)
        self._layer = 3

        # animation --------------------------------
        self.animation_hammer = Hammer_Hand_Animation(self)
        group.all_sprites.add(self.animation_hammer)


    def direction_in_x_axis(self):
        if self.sprite_object.jump_count < self.sprite_object.jump_limit:
            if self.sprite_object.player.rect.center[0] <= self.sprite_object.rect.center[0]:
                self.direction_x = True

            if self.sprite_object.player.rect.center[0] >= self.sprite_object.rect.center[0]:
                self.direction_x = False

        else:
            if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) < 0:
                self.direction_x = True

            if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) > 0:
                self.direction_x = False


    def controll_states(self):
        if self.sprite_object.drop_time.time <= .5 and self.can_display:
            self.sprite_states = self.hammer_states
            self.animation_hammer.set_visibility(True)

        else:
            self.sprite_states = self.walk_states
            self.animation_hammer.set_visibility(False)


    def position(self, delta_time):
        self.left_top  = self.sprite_object.rect.x-24
        self.right_top = self.sprite_object.rect.x+12

        if self.sprite_object.jump_count < self.sprite_object.jump_limit:
            self.rect.x += int(self.x_velocity*group.time*delta_time)
            if self.rect.x <= self.left_top:
                self.rect.x = self.left_top
                self.x_velocity = self.attac_walk_vel

            if self.rect.x >= self.right_top:
                self.rect.x = self.right_top
                self.x_velocity  = self.attac_walk_vel*-1

        else:
            self.rect.center = self.sprite_object.rect.center

        self.rect.bottom = self.sprite_object.rect.bottom+3

    
    def animation(self):
        self.sheet.set_clip(pygame.Rect((self.sprite_states[enemy_frame], 0, 16, 32)))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (48, 96))
        self.image = pygame.transform.flip(self.image, self.direction_x, False)


    def update_animation(self, delta_time):
        self.direction_in_x_axis()
        self.controll_states()
        self.position(delta_time)
        self.animation()
        self.animation_hammer.update_animation()


class Hammer_Hand_Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.palette = palette.palette_1
        self.sprite_object = sprite_object

        self.sheet = group.items_objects_sheet.copy()

        
        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace( self.palette[0][0], self.palette[palette.index][0] )
        self.image_pixel_array.replace( self.palette[0][1], self.palette[palette.index][1] )
        self.image_pixel_array.replace( self.palette[0][2], self.palette[palette.index][2] )


        self.set_visibility(False)

        self.rect = self.image.get_rect()
        self.position()
        
        self._layer = 4


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.top +33


    def set_visibility(self, val_bool):
        if val_bool:
            self.sheet.set_clip(pygame.Rect(16, 80, 16, 16))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.image.set_colorkey((0, 0, 0))
            self.image = pygame.transform.scale(self.image, (48, 48))
            self.image = pygame.transform.flip(self.image, self.sprite_object.direction_x, False)

        if not val_bool:
            self.image = pygame.Surface((48, 48))
            self.image.fill((0, 0, 0))
            self.image.set_colorkey((0, 0, 0))
        

    def update_animation(self):
        self.position()


class Hammer_Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.palette = palette.palette_1
        self.sprite_object = sprite_object
        self.sprite_states = ((16, 80), (16, 96), (0, 96), (0, 80))
        self.conv = (48, 48)
        self.geometry = (16, 16)

        self.sheet = group.items_objects_sheet.copy()

        self.sheet.set_clip(pygame.Rect(self.sprite_states[hammer_frame] + self.geometry))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace( self.palette[0][0], self.palette[palette.index][0] )
        self.image_pixel_array.replace( self.palette[0][1], self.palette[palette.index][1] )
        self.image_pixel_array.replace( self.palette[0][2], self.palette[palette.index][2] )

        self.image = pygame.transform.scale(self.image, self.conv)
        self.image = pygame.transform.flip(self.image, self.sprite_object.direction, False)

        self.rect = self.image.get_rect()
        self.position()
        
        self._layer = 3


    def position(self):
        self.rect.center = self.sprite_object.rect.center


    def animation(self):
        self.sheet.set_clip(pygame.Rect(self.sprite_states[hammer_frame] + self.geometry))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))

        self.image = pygame.transform.scale(self.image, self.conv)
        self.image = pygame.transform.flip(self.image, self.sprite_object.direction, False)
        self.rect = self.image.get_rect()


    def update_animation(self):
        self.animation()
        self.position()


class Bloober_Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.palette = palette.palette_1
        self.normal_states = 97
        self.up_states     = 113

        self.sprite_states = self.normal_states

        self.sheet = group.enemy_n_bosses_sheet.copy()
        self.sheet.set_clip(pygame.Rect(self.sprite_states, 8, 16, 24  ))
        
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace( self.palette[0][0], self.palette[palette.index][0] )
        self.image_pixel_array.replace( self.palette[0][1], self.palette[palette.index][1] )
        self.image_pixel_array.replace( self.palette[0][2], self.palette[palette.index][2] )
        self.image = pygame.transform.scale(self.image, (48, 72))
        self.rect = self.image.get_rect()
        self.position()

        self._layer = 3


    def controll_states(self):
        if self.sprite_object.player.rect.top < self.rect.bottom:
            if self.sprite_object.jump_time.time <= .3:
                self.sprite_states = self.up_states

            else:
                self.sprite_states = self.normal_states

        if self.sprite_object.player.rect.top >= self.sprite_object.rect.bottom:
            if self.sprite_object.jump_time.time <= .01 and self.sprite_object.player.rect.top-45 <= self.rect.bottom:
                self.sprite_states = self.up_states

            else:
                self.sprite_states = self.normal_states


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.top = self.sprite_object.rect.top


    def animation(self):
        self.sheet.set_clip(pygame.Rect(self.sprite_states, 8, 16, 24  ))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (48, 72))


    def update_animation(self):
        self.controll_states()
        self.animation()
        self.position()


class Cheep_Cheep_Green_Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.palette = palette.palette_1
        self.direction_in_x_axis()

        self.sprite_states = (80, 64)

        self.sheet = group.enemy_n_bosses_sheet.copy()

        self.sheet.set_clip(pygame.Rect(self.sprite_states[enemy_frame], 16, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace( self.palette[0][3], self.palette[palette.index][3] )
        self.image_pixel_array.replace( self.palette[0][4], self.palette[palette.index][4] )
        self.image_pixel_array.replace( self.palette[0][5], self.palette[palette.index][5] )

        self.image = pygame.transform.scale(self.image, (48, 48))
        self.image = pygame.transform.flip(self.image, self.direction_x, False)
        self.rect = self.image.get_rect()

        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom+3

        self._layer = 3


    def direction_in_x_axis(self):
        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) < 0:
            self.direction_x = True

        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) > 0:
            self.direction_x = False


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom+3

    
    def animation(self):
        self.sheet.set_clip(pygame.Rect((self.sprite_states[enemy_frame], 16, 16, 16)))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.image = pygame.transform.flip(self.image, self.direction_x, False)


    def update_animation(self):
        self.position()
        self.animation()


class Cheep_Cheep_Red_Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.palette = palette.palette_1
        self.direction_in_x_axis()

        self.sprite_states = (80, 64)

        self.sheet = group.enemy_n_bosses_sheet.copy()

        self.sheet.set_clip(pygame.Rect(self.sprite_states[enemy_frame], 16, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image_pixel_array = pygame.PixelArray(self.sheet)
        self.image_pixel_array.replace( self.palette[0][3], self.palette[0][3] )
        self.image_pixel_array.replace( self.palette[0][4], self.palette[0][6] )
        self.image_pixel_array.replace( self.palette[0][5], self.palette[0][5] )

        self.image = pygame.transform.scale(self.image, (48, 48))
        self.image = pygame.transform.flip(self.image, self.direction_x, False)
        self.rect = self.image.get_rect()

        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom+3

        self._layer = 3


    def direction_in_x_axis(self):
        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) < 0:
            self.direction_x = True

        if int(self.sprite_object.left_velocity + self.sprite_object.right_velocity) > 0:
            self.direction_x = False


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom+3

    
    def animation(self):
        self.sheet.set_clip(pygame.Rect((self.sprite_states[enemy_frame], 16, 16, 16)))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.image = pygame.transform.flip(self.image, self.direction_x, False)


    def update_animation(self):
        self.position()
        self.animation()


class Podoboo_Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.palette = palette.palette_1

        self.direction_in_y_axis()

        self.sprite_states = (65, 81)

        self.sheet = group.enemy_n_bosses_sheet.copy()

        self.sheet.set_clip(pygame.Rect(self.sprite_states[enemy_frame], 0, 16, 16))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.image = pygame.transform.flip(self.image, False, self.direction_y)
        self.rect = self.image.get_rect()
        self.position()

        self._layer = 3


    def direction_in_y_axis(self):
        if int(self.sprite_object.bottom_velocity) <= 0:
            self.direction_y = False

        if int(self.sprite_object.bottom_velocity) >= 0:
            self.direction_y = True


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom+3

    
    def animation(self):
        self.sheet.set_clip(pygame.Rect((self.sprite_states[enemy_frame], 0, 16, 16)))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.image = pygame.transform.flip(self.image, False, self.direction_y)


    def update_animation(self):
        self.direction_in_y_axis()
        self.position()
        self.animation()


class Bowser_Fire_Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.palette = palette.palette_1

        self.sprite_states = (80, 88)

        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60


        self.sheet = group.items_objects_sheet.copy()

        self.sheet.set_clip(pygame.Rect((36, self.sprite_states[0], 24, 8)))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (72, 24))
        self.image = pygame.transform.flip(self.image, self.sprite_object.direction, False)

        self.rect = self.image.get_rect()

        self.position()

        self._layer = 3

    def position(self):
        self.rect.center = self.sprite_object.rect.center

    
    def animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1

            if self.frame >= len(self.sprite_states):
                self.frame = 0

            self.sheet.set_clip(pygame.Rect((36, self.sprite_states[self.frame], 24, 8)))
            self.image = self.sheet.subsurface(self.sheet.get_clip())
            self.image.set_colorkey((0, 0, 0))
            self.image = pygame.transform.scale(self.image, (72, 24))
            self.image = pygame.transform.flip(self.image, self.sprite_object.direction, False)


    def update_animation(self):
        self.position()
        self.animation()


class Bowser_Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object

        self.normal_states = ( (32, 32), (0, 32)  )
        self.attac_states  = ( (32, 0), (0, 0)  )

        self.controll_states()

        self.sheet = group.enemy_n_bosses_sheet.copy()

        self.animation()
        self.rect = self.image.get_rect()

        self.position()
        self._layer = 3


    def controll_states(self):
        if self.sprite_object.tick_to_drop_fire.time <= .3:
            self.sprite_states = self.attac_states

        else:
            self.sprite_states = self.normal_states


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.bottom+3

        if self.sprite_object.direction:
            self.rect.right = self.sprite_object.rect.right+6

        if not self.sprite_object.direction:
            self.rect.left = self.sprite_object.rect.left-6

    
    def animation(self):
        self.sheet.set_clip(pygame.Rect((self.sprite_states[enemy_frame] + (32, 32) )))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (96, 96))
        self.image = pygame.transform.flip(self.image, self.sprite_object.direction, False)


    def update_animation(self):
        self.controll_states()
        self.position()
        self.animation()

