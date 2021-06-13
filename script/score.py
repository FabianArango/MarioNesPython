import pygame
from pygame import *
pygame.init()

from script import font, group, sound, levels, seam

data = group.get_data()

score = int(data[4])
coin = int(data[5])
h_score = 0
lives = int(data[3])
time  = 0
time_goal = 0
can_time_goal = True

time_to_continue = group.Chronometer_Continuous(2)

def display_score():
    display_score = "00000000"+str(int(score))
    display_score = display_score[len(display_score)-9:len(display_score)]
    font.Kill_Identifier("display_score")
    font.Generate_Message(display_score, group.geometry[0]-(    ( len(display_score)*24  ) +164 )   , 72, (255, 255, 255), "display_score")


def display_coin():
    global coin, lives
    if coin >= 100:
        coin = 0
        lives += 1
        sound.coin_sound.stop()
        sound.one_up_sound.stop()
        sound.one_up_sound.play()


    display_coin = "0"+str(coin)
    display_coin = display_coin[len(display_coin)-2:len(display_coin)]
    font.Kill_Identifier("display_coin")
    font.Generate_Message("*"+display_coin, 48, 72, (255, 255, 255), "display_coin")


def display_time(delta_time):
    global time, score, can_time_goal, time_goal
    if not group.stop:
        for player in group.player_sprites:
            player = player
        if not player.auto_mode:
            can_time_goal = True
            if time > 0:
                time -= 0.01666666666*group.time*delta_time
            else:
                font.Generate_Message("time up!", int(group.geometry[0]/2-96), 312, (255, 255, 255), "screen")
                player.kill_player()

        elif player.right_collision[0]:
            if tuple(player.right_collision[1].sheet.get_clip()) == (32, 0, 16, 16):
                if can_time_goal:
                    time_goal = score + int(time)*50
                    can_time_goal = False
                    player.animation.set_visibility(False)

                if time > 0:
                    time -= 1 *group.time*delta_time
                    score += (1 *group.time*delta_time)*50

                else:
                    score = time_goal
                    if not bool(int(pygame.mixer.get_busy())) and time_to_continue.time_over():
                        time_to_continue.reset()
                        levels.level += 1

                        if levels.level >= 4:
                            levels.world += 1
                            levels.level = 0

                        seam.Clear()
                        group.all_sprites.add(seam.Black_Screen())
                        seam.Set_Data(levels.world_array[levels.world][levels.level], 0)
                        seam.Load(0)

    display_time = "00"+str(int(time))
    display_time = display_time[len(display_time)-3:len(display_time)]
    font.Kill_Identifier("display_time")
    font.Generate_Message("+"+display_time, group.geometry[0]-120, 72, (255, 255, 255), "display_time")


def display_goals(delta_time):
    display_score()
    display_coin()
    display_time(delta_time)


    #font.Generate_Message("*"+display_coin, 312-21, 72, (255, 255, 255), "display_coin")
    #font.Generate_Message(display_score, 72, 72, (255, 255, 255), "display_score")