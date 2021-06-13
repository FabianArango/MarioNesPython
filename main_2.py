import pygame
from pygame.locals import *
pygame.init()

from script import group, font, player, tile, animation, palette, score, enemy, seam, levels, sound, physic, obj

"""
    name

    world
    level
    lives

    score
    coins

    player size
    player fire
"""

class Game(object): 
    def __init__(self):
        group.init()
        physic.init()
        self.fullscreen = False
        self.pause = False

        self.main_menu = False
        self.message = 0

        self.menu_stade = None
        self.first_run = True

        group.all_sprites.add(animation.Coin_Display_Animation(24, 72))
        self.player = player.Player()
        group.all_sprites.add(self.player)
        group.player_sprites.add(self.player)

        self.start_menu()

        if self.player.name == "mario":
            self.name_palette = (174,  47,  40)

        if self.player.name == "luigi":
            self.name_palette = (36 , 151,   0)

        for n in range(0, 720, 48):  
            tile_obj = tile.Seam_Tile(n)
            group.all_sprites.add(tile_obj)
            group.tile_sprites.add(tile_obj)
            

    def start_menu(self):
        self.main_menu = True
        self.message = 0

        seam.Clear()
        seam.Set_Data(levels.tll, 0)
        seam.Load(0)

        group.stop = True
        #pygame.mixer.stop()
        #sound.stop()

        self.poster = font.Poster(  int(group.geometry[0]/2 -264) , 96)
        group.all_sprites.add(self.poster)

        self.cursor = font.Cursor( int(group.geometry[0]/2-168  ), 432   )
        group.all_sprites.add(self.cursor)

        self.player.right_velocity = 10
        self.player.animation.direction_x = False
        self.player.right_velocity = 0

        self.menu_message()


    def menu_message(self):
        self.menu_stade = "menu"
        font.Kill_Identifier("main")

        self.cursor.set_data(408, 504, ( int(group.geometry[0]/2-168  ), 408  ) )

        display_h_score = "00000"+str(int(score.h_score))
        display_h_score = display_h_score[len(display_h_score)-6:len(display_h_score)]

        font.Generate_Message("the fan made", int(group.geometry[0]/2-24), 360, (255, 206, 198), "main" )
        font.Generate_Message("play game!//options//exit", int(group.geometry[0]/2-120  ), 408, (255, 255, 255), "main" )
        #font.Generate_Message("options",     int(group.geometry[0]/2-120   ), 480, (255, 255, 255), "main" )
        
        #font.Generate_Message("top- "+display_h_score, int(group.geometry[0]/2-96), 552, (255, 255, 255), "main")


    def options_message(self):
        self.menu_stade = "options"

        font.Kill_Identifier("main")
        self.cursor.set_data(408, 552, ( int(group.geometry[0]/2-168  ), 408  )   )

        font.Generate_Message("skin//reset//credits//done", int(group.geometry[0]/2-120  ), 408, (255, 255, 255), "main" )
        font.Generate_Message("     " +self.player.name, int(group.geometry[0]/2-120  ), 408, self.name_palette, "main" )
        #font.Generate_Message("reset", int(group.geometry[0]/2-120  ), 480, (255, 255, 255), "main" )
        #font.Generate_Message("done", int(group.geometry[0]/2-120  ), 528, (255, 255, 255), "main" )

    
    def credit_message(self):
        self.menu_stade = "credit"
        font.Kill_Identifier("main")
        font.Generate_Message("this game was programed by/fabian santiago", int(group.geometry[0]/2-120  ), 432, (255, 255, 255), "main" )


    def start_game(self):
        font.Kill_Identifier("main")
        self.main_menu = False    
        
        #levels.world = int(data[1])

        #levels.level = int(data[2])
        #score.lives  = int(data[3])

        seam.Clear()
        group.all_sprites.add(seam.Black_Screen())
        seam.Set_Data(levels.world_array[levels.world][levels.level], 0)
        seam.Load(0) # 188


    def controll_game_over(self):
        if group.game_over and not group.stop:
            group.game_over = False
            self.start_menu()


    def save_game(self):
        group.write_data(  (str(levels.world), str(levels.level), str(score.lives), 

                            str(score.score), str(score.coin),

                            str(int(self.player.size)), str(int(self.player.fire_power)) ) , (1, 2, 3, 4, 5, 6, 7)  )


    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #self.save_game()
                return True

            try:
                cursor_r = self.cursor.handle(event)

            except:
                pass

            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE: # cierre de emergencia ------
                    return True

                if event.key == pygame.K_SPACE:
                    pass

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
                    if not self.main_menu:
                        if self.pause:
                            font.Kill_Identifier("pause")
                            self.pause = False
                            self.cursor.kill()
                            if cursor_r == 360:
                                sound.unpause()
                                pygame.mixer.unpause()
                                
                            if cursor_r == 408:
                                self.start_menu()
                                self.save_game()
                                break
                            
                        else:
                            sound.pause()
                            pygame.mixer.pause()
                            sound.pause_sound.stop()
                            sound.pause_sound.play()
                            if not group.stop and not self.player.auto_mode:
                                font.Generate_Message("continue game//save and quit", int(group.geometry[0]/2-120), 360, (255, 255, 255), "pause")
                                b_limit = 408

                            else:
                                font.Generate_Message("continue game", int(group.geometry[0]/2-120), 360, (255, 255, 255), "pause")
                                b_limit = 360

                            self.cursor = font.Cursor( int(group.geometry[0]/2-168  ), 432   )
                            group.all_sprites.add(self.cursor)

                            self.cursor.set_data(360, b_limit, ( int(group.geometry[0]/2-168), 360)   )

                            self.pause = True                        

            if self.main_menu:
                if self.menu_stade == "menu":
                    if cursor_r == 408:
                        self.start_game()

                    if cursor_r == 456:
                        self.options_message()

                    if cursor_r == 504:
                        self.save_game()
                        return True

                elif self.menu_stade == "options":
                    if cursor_r == 408:
                        if self.player.name == "mario":
                            self.player.name = "luigi"
                            self.name_palette = (36 , 151,   0)

                        elif self.player.name == "luigi":
                            self.player.name = "mario"
                            self.name_palette = (174,  47,  40)

                        self.options_message()

                    if cursor_r == 456:
                        if group.reset_warning == 0:
                            font.Kill_Identifier("reset_warning")
                            font.Generate_Message("//      are you sure", int(group.geometry[0]/2-120  ), 408, (174,  47,  40), "reset_warning")
                            group.reset_warning += 1

                        elif group.reset_warning == 1:
                            font.Kill_Identifier("reset_warning")
                            font.Generate_Message("//      very sure", int(group.geometry[0]/2-120  ), 408, (174,  47,  40), "reset_warning")
                            group.reset_warning += 1

                        elif group.reset_warning == 2:
                            font.Kill_Identifier("reset_warning")
                            font.Generate_Message("//      game reset", int(group.geometry[0]/2-120  ), 408, (174,  47,  40), "reset_warning")

                            levels.world = 0
                            levels.level = 0
                            score.lives  = 3

                            score.coin =  0
                            score.score = 0

                            if self.player.size:
                                self.player.rect.y += 45

                            self.player.size = False
                            self.player.fire_power = False

                            self.player.resize(False)
                            self.player.resize(False)

                            group.reset_warning = 0

                            self.save_game()
                        

                    if cursor_r == 552:
                        self.menu_message()
                        group.write_data(  (self.player.name, ),    (0, )   )

            else:
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
            self.controll_game_over()


    def display_frame(self, screen, fake_screen):
        fake_screen.fill(group.background_color)
        group.all_sprites.draw(fake_screen)
        screen.blit(pygame.transform.scale(fake_screen, group.geometry_scale), (0, 0))
        # screen.blit(pygame.transform.scale(fake_screen, (16*26, 16*15)), (0, 0))
        pygame.display.flip()


def display_fps(clock):
    font.Kill_Identifier("fps")
    font.Generate_Message(str( int( clock.get_fps() ) ), group.geometry[0]-56, 144, (255, 255, 255), "fps")
    #font.Generate_Message( str(len(group.enemy_sprites)), group.geometry[0]-72, 72, (255, 255, 255), "fps"  )


def main():
    screen = pygame.display.set_mode(group.geometry) #pygame.FULLSCREEN  
    # screen = pygame.display.set_mode( (16*26*3, 16*15*3)    ) #pygame.FULLSCREEN  
    fake_screen = screen.copy()
    pygame.display.set_mode(group.geometry_scale)
    # pygame.display.set_mode( (16*26, 16*15)  )
    
    pygame.display.set_caption("Super Mario Bros!!")

    icon_game = pygame.image.load("resources/sprite/smb icon.png")
    pygame.display.set_icon(icon_game)

    clock = pygame.time.Clock()
    game = Game()
    
    done = False
    while not done:
        delta_time = clock.tick(60)/1000  #.016666666666666 
        #display_fps(clock)
        done = game.process_events()       
        game.run_logic(delta_time)
        game.display_frame(screen, fake_screen)
    pygame.quit()


if __name__ == "__main__":
    main()