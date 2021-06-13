import pygame
from pygame.locals import *

try:
    from script import group

except:
    pass

width = 30
height = 48

def init():
    from script import tile
    global tile


class Collider_2D():
    def __init__(self, sprite_object, special_top_collide=False, special_bottom_collide=False):

        self.sprite_object = sprite_object
        self.special_top_collide = special_top_collide
        self.special_bottom_collide = special_bottom_collide
        
        self.top_collider    = TOP_Collider(self.sprite_object, self.special_top_collide)
        self.left_collider   = LEFT_Collider(self.sprite_object)
        self.bottom_collider = BOTTOM_Collider(self.sprite_object, self.special_bottom_collide)
        self.right_collider  = RIGHT_Collider(self.sprite_object)
        
        """
        group.all_sprites.add(self.bottom_collider)
        group.all_sprites.add(self.top_collider)
        group.all_sprites.add(self.left_collider)
        group.all_sprites.add(self.right_collider)
        """     
                       
            
    def resize(self):
        """
        if not self.special_top_collide:
            self.top_collider.image = pygame.Surface((self.top_collider.sprite_object.image.get_width(), height))
        else:
            self.top_collider.image = pygame.Surface((12, height))
        self.top_collider.image.fill((0, 255, 0))
        self.top_collider.image.set_colorkey((0, 0, 0))
        self.top_collider.rect = self.top_collider.image.get_rect()

        self.left_collider.image = pygame.Surface((width, self.left_collider.sprite_object.image.get_height()))
        self.left_collider.image.fill((0, 255, 0))
        self.left_collider.image.set_colorkey((0, 0, 0))
        self.left_collider.rect = self.left_collider.image.get_rect()

        if not self.special_bottom_collide:
            self.bottom_collider.image = pygame.Surface((self.bottom_collider.sprite_object.image.get_width(), height))
        else:
            self.top_collider.image = pygame.Surface((12, height))
        self.bottom_collider.image.fill((0, 255, 0))
        self.bottom_collider.image.set_colorkey((0, 0, 0))
        self.bottom_collider.rect = self.bottom_collider.image.get_rect()


        self.right_collider.image = pygame.Surface((width, self.right_collider.sprite_object.image.get_height()))
        self.right_collider.image.fill((0, 255, 0))
        self.right_collider.image.set_colorkey((0, 0, 0))
        self.right_collider.rect = self.right_collider.image.get_rect()

        
        self.top_collider.__init__(self.sprite_object, self.special_top_collide)
        self.left_collider.__init__(self.sprite_object)
        self.bottom_collider.__init__(self.sprite_object)
        self.right_collider.__init__(self.sprite_object)
        """

        self.top_collider.resize()
        self.left_collider.resize()
        self.bottom_collider.resize()
        self.right_collider.resize()


    def kill(self):
        self.top_collider.kill()
        self.left_collider.kill()
        self.bottom_collider.kill()
        self.right_collider.kill()      
       
       
    def update(self):
        self.top_collider.update_collide()
        self.left_collider.update_collide()
        self.bottom_collider.update_collide()
        self.right_collider.update_collide()


class BOTTOM_Collider(pygame.sprite.Sprite):
    def __init__(self, sprite_object, special_bottom_collide=False):
        super().__init__()
        self.sprite_object = sprite_object
        self.special_bottom_collide = special_bottom_collide
        if not self.special_bottom_collide:
            self.image = pygame.Surface((self.sprite_object.image.get_width(), height))

        else:
            self.image = pygame.Surface((12, height))
        
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 0, 0))

        self._layer = 4

        self.rect = self.image.get_rect()
        self.position()


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.top = self.sprite_object.rect.bottom


    def permanent_collision(self, list_object, velocity): # Pasar el argumento de velocidad ya multiplicado por el tiempo y por delta_time
        all_collide = pygame.sprite.spritecollide(self, list_object, False)
        for collide_object in all_collide:
            if self.sprite_object.rect.bottom-3 <= collide_object.rect.top: # test ????
                if self.sprite_object.rect.bottom + velocity >= collide_object.rect.top and collide_object != self.sprite_object:
                    return (True, collide_object)

                else:
                    return (False, None)

            else:
                return (False, None)

        if not pygame.sprite.spritecollide(self, list_object, False):
            return (False, None)


    def temporal_collision(self, list_object, velocity): # Pasar el argumento de velocidad ya multiplicado por el tiempo y por delta_time
        all_collide = pygame.sprite.spritecollide(self, list_object, False)
        for collide_object in all_collide:
            
            if self.sprite_object.rect.bottom + velocity > collide_object.rect.top and collide_object != self.sprite_object:
                return (True, collide_object)

            else:
                return (False, None)

        if not pygame.sprite.spritecollide(self, list_object, False):
            return (False, None)


    def resize(self):
        if not self.special_bottom_collide:
            self.image = pygame.Surface((self.sprite_object.image.get_width(), height))

        else:
            self.image = pygame.Surface((12, height))
        
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.position()


    def update_collide(self):
        self.position()


class TOP_Collider(pygame.sprite.Sprite):
    def __init__(self, sprite_object, special_collide=False):
        super().__init__()
        self.sprite_object = sprite_object
        self.special_collide = special_collide
        if not self.special_collide:
            self.image = pygame.Surface((self.sprite_object.image.get_width(), height))

        else:
            self.image = pygame.Surface((12, height))

        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 0, 0))

        self._layer = 4

        self.rect = self.image.get_rect()
        self.position()


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.bottom = self.sprite_object.rect.top


    def permanent_collision(self, list_object, velocity): # Pasar el argumento de velocidad ya multiplicado por el tiempo y por delta_time
        all_collide = pygame.sprite.spritecollide(self, list_object, False)
        for collide_object in all_collide:
            if self.sprite_object.rect.top >= collide_object.rect.bottom: # test ????
                if isinstance(collide_object, tile.Platform):
                    add_val = collide_object.y_velocity

                else:
                    add_val = 0

                if self.sprite_object.rect.top + velocity <= collide_object.rect.bottom + add_val and collide_object != self.sprite_object:
                    return (True, collide_object)

                else:
                    return (False, None)

            else:
                return (False, None)

        if not pygame.sprite.spritecollide(self, list_object, False):
            return (False, None)


    def temporal_collision(self, list_object, velocity): # Pasar el argumento de velocidad ya multiplicado por el tiempo y por delta_time
        all_collide = pygame.sprite.spritecollide(self, list_object, False)
        for collide_object in all_collide:
            if isinstance(collide_object, tile.Platform):
                add_val = collide_object.y_velocity

            else:
                add_val = 0

            if self.sprite_object.rect.top + velocity <  collide_object.rect.bottom + add_val and collide_object != self.sprite_object:
                return (True, collide_object)

            else:
                return (False, None)

        if not pygame.sprite.spritecollide(self, list_object, False):
            return (False, None)


    def resize(self):
        if not self.special_collide:
            self.image = pygame.Surface((self.sprite_object.image.get_width(), height))

        else:
            self.image = pygame.Surface((12, height))

        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.position()

    
    def update_collide(self):
        self.position()


class LEFT_Collider(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object

        self.image = pygame.Surface((width, self.sprite_object.image.get_height()))
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 0, 0))

        self._layer = 4

        self.rect = self.image.get_rect()
        self.position()


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.right = self.sprite_object.rect.left


    def permanent_collision(self, list_object, velocity): # Pasar el argumento de velocidad ya multiplicado por el tiempo y por delta_time
        all_collide = pygame.sprite.spritecollide(self, list_object, False)
        for collide_object in all_collide:
            if self.sprite_object.rect.left + velocity <= collide_object.rect.right and collide_object != self.sprite_object:
                return (True, collide_object)

            else:
                return (False, None)

        if not pygame.sprite.spritecollide(self, list_object, False):
            return (False, None)


    def temporal_collision(self, list_object, velocity): # Pasar el argumento de velocidad ya multiplicado por el tiempo y por delta_time
        all_collide = pygame.sprite.spritecollide(self, list_object, False)
        for collide_object in all_collide:

            if self.sprite_object.rect.left + velocity < collide_object.rect.right and collide_object != self.sprite_object:
                return (True, collide_object)

            else:
                return (False, None)

        if not pygame.sprite.spritecollide(self, list_object, False):
            return (False, None)


    def resize(self):
        self.image = pygame.Surface((width, self.sprite_object.image.get_height()))
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.position()    


    def update_collide(self):
        self.position()


class RIGHT_Collider(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object

        self.image = pygame.Surface((width, self.sprite_object.image.get_height()))
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 0, 0))

        self._layer = 4

        self.rect = self.image.get_rect()
        self.position()


    def position(self):
        self.rect.center = self.sprite_object.rect.center
        self.rect.left = self.sprite_object.rect.right


    def permanent_collision(self, list_object, velocity): # Pasar el argumento de velocidad ya multiplicado por el tiempo y por delta_time
        all_collide = pygame.sprite.spritecollide(self, list_object, False)
        for collide_object in all_collide:

            if self.sprite_object.rect.right + velocity >= collide_object.rect.left and collide_object != self.sprite_object:
                return (True, collide_object)

            else:
                return (False, None)

        if not pygame.sprite.spritecollide(self, list_object, False):
            return (False, None)


    def temporal_collision(self, list_object, velocity): # Pasar el argumento de velocidad ya multiplicado por el tiempo y por delta_time
        all_collide = pygame.sprite.spritecollide(self, list_object, False)
        for collide_object in all_collide:

            if self.sprite_object.rect.right + velocity > collide_object.rect.left and collide_object != self.sprite_object:
                return (True, collide_object)

            else:
                return (False, None)

        if not pygame.sprite.spritecollide(self, list_object, False):
            return (False, None)


    def resize(self):
        self.image = pygame.Surface((width, self.sprite_object.image.get_height()))
        self.image.fill((0, 255, 0))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.position()

    
    def update_collide(self):
        self.position()


class Depression_Detector():
    def __init__(self, sprite_object):
        self.sprite_object = sprite_object

        self.left_detector = Depression_Detector_Left(self.sprite_object)
        self.right_detector = Depression_Detector_Right(self.sprite_object)

        """
        group.all_sprites.add(self.left_detector)
        group.all_sprites.add(self.right_detector)
        """      
        

    def update(self):
        self.left_detector.update_detector()
        self.right_detector.update_detector()


class Depression_Detector_Left(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.image = pygame.Surface((1, 2))
        self.image.fill((255, 0, 0))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()

        self.rect.right = self.sprite_object.rect.left+18
        self.rect.y = self.sprite_object.rect.bottom

        self._layer = 3


    def position(self):
        self.rect.right = self.sprite_object.rect.left#+18
        self.rect.y = self.sprite_object.rect.bottom


    def is_collide(self, list_object):
        if pygame.sprite.spritecollide(self, list_object, False):
            return True

        else:
            return False


    def update_detector(self):
        self.position()


class Depression_Detector_Right(pygame.sprite.Sprite):
    def __init__(self, sprite_object):
        super().__init__()
        self.sprite_object = sprite_object
        self.image = pygame.Surface((1, 2))
        self.image.fill((0, 0, 255))
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()

        self.rect.left = self.sprite_object.rect.right-18
        self.rect.y = self.sprite_object.rect.bottom

        self._layer = 3


    def position(self):
        self.rect.left = self.sprite_object.rect.right#-18
        self.rect.y = self.sprite_object.rect.bottom


    def is_collide(self, list_object):
        if pygame.sprite.spritecollide(self, list_object, False):
            return True

        else:
            return False


    def update_detector(self):
        self.position()


def Rebound(velocity, esp=False):
    if not esp:
        return (velocity/2)*-1

    else:
        return (velocity/esp)*-1


def Accelearted_Linear_Movement(velocity, delta_time, MAX_velocity, acceleation, deceleration, symbol):
    if symbol:

        if velocity <= MAX_velocity:
            
            if velocity >= MAX_velocity:
                velocity = MAX_velocity

            else:
                velocity += acceleation*group.time*delta_time

        if velocity >= MAX_velocity:

            if velocity <= MAX_velocity:
                velocity = MAX_velocity

            else:
                velocity += deceleration*group.time*delta_time

        return velocity

    if not symbol:
        
        if velocity >= MAX_velocity:
            
            if velocity <= MAX_velocity:
                velocity = MAX_velocity

            else:
                velocity += acceleation*group.time*delta_time

        if velocity <= MAX_velocity:

            if velocity >= MAX_velocity:
                velocity = MAX_velocity

            else:
                velocity += deceleration*group.time*delta_time

        return velocity


def Directional_Velocity(vel_1, vel_2, delta_time):
    return int(  int(vel_1*group.time*delta_time)  +  int(vel_2*group.time*delta_time)  )


def get_distance(obj_1, obj_2, only_x=False, only_y=False):
    c_a = obj_1.rect.center[0] - obj_2.rect.center[0]
    c_b = obj_1.rect.center[1] - obj_2.rect.center[1]

    if only_x and only_y:
        raise Exception("No se aceptan ambos parametros a la vez")

    if not only_x and not only_y:
        return ( (c_a**2) + (c_b**2) )**.5

    elif only_x:
        return c_a

    elif only_y:
        return c_b


def convert(numer):
    count = 0

    data_1 =   ["#", "!", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q"]
    data_2 = [True, False, 0 ,  1 ,  2 ,  3 ,  4 ,  5 ,  6 ,  7 ,  8 ,  9 ,  10,  11,  12,  13,  14,  15,  16,  17,  18,  19,  20,  21, 22, 23, 24, 25, 26]
    for n in data_1:
        if n == numer:
            numer = data_2[count]
            return numer
        
        count += 1


def convert_2(numer):
    n_1 = convert(numer[0])
    n_2 = convert(numer[1])

    return (n_1 * 27**1) + (n_2 * 27**0) 