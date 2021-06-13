import pygame
from pygame.locals import *
pygame.init()

from script import group



letter_sheet = {
                "0": (3  , 5),
                "1": (11 , 5),
                "2": (19 , 5),
                "3": (27 , 5),
                "4": (35 , 5),
                "5": (43 , 5),
                "6": (51 , 5),
                "7": (59 , 5),
                "8": (67 , 5),
                "9": (75 , 5),
                "a": (83 , 5),
                "b": (91 , 5),
                "c": (99 , 5),
                "d": (107, 5),
                "e": (115, 5),
                "f": (123, 5),

                "g": (3  , 13),
                "h": (11 , 13),
                "i": (19 , 13),
                "j": (27 , 13),
                "k": (35 , 13),
                "l": (43 , 13),
                "m": (51 , 13),
                "n": (59 , 13),
                "o": (67 , 13),
                "p": (75 , 13),
                "q": (83 , 13),
                "r": (91 , 13),
                "s": (99 , 13),
                "t": (107, 13),
                "u": (115, 13),
                "v": (123, 13),

                "w": (3  , 21),
                "x": (11 , 21),
                "y": (19 , 21),
                "z": (27 , 21),
                "@": (35 , 21),
                ".": (59 , 21),
                "-": (67 , 21),
                "*": (75 , 21),
                "+": (83 , 21),
                "!": (91 , 21),
                " ": (115, 21),
                "|": (52 , 30),
                "=": (68 , 30)
               }


point_sheet = ( 19, 24, 29, 0, 34, 39, 0, 0, 44 )

class Font(pygame.sprite.Sprite):
    def __init__(self, letter, color, x, y, identifier):
        super().__init__()

        self.letter = letter

        if self.letter != "@" or self.lettertter != "!":
            wh = (7, 7)
            conv = (21, 21)

        if self.letter == "@":
            wh = (9, 8)
            conv = (27, 24)

        if self.letter == "!":
            wh = (7, 8)
            conv = (21, 24)

        if self.letter == "|" or self.letter == "=":
            wh = (16, 16)
            conv = (48, 48)

        self.sheet = group.font_sheet.copy()
        self.sheet.set_clip(pygame.Rect(letter_sheet[self.letter]  + wh ))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        
        self.image_pixel_array = pygame.PixelArray(self.image)
        self.image_pixel_array.replace((255, 255, 255), color)
        self.image = pygame.transform.scale(self.image, conv)

        self.rect = self.image.get_rect()
        
        self.rect.x, self.rect.y = x, y
    
        self._layer = 5
        self.identifier = identifier


def Generate_Message(message, x, y, color, identifier):
    message = message.lower()
    x_pos = x
    for letter in message:
        if letter == "/":
            x_pos = x
            y += 24      
        try:
            font = Font(letter, color, x_pos, y, identifier)
            group.all_sprites.add(font)
            group.font_sprites.add(font)
            x_pos += 24
        except:
            pass


class Point(pygame.sprite.Sprite):
    def __init__(self, point, x, y):
        super().__init__()
        self.sheet = group.font_sheet.copy()
        self.sheet.set_clip(pygame.Rect(  point_sheet[point], 29, 4, 8 ))
        self.image = self.sheet.subsurface(self.sheet.get_clip())

        self.image = pygame.transform.scale(self.image, (12, 24))
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = x, y

        self._layer = 5

        self.Y_Y = y-144

        self.y_vel = -2

        self.identifier = None


    def update(self, delta_time):
        self.rect.y += int(self.y_vel*group.time*delta_time)

        if self.rect.y < self.Y_Y:
            self.kill()


def Generate_Point(points, *args):
    x_pos = args[0]
    for point in points:
        P = Point(int(point), x_pos, args[1])
        group.all_sprites.add(P)
        group.font_sprites.add(P)
        x_pos += 15


class Generate_ONE_UP(pygame.sprite.Sprite):
    def __init__(self, center, point=False):
        super().__init__()
        self.sheet = group.font_sheet.copy()
        if point:
            self.sheet.set_clip(pygame.Rect( 3, 45, 16, 8 ))
        else:
            self.sheet.set_clip(pygame.Rect( 3, 29, 16, 8 ))
            
        self.image = self.sheet.subsurface(self.sheet.get_clip())

        self.image = pygame.transform.scale(self.image, (48, 24))
        self.rect = self.image.get_rect()

        self.rect.center = center

        self._layer = 5

        self.Y_Y = center[1]-144

        self.y_vel = -2

        self.identifier = None


    def update(self, delta_time):
        self.rect.y += int(self.y_vel*group.time*delta_time)

        if self.rect.y < self.Y_Y:
            self.kill()


class S_Point(pygame.sprite.Sprite):
    def __init__(self, letter, x, y, identifier):
        super().__init__()

        self.letter = letter

        self.sheet = group.font_sheet.copy()
        self.sheet.set_clip(pygame.Rect(point_sheet[self.letter], 29, 4, 8 ))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
    
        self.image = pygame.transform.scale(self.image, (12, 24))

        self.rect = self.image.get_rect()
        
        self.rect.x, self.rect.y = x, y
    
        self._layer = 5
        self.identifier = identifier


def Generate_S_Point(points, x, y, identifier):
    x_pos = x
    for letter in points:   
        try:
            font = S_Point(int(letter), x_pos, y, identifier)
            group.all_sprites.add(font)
            group.font_sprites.add(font)
            x_pos += 15
        except:
            pass


def Kill_Identifier(identifier):
    for font in group.font_sprites:
        if font.identifier == identifier:
            font.kill()


class Poster(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sheet = group.poster_sprites.copy()
        self.sheet.set_clip(pygame.Rect(0, 0, 176, 88))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        
        self.image_pixel_array = pygame.PixelArray(self.image)
        self.image = pygame.transform.scale(self.image, (528, 264))

        self.rect = self.image.get_rect()
        
        self.rect.x, self.rect.y = x, y
    
        self._layer = 5


class Cursor(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sheet = group.font_sheet.copy()
        self.sheet.set_clip(pygame.Rect(107, 21, 8, 8  ))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        
        self.image_pixel_array = pygame.PixelArray(self.image)
        self.image = pygame.transform.scale(self.image, (24, 24))

        self.rect = self.image.get_rect()
        
        self.rect.x, self.rect.y = x, y
    
        self._layer = 5

        self.up_top = 0
        self.down_top = 0


    def set_data(self, up_top, down_top, coor=False):
        self.up_top = up_top
        self.down_top = down_top

        if not coor:
            pass

        else:
            self.rect.x, self.rect.y = coor[0], coor[1]


    def reset_warning(self):
        group.reset_warning = 0
        Kill_Identifier("reset_warning")


    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_w and not self.rect.y <= self.up_top:
                self.reset_warning()
                self.rect.y -= 48

            if event.key == pygame.K_s and not self.rect.y >= self.down_top:
                self.reset_warning()
                self.rect.y += 48

            if event.key == pygame.K_RETURN:
                return self.rect.y
