import pygame
from pygame.locals import * 
pygame.init()

from script import group, score

volume = .4


# efectos de sonido -----------------------------------------------------------
pipe_sound     = pygame.mixer.Sound("resources\sound fx\smb_pipe.wav")
pipe_sound.set_volume(volume)

stomp_sound = pygame.mixer.Sound("resources\sound fx\smb_stomp.wav")
stomp_sound.set_volume(volume)

kick_sound  = pygame.mixer.Sound("resources\sound fx\smb_kick.wav")
kick_sound.set_volume(volume)

fireworks_sound = pygame.mixer.Sound("resources\sound fx\smb_fireworks.wav")
fireworks_sound.set_volume(volume)

fireball_sound = pygame.mixer.Sound("resources\sound fx\smb_fireball.wav")
fireball_sound.set_volume(volume)

power_up_appears_sound = pygame.mixer.Sound("resources\sound fx\smb_powerup_appears.wav")
power_up_appears_sound.set_volume(volume)

power_up_sound = pygame.mixer.Sound("resources\sound fx\smb_powerup.wav")
power_up_sound.set_volume(volume)

one_up_sound   = pygame.mixer.Sound("resources\sound fx\smb_1-up.wav")
one_up_sound.set_volume(volume)

jump_small_sound = pygame.mixer.Sound("resources/sound fx/smb_jump-small.wav")
jump_small_sound.set_volume(volume)

jump_super_sound = pygame.mixer.Sound("resources/sound fx/smb_jump-super.wav")
jump_super_sound.set_volume(volume)

coin_sound = pygame.mixer.Sound("resources/sound fx/smb_coin.wav")
coin_sound.set_volume(volume)

breakblock_sound = pygame.mixer.Sound("resources/sound fx/smb_breakblock.wav")
breakblock_sound.set_volume(volume)

bump_sound = pygame.mixer.Sound("resources/sound fx/smb_bump.wav")
bump_sound.set_volume(volume)

vine_sound = pygame.mixer.Sound("resources/sound fx/smb_vine.wav")
vine_sound.set_volume(volume)

flag_pole_sound = pygame.mixer.Sound("resources\sound fx\smb_flagpole.wav")
flag_pole_sound.set_volume(volume)

pause_sound = pygame.mixer.Sound("resources/sound fx/smb_pause.wav")
pause_sound.set_volume(volume)

player_die_sound = pygame.mixer.Sound("resources/music_fx/smb_mariodie.wav")
player_die_sound.set_volume(volume)

game_over_sound = pygame.mixer.Sound("resources\music_fx\smb_gameover.wav")
game_over_sound.set_volume(volume)

skid_sound = pygame.mixer.Sound("resources\sound fx\smb_skid.wav")
skid_sound.set_volume(volume)

warning_sound = pygame.mixer.Sound("resources\music_fx\smb_warning.wav")
warning_sound.set_volume(volume)

stage_clear = pygame.mixer.Sound("resources\music_fx\smb_stage_clear.wav")
stage_clear.set_volume(volume)

bowserfire_sound = pygame.mixer.Sound("resources\sound fx\smb_bowserfire.wav")
bowserfire_sound.set_volume(volume)

bowserfall_sond = pygame.mixer.Sound("resources\sound fx\smb_bowserfalls.wav")
bowserfall_sond.set_volume(volume)

world_clear_sound_simple = pygame.mixer.Sound("resources\music_fx\smb_world_clear_simple.wav")
world_clear_sound_simple.set_volume(volume)

world_clear_sound_bowser = pygame.mixer.Sound("resources\music_fx\smb_world_clear_bowser.wav")
world_clear_sound_bowser.set_volume(volume)

end_sound = pygame.mixer.Sound("resources\music_fx\smd_ending.wav")
end_sound.set_volume(volume)


# musica -------------------------------------------------------------------

o_w_theme_1 = pygame.mixer.Sound("resources/music/01 - Super Mario Bros.ogg")
o_w_theme_1.set_volume(volume)

o_w_theme_2 = pygame.mixer.Sound("resources/music/03 - Hurry - Super Mario Bros.ogg")
o_w_theme_2.set_volume(volume)

u_g_theme_1 = pygame.mixer.Sound("resources/music/06 - Underground.ogg")
u_g_theme_1.set_volume(volume)

u_g_theme_2 = pygame.mixer.Sound("resources/music/07 - Hurry - Underground.ogg")
u_g_theme_2.set_volume(volume)

w_t_1 = pygame.mixer.Sound("resources/music/08 - Water World.ogg")
w_t_1.set_volume(volume)

w_t_2 = pygame.mixer.Sound("resources/music/09 - Hurry - Water World.ogg")
w_t_2.set_volume(volume)

c_t_1 = pygame.mixer.Sound("resources/music/10 - Castle.ogg")
c_t_1.set_volume(volume)

c_t_2 = pygame.mixer.Sound("resources/music/11 - Hurry - Castle.ogg")
c_t_2.set_volume(volume)

star_man_theme   = pygame.mixer.Sound("resources/music/02 - Invincibility Star.wav")
star_man_theme.set_volume(volume)

s_th = pygame.mixer.Sound("resources/music/01 - Short Theme.ogg")
s_th.set_volume(volume)


over_world_theme   = (o_w_theme_1, o_w_theme_2)
under_ground_theme = (u_g_theme_1, u_g_theme_2)
wather_theme       = (w_t_1, w_t_2)
castle_theme       = (c_t_1, c_t_2)
sky_theme          = (star_man_theme, star_man_theme)
short_theme        = (s_th, o_w_theme_2)

hurry = False

main_theme = None

song = None

index = 0

# funciones -------------------------------------

def load(song_to):
    global song

    try:
        stop()

    except:
        pass
    
    song = song_to

def play(r=1):
    song.play(r)

def stop():
    song.stop()

def pause():
    pass

def unpause():
    pass

def set_volume():
    pass

def get_busy():
    return pygame.mixer.get_busy()


def Sound_Controller(player):
    global hurry, index

    if not hurry and not group.stop and not player.auto_mode:
        if score.time <= 91:
            stop()
            warning_sound.stop()
            warning_sound.play()
            index = 1
            hurry = True

    elif hurry:
        if not bool(int(pygame.mixer.get_busy())) and score.time <= 91 and not bool(int(get_busy())) and not group.stop and not player.auto_mode:
            stop()
            load(main_theme[index])
            play(-1)

        if score.time >= 92:
            hurry = False
