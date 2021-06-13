import pygame, random, math
from pygame.locals import *
pygame.init()

from script import group, physic, animation, obj, seam, sound, score, font, tile

color = (0, 0, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #self.image = pygame.Surface((48, 45))
        self.image = pygame.Surface((30, 45))
        self.image.fill(color)
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()

        self._layer = 3

        self.rect.x, self.rect.y = x, y

        self.can_smash = True
        self.can_death_jump = True
        self.can_fire_works = True
        self.collide_enemy  = True

        self.score = 100

        # Fuerzas de velocidad --------------------------------------------
        self.walk_vel = 2
        self.run_vel  = 8
        self.jump_force = -12
        self.bottom_MAX_VEL = 0
        self.fall_vel = 12


        self.left_velocity  = self.walk_vel*-1
        self.right_velocity = 0
        self.top_velocity = 0
        self.bottom_velocity = 1

        # datos de el collider --------------------------------------------
        self.collider = physic.Collider_2D(self, True, True)

        self.bottom_collision = (False, None) # bloques
        self.top_collision    = (False, None)
        self.right_collision  = (False, None)
        self.left_collision   = (False, None)

        self.enemy_right_collision = (False, None) # Enemigos
        self.enemy_left_collision  = (False, None)

        self.player_right_collision  = (False, None) # Player
        self.player_left_collision   = (False, None)
        self.player_bottom_collision = (False, None)
        self.player_top_collision    = (False, None)


    # Metodos basicos ----------------------------------------------
    def manage_velocity(self, delta_time):
        if self.bottom_velocity >= 0: # La fuerza de gravedad cambia su velor dependiendo del signo de la velocidad
            self.gravity = group.gravity_in_down_GRASS

        if self.bottom_velocity < 0:
            self.gravity = group.gravity_in_up_GRASS

        self.bottom_velocity = physic.Accelearted_Linear_Movement(self.bottom_velocity, delta_time, self.bottom_MAX_VEL, self.gravity, -.01, True) # acelerar/desacelerar


    def update_collider_2d(self, delta_time):
        # Colisiones contra los tiles -----------------------------------------------------------------------------------------------------------------------------------------------------
        self.bottom_collision = self.collider.bottom_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.top_velocity, self.bottom_velocity, delta_time))

        self.top_collision    = self.collider.top_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.top_velocity, self.bottom_velocity, delta_time)) 

        self.right_collision  = self.collider.right_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.right_velocity, self.left_velocity, delta_time))

        self.left_collision   = self.collider.left_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.right_velocity, self.left_velocity, delta_time))

        # Colisiones contra los enemigos -----------------------------------------------------------------------------------------------------------------------------------------------------
        self.enemy_right_collision  = self.collider.right_collider.temporal_collision(group.enemy_sprites, physic.Directional_Velocity(self.right_velocity, self.left_velocity, delta_time))

        self.enemy_left_collision   = self.collider.left_collider.temporal_collision(group.enemy_sprites, physic.Directional_Velocity(self.right_velocity, self.left_velocity, delta_time))

        # Colisiones contra los enemigos -----------------------------------------------------------------------------------------------------------------------------------------------------
        self.player_bottom_collision = self.collider.bottom_collider.permanent_collision(group.player_sprites, physic.Directional_Velocity(self.top_velocity, self.bottom_velocity, delta_time))

        self.player_top_collision = self.collider.top_collider.permanent_collision(group.player_sprites, physic.Directional_Velocity(self.top_velocity, self.bottom_velocity, delta_time))

        self.player_left_collision  = self.collider.left_collider.temporal_collision(group.player_sprites, physic.Directional_Velocity(self.right_velocity, self.left_velocity, delta_time))

        self.player_right_collision   = self.collider.right_collider.temporal_collision(group.player_sprites, physic.Directional_Velocity(self.right_velocity, self.left_velocity, delta_time))


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
                self.bottom_velocity = 0

                if self.bottom_collision[1].is_rebound:
                    self.death_jump(bool(random.randint(0, 1)), True)

                if self.bottom_collision[1].jump_board:
                    if self.bottom_collision[1].can_jump:
                        self.bottom_collision[1].jump()
                        self.bottom_velocity = self.jump_force

            else:
                if self.bottom_velocity > 0:
                    self.rect.y += int( self.bottom_velocity*group.time*delta_time )
                    self.bottom_MAX_VEL = self.fall_vel  

        if self.top_collision[0]:
            if self.top_collision[1].bottom_collide:
                self.rect.top = self.top_collision[1].rect.bottom
                self.bottom_velocity = physic.Rebound(self.bottom_velocity) # rebote con los bloques cuando mario los golpea

            else:
                if self.top_velocity < 0:
                    self.rect.y += int( self.top_velocity*group.time*delta_time )        

        if self.left_collision[0]:
            if self.left_collision[1].right_collide:
                self.rect.left = self.left_collision[1].rect.right
                self.left_velocity = 0
                self.right_velocity = self.walk_vel

            else:
                self.rect.x += int( self.left_velocity*group.time*delta_time )

        if self.right_collision[0]:
            if self.right_collision[1].left_collide: 
                self.rect.right = self.right_collision[1].rect.left
                self.left_velocity = self.walk_vel*-1
                self.right_velocity = 0
                

            else:
                self.rect.x += int( self.right_velocity*group.time*delta_time )


    def manage_enemy_collide(self):
        if self.enemy_left_collision[0]: #and isinstance(self, type(self.enemy_left_collision[1])):
            if self.enemy_left_collision[1].collide_enemy:# and self.enemy_left_collision[1].left_velocity == self.right_velocity:
                self.rect.left = self.enemy_left_collision[1].rect.right
                self.left_velocity = 0
                self.right_velocity = self.walk_vel

        if self.enemy_right_collision[0]: #and isinstance(self, type(self.enemy_right_collision[1])):
            if self.enemy_right_collision[1].collide_enemy:# and self.enemy_right_collision[1].right_velocity == self.left_velocity:
                self.rect.right = self.enemy_right_collision[1].rect.left
                self.left_velocity = self.walk_vel*-1
                self.right_velocity = 0


    def manage_player_collide(self):
        if self.player_left_collision[0]:
            self.player_left_collision[1].damage(self, (False, True))

        if self.player_right_collision[0]:
            self.player_right_collision[1].damage(self, (True, True))

        if self.player_bottom_collision[0]:
            self.player_bottom_collision[1].damage(self, (bool(random.randint(0, 1)), True))


        if self.player_top_collision[0]:
            if not self.can_smash:
                self.player_top_collision[1].damage(self, (bool(random.randint(0, 1)), True))


    def manage_collide(self, delta_time):
        self.manage_movement(delta_time)
        self.manage_enemy_collide()
        self.manage_player_collide()

    # Metodos micelaneos ------------------------------------------------------
    def screen_collide(self):
        if self.rect.y-48 > group.geometry[1]:
            try:
                self.animation.kill()
            except:
                pass
            self.collider.kill()
            self.kill()


    def smash(self, obj=None):
        if self.can_smash:
            try:
                self.animation.kill()
            except:
                pass
            self.collider.kill()
            self.kill()


    def death_jump(self, *direction):
        if self.can_death_jump:
            try:
                self.animation.kill()
            except:
                pass
            self.collider.kill()
            self.kill()


    def seam_collide(self):
        pass
        """
        if self.rect.x >= seam.seam-48:
            self.rect.x = seam.seam-48
        """


    def drop_point(self, score_=100):
        font.Generate_Point(str(score_), self.rect.x+3, self.rect.y)
        score.score += score_


    def update(self, delta_time):
        self.seam_collide()
        self.manage_velocity(delta_time)
        self.update_collider_2d(delta_time)
        self.manage_collide(delta_time)

        self.collider.update()


class Tortoise(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.is_hide = False
        self.is_round = False
        self.hide_time = group.Chronometer(10)

        self.run_vel = 11
        self.init_walk_vel = self.walk_vel
        self.walk_vel = self.init_walk_vel

        # animation ------------------------------------
        """
        self.animation = animation.Koopa_Troopa_Animartion(self)
        group.all_sprites.add(self.animation)

        self.palette = self.animation.palette
        self.sheet = self.animation.sheet.copy()
  
        self.c_i = (3, 4, 5)
        """


    def manage_enemy_collide(self):
        if not self.is_round:
            Enemy.manage_enemy_collide(self)

        else:
            if self.enemy_left_collision[0]:
                self.enemy_left_collision[1].death_jump(True, True)

            if self.enemy_right_collision[0]:
                self.enemy_right_collision[1].death_jump(False, True)


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
                self.bottom_velocity = 0

                if self.is_hide and not self.is_round:
                    self.left_velocity = 0
                    self.right_velocity = 0    

                if self.bottom_collision[1].is_rebound:
                    self.bottom_velocity = self.jump_force
                    if not self.is_hide:
                        self.animation.direction_y = True
                        self.smash()

                if self.bottom_velocity != 0 and self.is_hide and not self.is_round:
                    for player in group.player_sprites:
                        if player.rect.center[0] <= self.rect.center[0]:
                            self.left_velocity = 0
                            self.right_velocity = self.walk_vel

                        if player.rect.center[0] >= self.rect.center[0]:
                            self.left_velocity = self.walk_vel*-1
                            self.right_velocity = 0

                if self.bottom_collision[1].jump_board:
                    if self.bottom_collision[1].can_jump:
                        self.bottom_collision[1].jump()
                        self.bottom_velocity = self.jump_force

            else:
                if self.bottom_velocity > 0:
                    self.rect.y += int( self.bottom_velocity*group.time*delta_time )
                    self.bottom_MAX_VEL = self.fall_vel  

        if self.top_collision[0]:
            if self.top_collision[1].bottom_collide:
                self.rect.top = self.top_collision[1].rect.bottom
                self.bottom_velocity = physic.Rebound(self.bottom_velocity) # rebote con los bloques cuando mario los golpea

            else:
                if self.top_velocity < 0:
                    self.rect.y += int( self.top_velocity*group.time*delta_time )        

        if self.left_collision[0]:
            if self.left_collision[1].right_collide:
                self.rect.left = self.left_collision[1].rect.right

                if self.is_round and self.left_collision[1].breakable:
                    self.left_collision[1].break_tile()
                elif self.is_round and self.left_collision[1].can_rebound:
                    self.left_collision[1].rebound()
                else:
                    if self.is_round:
                        self.left_collision[1].bump()

                self.left_velocity = 0
                self.right_velocity = self.walk_vel

            else:
                self.rect.x += int( self.left_velocity*group.time*delta_time )

        if self.right_collision[0]:
            if self.right_collision[1].left_collide: 
                self.rect.right = self.right_collision[1].rect.left

                if self.is_round and self.right_collision[1].breakable:
                    self.right_collision[1].break_tile()
                elif self.is_round and self.right_collision[1].can_rebound:
                    self.right_collision[1].rebound()
                else:
                    if self.is_round:
                        self.right_collision[1].bump()

                self.left_velocity = self.walk_vel*-1
                self.right_velocity = 0

            else:
                self.rect.x += int( self.right_velocity*group.time*delta_time )


    def manage_player_collide(self):
        if not self.is_hide or self.is_round:
            Enemy.manage_player_collide(self)

        else:
            if self.player_left_collision[0]:
                self.round(self.player_left_collision[1])

            if self.player_right_collision[0]:
                self.round(self.player_right_collision[1])

            if self.player_bottom_collision[0]:
                self.player_bottom_collision[1].damage(self, (bool(random.randint(0, 1)), True))


    def controll_hide_time(self):
        if self.is_hide and not self.is_round:
            if self.hide_time.time_over():
                self.animation.direction_y = False
                self.hide_time.reset()
                self.is_hide = False
                self.is_round = False
                self.walk_vel = self.init_walk_vel

                if self.animation.direction_x:
                    self.left_velocity = self.walk_vel*-1
                    self.right_velocity = 0

                if not self.animation.direction_x:
                    self.left_velocity = 0
                    self.right_velocity = self.walk_vel


    def death_jump(self, *direction):
        if self.can_death_jump:
            sound.kick_sound.stop()
            sound.kick_sound.play()
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def smash(self, obj=None):
        if self.can_smash:
            if self.is_hide:
                if self.is_round:
                    self.is_hide = False

                if not self.is_round:
                    self.round(obj) 

            if not self.is_hide:
                self.hide()


    def round(self, obj):
        self.drop_point(400)
        sound.kick_sound.stop()
        sound.kick_sound.play()
        self.walk_vel = self.run_vel
        self.hide_time.reset()
        self.is_round = True
        if obj.rect.center[0] <= self.rect.center[0]:
            self.left_velocity = 0
            self.right_velocity = self.walk_vel

        if obj.rect.center[0] >= self.rect.center[0]:
            self.left_velocity = self.walk_vel*-1
            self.right_velocity = 0


    def hide(self):
        self.drop_point()
        sound.stomp_sound.stop()
        sound.stomp_sound.play()
        self.is_hide = True
        self.is_round = False
        #self.left_velocity  = 0
        #self.right_velocity = 0


    def update(self, delta_time):
        if not group.stop:
            self.controll_hide_time()
            Enemy.update(self, delta_time)
            self.animation.update_animation()


class Goomba(Enemy): ### #
    def __init__(self, x, y):
        super().__init__(x, y) 
        # animacion ------------------------------------------
        self.animation = animation.Goomba_Animation(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)

        self.sheet = self.animation.sheet.copy()


    def smash(self, obj=None):
        if self.can_smash:
            self.drop_point()
            sound.stomp_sound.stop()
            sound.stomp_sound.play()
            death_animation = animation.Death_Animation(self, ((65, 48, 16, 16), ), 300, self.rect.center[0], self.rect.center[1]+3 )
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def death_jump(self, *direction):
        if self.can_death_jump:
            self.drop_point()
            sound.kick_sound.stop()
            sound.kick_sound.play()
            death_animation = animation.Death_Jump(self, (81, 48, 16, 16), direction, -16)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def update(self, delta_time):
        if not group.stop:
            Enemy.update(self, delta_time)
            self.animation.update_animation()


class Koopa_Paratroopa_Green(Tortoise): ### #
    def __init__(self, x, y):
        super().__init__(x, y)
        self.can_fly = True

        # animation ---------------------------
        self.animation = animation.Koopa_Troopa_Paratroopa_Green_Animartion(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)

        self.sheet = self.animation.sheet.copy()


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
                if self.can_fly:
                    self.bottom_velocity = self.jump_force+2.5

                else:
                    self.bottom_MAX_VEL = 0
                    self.bottom_velocity = 0

                if self.is_hide and not self.is_round:
                    self.left_velocity = 0
                    self.right_velocity = 0    

                if self.bottom_collision[1].is_rebound:
                    self.bottom_velocity = self.jump_force
                    if not self.is_hide:
                        self.animation.direction_y = True
                        self.smash()

                if self.bottom_velocity != 0 and self.is_hide and not self.is_round:
                    for player in group.player_sprites:
                        if player.rect.center[0] <= self.rect.center[0]:
                            self.left_velocity = 0
                            self.right_velocity = self.walk_vel

                        if player.rect.center[0] >= self.rect.center[0]:
                            self.left_velocity = self.walk_vel*-1
                            self.right_velocity = 0

            else:
                if self.bottom_velocity > 0:
                    self.rect.y += int( self.bottom_velocity*group.time*delta_time )
                    self.bottom_MAX_VEL = self.fall_vel  

        if self.top_collision[0]:
            if self.top_collision[1].bottom_collide:
                self.rect.top = self.top_collision[1].rect.bottom
                self.bottom_velocity = physic.Rebound(self.bottom_velocity) # rebote con los bloques cuando mario los golpea

            else:
                if self.top_velocity < 0:
                    self.rect.y += int( self.top_velocity*group.time*delta_time ) 

        if self.left_collision[0]:
            if self.left_collision[1].right_collide:
                self.rect.left = self.left_collision[1].rect.right

                if self.is_round and self.left_collision[1].breakable:
                    self.left_collision[1].break_tile()
                elif self.is_round and self.left_collision[1].can_rebound:
                    self.left_collision[1].rebound()
                else:
                    if self.is_round:
                        self.left_collision[1].bump()

                self.left_velocity = 0
                self.right_velocity = self.walk_vel

            else:
                self.rect.x += int( self.left_velocity*group.time*delta_time )

        if self.right_collision[0]:
            if self.right_collision[1].left_collide: 
                self.rect.right = self.right_collision[1].rect.left

                if self.is_round and self.right_collision[1].breakable:
                    self.right_collision[1].break_tile()
                elif self.is_round and self.right_collision[1].can_rebound:
                    self.right_collision[1].rebound()
                else:
                    if self.is_round:
                        self.right_collision[1].bump()

                self.left_velocity = self.walk_vel*-1
                self.right_velocity = 0

            else:
                self.rect.x += int( self.right_velocity*group.time*delta_time )


    def death_jump(self, *direction):
        if self.can_death_jump:
            self.drop_point(200)
            sound.kick_sound.stop()
            sound.kick_sound.play()
            if not self.is_round:
                img_data = (130, 32, 16, 16)

            else:
                img_data = self.animation.sprite_states[self.animation.frame]

            death_animation = animation.Death_Jump(self, img_data, direction, -16)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def smash(self, obj=None):
        if self.can_smash:
            if self.can_fly:
                self.drop_point(200)
                sound.stomp_sound.stop()
                sound.stomp_sound.play()
                self.can_fly = False
                self.bottom_velocity = 0

            elif not self.can_fly:
                if self.is_hide:
                    if self.is_round:
                        self.is_hide = False

                    if not self.is_round:
                        self.round(obj)  

                if not self.is_hide:
                    self.hide()


class Koopa_Troopa_Green(Koopa_Paratroopa_Green): ### #
    def __init__(self, x, y):
        super().__init__(x, y)
        self.can_fly = False


class Koopa_Paratroopa_Red(Tortoise): ### #
    def __init__(self, x, y):
        super().__init__(x, y)
        self.collide_enemy = False
        self.can_fly = True
        self.fly_max_vel = 5

        self.fly_max_vel_top = 0
        self.fly_max_vel_bottom = 0

        self.top_y = y+48
        self.bottom_y = y+(48*3)

        # animation ---------------------------
        self.animation = animation.Koopa_Troopa_Paratroopa_Red_Animartion(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)

        self.animation.direction_x = True

        self.sheet = self.animation.sheet.copy()

        # detector ---------------------------
        self.detector = physic.Depression_Detector(self)

        self.left_velocity = 0
        self.right_velocity = 0


    def manage_velocity(self, delta_time):
        if not self.can_fly:
            if self.bottom_velocity >= 0: # La fuerza de gravedad cambia su velor dependiendo del signo de la velocidad
                self.gravity = group.gravity_in_down_GRASS

            if self.bottom_velocity < 0:
                self.gravity = group.gravity_in_up_GRASS

            self.top_velocity = 0 
            self.bottom_velocity = physic.Accelearted_Linear_Movement(self.bottom_velocity, delta_time, self.bottom_MAX_VEL, self.gravity, -.01, True) # acelerar/desacelerar
            

        if self.can_fly:
            self.gravity = 0.04
            if self.rect.y <= self.top_y:
                self.fly_max_vel_top = 0
                self.fly_max_vel_bottom = self.fly_max_vel

            if self.rect.y >= self.bottom_y:
                self.fly_max_vel_top =  self.fly_max_vel*-1
                self.fly_max_vel_bottom = 0
            

            self.top_velocity    = physic.Accelearted_Linear_Movement(self.top_velocity,   delta_time, self.fly_max_vel_top,     self.gravity*-1, self.gravity*2, False)
            self.bottom_velocity = physic.Accelearted_Linear_Movement(self.bottom_velocity, delta_time, self.fly_max_vel_bottom, self.gravity, self.gravity*-1*2, True)

    
    def manage_enemy_collide(self):
        if self.can_fly:
            pass

        else:
            Tortoise.manage_enemy_collide(self)

        
    def manage_depresion_collide(self):
        if not self.is_hide and not self.is_round and not self.can_fly:
            if not self.detector.left_detector.is_collide(group.tile_sprites):
                self.left_velocity = 0
                self.right_velocity = self.walk_vel


            if not self.detector.right_detector.is_collide(group.tile_sprites):
                self.left_velocity = self.walk_vel*-1
                self.right_velocity = 0


    def seam_collide(self):
        if self.can_fly:
            pass

        else:
            Tortoise.seam_collide(self)


    def death_jump(self, *direction):
        if self.can_death_jump:
            self.drop_point(200)
            sound.kick_sound.stop()
            sound.kick_sound.play()
            if not self.is_round:
                img_data = (130, 32, 16, 16)

            else:
                img_data = self.animation.sprite_states[self.animation.frame]

            death_animation = animation.Death_Jump(self, img_data, direction, -16)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def smash(self, obj=None):
        if self.can_smash:
            if self.can_fly:
                self.drop_point(200)
                sound.stomp_sound.stop()
                sound.stomp_sound.play()
                self.can_fly = False
                self.bottom_velocity = 0

            elif not self.can_fly:
                if self.is_hide:
                    if self.is_round:
                        self.is_hide = False

                    if not self.is_round:
                        self.round(obj)  

                if not self.is_hide:
                    self.hide()


    def update(self, delta_time):
        self.manage_depresion_collide()
        Tortoise.update(self, delta_time)
        self.detector.update()


class Koopa_Troopa_Red(Koopa_Paratroopa_Red): ### #
    def __init__(self, x, y):
        super().__init__(x, y)
        self.can_fly = False
        collide_enemy = True


class Buzzy_Beetle(Tortoise): ### #
    def __init__(self, x, y):
        super().__init__(x, y)
        self.can_fire_works = False

        # animation ----------------------------
        self.animation = animation.Buzzy_Beetle_Animation(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)

        self.sheet = self.animation.sheet.copy()


    def death_jump(self, *direction):
        if self.can_death_jump:
            self.drop_point(200)
            sound.kick_sound.stop()
            sound.kick_sound.play()
            if not self.is_round:
                img_data = (147, 16, 16, 16)

            else:
                img_data = self.animation.sprite_states[self.animation.frame]

            death_animation = animation.Death_Jump(self, img_data, direction, -16)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()


class Spiny(Tortoise): ### #
    def __init__(self, x, y):
        super().__init__(x, y)
        sound.kick_sound.stop()
        sound.kick_sound.play()
        self.can_smash = False
        self.collide_enemy = False
        self.touch_the_floor = False
        self.can_touch = True
        
        self.animation = animation.Spiny_Animation(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)
        
        self.sheet = self.animation.sheet.copy()

        self.left_velocity = 0
        self.right_velocity = 0
        self.bottom_velocity = self.jump_force/1.5


    def death_jump(self, *direction): 
        if self.can_death_jump:
            self.drop_point(200)
            sound.kick_sound.stop()
            sound.kick_sound.play()

            death_animation = animation.Death_Jump(self, (212, 16, 16, 16), direction, -16)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()

    
    def manage_enemy_collide(self):
        pass
        """
        if self.touch_the_floor:
            Enemy.manage_enemy_collide(self)
        """


    def smash(self, obj=None):
        self.bottom_velocity = self.jump_force/1.5
        self.animation.direction_y = False


    def update(self, delta_time):
        Tortoise.update(self, delta_time)
        if self.bottom_collision[0] and self.can_touch:
            self.touch_the_floor = True
            self.can_touch = False
            for player in group.player_sprites:
                if player.rect.center[0] <= self.rect.center[0]:
                    self.right_velocity = 0
                    self.left_velocity = self.walk_vel*-1
                    
                if player.rect.center[0] >= self.rect.center[0]:
                    self.right_velocity = self.walk_vel
                    self.left_velocity = 0


class Lakitu(Enemy): ### #
    def __init__(self, x, y):
        super().__init__(x, y)

        self.can_drop = group.Chronometer(2)

        self.animation = animation.Lakitu_Animation(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)
        
        self.sheet = self.animation.sheet.copy()

        self.left_top = 48
        self.rigth_top = group.geometry[0]-(48*4)

        self.walk_vel = 2

        self.screen_reound = False

        for player in group.player_sprites:
            self.player = player


    def manage_velocity(self, delta_time):
        if group.is_scroll and bool(int(self.player.left_velocity+self.player.right_velocity*group.time*delta_time)):
            self.screen_reound = False
            if self.player.KEY_K:
                self.right_velocity = self.run_vel

            else:
                self.right_velocity = self.player.walk_vel+2
            self.left_velocity  = 0

        else:
            if not self.screen_reound:
                self.right_velocity = 0
                self.left_velocity = self.walk_vel*-1


    def manage_movement(self, delta_time):
        self.rect.x += int( self.left_velocity*group.time*delta_time )

        self.rect.x += int( self.right_velocity*group.time*delta_time )

        if self.rect.left < self.left_top:
            self.rect.left = self.left_top
            self.left_velocity *= -1
            self.screen_reound = True

        if self.rect.right > self.rigth_top:
            self.rect.right = self.rigth_top
            if self.screen_reound:
                self.left_velocity *= -1


    def manage_enemy_collide(self):
        pass


    def drop_spiny(self):
        if self.can_drop.time_over():
            self.can_drop.reset()

            spiny = Spiny(self.rect.x, self.rect.y)
            group.all_sprites.add(spiny)
            group.enemy_sprites.add(spiny)


    def smash(self, obj=None):
        self.death_jump(obj.animation.direction_x, True)


    def death_jump(self, *direction):
        if self.can_death_jump:
            self.drop_point(200)
            sound.kick_sound.stop()
            sound.kick_sound.play()

            death_animation = animation.Death_Jump(self, (294, 0, 16, 32), (self.animation.direction_x, True), -16)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            death_animation.x_velocity = 0
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def update(self, delta_time):
        if not group.stop:
            Enemy.update(self, delta_time)
            self.drop_spiny()
            self.animation.update_animation()


class Bullet_Bill(Enemy): ### #
    def __init__(self, x, y):
        super().__init__(x, y)
        self.collide_enemy = False
        sound.fireworks_sound.stop()
        sound.fireworks_sound.play()

        self.image = pygame.Surface((48, 42))
        self.image.fill(color)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.walk_vel = 5
        for player in group.player_sprites:
            self.player = player

        if self.player.rect.center[0] <= self.rect.center[0]:
            self.left_velocity = self.walk_vel*-1
            self.right_velocity = 0

        if self.player.rect.center[0] >= self.rect.center[0]:
            self.left_velocity = 0
            self.right_velocity = self.walk_vel

        self.bottom_MAX_VEL = 0
        self.bottom_velocity = 0

        # animation -------------------------------------
        self.animation = animation.Bullet_Bill_Animation(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)

        self.sheet = self.animation.sheet.copy()


    def manage_enemy_collide(self):
        pass


    def manage_movement(self, delta_time):
        self.rect.y += int( self.bottom_velocity*group.time*delta_time )

        self.rect.y += int( self.top_velocity*group.time*delta_time )

        self.rect.x += int( self.left_velocity*group.time*delta_time )

        self.rect.x += int( self.right_velocity*group.time*delta_time )

        self.screen_collide()


    def screen_collide(self):
        if self.rect.x <= -240 or self.rect.x >= group.geometry[0]+240:
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def death_jump(self, *direction):
        if self.can_death_jump:
            self.drop_point(200)
            sound.kick_sound.stop()
            sound.kick_sound.play()
            death_animation = animation.Death_Jump(self, (130, 16, 16, 16), direction, -2)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            death_animation.x_velocity = 0
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def smash(self, obj=None):
        sound.stomp_sound.stop()
        sound.stomp_sound.play()
        self.death_jump(self.animation.direction_x, False)
        sound.kick_sound.stop()


    def update(self, delta_time):
        if not group.stop:
            Enemy.update(self, delta_time)
            self.animation.update_animation()


class Pirana_Plant_Green(Enemy): ### #
    def __init__(self, x, y, go):
        super().__init__(x, y)
        self.collide_enemy = False
        self.image = pygame.Surface((48, 48))
        self.image.fill(color)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x+24, y
        self.collider.top_collider.special_collide = False
        self.collider.resize()
        
        self.can_change = True
        self.inside = True
        self.can_smash = False
        self.go = go

        if not self.go:
            self.inside_y = self.rect.y+96
            self.outside_y = self.rect.y
            self.rect.y += 96

        if self.go:
            self.inside_y = self.rect.y-96
            self.outside_y = self.rect.y
            self.rect.y -= 96

        self.left_velocity   = 0
        self.right_velocity  = 0
        self.bottom_velocity = 10
        self.top_velocity    = -10
        self.bottom_MAX_VEL  = 0

        self.inside_time = group.Chronometer(2)
        self.inside_time.time = 0
        self.outside_time    = group.Chronometer(2)

        self.y_velocity = 0

        for player in group.player_sprites:
            self.player = player
       
        self.animation = animation.Pirana_Plant_Green_Animation(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)

        group.all_sprites.change_layer(self.animation, self.animation._layer-2)

        self.sheet = self.animation.sheet.copy()

        self.collider.update()


    def manage_timing(self):
        if self.inside:
            if abs(physic.get_distance(self.player, self)) >= 120:
                if self.inside_time.time_over():
                    self.inside_time.reset()
                    
                    self.inside = False

        if not self.inside:
            if self.outside_time.time_over():
                self.outside_time.reset()
                group.all_sprites.change_layer(self.animation, self.animation._layer-2)
                self.can_change = True
                self.inside = True


    def manage_velocity(self, delta_time):
        if not self.go:
            if self.inside:
                self.y_velocity = self.walk_vel

            if not self.inside:
                self.y_velocity = self.walk_vel*-1

        if self.go:
            if self.inside:
                self.y_velocity = self.walk_vel*-1

            if not self.inside:
                self.y_velocity = self.walk_vel


    def manage_enemy_collide(self):
        pass


    def manage_movement(self, delta_time):
        self.rect.y += int( self.y_velocity*group.time*delta_time )

        if not self.go:
            if self.rect.y <= self.outside_y:
                self.rect.y = self.outside_y
                if self.can_change:
                    group.all_sprites.change_layer(self.animation, self.animation._layer+2)
                    self.can_change = False

            if self.rect.y >= self.inside_y:
                self.rect.y = self.inside_y

        if self.go:
            if self.rect.y >= self.outside_y:
                self.rect.y = self.outside_y
                if self.can_change:
                    group.all_sprites.change_layer(self.animation, self.animation._layer+2)
                    self.can_change = False

            if self.rect.y <= self.inside_y:
                self.rect.y = self.inside_y

        self.screen_collide()


    def screen_collide(self):
        if self.rect.x <= -240:
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def seam_collide(self):
        pass


    def death_jump(self, *direction):
        if self.can_death_jump:
            self.drop_point(200)
            sound.kick_sound.stop()
            sound.kick_sound.play()
            death_animation = animation.Death_Jump(self, (243, 32, 16, 32), direction, -16)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def update(self, delta_time):
        if not group.stop:
            self.manage_timing()
            Enemy.update(self, delta_time)
            self.animation.update_animation()


class Hammer_Brother(Enemy): ### #
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = pygame.Surface((48, 69))
        self.image.fill(color)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        #self.collider.bottom_collider.special_bottom_collide = False
        self.collider.resize()

        self.left_velocity = 0
        self.right_velocity = 0

        self.jump_time = group.Chronometer(3)
        self.jump_count = 0
        self.jump_limit = 13
        self.can_across = False
        self.reset_across = False
        self.can_jump = True
        self.mul_val = 1

        self.drop_time = group.Chronometer(1)
        self.reset_time = group.Chronometer(1)

        self.drop_hammer_count = 0

        self.fall_force = self.jump_force/2
        self.y_force = self.fall_force

        for player in group.player_sprites:
            self.player = player

        # animation -----------------------------------
        self.animation = animation.Hammer_Brother_Aniamtion(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)
        self.sheet = self.animation.sheet.copy()


    def manage_across(self):
        if self.can_across:
            if self.bottom_collision[0] or self.top_collision[0]:
                self.reset_across = True

            if self.reset_across:
                if not self.bottom_collision[0] and not self.top_collision[0] and not self.left_collision[0] and not self.right_collision[0]:
                    self.reset_across = False
                    self.can_across   = False


    def manage_velocity(self, delta_time):
        if self.jump_count >= self.jump_limit:
            if self.player.rect.center[0]+144 <= self.rect.center[0]:
                self.right_velocity = 0
                self.left_velocity  = self.walk_vel*-1

            if self.player.rect.center[0]-144 >= self.rect.center[0]:
                self.right_velocity = self.walk_vel
                self.left_velocity  = 0
    
        Enemy.manage_velocity(self, delta_time)


    def manage_movement(self, delta_time):
        if self.can_across:
            if not self.bottom_collision[0]:
                self.bottom_MAX_VEL = self.fall_vel
            self.rect.y += int( self.bottom_velocity*group.time*delta_time )
            self.rect.y += int( self.top_velocity*group.time*delta_time )
            self.rect.x += int( self.left_velocity*group.time*delta_time )
            self.rect.x += int( self.right_velocity*group.time*delta_time )

            if self.rect.bottom > 624:
                self.can_across = False
                self.reset_across = False

        if not self.can_across:
            if not self.bottom_collision[0]:
                self.rect.y += int( self.bottom_velocity*group.time*delta_time )
                self.bottom_MAX_VEL = self.fall_vel

            if not self.top_collision[0]:
                self.rect.y += int( self.top_velocity*group.time*delta_time )

            if not self.left_collision[0]:
                self.rect.x += int( self.left_velocity*group.time*delta_time )

            if not self.right_collision[0]:
                self.rect.x += int( self.right_velocity*group.time*delta_time )


            if self.bottom_collision[0]:
                if self.bottom_collision[1].top_collide: # Revisar si las colisiones del bloque estan activadas
                    self.rect.bottom = self.bottom_collision[1].rect.top
                    self.bottom_MAX_VEL = 0
                    self.bottom_velocity = 0
                    self.can_jump = True

                    if self.bottom_collision[1].is_rebound:
                        self.death_jump(bool(random.randint(0, 1)), True)

                else:
                    if self.bottom_velocity > 0:
                        self.rect.y += int( self.bottom_velocity*group.time*delta_time )
                        self.bottom_MAX_VEL = self.fall_vel  

            if self.top_collision[0]:
                if self.top_collision[1].bottom_collide:
                    self.rect.top = self.top_collision[1].rect.bottom
                    self.bottom_velocity = physic.Rebound(self.bottom_velocity) # rebote con los bloques cuando mario los golpea

                else:
                    if self.top_velocity < 0:
                        self.rect.y += int( self.top_velocity*group.time*delta_time )        

            if self.left_collision[0]:
                if self.left_collision[1].right_collide:
                    self.rect.left = self.left_collision[1].rect.right
                    self.jump()

                else:
                    self.rect.x += int( self.left_velocity*group.time*delta_time )

            if self.right_collision[0]:
                if self.right_collision[1].left_collide: 
                    self.rect.right = self.right_collision[1].rect.left
                    self.jump()

                else:
                    self.rect.x += int( self.right_velocity*group.time*delta_time )
            
        self.screen_collide()


    def manage_enemy_collide(self):
        pass


    def seam_collide(self):
        pass


    def jump(self):
        if self.can_jump:
            self.bottom_velocity = self.jump_force
            self.can_jump = False
       

    def manage_jump(self):
        if self.jump_count < self.jump_limit:
            if self.jump_time.time_over():
                self.jump_time.reset()
                self.jump_count += 1
                
                if self.jump_count/4 == float(self.mul_val):
                    self.mul_val += 1
                    if bool(int(random.randint(0, 2))):
                        if self.y_force == self.jump_force:
                            self.can_across = True
                            self.y_force = self.fall_force
                            self.bottom_velocity = self.y_force

                        elif self.y_force == self.fall_force:
                            self.can_across = True
                            self.y_force = self.jump_force
                            self.bottom_velocity = self.y_force


                if self.y_force == self.jump_force:
                    self.can_across = True
                    self.y_force = self.fall_force
                    self.bottom_velocity = self.y_force

                elif self.y_force == self.fall_force:
                    self.can_across = True
                    self.y_force = self.jump_force
                    self.bottom_velocity = self.y_force

        else:
            self.can_across = False


    def drop_hammer(self):
        if self.reset_time.time_over():
            if self.drop_time.time_over():
                self.drop_hammer_count +=1
                self.drop_time.reset()
                hammer = Hammer(self.rect.x, self.rect.y, self.animation.direction_x)

                if physic.get_distance(self, self.player, True) < 336:
                    if self.jump_count < self.jump_limit:
                        mul_val = 1

                    else:
                        mul_val = 2
                    
                    hammer.walk_vel = abs(int(physic.get_distance(self, self.player, True)/48))*mul_val
                    if hammer.direction:
                        hammer.left_velocity = hammer.walk_vel*-1
                        hammer.right_velocity = 0 

                    if not hammer.direction:
                        hammer.left_velocity = 0
                        hammer.right_velocity = hammer.walk_vel

                group.all_sprites.add(hammer)
                group.enemy_sprites.add(hammer)

                if self.drop_hammer_count >= 2:
                    self.reset_time.reset()
                    self.drop_hammer_count = 0


    def death_jump(self, *direction):
        if self.can_death_jump:
            self.drop_point(1000)
            sound.kick_sound.stop()
            sound.kick_sound.play()
            death_animation = animation.Death_Jump(self, (277, 0, 16, 32), direction, -9)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            death_animation.x_velocity = 0
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.animation_hammer.kill()
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def smash(self, obj=None):
        if self.can_smash:
            sound.stomp_sound.stop()
            sound.stomp_sound.play()
            self.death_jump(self.animation.direction_x, True)
            sound.kick_sound.stop()


    def update(self, delta_time):
        if not group.stop:
            self.manage_across()
            self.manage_jump()
            Enemy.update(self, delta_time)
            self.drop_hammer()
            self.animation.update_animation(delta_time)


class Hammer(Enemy): #
    def __init__(self, x, y, direction):
        super().__init__(x, y)
        self.collide_enemy = False
        sound.kick_sound.stop()
        sound.kick_sound.play()
        self.image = pygame.Surface((24, 24))
        self.image.fill(color)
        self.image.set_colorkey((0, 0, 0))
        self.collider.resize()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.direction = direction

         # Fuerzas de velocidad -------------------------------------------
        self.walk_vel = 5
        if self.direction:
            self.left_velocity = self.walk_vel*-1
            self.right_velocity = 0 

        if not self.direction:
            self.left_velocity = 0
            self.right_velocity = self.walk_vel

        self.jump_force = -8

        self.top_velocity    = 0
        self.bottom_velocity = self.jump_force

        self.gravity = 0
        self.bottom_MAX_VEL = 12

        # animation ------------------------------------------------------
        self.animation = animation.Hammer_Animation(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)

        self.sheet = self.animation.sheet.copy()


    def manage_movement(self, delta_time):
        self.rect.y += int( self.bottom_velocity*group.time*delta_time )
        self.rect.y += int( self.top_velocity*group.time*delta_time )
        self.rect.x += int( self.left_velocity*group.time*delta_time )
        self.rect.x += int( self.right_velocity*group.time*delta_time )

        self.screen_collide()


    def death_jump(self, *direction):
        if self.can_death_jump:
            self.drop_point(200)
            sound.kick_sound.stop()
            sound.kick_sound.play()
            death_animation = animation.Death_Jump(self, (16, 80, 16, 16), direction, -2)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            death_animation.x_velocity = 0
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def manage_enemy_collide(self):
        pass


    def smash(self, obj=None):
        sound.stomp_sound.stop()
        sound.stomp_sound.play()
        self.death_jump(self.animation.sprite_object.direction, True)
        sound.kick_sound.stop()


    def update(self, delta_time):
        if not group.stop:
            Enemy.update(self, delta_time)
            self.animation.update_animation()


class Fire_Ball(Hammer):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        sound.kick_sound.stop()
        sound.fireball_sound.stop()
        sound.fireball_sound.play()
        
        self.can_smash = False
        self.animation.sprite_states = ((40, 96), (32, 104), (40, 104), (32, 96),)
        self.animation.conv = (24, 24)
        self.animation.geometry = (8, 8)
        self.jump_force = -18

        
        self.walk_vel = 12
        if self.direction:
            self.left_velocity = self.walk_vel*-1
            self.right_velocity = 0 

        if not self.direction:
            self.left_velocity = 0
            self.right_velocity = self.walk_vel
        
        

    def manage_velocity(self, delta_time):
        self.bottom_velocity = physic.Accelearted_Linear_Movement(self.bottom_velocity, delta_time, self.bottom_MAX_VEL, group.gravity_in_down_GRASS, -0.1, True)

   
    def smash(self, obj=None):
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

        self.animation.kill()
        self.collider.kill()
        self.kill()


    def death_jump(self, *direction):
        if self.can_death_jump:
            sound.kick_sound.stop()
            sound.kick_sound.play()
            self.animation.kill()
            self.collider.kill()
            self.kill()


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
                self.bottom_velocity = self.jump_force

                if self.bottom_collision[1].is_rebound:
                    self.death_jump(bool(random.randint(0, 1)), True)

            else:
                if self.bottom_velocity > 0:
                    self.rect.y += int( self.bottom_velocity*group.time*delta_time )
                    self.bottom_MAX_VEL = self.fall_vel  

    
        if self.left_collision[0]:
            if self.left_collision[1].right_collide:
                self.rect.left = self.left_collision[1].rect.right
                self.smash()

            else:
                self.rect.x += int( self.left_velocity*group.time*delta_time )

        if self.right_collision[0]:
            if self.right_collision[1].left_collide: 
                self.rect.right = self.right_collision[1].rect.left
                self.smash()
                

            else:
                self.rect.x += int( self.right_velocity*group.time*delta_time )


class Fireball_Brother(Hammer_Brother):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.can_fire_works = False

        self.animation.image_pixel_array = pygame.PixelArray(self.animation.sheet)
        self.animation.image_pixel_array.replace( self.animation.palette[self.animation.index][3], self.animation.palette[0][3] )
        self.animation.image_pixel_array.replace( self.animation.palette[self.animation.index][4], self.animation.palette[0][6] )
        self.animation.image_pixel_array.replace( self.animation.palette[self.animation.index][5], self.animation.palette[0][5] )

        self.sheet = self.animation.sheet.copy()
        self.animation.can_display = False


    def drop_hammer(self):
        if self.reset_time.time_over():
            if self.drop_time.time_over():
                self.drop_hammer_count +=1
                self.drop_time.reset()
                hammer = Fire_Ball(self.rect.x, self.rect.y, self.animation.direction_x)
                group.all_sprites.add(hammer)
                group.enemy_sprites.add(hammer)

                if self.drop_hammer_count >= 2:
                    self.reset_time.reset()
                    self.drop_hammer_count = 0


class Bloober(Enemy): ### #
    def __init__(self, x, y):
        super().__init__(x, y)
        self.can_smash = False
        self.collide_enemy = False
        self.image = pygame.Surface((48, 48))
        self.image.fill(color)
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        self.left_velocity = 0
        self.right_velocity = 0
        self.jump_force = -6
        self.fall_vel   = 2

        self.can_jump = True
        self.jump_time = group.Chronometer_Continuous(1)

        for player in group.player_sprites:
            self.player = player

        self.animation = animation.Bloober_Animation(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)

        self.sheet = self.animation.sheet.copy()


    def manage_velocity(self, delta_time):
        if self.bottom_velocity >= 0: # La fuerza de gravedad cambia su velor dependiendo del signo de la velocidad
            self.right_velocity = 0
            self.left_velocity  = 0
            self.gravity = group.gravity_in_down_WATHER

        if self.bottom_velocity < 0:
            self.gravity = group.gravity_in_up_WATHER

        self.bottom_velocity = physic.Accelearted_Linear_Movement(self.bottom_velocity, delta_time, self.bottom_MAX_VEL, self.gravity, -.01, True) # acelerar/desacelerar

        if self.can_jump:
            if self.player.rect.center[0] <= self.rect.center[0]:
                self.right_velocity = 0
                self.left_velocity  = self.walk_vel*-1

            if self.player.rect.center[0] >= self.rect.center[0]:
                self.right_velocity = self.walk_vel
                self.left_velocity = 0

            self.bottom_velocity = self.jump_force
            self.can_jump = False


    def manage_movement(self, delta_time):
        self.rect.y += int( self.bottom_velocity*group.time*delta_time )

        self.rect.y += int( self.top_velocity*group.time*delta_time )

        self.rect.x += int( self.left_velocity*group.time*delta_time )

        self.rect.x += int( self.right_velocity*group.time*delta_time )

        self.screen_collide()


    def manage_enemy_collide(self):
        pass


    def manage_jump(self):
        if not self.can_jump:
            self.bottom_MAX_VEL = self.fall_vel
            if self.jump_time.time_over():
                if self.player.rect.top-6 <= self.rect.bottom+24:
                    self.jump_time.reset()
                    self.can_jump = True


    def resize(self, val_bool):
        x = self.rect.x
        y = self.rect.y

        if val_bool:
            self.image = pygame.Surface((48, 48))
            self.image.fill(color)
            self.image.set_colorkey((0, 0, 0))

            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y

        else:
            self.image = pygame.Surface((48, 72))
            self.image.fill(color)
            self.image.set_colorkey((0, 0, 0))

            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = x, y


    def death_jump(self, *direction):
        if self.can_death_jump:
            self.drop_point(200)
            sound.kick_sound.stop()
            sound.kick_sound.play()
            death_animation = animation.Death_Jump(self, (113, 8, 16, 24), direction, -16)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def update(self, delta_time):
        if not group.stop:
            self.manage_jump()
            Enemy.update(self, delta_time)
            self.animation.update_animation()

            if self.rect.y <= 96:
                self.rect.y = 96
            

class Cheep_Cheep_Wather(Enemy): ### #
    def __init__(self, x, y, val_bool):
        super().__init__(x, y)
        self.collide_enemy = False
        if not val_bool:
            self.walk_vel = self.walk_vel/1.3
        self.right_velocity = 0
        self.left_velocity = self.walk_vel*-1

        self.bottom_velocity = 0

        self.y_top    = y
        self.y_bottom = y+48

        if not val_bool:
            self.animation = animation.Cheep_Cheep_Green_Animation(self)

        else:
            self.animation = animation.Cheep_Cheep_Red_Animation(self)

        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)
        self.sheet = self.animation.sheet.copy()


    def manage_velocity(self, delta_time):
        pass


    def manage_enemy_collide(self):
        pass


    def death_jump(self, *direction):
        if self.can_death_jump:
            self.drop_point(200)
            sound.kick_sound.stop()
            sound.kick_sound.play()
            death_animation = animation.Death_Jump(self, (80, 16, 16, 16), direction, -16)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def smash(self, obj=None):
        if self.can_smash:
            self.drop_point(200)
            sound.kick_sound.stop()
            sound.kick_sound.play()
            death_animation = animation.Death_Jump(self, (80, 16, 16, 16), (self.animation.direction_x, True), -2)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            death_animation.x_velocity = 0
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def manage_movement(self, delta_time):
        self.rect.y += int( self.bottom_velocity*group.time*delta_time )
        self.rect.y += int( self.top_velocity*group.time*delta_time )
        self.rect.x += int( self.left_velocity*group.time*delta_time )
        self.rect.x += int( self.right_velocity*group.time*delta_time )

        self.screen_collide()


    def update(self, delta_time):
        if not group.stop:
            Enemy.update(self, delta_time)
            self.animation.update_animation()


class Cheep_Cheep_Grass(Enemy): ### # Corregir su posicición !!!!!
    def __init__(self, x, y):
        super().__init__(x, y)
        self.jump_force = -21
        self.bottom_velocity = self.jump_force
        self.bottom_MAX_VEL = self.fall_vel
        self.collide_enemy = False

        self.rect.x = random.randrange(48, 672, 48)

        self.walk_vel += 1

        """

        for player in group.player_sprites:
            if player.rect.center[0] <= self.rect.center[0]:
                self.right_velocity = 0
                if not bool(int(player.left_velocity)):
                    self.left_velocity = self.walk_vel*-1
                else:
                    self.left_velocity = player.left_velocity-1
                
            if player.rect.center[0] >= self.rect.center[0]:
                if not bool(int(player.right_velocity)):
                    self.right_velocity = self.walk_vel
                else:  
                    self.right_velocity = player.right_velocity+1
                self.left_velocity = 0

        """
        self.left_velocity = 0
        self.right_velocity = self.walk_vel

        self.animation = animation.Cheep_Cheep_Red_Animation(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)

        self.sheet = self.animation.sheet.copy()


    def manage_enemy_collide(self):
        pass


    def manage_movement(self, delta_time):
        self.rect.y += int( self.bottom_velocity*group.time*delta_time )
        self.rect.y += int( self.top_velocity*group.time*delta_time )
        self.rect.x += int( self.left_velocity*group.time*delta_time )
        self.rect.x += int( self.right_velocity*group.time*delta_time )


    def screen_collide(self):
        if self.rect.top-48 >= group.geometry[0]:
            try:
                self.animation.kill()

            except:
                pass

            self.collider.kill()
            self.kill()


    def death_jump(self, *direction):
        if self.can_death_jump:
            self.drop_point(200)
            sound.kick_sound.stop()
            sound.kick_sound.play()
            death_animation = animation.Death_Jump(self, (80, 16, 16, 16), direction, -16)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def smash(self, obj=None):
        if self.can_smash:
            self.drop_point(200)
            sound.kick_sound.stop()
            sound.kick_sound.play()
            death_animation = animation.Death_Jump(self, (80, 16, 16, 16), (self.animation.direction_x, True), -2)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            death_animation.x_velocity = 0
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def update(self, delta_time):
        if not group.stop:
            Enemy.update(self, delta_time)
            self.animation.update_animation()


class Podoboo(Enemy): ### #
    def __init__(self, x, y, jump_force): # random.randint(1, 10), 1, ......... 
        super().__init__(x+18, y)
        self.can_smash = False
        self.can_fire_works = False
        self.collide_enemy = False
        self.right_velocity = 0
        self.left_velocity  = 0

        # print( y, (group.geometry[1]-y)/24 )
        # print(  18/  math.log(18, (group.geometry[1]-y)/24 )  )

        # self.jump_force = 18*-1 #( physic.convert(jump_force[0]) + physic.convert(jump_force[1]) )  *-1
        self.jump_force =  int(18/  math.log(18, (group.geometry[1]-y)/24 ) ) *-1

        print(self.jump_force)
    

        self.can_jump = True
        self.wait_time = group.Chronometer(int(self.jump_force/4)*-1 )
        self.wait_time.time = 0
        self.one_jump = False
        self.jump_count = 0
        self.jump_limit = random.randint(1, 10)

        self.bottom_MAX_VEL = self.fall_vel

        # animartion -------------------------------------------------------------
        self.animation = animation.Podoboo_Animation(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)

        self.sheet = self.animation.sheet.copy()


    def manage_jump(self):
        if self.wait_time.time_over():
            if self.can_jump:
                if self.one_jump:
                    self.wait_time.reset()
                    self.one_jump = False
                    self.jump_limit = random.randint(1, 10)

                elif not self.one_jump:
                    if not self.jump_count >= self.jump_limit:
                        self.jump_count += 1

                    else:
                        self.jump_count = 0
                        self.wait_time.reset()
                        self.one_jump = True

                self.bottom_velocity = self.jump_force
                self.can_jump = False

            if not self.can_jump:
                if self.rect.y >= group.geometry[1]+48:
                    self.can_jump = True


    def manage_movement(self, delta_time):
        self.rect.y += int( self.bottom_velocity*group.time*delta_time )
        self.rect.y += int( self.top_velocity*group.time*delta_time )
        self.rect.x += int( self.left_velocity*group.time*delta_time )
        self.rect.x += int( self.right_velocity*group.time*delta_time )

        if self.rect.y >= group.geometry[1]+48:
            self.rect.y = group.geometry[1]+48

        
    def manage_enemy_collide(self):
        pass

    
    def death_jump(self, *direction):
        if self.can_death_jump:
            self.drop_point(200)
            sound.kick_sound.stop()
            sound.kick_sound.play()
            death_animation = animation.Death_Jump(self, (65, 0, 16, 16), (direction[0], self.animation.direction_y), -16)
            death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
            group.all_sprites.add(death_animation)
            group.death_sprites.add(death_animation)
            self.animation.kill()
            self.collider.kill()
            self.kill()


    def update(self, delta_time):
        if not group.stop:
            self.manage_jump()
            Enemy.update(self, delta_time)
            self.animation.update_animation()


class Spinning_Fire_Ball(Enemy):
    def __init__(self, sprite_object, distance, angle, direction_to_rotate):
        super().__init__(0, 0)
        self.can_death_jump = False
        self.can_fire_works = False
        self.can_smash      = False
        self.collide_enemy  = False
        self.sprite_object = sprite_object
        self.angle = angle
        
        self.distance = distance
        self.direction = True
        self.direction_to_rotate = direction_to_rotate

        self.angle_vel = 2

        if not self.direction_to_rotate:
            self.angle_vel *= -1

        self.image = pygame.Surface((24, 24))
        self.image.fill(color)
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()

        self.rect.center = (self.sprite_object.rect.center[0] + math.sin(math.radians(int(self.angle))) *self.distance, 
                            self.sprite_object.rect.center[1] + math.cos(math.radians(int(self.angle))) *self.distance)

        #self.rect.x = self.sprite_object.rect.x + math.sin(math.radians(int(self.angle))) *48
        #self.rect.y = self.sprite_object.rect.y + math.cos(math.radians(int(self.angle))) *48

        self.collider.resize()
        
        # animation --------------------------------------------------------------------------
        self.animation = animation.Hammer_Animation(self)
        self.animation.sprite_states = ((40, 96), (32, 104), (40, 104), (32, 96),)
        self.animation.conv = (24, 24)
        self.animation.geometry = (8, 8)
        self.animation.update_animation()
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)
        self.sheet = self.animation.sheet.copy()


    def manage_enemy_collide(self):
        pass


    def manage_movement(self, delta_time):
        pass


    def update(self, delta_time):
        if not group.stop:
            Enemy.update(self, delta_time)
            self.angle += self.angle_vel*group.time*delta_time

            self.rect.center = (self.sprite_object.rect.center[0] + math.sin(math.radians(int(self.angle))) *self.distance, 
                                self.sprite_object.rect.center[1] + math.cos(math.radians(int(self.angle))) *self.distance)

            self.animation.update_animation()


class Bowser_Fire(Enemy): ### 
    def __init__(self, x, y, direction):
        super().__init__(x, y)
        sound.bowserfire_sound.stop()
        sound.bowserfire_sound.play()
        self.can_smash = False
        self.can_death_jump = False
        self.can_fire_works = False
        self.collide_enemy = False

        self.image = pygame.Surface((12, 12))
        self.image.fill(color)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.collider.resize()
        

        if bool(int(random.randint(0, 1))):
            self.y_velocity = self.walk_vel*-1
            self.y_limit = self.rect.y -48


        else:
            self.y_velocity = self.walk_vel
            self.y_limit = self.rect.y +48

        self.direction = direction

        self.left_velocity  = 0
        self.right_velocity = 0

        self.walk_vel = 3

        if not self.direction:
            self.right_velocity = self.walk_vel

        if self.direction:
            self.left_velocity = self.walk_vel*-1

        self.animation = animation.Bowser_Fire_Animation(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)
        

    def manage_velocity(self, delta_time):
        pass


    def manage_movement(self, delta_time):
        self.rect.x += int( self.left_velocity*group.time*delta_time )
        self.rect.x += int( self.right_velocity*group.time*delta_time )
        
        if self.y_velocity < 0:
            if not self.rect.y <= self.y_limit:
                self.rect.y += int(self.y_velocity*group.time*delta_time)

            else:
                self.rect.y = self.y_limit


        if self.y_velocity > 0:
            if not self.rect.y >= self.y_limit:
                self.rect.y += int(self.y_velocity*group.time*delta_time)

            else:
                self.rect.y = self.y_limit        


    def manage_enemy_collide(self):
        pass


    def update(self, delta_time):
        if not group.stop:
            Enemy.update(self, delta_time)
            self.animation.update_animation()


class Bowser(Enemy): ### #
    def __init__(self, x, y, texture=None, sprite_object=None, can_hammer_drop=False):
        super().__init__(x, y)
        self.texture = texture
        self.sprite_object = sprite_object
        self.can_hammer_drop = can_hammer_drop
        self.collide_enemy = False
        self.direction = True

        if self.sprite_object == None:
            self.texture = self.texture[1]/16
            self.image = pygame.Surface((42, 69))
            self.sprite_object = Bowser(x, y, None, self)
            group.all_sprites.add(self.sprite_object)
            group.enemy_sprites.add(self.sprite_object)

            self.tile_obj = tile.No_Solid_Tile(x, y, (288, 16))
            group.all_sprites.add(self.tile_obj)
            group.background_sprites.add(self.tile_obj)

            self.body = True
            
        else:
            self.image = pygame.Surface((36, 36))

            self.body = False

        self.image.fill(color)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.collider.resize()

        for player in group.player_sprites:
            self.player = player

        self.live = 5
        self.can_move = True

        # time -------------------------------
        self.time_to_drop_fire = group.Chronometer(3)
        self.tick_to_drop_fire = group.Chronometer_Continuous(1)

        self.time_to_drop_hammer = group.Chronometer(random.randrange(10, 15)/10)
        self.tick_to_drop_hammer = group.Chronometer_Continuous(.1)

        self.time_to_jump = group.Chronometer_Continuous(random.randrange(10, 30)/10)

        self.time_to_stop = group.Chronometer_Continuous(random.randrange(10, 50)/10)
        self.tick_to_stop = group.Chronometer_Continuous(1)

        #self.time_to_stop = group.Chronometer_Continuous()

        # count ------------------------------
        self.one_fire_drop   = True
        self.fire_drop_count = 1
        self.hammer_drop_count = 10

        self.jump_force = -6
        self.walk_vel   = 1

        self.left_velocity = 0
        self.right_velocity = self.walk_vel


        if self.body:
            # animartion -------------------------------------------------------------
            self.animation = animation.Bowser_Animation(self)
            group.all_sprites.add(self.animation)
            group.animation_sprites.add(self.animation)

            self.sheet = self.animation.sheet.copy()
        

    def manage_velocity(self, delta_time):
        if self.bottom_velocity >= 0: # La fuerza de gravedad cambia su velor dependiendo del signo de la velocidad
            self.gravity = group.gravity_in_down_WATHER

        if self.bottom_velocity < 0:
            self.gravity = group.gravity_in_up_WATHER

        self.bottom_velocity = physic.Accelearted_Linear_Movement(self.bottom_velocity, delta_time, self.bottom_MAX_VEL, self.gravity, -.01, True) # acelerar/desacelerar

        if self.rect.x <= self.tile_obj.rect.x-192:
            self.left_velocity  = 0
            self.right_velocity = self.walk_vel

        if self.rect.x >= self.tile_obj.rect.x+192:
            self.left_velocity  = self.walk_vel*-1
            self.right_velocity = 0

        if not self.direction:
            self.can_move = True
            self.left_velocity = 0
            self.right_velocity = self.walk_vel

    
    def manage_movement(self, delta_time):
        if not self.bottom_collision[0]:
            self.rect.y += int( self.bottom_velocity*group.time*delta_time )
            self.bottom_MAX_VEL = self.fall_vel

        if not self.top_collision[0]:
            self.rect.y += int( self.top_velocity*group.time*delta_time )

        if not self.left_collision[0]:
            if self.can_move:
                self.rect.x += int( self.left_velocity*group.time*delta_time )

        if not self.right_collision[0]:
            if self.can_move:
                self.rect.x += int( self.right_velocity*group.time*delta_time )

        self.screen_collide()

        if self.bottom_collision[0]:
            if self.bottom_collision[1].top_collide: # Revisar si las colisiones del bloque estan activadas
                self.rect.bottom = self.bottom_collision[1].rect.top
                self.bottom_MAX_VEL = 0
                self.bottom_velocity = 0

                if self.bottom_collision[1].is_rebound:
                    self.bottom_velocity = self.jump_force
                    self.time_to_jump.reset(random.randrange(10, 30)/10)

                if self.bottom_collision[1].jump_board:
                    if self.bottom_collision[1].can_jump:
                        self.bottom_collision[1].jump()
                        self.bottom_velocity = self.jump_force

            else:
                if self.bottom_velocity > 0:
                    self.rect.y += int( self.bottom_velocity*group.time*delta_time )
                    self.bottom_MAX_VEL = self.fall_vel  

        if self.top_collision[0]:
            if self.top_collision[1].bottom_collide:
                self.rect.top = self.top_collision[1].rect.bottom
                self.bottom_velocity = physic.Rebound(self.bottom_velocity) # rebote con los bloques cuando mario los golpea

            else:
                if self.top_velocity < 0:
                    self.rect.y += int( self.top_velocity*group.time*delta_time )        

        if self.left_collision[0]:
            if self.left_collision[1].right_collide:
                self.rect.left = self.left_collision[1].rect.right
            else:
                if self.can_move:
                    self.rect.x += int( self.left_velocity*group.time*delta_time )

        if self.right_collision[0]:
            if self.right_collision[1].left_collide: 
                self.rect.right = self.right_collision[1].rect.left

            else:
                if self.can_move:
                    self.rect.x += int( self.right_velocity*group.time*delta_time )


    def manage_enemy_collide(self):
        pass


    def controll_direction(self):
        if self.rect.left >= self.player.rect.right:
            self.direction = True
            self.sprite_object.direction = True
        

        if self.rect.right <= self.player.rect.left:
            self.direction = False
            self.sprite_object.direction = False


    def controll_position(self):
        if self.direction:
            self.rect.right = self.sprite_object.rect.left

        if not self.direction:
            self.rect.left  = self.sprite_object.rect.right

        self.rect.bottom = self.sprite_object.rect.top+21


    def controll_drop_fire(self):
        if self.time_to_drop_fire.time_over():
            if self.tick_to_drop_fire.time_over():
                if self.direction:
                    x_plus = -57

                if not self.direction:
                    x_plus = 96

                fire = Bowser_Fire(self.rect.x+x_plus, self.rect.y-6, self.direction)
                group.all_sprites.add(fire)
                group.enemy_sprites.add(fire)
                self.fire_drop_count -= 1
                self.tick_to_drop_fire.reset()
            
            if self.fire_drop_count <= 0:
                self.time_to_drop_fire.reset()

                if self.one_fire_drop:
                    self.one_fire_drop = False
                    self.fire_drop_count = random.randrange(2, 5)

                else:
                    self.one_fire_drop = True
                    self.fire_drop_count = 1


    def controll_drop_hammer(self):
        if self.can_hammer_drop:
            if self.time_to_drop_hammer.time_over():
                if self.tick_to_drop_hammer.time_over():
                    self.hammer_drop_count -= 1

                    hammer = Hammer(self.rect.x, self.rect.y, self.direction)
                    group.all_sprites.add(hammer)
                    group.enemy_sprites.add(hammer)
                    self.tick_to_drop_hammer.reset()

                if self.hammer_drop_count <= 0:
                    self.time_to_drop_hammer.reset(random.randrange(10, 15)/10)
                    self.hammer_drop_count = 10


    def controll_jump(self):
        if self.time_to_jump.time_over():
            self.bottom_velocity = self.jump_force
            self.time_to_jump.reset(random.randrange(10, 30)/10)


    def controll_stop(self):
        if self.time_to_stop.time_over():
            self.can_move = False
            if self.tick_to_stop.time_over():
                self.can_move = True
                self.time_to_stop.reset(random.randrange(10, 50)/10)
                self.tick_to_stop.reset()


    def smash(self, obj=None):
        pass
        #sound.stomp_sound.stop()
        #sound.stomp_sound.play()
        #self.death_jump( (bool(int(random.randint(0, 1)))), True )
        

    def death_jump(self, *direction):
        if self.can_death_jump:
            if self.body:
                self.live -= 1

                if self.live <= 0:
                    self.drop_point(5000)
                    sound.stomp_sound.stop()
                    sound.bowserfall_sond.stop()
                    sound.bowserfall_sond.play()
                    death_animation = animation.Death_Jump(self, self.death_image(), direction, -16)
                    death_animation.gravity_in_up = group.gravity_in_down_GRASS-.3
                    group.all_sprites.add(death_animation)
                    group.death_sprites.add(death_animation)
                    self.animation.kill()
                    self.collider.kill()
                    self.kill()

                    self.sprite_object.collider.kill()
                    self.sprite_object.kill()

            else:
                self.sprite_object.death_jump(*direction)


    def death_image(self):
        if self.texture == 0:
            data = (81, 48, 16, 16)

        if self.texture == 1:
            data = (130, 32, 16, 16)

        if self.texture == 2:
            data = (147, 16, 16, 16)

        if self.texture == 3:
            data = (212, 16, 16, 16)

        if self.texture == 4:
            data = (294, 8, 16, 24)

        if self.texture == 5:
            data = (133, 8, 16, 24)

        if self.texture == 6:
            data = (261, 8, 16, 24)

        if self.texture == 7:
            data = (32, 32, 32, 32)

        return data


    def update(self, delta_time):
        if not group.stop:
            if self.body:
                Enemy.update(self, delta_time)
                self.controll_direction()
                if self.direction:
                    self.controll_drop_fire()
                    self.controll_drop_hammer()
                    self.controll_jump()
                    self.controll_stop()

                self.animation.update_animation()

            else:
                self.controll_position()

            

            