import pygame
from pygame.locals import *
pygame.init()

from script import group, physic, animation, palette, obj, score, font, seam, levels, sound

"""
    llamadas del teclado

    manejar las fuerzas de velocidad

    actualizar los datos de el collider  (False, None)

    hacer el mocimiento en base a los resultados de el colider 

    actualizar el collider "collider.updtade()"
"""

color = (0, 0, 255)

small_size = (36, 42)
big_size   = (36, 87)



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface(small_size)
        self.image.fill((0, 0, 255))
        self.image.set_colorkey(color)
        
        self.rect = self.image.get_rect()

        self.rect.y = 500
        self.rect.x = 96

        self._layer = 6

        data = group.get_data()

        # datos del juagdor -----------------------------------------------
        try:
            self.name = data[0]
            self.size = bool(int(data[6]))
            self.fire_power = bool(int(data[7]))
        except:
            self.name = "mario"
            self.size = False
            self.fire_power = False   

        self.is_crouched_down = False
        self.wather = False
        
        self.invincibility_power = False
        self.invincibility_time  = group.Chronometer(11)
        self.not_damage_time     = group.Chronometer(3)
        self.not_damage_time.time = 0
        self.handle_mode = 0
        self.auto_mode   = False
        self.can_pole    = True
        self.can_drop_bubble = 0

        

        self.re_appear_index = 0

        # pulsaciones constantes-------------------------------------------
        self.KEY_A = False
        self.KEY_D = False
        self.KEY_K = False
        self.KEY_S = False
        self.KEY_W = False
        self.KEY_L = False

        self.can_jump = True
        self.can_doubble_jump = False
        self.can_supper_jump  = False
        self.can_drop_fireball = 0
        self.key_a_time = 0 
        self.key_d_time = 0
        self.key_s_time = 0

        # fuerzas de velocidad -------------------------------------------
        """
        Estas son las fuerza de velociudad en el eje X
        """

        self.left_velocity  = 0
        self.right_velocity = 0

        self.platform_velocity_x = 0 
        self.platform_velocity_y = 0


        self.left_MAX_VEL  = 0
        self.right_MAX_VEL = 0

    
        """
        Estas son las fuerzas de velocidad en el eje Y
        """

        self.top_velocity = 0
        self.bottom_velocity = 1

        self.bottom_MAX_VEL = 0

        self.gravity = 0
        
        self.set_physic(self.wather)

        # datos de el collider --------------------------------------------
        self.collider = physic.Collider_2D(self, True)

        self.bottom_collision = (False, None) # bloques
        self.top_collision    = (False, None)
        self.right_collision  = (False, None)
        self.left_collision   = (False, None)

        self.bottom_collision_enemy = (False, None) # enemigos

        # animacion -------------------------------------------------------
        self.animation = animation.Animation_Player(self)
        group.all_sprites.add(self.animation)
        group.animation_sprites.add(self.animation)

        # rezise ----------------------------------------------------------
        self.resize(False)
        self.resize(False)


    # Metodos basicos -------------------------------------------------------------------
    def handle(self, event, pause):
        if event.type == pygame.KEYDOWN:
            if not self.auto_mode:
                if event.key == pygame.K_a: # fuerzas constantes 
                    self.KEY_A = True

                if event.key == pygame.K_d:
                    self.KEY_D = True

                if event.key == pygame.K_w:
                    self.KEY_W = True

                if event.key == pygame.K_s:
                    if self.size:
                        self.crouched_down()
                    self.KEY_S = True

                if event.key == pygame.K_k:
                    if self.fire_power and not group.stop and not pause:
                        if  bool( int(self.can_drop_fireball) ):
                            self.drop_fireball()
                            self.can_drop_fireball = 0
                    self.KEY_K = True

                if event.key == pygame.K_l and not group.stop and not pause:
                    if self.wather:
                        sound.stomp_sound.stop()
                        sound.stomp_sound.play()
                        self.bottom_velocity = self.jump_force
                        self.can_jump = False

                    if not self.wather:
                        if self.can_jump and self.bottom_collision[0]:
                            if not self.size:
                                sound.jump_small_sound.stop()
                                sound.jump_small_sound.play()
                            if self.size:
                                sound.jump_super_sound.stop()
                                sound.jump_super_sound.play()
                            self.bottom_velocity = self.jump_force
                            self.can_jump = False

                    self.KEY_L = True

                if event.key == pygame.K_p:
                    if self.wather:
                        self.set_physic(False)

                    elif not self.wather:
                        self.set_physic(True)

            if event.key == pygame.K_i:
                levels.level += 1

                if levels.level >= 4:
                    levels.world += 1
                    levels.level = 0
                seam.Clear()
                group.all_sprites.add(seam.Black_Screen())
                seam.Set_Data(levels.world_array[levels.world][levels.level], 0)
                seam.Load(0)

            if event.key == pygame.K_o:
                self.set_invincibility_power(True)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: # fuerzas constantes 
                self.KEY_A = False

            if event.key == pygame.K_d:
                self.KEY_D = False
                

            if event.key == pygame.K_w:
                self.KEY_W = False

            if event.key == pygame.K_s:
                if self.size:
                    self.crouched_down()
                self.KEY_S = False

            if event.key == pygame.K_k:
                self.KEY_K = False

            if event.key == pygame.K_l:
                if self.bottom_velocity < 0:
                    self.bottom_velocity = 0
                self.KEY_L = False


    def manage_keys(self, delta_time):
        if not self.auto_mode:
            if self.handle_mode == 0:
                self.key_a_time = 0
                self.key_d_time = 0
                if not self.KEY_S:
                    if self.KEY_A:
                        if self.KEY_K:
                            self.left_MAX_VEL = self.run_vel*-1

                        if not self.KEY_K:
                            self.left_MAX_VEL = self.walk_vel*-1


                    if self.KEY_D:
                        if self.KEY_K:
                            self.right_MAX_VEL = self.run_vel

                        if not self.KEY_K:
                            self.right_MAX_VEL = self.walk_vel

                    if not self.KEY_A:
                        self.left_MAX_VEL = 0

                    if not self.KEY_D:
                        self.right_MAX_VEL = 0

                if self.KEY_S:
                    self.left_MAX_VEL = 0
                    self.right_MAX_VEL = 0
                    self.key_s_time += .01*group.time*delta_time
                    if self.key_s_time >= 1:
                        self.key_s_time = 1

                else:
                    self.key_s_time = 0

            if self.handle_mode == 1:
                add_time = .05
                if self.KEY_A:
                    if self.rect.bottom <= 624:
                        self.key_a_time += add_time*group.time*delta_time
                    if self.animation.direction_x:
                        self.animation.direction_x = False

                if not self.KEY_A:
                    self.key_a_time = 0

                if self.KEY_D:
                    if self.rect.bottom <= 624:
                        self.key_d_time += add_time*group.time*delta_time
                    if not self.animation.direction_x:
                        self.animation.direction_x = True

                if not self.KEY_D:
                    self.key_d_time = 0

                if self.KEY_W:
                    self.key_a_time = 0
                    self.key_d_time = 0
                    self.top_velocity = -3

                if not self.KEY_W:
                    self.top_velocity = 0

                if self.KEY_S:
                    self.bottom_velocity = 3

                if not self.KEY_S:
                    self.bottom_velocity = 0
    
        else:
            if self.handle_mode == 0:
                
                if not self.right_collision[0]:
                    self.left_MAX_VEL = 0
                    self.right_MAX_VEL = self.walk_vel

                else:
                    self.left_MAX_VEL = 0
                    self.right_MAX_VEL = 0

                """
                if self.right_collision[0]:
                    if self.wather:
                        sound.stomp_sound.stop()
                        sound.stomp_sound.play()
                        self.bottom_velocity = self.jump_force
                        self.can_jump = False

                    if not self.wather:
                        if self.can_jump and self.bottom_collision[0]:
                            if not self.size:
                                sound.jump_small_sound.stop()
                                sound.jump_small_sound.play()
                            if self.size:
                                sound.jump_super_sound.stop()
                                sound.jump_super_sound.play()
                            self.bottom_velocity = self.jump_force
                            self.can_jump = False
                """

            if self.handle_mode == 1:
                if not self.bottom_collision[0]:
                    self.bottom_velocity = 5
                """
                else:
                    #add_time = .05
                    #self.key_d_time += add_time*group.time*delta_time
                    if not self.animation.direction_x:
                        self.animation.direction_x = True
                """


    def manage_velocity(self, delta_time):
        if self.handle_mode == 0:
            # Velocidades en el eje X

            if self.right_collision[0] or self.rect.x >= group.geometry[0]:  # Limitar la velocidad cuando chocas 
                if self.right_MAX_VEL != 0:
                    self.right_MAX_VEL = self.walk_vel

            if self.left_collision[0] or self.rect.x <= 0:   # Limitar la velocidad cuando chocas 
                if self.left_MAX_VEL != 0:
                    self.left_MAX_VEL = self.walk_vel*-1

            self.right_velocity = physic.Accelearted_Linear_Movement(self.right_velocity, delta_time, self.right_MAX_VEL, self.acceleration, self.deceleration*-1, True) # acelerar/desacelerar

            self.left_velocity  = physic.Accelearted_Linear_Movement(self.left_velocity, delta_time, self.left_MAX_VEL, self.acceleration*-1, self.deceleration, False)  # acelerar/desacelerar

            if int(self.right_velocity + self.left_velocity ) == 0 and int(self.left_MAX_VEL+self.right_MAX_VEL)  == 0: # TEST !!!!!        
                self.right_velocity = self.left_velocity = 0 # Ambas velocidades se anulan, entonces se redondean a 0

            """
            if abs(round(self.right_velocity + self.left_velocity, 1 )) <= 0.1 and int(self.left_MAX_VEL+self.right_MAX_VEL)  == 0: # TEST !!!!!        
                self.right_velocity = self.left_velocity = 0
            """

            # Velocidades en el eje y

            if self.bottom_velocity > 0: # La fuerza de gravedad cambia su velor dependiendo del signo de la velocidad
                self.gravity = self.gravity_in_down

            if self.bottom_velocity < 0:
                self.gravity = self.gravity_in_up

            self.bottom_velocity = physic.Accelearted_Linear_Movement(self.bottom_velocity, delta_time, self.bottom_MAX_VEL, self.gravity, -.01, True) # acelerar/desacelerar

            if self.bottom_collision[0] and self.can_jump and not self.bottom_collision_enemy[0]:
                #if not self.bottom_collision[1].platform:
                self.bottom_velocity = 0 # La velocidad en el eje y es 0 cuando colisionas contra el suelo y puedes saltar

                #else:
                #    self.bottom_velocity = self.bottom_collision[1].y_velocity

                if self.bottom_collision[1].platform and self.bottom_collision[1].rect.bottom > 0 and self.bottom_collision[1].rect.top < group.geometry[1]:
                    self.rect.bottom = self.bottom_collision[1].rect.top




        if self.handle_mode == 1:
            self.left_MAX_VEL = 0
            self.right_MAX_VEL = 0
            self.bottom_MAX_VEL = 0
      

    def update_collider_2d(self, delta_time):
        # Colisiones contra los tiles -----------------------------------------------------------------------------------------------------------------------------------------------------
        self.bottom_collision = self.collider.bottom_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.top_velocity, self.bottom_velocity, delta_time))

        self.top_collision    = self.collider.top_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.top_velocity, self.bottom_velocity, delta_time)) 

        self.right_collision  = self.collider.right_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.right_velocity, self.left_velocity, delta_time))

        self.left_collision   = self.collider.left_collider.permanent_collision(group.tile_sprites, physic.Directional_Velocity(self.right_velocity, self.left_velocity, delta_time))

        # Colisiones contra los enemigos ---------------------------------------------------------------------------------------------------------------------------------------------------
        self.bottom_collision_enemy = self.collider.bottom_collider.permanent_collision(group.enemy_sprites, physic.Directional_Velocity(self.top_velocity, self.bottom_velocity, delta_time))


    def manage_movement(self, delta_time):
        if not self.bottom_collision[0]:
            self.rect.y += int( self.bottom_velocity*group.time*delta_time )
            #self.can_jump = False
            self.bottom_MAX_VEL = self.fall_vel
            self.platform_velocity_x = 0

        if not self.top_collision[0]:
            self.rect.y += int( self.top_velocity*group.time*delta_time )

        if not self.left_collision[0]:
            self.rect.x += int( self.left_velocity*group.time*delta_time )
            if self.platform_velocity_x < 0:
                self.rect.x += int(self.platform_velocity_x*group.time*delta_time)

        if not self.right_collision[0]:
            self.rect.x += int( self.right_velocity*group.time*delta_time )
            if self.platform_velocity_x > 0:
                self.rect.x += int(self.platform_velocity_x*group.time*delta_time)

        self.screen_collide()

        if self.bottom_collision[0]:
            if self.bottom_collision[1].top_collide: # Revisar si las colisiones del bloque estan activadas
                self.rect.bottom = self.bottom_collision[1].rect.top
                self.can_jump = True
                self.bottom_MAX_VEL = 0

                if self.bottom_collision[1].jump_board:
                    if self.bottom_collision[1].can_jump:
                        self.bottom_collision[1].jump()

                    if not self.bottom_collision[1].can_jump:
                        if self.KEY_L:
                            self.bottom_velocity = self.super_jump_force

                        else:
                            self.bottom_velocity = self.jump_force
                        if self.size:
                            sound.jump_super_sound.stop()
                            sound.jump_super_sound.play()

                        if not self.size:
                            sound.jump_small_sound.stop()
                            sound.jump_small_sound.play()
                            
                        self.can_jump = False

             
                if self.bottom_collision[1].platform:
                    self.platform_velocity_x = self.bottom_collision[1].x_velocity

                if self.bottom_collision[1].teleporter:
                    self.bottom_collision[1].teleport()

                if self.bottom_collision[1].killer:
                    self.kill_player()

                if self.bottom_collision[1].spiny:
                    self.damage(None, (True, True))


            else:
                if self.bottom_velocity > 0:
                    self.rect.y += int( self.bottom_velocity*group.time*delta_time )
                    self.bottom_MAX_VEL = self.fall_vel  
                    self.platform_velocity_x = 0

        if self.top_collision[0]:
            if self.top_collision[1].bottom_collide:
                sound.jump_small_sound.stop()
                sound.jump_super_sound.stop()
                sound.stomp_sound.stop()
                self.rect.top = self.top_collision[1].rect.bottom

                if self.top_collision[1].teleporter:
                    self.top_collision[1].teleport()

                if self.top_collision[1].killer:
                    self.kill_player()

                if self.top_collision[1].spiny:
                    self.damage(None, (False, False))


                if self.handle_mode == 0:
                    if not self.size and self.top_collision[1].can_rebound:
                        self.top_collision[1].rebound()

                    elif self.size and self.top_collision[1].breakable:
                        self.top_collision[1].break_tile()

                    elif self.size and self.top_collision[1].can_rebound and not self.top_collision[1].breakable: 
                            self.top_collision[1].rebound()

                    else:
                        self.top_collision[1].bump()
                    

                    self.bottom_velocity = physic.Rebound(self.bottom_velocity) # rebote con los bloques cuando mario los golpea

            else:
                if self.top_velocity < 0:
                    self.rect.y += int( self.top_velocity*group.time*delta_time )        

        if self.left_collision[0]:
            if self.left_collision[1].right_collide:
                self.rect.left = self.left_collision[1].rect.right

                if self.left_collision[1].teleporter:
                    self.left_collision[1].teleport()

                if self.left_collision[1].killer:
                    self.kill_player()

                if self.left_collision[1].spiny:
                    self.damage(None, (True, True))

            else:
                self.rect.x += int( self.left_velocity*group.time*delta_time )
                if self.platform_velocity_x < 0:
                    self.rect.x += int(self.platform_velocity_x*group.time*delta_time)

        if self.right_collision[0]:
            if self.right_collision[1].left_collide: 
                self.rect.right = self.right_collision[1].rect.left

                if self.right_collision[1].teleporter:
                    self.right_collision[1].teleport()

                if self.right_collision[1].killer:
                    self.kill_player()

                if self.right_collision[1].spiny:
                    self.damage(None, (True, True))
                
            else:
                self.rect.x += int( self.right_velocity*group.time*delta_time )
                if self.platform_velocity_x > 0:
                    self.rect.x += int(self.platform_velocity_x*group.time*delta_time)


    def manage_enemy_collide(self):
        if not self.KEY_L:
            self.can_doubble_jump = True
            
        if self.can_jump:
            self.can_doubble_jump = False

        if self.bottom_collision_enemy[0]:
            if self.bottom_collision_enemy[1].can_smash:
                self.rect.bottom = self.bottom_collision_enemy[1].rect.top
                self.bottom_collision_enemy[1].smash(self)
                if not self.can_doubble_jump or not self.KEY_L:
                    self.bottom_velocity = physic.Rebound(self.jump_force/1.1*-1)
                if self.KEY_L and self.can_doubble_jump:
                    self.bottom_velocity = self.jump_force

                self.can_doubble_jump = False
   

    def manage_coin_collide(self):
        coin_collide = pygame.sprite.spritecollide(self, group.coin_sprites, True)
        for coin in coin_collide:
            sound.coin_sound.stop()
            sound.coin_sound.play()

            #font.Generate_Point("200", self.rect.x +3, self.rect.y)

            score.coin  += 1
            score.score += 200


    def manage_stair_collide(self):
        stair_collide = pygame.sprite.spritecollide(self, group.stair_sprites, False)
        for stair in stair_collide:
            if stair.pole and self.rect.x < stair.rect.x:
                self.auto_mode = True
                if self.can_pole:
                    self.KEY_W = True
                    self.can_pole = False

                else:
                    if self.bottom_collision[0]:
                        self.KEY_W = False

            if self.KEY_W:
                self.handle_mode = 1
                self.left_velocity = 0
                self.right_velocity = 0
                if self.rect.x < stair.rect.x:
                    self.animation.direction_x = False

                if self.rect.x > stair.rect.x:
                    self.animation.direction_x = True

            if self.handle_mode == 1:
                if self.animation.direction_x:
                   self.rect.x = stair.rect.x+27
                    
                if not self.animation.direction_x:
                   self.rect.x = stair.rect.x-15

        if self.handle_mode == 1:
            if bool(int(self.key_a_time)) or bool(int(self.key_d_time)) or (self.KEY_L and not self.KEY_W and self.rect.bottom <= 624):
                if self.KEY_L and self.rect.bottom <= 624:
                    if self.wather:
                        sound.stomp_sound.stop()
                        sound.stomp_sound.play()
                    else:
                        if not self.size:
                            sound.jump_small_sound.stop()
                            sound.jump_small_sound.play()
                        if self.size:
                            sound.jump_super_sound.stop()
                            sound.jump_super_sound.play()
                    if self.animation.direction_x:
                        self.right_velocity = self.walk_vel

                    if not self.animation.direction_x:
                        self.left_velocity = self.walk_vel*-1
                    self.bottom_velocity = self.jump_force

                elif self.KEY_D:
                    self.right_velocity = self.walk_vel/2

                elif self.KEY_A:
                    self.left_velocity = (self.walk_vel/2)*-1

                self.can_pole = True
                self.can_jump = False
                self.handle_mode = 0


    def manage_pipe_collide(self):
        pipe_collide = pygame.sprite.spritecollide(self, group.pipe_sprites, False)
        for pipe in pipe_collide:
            if pipe.direction_1 == 0:
                if self.KEY_S:
                    group.all_sprites.add(animation.Animation_Pipe(self, pipe))

            if pipe.direction_1 == 1:
                if self.KEY_W:
                    group.all_sprites.add(animation.Animation_Pipe(self, pipe))

            if pipe.direction_1 == 2:
                if self.right_collision[0]:
                    group.all_sprites.add(animation.Animation_Pipe(self, pipe))
                    if self.auto_mode:
                        self.re_appear_index = 1

            if pipe.direction_2 == 3:
                if self.left_collision[0]:
                    group.all_sprites.add(animation.Animation_Pipe(self, pipe))


    def manage_collide(self, delta_time): # Los resultados de las colisiones
        self.manage_movement(delta_time)
        self.manage_enemy_collide()
        self.manage_coin_collide()
        self.manage_stair_collide()
        self.manage_pipe_collide()


    # Metodos miscelaneos -----------------------------------------------------------------
    def resize(self, a=True):
        if self.size:
            x = self.rect.x
            y = self.rect.y

            self.image = pygame.Surface(small_size)
            self.image.fill((0, 0, 255))
            self.image.set_colorkey(color)
            
            self.rect = self.image.get_rect()

            self.rect.x = x
            self.rect.y = y+abs(small_size[1]-big_size[1])
            if a:
                group.all_sprites.add(animation.Power_up_transformation(self.animation, 1))   
            self.size = False


        elif not self.size:
            x = self.rect.x
            y = self.rect.y

            self.image = pygame.Surface(big_size)
            self.image.fill((0, 0, 255))
            self.image.set_colorkey(color)
            
            self.rect = self.image.get_rect()

            self.rect.x = x
            self.rect.y = y-abs(small_size[1]-big_size[1])

            if a:
                group.all_sprites.add(animation.Power_up_transformation(self.animation, 0))
                self.not_damage_time.time = 0
            self.size = True     

        self.animation.resize()
        self.collider.resize()


    def set_fire_power(self, val_bool):
        if val_bool and not self.fire_power:
            self.not_damage_time.time = 0
            group.all_sprites.add(animation.Power_up_transformation(self.animation, 2))
                 
        self.fire_power = val_bool


    def set_invincibility_power(self, val_bool):
        self.invincibility_time.reset()
        self.invincibility_power = True
        sound.stop()
        sound.star_man_theme.stop()
        sound.star_man_theme.play(-1)
        self.not_damage_time.time = 0


    def controll_invincibility_power(self):
        if self.invincibility_power:
            if self.invincibility_time.time_over():
                self.invincibility_power = False
                self.invincibility_time.reset()
                sound.star_man_theme.stop()
                sound.stop()
                sound.load(sound.main_theme[sound.index])
                sound.play(-1)
                

    def set_physic(self, bool_val):
        if bool_val:
            # Eje x ----------------------
            self.walk_vel = 4
            self.run_vel  = 8

            self.acceleration = .1
            self.deceleration = .1
            
            # Eje y ----------------------
            self.jump_force = -6
            self.super_jump_force = -9
            self.fall_vel = 6 #BOTTOM_MAX_VEL
            
            self.gravity_in_up   = group.gravity_in_up_WATHER
            self.gravity_in_down = group.gravity_in_down_WATHER

            self.wather = True


        elif not bool_val: # Fuerazas en la tierra
            # Eje x ----------------------
            self.walk_vel = 5
            self.run_vel  = 8

            self.acceleration = .1
            self.deceleration = .2

            # Eje y ----------------------
            self.jump_force = -12
            self.super_jump_force = -18
            self.fall_vel = 12 #BOTTOM_MAX_VEL

            self.gravity_in_up   = group.gravity_in_up_GRASS
            self.gravity_in_down = group.gravity_in_down_GRASS

            self.wather = False


    def crouched_down(self):
        if not self.is_crouched_down:
            x = self.rect.x
            y = self.rect.y

            self.image = pygame.Surface(small_size)
            self.image.fill((0, 0, 255))
            self.image.set_colorkey(color)
            
            self.rect = self.image.get_rect()

            self.rect.x = x
            self.rect.y = y+abs(small_size[1]-big_size[1])

            self.is_crouched_down = True


        elif self.is_crouched_down:
            x = self.rect.x
            y = self.rect.y

            self.image = pygame.Surface(big_size)
            self.image.fill((0, 0, 255))
            self.image.set_colorkey(color)
            
            self.rect = self.image.get_rect()

            self.rect.x = x
            self.rect.y = y-abs(small_size[1]-big_size[1])

            self.is_crouched_down = False

        self.collider.resize()


    def segurity_crouched_down(self):
        if not self.size:
            if self.is_crouched_down:
                self.resize(False)
                self.crouched_down()
                self.resize(False)

        if self.size:
            if self.KEY_S:
                if not self.is_crouched_down:
                    self.crouched_down()


    def display_rect(self):
        font.Kill_Identifier("rect")
        font.Generate_Message( str(self.rect.x), group.geometry[0]-96, 120, (255, 255, 255), "rect")
        font.Generate_Message( str(self.rect.bottom), group.geometry[0]-96, 168, (255, 255, 255), "rect")


    def screen_collide(self):
        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.right >= group.geometry[0]:
            self.rect.right = group.geometry[0] 

        
        if self.rect.y >= group.geometry[1]+192:
            self.kill_player()
        

    def drop_fireball(self):
        if self.animation.direction_x:
            x = -6

        if not self.animation.direction_x:
            x = +18

        fire_ball = obj.Fire_Ball(self.rect.x+x, self.rect.y+9, self.animation.direction_x)
        group.all_sprites.add(fire_ball)
        group.mario_fireball_sprites.add(fire_ball)


    def controll_drop(self, delta_time):
        self.can_drop_fireball += .07*delta_time*group.time

        if self.can_drop_fireball >= 1:
            self.can_drop_fireball = 1


    def drop_bubble(self, delta_time):
        if self.wather:
            self.can_drop_bubble += .012*group.time*delta_time

            if self.can_drop_bubble >= 1:
                self.can_drop_bubble = 1
            
            if bool(int(self.can_drop_bubble)):
                self.can_drop_bubble = 0
                if self.animation.direction_x:
                    x = -9
                if not self.animation.direction_x:
                    x = +33
                bubble = animation.Bubble(self.rect.x+x, self.rect.y+9)
                group.all_sprites.add(bubble)
                group.death_sprites.add(bubble)


    def damage(self, enemy, direction):
        if not self.auto_mode:
            if not self.invincibility_power:
                if self.size and self.not_damage_time.time_over():
                    sound.pipe_sound.stop()
                    sound.pipe_sound.play()

                    self.fire_power = False
                    self.resize()

                    self.not_damage_time.reset()

                if not self.size and self.not_damage_time.time_over():
                    self.kill_player()

            else:
                try:
                    enemy.death_jump(*direction)
                
                except:
                    pass

        
    def kill_player(self):
        sound.stop()
        pygame.mixer.stop()

        if self.size:
            self.resize(False)

        self.fire_power = False
        self.invincibility_power = False
        self.invincibility_time.reset()

        self.right_velocity = 10
        self.animation.direction_x = False
        self.right_velocity = 0

        score.lives -= 1
        group.all_sprites.add(animation.Player_Death_Jump(self))


    def update(self, delta_time):
        self.segurity_crouched_down()
        self.controll_drop(delta_time) 

        if not group.stop:
            self.drop_bubble(delta_time)
            self.controll_invincibility_power()
            self.manage_keys(delta_time)
            self.manage_velocity(delta_time)
            self.update_collider_2d(delta_time)
            self.manage_collide(delta_time) # Los resultados de las colsiones

        self.collider.update()
        self.animation.update_animation()
        #self.display_rect()

        #print(self.bottom_collision[0], self.bottom_velocity)