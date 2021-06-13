import pygame
from pygame.locals import *
pygame.init()

from script import group, physic, tile, animation, font, score, sound

class Magic_Mushroom(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        sound.power_up_appears_sound.stop()
        sound.power_up_appears_sound.play()
        self.sprite_object = sprite_object
        self.stade = False

        self.image = pygame.Surface((24, 45))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.sprite_object.rect.x+12, self.sprite_object.rect.y 

        self._layer = 3


        # Fuerzas de velocidad -------------------------------------------
        self.wal_vel = 3
        self.left_velocity = 0
        self.right_velocity = 0
        

        self.top_velocity    = 0
        self.bottom_velocity = 0

        self.jump_force = -8

        self.gravity = 0
        self.bottom_MAX_VEL = 0
        self.fall_vel = 12


        # datos de el collider --------------------------------------------
        self.collider = physic.Collider_2D(self, True, True)

        self.bottom_collision = (True, None) # bloques
        self.top_collision    = (False, None)
        self.right_collision  = (False, None)
        self.left_collision   = (False, None)  

        # animacion --------------------------------------------------------
        self.animation = animation.Animation_Magic_Mushroom(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)


    def manage_velocity(self, delta_time):
        if self.bottom_velocity < 0:
            self.gravity = group.gravity_in_up_GRASS

        if self.bottom_velocity >= 0:
            self.gravity = group.gravity_in_down_GRASS

        self.bottom_velocity = physic.Accelearted_Linear_Movement(self.bottom_velocity, delta_time, self.bottom_MAX_VEL, self.gravity, .01, True)


    def update_collider_2d(self, delta_time):
        # Colisiones contra los tiles -----------------------------------------------------------------------------------------------------------------------------------------------------
        self.bottom_collision = self.collider.bottom_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.top_velocity, self.bottom_velocity, delta_time))

        self.top_collision    = self.collider.top_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.top_velocity, self.bottom_velocity, delta_time)) 

        self.right_collision  = self.collider.right_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.right_velocity, self.left_velocity, delta_time))

        self.left_collision   = self.collider.left_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.right_velocity, self.left_velocity, delta_time))


    def manage_movement(self, delta_time):
        if not self.bottom_collision[0]:
            self.rect.y += int( self.bottom_velocity*group.time*delta_time )
            self.bottom_MAX_VEL = self.fall_vel

        if not self.top_collision[0]:
            self.rect.y += int( self.top_velocity*group.time*delta_time )

        if not self.left_collision[0]:
            self.rect.x += int( self.left_velocity*group.time*delta_time )

        if not self.right_collision[0]:
            self.rect.x += int( self.right_velocity*group.time*delta_time )

        self.screen_collide()

        if self.bottom_collision[0]:
            if self.bottom_collision[1].top_collide: # Revisar si las colisiones del bloque estan activadas
                self.rect.bottom = self.bottom_collision[1].rect.top
                self.bottom_MAX_VEL = 0

                if self.bottom_collision[1].is_rebound:
                    self.bottom_velocity = self.jump_force

            else:
                if self.bottom_velocity > 0:
                    self.rect.y += int( self.bottom_velocity*group.time*delta_time )
                    self.bottom_MAX_VEL = self.fall_vel  

        if self.top_collision[0]:
            if self.top_collision[1].bottom_collide:
                self.bottom_velocity = physic.Rebound(self.bottom_velocity) # rebote con los bloques 

            else:
                if self.top_velocity < 0:
                    self.rect.y += int( self.top_velocity*group.time*delta_time )        

        if self.left_collision[0]:
            if self.left_collision[1].right_collide:
                self.rect.left = self.left_collision[1].rect.right
                self.left_velocity = 0
                self.right_velocity = self.wal_vel

            else:
                self.rect.x += int( self.left_velocity*group.time*delta_time )

        if self.right_collision[0]:
            if self.right_collision[1].left_collide: 
                self.rect.right = self.right_collision[1].rect.left
                self.left_velocity = self.wal_vel*-1
                self.right_velocity = 0
                

            else:
                self.rect.x += int( self.right_velocity*group.time*delta_time )


    def manage_player_collide(self):
        player_collide = pygame.sprite.spritecollide(self, group.player_sprites, False)
        for player in player_collide:
            sound.power_up_sound.stop()
            sound.power_up_sound.play()

            score.score += 1000
            font.Generate_Point("1000", player.rect.x-12, player.rect.y-48)

            player.resize()
            self.collider.kill()
            self.animation.kill()
            self.kill()


    def screen_collide(self):
        if self.rect.y > group.geometry[1]:
            self.collider.kill()
            self.animation.kill()
            self.kill()
            

    def manage_collide(self, delta_time):
        self.manage_movement(delta_time)
        

    def grow_up(self, delta_time):
        if not self.rect.y < self.sprite_object.rect.y-48:
            self.rect.y -= int(1*group.time*delta_time)

        else:
            self.stade = True
            group.all_sprites.change_layer(self.animation, self.sprite_object._layer+1)
            """
            for player in group.player_sprites:
                if player.animation.direction_x:
                    self.left_velocity = self.wal_vel*-1
                    self.right_velocity = 0

                if not player.animation.direction_x:
            """
            self.left_velocity = 0
            self.right_velocity = self.wal_vel


    def update(self, delta_time):
        if not group.stop:
            if self.stade:
                self.manage_velocity(delta_time)
                self.update_collider_2d(delta_time)
                self.manage_collide(delta_time)

            else:
                self.grow_up(delta_time)

        self.manage_player_collide()
        self.collider.update()
        self.animation.update_animation()


class One_Up_Mushroom(Magic_Mushroom): # Actualizar el metodo manage_player_collide !!!!!!!
    def __init__(self, sprite_object):
        super().__init__(sprite_object)
        self.animation.kill()

        self.animation = animation.Animation_One_Up_Mushroom(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)


    def manage_player_collide(self):
        player_collide = pygame.sprite.spritecollide(self, group.player_sprites, False)
        for player in player_collide:
            sound.one_up_sound.stop()
            sound.one_up_sound.play()
            score.lives += 1
            group.all_sprites.add(font.Generate_ONE_UP(self.rect.center))
            self.collider.kill()
            self.animation.kill()
            self.kill()


class Poison_Mushroom(Magic_Mushroom):
    def __init__(self, sprite_object):
        super().__init__(sprite_object)
        self.animation.kill()

        self.animation = animation.Animation_Poison_Mushroom(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)


    def manage_player_collide(self):
        player_collide = pygame.sprite.spritecollide(self, group.player_sprites, False)
        for player in player_collide:
            if player.size and not player.invincibility_power:
                sound.pipe_sound.stop()
                sound.pipe_sound.play()
                player.fire_power = False
                player.resize()

            self.collider.kill()
            self.animation.kill()
            self.kill()


class Fire_Flower(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        sound.power_up_appears_sound.stop()
        sound.power_up_appears_sound.play()
        self.sprite_object = sprite_object
        self.stade = False

        self.image = pygame.Surface((24, 45))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.sprite_object.rect.x+12, self.sprite_object.rect.y 

        self._layer = 3

        self.animation = animation.Animation_Fire_Flower(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)


    def manage_player_collide(self):
        player_collide = pygame.sprite.spritecollide(self, group.player_sprites, False)
        for player in player_collide:
            sound.power_up_sound.stop()
            sound.power_up_sound.play()

            score.score += 1000
            font.Generate_Point("1000", player.rect.x-12, player.rect.y-48)

            if player.size:
                player.set_fire_power(True)

            else:
                player.resize()

            self.animation.kill()
            self.kill()


    def grow_up(self, delta_time):
        if not self.stade:
            if not self.rect.y <= self.sprite_object.rect.y-45:
                self.rect.y -= int(1*group.time*delta_time)

            else:
                group.all_sprites.change_layer(self.animation, self.sprite_object._layer+1)
                self.stade = True


    def screen_collide(self):
        if self.rect.right < 0 or self.rect.y > group.geometry[1]:
            self.animation.kill()
            self.kill()


    def update(self, delta_time):
        if not group.stop:
            self.grow_up(delta_time)
            self.manage_player_collide()
            self.animation.update_animation()
            self.screen_collide()


class Starman(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        sound.power_up_appears_sound.stop()
        sound.power_up_appears_sound.play()
        self.sprite_object = sprite_object
        self.stade = False

        self.image = pygame.Surface((24, 45))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = self.sprite_object.rect.x+12, self.sprite_object.rect.y

        self._layer = 3

        # Fuerzas de velocidad -------------------------------------------
        self.wal_vel = 3
        self.left_velocity = 0
        self.right_velocity = 0
        

        self.top_velocity    = 0
        self.bottom_velocity = 0

        self.jump_force = -12

        self.gravity = 0
        self.bottom_MAX_VEL = 0
        self.fall_vel = 12


        # datos de el collider --------------------------------------------
        self.collider = physic.Collider_2D(self, True, True)

        self.bottom_collision = (True, None) # bloques
        self.top_collision    = (False, None)
        self.right_collision  = (False, None)
        self.left_collision   = (False, None)

        # animacion -------------------------------------------------------
        self.animation = animation.Animation_Star_Man(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)


    def manage_velocity(self, delta_time):
        if self.bottom_velocity < 0:
            self.gravity = group.gravity_in_up_GRASS

        if self.bottom_velocity >= 0:
            self.gravity = group.gravity_in_down_GRASS

        self.bottom_velocity = physic.Accelearted_Linear_Movement(self.bottom_velocity, delta_time, self.bottom_MAX_VEL, self.gravity, .01, True)
    

    def update_collider_2d(self, delta_time):
        # Colisiones contra los tiles -----------------------------------------------------------------------------------------------------------------------------------------------------
        self.bottom_collision = self.collider.bottom_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.top_velocity, self.bottom_velocity, delta_time))

        self.top_collision    = self.collider.top_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.top_velocity, self.bottom_velocity, delta_time)) 

        self.right_collision  = self.collider.right_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.right_velocity, self.left_velocity, delta_time))

        self.left_collision   = self.collider.left_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.right_velocity, self.left_velocity, delta_time))


    def manage_movement(self, delta_time):
        if not self.bottom_collision[0]:
            self.rect.y += int( self.bottom_velocity*group.time*delta_time )
            self.bottom_MAX_VEL = self.fall_vel

        if not self.top_collision[0]:
            self.rect.y += int( self.top_velocity*group.time*delta_time )

        if not self.left_collision[0]:
            self.rect.x += int( self.left_velocity*group.time*delta_time )

        if not self.right_collision[0]:
            self.rect.x += int( self.right_velocity*group.time*delta_time )

        self.screen_collide()

        if self.bottom_collision[0]:
            if self.bottom_collision[1].top_collide: # Revisar si las colisiones del bloque estan activadas
                self.rect.bottom = self.bottom_collision[1].rect.top
                self.bottom_MAX_VEL = 0

                if self.bottom_collision[1].is_rebound:
                    self.bottom_velocity = self.jump_force

                self.bottom_velocity = self.jump_force

            else:
                if self.bottom_velocity > 0:
                    self.rect.y += int( self.bottom_velocity*group.time*delta_time )
                    self.bottom_MAX_VEL = self.fall_vel  

        if self.top_collision[0]:
            if self.top_collision[1].bottom_collide:
                self.bottom_velocity = physic.Rebound(self.bottom_velocity/2) # rebote con los bloques 

            else:
                if self.top_velocity < 0:
                    self.rect.y += int( self.top_velocity*group.time*delta_time )        

        if self.left_collision[0]:
            if self.left_collision[1].right_collide:
                self.rect.left = self.left_collision[1].rect.right
                self.left_velocity = 0
                self.right_velocity = self.wal_vel

            else:
                self.rect.x += int( self.left_velocity*group.time*delta_time )

        if self.right_collision[0]:
            if self.right_collision[1].left_collide: 
                self.rect.right = self.right_collision[1].rect.left
                self.left_velocity = self.wal_vel*-1
                self.right_velocity = 0
                

            else:
                self.rect.x += int( self.right_velocity*group.time*delta_time )
    

    def manage_player_collide(self):
        player_collide = pygame.sprite.spritecollide(self, group.player_sprites, False)
        for player in player_collide:
            sound.power_up_sound.stop()
            sound.power_up_sound.play()

            score.score += 1000
            font.Generate_Point("1000", player.rect.x-12, player.rect.y-48)
            
            player.set_invincibility_power(True)

            self.animation.kill()
            self.collider.kill()
            self.kill()


    def screen_collide(self):
        if self.rect.y > group.geometry[1]:
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def grow_up(self, delta_time):
        if not self.rect.y < self.sprite_object.rect.y-48:
            self.rect.y -= int(1*group.time*delta_time)

        else:
            self.stade = True
            group.all_sprites.change_layer(self.animation, self.sprite_object._layer+1)
            """
            for player in group.player_sprites:
                if player.animation.direction_x:
                    self.left_velocity = self.wal_vel*-1
                    self.right_velocity = 0
                
                if not player.animation.direction_x:
            """
            self.left_velocity = 0
            self.right_velocity = self.wal_vel


    def update(self, delta_time):
        if not group.stop:
            if self.stade:
                self.manage_velocity(delta_time)
                self.update_collider_2d(delta_time)
                self.manage_movement(delta_time)

            else:
                self.grow_up(delta_time)

        self.manage_player_collide()
        self.collider.update()
        self.animation.update_animation()


class Fire_Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_x):
        super().__init__()
        sound.fireball_sound.stop()
        sound.fireball_sound.play()
        self.palette = None
        self.direction_x = direction_x
        self.sheet = group.items_objects_sheet.copy()
        self.sheet.set_clip(pygame.Rect((40, 96, 8, 8)))
        
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.image = pygame.transform.flip(self.image, self.direction_x, False)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self._layer = 3
        
        # Fuerzas de velocidad ------------------------------------------------
        self.velocity_x = 12

        if self.direction_x:
            self.left_velocity = self.velocity_x*-1
            self.right_velocity = 0

        if not self.direction_x:
            self.left_velocity = 0
            self.right_velocity = self.velocity_x

        self.bottom_velocity = 0
        self.bottom_MAX_VEL  = 12

        self.jump_force = -12
        self.gravity = 1.5

        # datos de el collider --------------------------------------------
        self.collider = physic.Collider_2D(self)

        self.bottom_collision = (False, None)
        self.right_collision  = (False, None)
        self.left_collision   = (False, None)

        # states ---------------------------------------------------------
        self.normal_states = (  
                               (40, 96, 8, 8), 
                               (32, 104, 8, 8), 
                               (40, 104, 8, 8),
                               (32, 96, 8, 8),
                               )

        self.sprite_states = self.normal_states

        self.frame = 0 
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100


    def manage_velocity(self, delta_time):
        self.bottom_velocity = physic.Accelearted_Linear_Movement(self.bottom_velocity, delta_time, self.bottom_MAX_VEL, self.gravity, -0.1, True)

        if self.bottom_collision[0]:
            self.bottom_velocity = 0
            self.bottom_velocity = self.jump_force


    def update_collider_2d(self, delta_time):
        self.left_collision = self.collider.left_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.left_velocity, self.right_velocity, delta_time))
        self.right_collision = self.collider.right_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.left_velocity, self.right_velocity, delta_time))
        self.bottom_collision = self.collider.bottom_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.bottom_velocity, 0, delta_time))


    def manage_movement(self, delta_time):
        if not self.bottom_collision[0]:
            self.rect.y += int( self.bottom_velocity*group.time*delta_time )

        if not self.left_collision[0]:
            self.rect.x += int( self.left_velocity*group.time*delta_time )

        if not self.right_collision[0]:
            self.rect.x += int( self.right_velocity*group.time*delta_time )

        self.kill_fireball()

        if self.bottom_collision[0]:
            if self.bottom_collision[1].top_collide: 
                self.rect.bottom = self.bottom_collision[1].rect.top

            else:
                if self.bottom_velocity > 0:
                    self.rect.y += int( self.bottom_velocity*group.time*delta_time )
   
        if self.left_collision[0]:
            if self.left_collision[1].right_collide:
                if self.rect.left >= self.left_collision[1].rect.right:
                    self.rect.left = self.left_collision[1].rect.right
                    self.explosion(self.left_collision[1])

                else:
                    self.rect.x += int( self.left_velocity*group.time*delta_time )

            else:
                self.rect.x += int( self.left_velocity*group.time*delta_time )

        if self.right_collision[0]:
            if self.right_collision[1].left_collide:
                if self.rect.right <= self.right_collision[1].rect.left:
                    self.rect.right = self.right_collision[1].rect.left
                    self.explosion(self.right_collision[1])

                else:
                    self.rect.x += int( self.right_velocity*group.time*delta_time )
                
            else:
                self.rect.x += int( self.right_velocity*group.time*delta_time )


    def manage_enemy_collide(self):
        fire_ball_enemy = pygame.sprite.spritecollide(self, group.enemy_sprites, False)
        for enemy in fire_ball_enemy:
            if enemy.can_fire_works:
                enemy.death_jump(self.direction_x, True)

            else:
                sound.bump_sound.stop()
                sound.bump_sound.play()

            self.explosion()


    def manage_collide(self, delta_time):
        self.manage_movement(delta_time)
        self.manage_enemy_collide()
        

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
            
            self.image = pygame.transform.scale(self.image, (24, 24))

            self.image = pygame.transform.flip(self.image, self.direction_x, False)


    def kill_fireball(self):
        if self.rect.bottom < 0:
            self.explosion()

        if self.rect.top > group.geometry[1]:
            self.explosion()


    def explosion(self, obj=None):
        if isinstance(obj, tile.Tile):
            sound.bump_sound.stop()
            sound.bump_sound.play()

        explosion = animation.Death_Animation(
                                            self, 
                                                (
                                                (48, 96, 16, 16), 
                                                (48, 112, 16, 16),
                                                (48, 128, 16, 16)
                                                ), 
                                                20, 
                                                self.rect.center
                                                )
        group.all_sprites.add(explosion)
        group.death_sprites.add(explosion)

        self.collider.kill()
        self.kill()


    def update(self, delta_time):
        if not group.stop:
            self.manage_velocity(delta_time)
            self.update_collider_2d(delta_time)
            self.manage_collide(delta_time)
            self.animation()

            self.collider.update()


class Fireworks(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        sound.fireworks_sound.stop()
        sound.fireworks_sound.play()

        self.sprite_states = (96, 112, 128)

        self.sheet = group.items_objects_sheet.copy()

        self.sheet.set_clip(pygame.Rect( 48, self.sprite_states[0], 16, 16 ) )
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale( self.image, (48, 48) )
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self._layer = 5

        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 150


    def animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now

            self.frame += 1

            if self.frame >= len(self.sprite_states):
                self.kill()

            else:

                self.sheet.set_clip(pygame.Rect( 48, self.sprite_states[self.frame], 16, 16 ) )
                self.image = self.sheet.subsurface(self.sheet.get_clip())
                self.image.set_colorkey((0, 0, 0))
                self.image = pygame.transform.scale( self.image, (48, 48) )
                

    def update(self, delta_time):
        self.animation()