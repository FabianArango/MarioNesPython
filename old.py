import pygame
from pygame.locals import *
pygame.init()

from script import group, font, player, tile, animation, palette, score, enemy, seam, levels, sound, physic

TILE_X_POS = 0


def display_fps(clock):
    font.Kill_Identifier("fps")
    font.Generate_Message(str( int( clock.get_fps() ) ), group.geometry[0]-56, 144, (255, 255, 255), "fps")
    #font.Generate_Message( str(len(group.enemy_sprites)), group.geometry[0]-72, 72, (255, 255, 255), "fps"  )
      

class MOUSE(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((1, 1))
        self.image.fill((0, 0, 0))
        self.image.set_colorkey((0, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.x = pygame.mouse.get_pos()[0]
        self.rect.y = pygame.mouse.get_pos()[1]

        self._layer = 3

    def update(self, delta_time):
        self.rect.x = pygame.mouse.get_pos()[0]
        self.rect.y = pygame.mouse.get_pos()[1]

        
class Game(object):
    def __init__(self):
        group.init()
        physic.init()
        self.fullscreen = False
        self.pause = False

        #font.Generate_Message("fps", group.geometry[0]-152, 72, (255, 255, 255), "1")
        #font.Generate_Message("+372", group.geometry[0]-120, 24, (255, 255, 255), "1")

        group.all_sprites.add(animation.Coin_Display_Animation(24, 72))

        self.player = player.Player()
        group.all_sprites.add(self.player)
        group.player_sprites.add(self.player)

        self.MOUSE = MOUSE()
        group.all_sprites.add(self.MOUSE)
        """
        x = -48
        for n in range(group.tile_w+2):
            tile.Generate_Tile((x, 13*48), "0100!!")
            tile.Generate_Tile((x, 14*48), "0100!!")
            x += 48
        """
        group.all_sprites.add(seam.Black_Screen())
        seam.Set_Data(levels.world_array[levels.world][levels.level]  , 0)
        seam.Load(0)
        
        #(16*int((self.MOUSE.rect.x /16)/3))*3 +TILE_X_POS , (16*int((self.MOUSE.rect.y /15)/3))*3

        #font.Generate_Message(self.player.name, 72, 48, (255, 255, 255), "name")
        #font.Generate_Message("time", group.geometry[0]-144, 48, (255, 255, 255), "name")
        self.gif = 13
        
        #font.Generate_Message("thank you!", 264, 216, (255, 255, 255), "i")
        #font.Generate_Message("but our princess is in", 120, 288, (255, 255, 255), "i")
        #font.Generate_Message("another castle!", 120, 336, (255, 255, 255), "i")
        
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.KEYDOWN: # cierre de emergencia ------
                if event.key == pygame.K_ESCAPE:
                    return True

                if event.key == pygame.K_F11:
                    if self.fullscreen:
                        self.fullscreen = False
                        group.geometry_scale = group.geometry_sub
                        pygame.display.set_mode(group.geometry_sub)

                    elif not self.fullscreen:
                        self.fullscreen = True
                        group.geometry_scale = group.geometry_full
                        pygame.display.set_mode(group.geometry_full, pygame.FULLSCREEN)

                if event.key == pygame.K_RETURN:
                    
                    if self.pause:
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
                        font.Kill_Identifier("pause")
                        self.pause = False

                    else:
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                        sound.pause_sound.stop()
                        sound.pause_sound.play()
                        font.Generate_Message("pause", int(group.geometry[0]/2-72), 360, (255, 255, 255), "pause")
                        self.pause = True

                if event.key == pygame.K_SPACE:
                    tile.Generate_Tile((group.geometry[0]/2, 300 ), "01i100" )
                    #tile_obj = tile.Spiny(0, 0)
                    #group.all_sprites.add(tile_obj)
                    #group.tile_sprites.add(tile_obj)


                if event.key == pygame.K_LEFT:
                    self.gif -= 1

                if event.key == pygame.K_RIGHT:
                    self.gif += 1

                    

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    for tile_obj in group.tile_sprites:
                        if pygame.sprite.collide_rect(tile_obj, self.MOUSE):
                            tile_obj.kill()
                            print("DELETED!!!!")
                    for tile_obj in group.coin_sprites:
                        if pygame.sprite.collide_rect(tile_obj, self.MOUSE):
                            tile_obj.kill()
                            print("DELETED!!!!")
                    for tile_obj in group.background_sprites:
                        if pygame.sprite.collide_rect(tile_obj, self.MOUSE):
                            tile_obj.kill()
                            print("DELETED!!!!")
                    for tile_obj in group.stair_sprites:
                        if pygame.sprite.collide_rect(tile_obj, self.MOUSE):
                            tile_obj.kill()
                            print("DELETED!!!!")
                        
            self.player.handle(event, self.pause)


    def run_logic(self, delta_time):
        if not self.pause:
            sound.Sound_Controller(self.player)
            score.display_goals(delta_time)
            tile.Global_Tile_Frame()
            animation.Global_Enemy_Frame()
            seam.Scroll(self.player, delta_time)
            seam.Seam(delta_time)
            group.all_sprites.update(delta_time)

        
    def display_frame(self, screen, fake_screen):
        fake_screen.fill(group.background_color)
        group.all_sprites.draw(fake_screen)
        screen.blit(pygame.transform.scale(fake_screen, group.geometry_scale), (0, 0))
        pygame.display.flip()


def main():
    screen = pygame.display.set_mode(group.geometry) #pygame.FULLSCREEN  
    fake_screen = screen.copy()
    pygame.display.set_mode(group.geometry_scale)
    
    pygame.display.set_caption("Super Mario Bros!!")

    icon_game = pygame.image.load("resources/sprite/smb icon.png")
    pygame.display.set_icon(icon_game)

    clock = pygame.time.Clock()
    game = Game()
    
    done = False
    while not done:
        delta_time = clock.tick(60)/1000  #.016666666666666 
        display_fps(clock)
        done = game.process_events()       
        game.run_logic(delta_time)
        game.display_frame(screen, fake_screen)
    pygame.quit()


if __name__ == "__main__":
    main()


"""#RETRASA EL PROGRAMA ?!?!?!?!?!?!?! >:C
    for number in range(0, 5):
        for sprite in group.all_sprites:
            if sprite.draw_level == number:
                sprite_to_draw = pygame.sprite.RenderPlain(sprite)
                sprite_to_draw.draw(screen)
    """

