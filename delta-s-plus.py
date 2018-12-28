# -*- coding: utf-8 -*-

# imports
import sys
import os
import pygame
import pytmx
from pytmx.util_pygame import load_pygame

pygame.init()

# verification (.exe or .py)

if getattr(sys, 'frozen', False):
    # The application is frozen
    verf_exe_py = os.path.dirname(sys.executable)
else:
    # The application is not frozen
    verf_exe_py = ''

# screen
pygame.display.set_caption("Delta S+")
scr_size = scr_width, scr_height = 800, 576
displaysurf = pygame.display.set_mode(scr_size)

# fps
t_fps = 60

# colors
black = (0, 0, 0, 180)
white = (255, 255, 255)

# intro
bomb = pygame.image.load(os.path.join(verf_exe_py, 'data', 'images', 'bomb.png'))
bomb_siz = bomb.get_size()
bomb_x, bomb_y = (scr_width - bomb_siz[0])/2, 100

# endscreen
curtain = displaysurf.convert_alpha()
curtain.fill(black)

# clock
game_clock = pygame.time.Clock()

# map
map_url = os.path.join(verf_exe_py, 'data', 'map', 'MTFG_Fase1_Map.tmx')
tmxdata = load_pygame(map_url)

#layers
entds_layer = tmxdata.get_layer_by_name('Entidades')

# tiles
ts = tw, th = tmxdata.tilewidth, tmxdata.tileheight
manip_tiles = [(1, 1), (2, 1), (1, 2), (2, 2), (22, 1), (23, 1), (22, 2), (23, 2), (22, 15), (23, 15), (22, 16), (23, 16), (1, 16)]

rot_pump_t = manip_tiles[:4]
cent_pump_t = manip_tiles[4:8]
pist_pump_t = manip_tiles[8:12]

player_t = manip_tiles[12]
player_xi, player_yi = player_t[0] * tw, player_t[1] * th

# surfaces & rects
vessel_rects = []
ves_dx, ves_dy = 7, 6
ves_w, ves_h = tw - 2*ves_dx, th - 2*ves_dy

rot_pump_s1 = pygame.image.load(os.path.join(verf_exe_py, 'data', 'images', 'MTFG_Fase1_Rot_Pump1.png'))
rot_pump_s2 = pygame.image.load(os.path.join(verf_exe_py, 'data', 'images', 'MTFG_Fase1_Rot_Pump2.png'))
rot_pump_s = rot_pump_s1

cent_pump_s1 = pygame.image.load(os.path.join(verf_exe_py, 'data', 'images', 'MTFG_Fase1_Cent_Pump1.png'))
cent_pump_s2 = pygame.image.load(os.path.join(verf_exe_py, 'data', 'images', 'MTFG_Fase1_Cent_Pump2.png'))
cent_pump_s = cent_pump_s1

pist_pump_s1 = pygame.image.load(os.path.join(verf_exe_py, 'data', 'images', 'MTFG_Fase1_Rec_Pump1.png'))
pist_pump_s2 = pygame.image.load(os.path.join(verf_exe_py, 'data', 'images', 'MTFG_Fase1_Rec_Pump2.png'))
pist_pump_s = pist_pump_s1

player_s = tmxdata.get_tile_image(player_t[0], player_t[1], 1)

rot_pump_r = rot_pump_s1.get_rect()
cent_pump_r = cent_pump_s1.get_rect()
pist_pump_r = pist_pump_s1.get_rect()

rot_pump_r.topleft = (rot_pump_t[0][0] * tw, rot_pump_t[0][1] * th)
cent_pump_r.topleft = (cent_pump_t[0][0] * tw, cent_pump_t[0][1] * th)
pist_pump_r.topleft = (pist_pump_t[0][0] * tw, pist_pump_t[0][1] * th)

pumps_rects = [rot_pump_r, cent_pump_r, pist_pump_r]

player_r = pygame.Rect((player_xi + 2), (player_yi + 2), 32 - 2*2, 32 - 2*2)

for tile in entds_layer.tiles():
    x, y, image = tile
    if (x, y) not in manip_tiles:
        ves_rect = pygame.Rect(((x * tw) + ves_dx, (y * th) + ves_dy), (ves_w, ves_h))
        vessel_rects.append(ves_rect)

# map render
def render():
    for layer in tmxdata.visible_layers:
        if layer.name == 'Chao':
            for tile in layer.tiles():
                x, y, image = tile
                displaysurf.blit(image, (x * tw, y * th))
        else:
            for tile in layer.tiles():
                x, y, image = tile
                if (x, y) not in manip_tiles:
                    displaysurf.blit(image, (x * tw, y * th))

# intro render
def intro():
    font_obj = pygame.font.Font(os.path.join(verf_exe_py, 'data', 'fonts', 'freesansbold.ttf'), 30)

    text1 = font_obj.render(u'Vá até a(s) bomba(s) de deslocamento positivo', 1, black, white)
    t1_siz = text1.get_size()
    t1_x, t1_y = (scr_width - t1_siz[0])/2, 350

    text2 = font_obj.render(u'[Aperte Qualquer Tecla]', 1, black, white)
    t2_siz = text2.get_size()
    t2_x, t2_y = (scr_width - t2_siz[0])/2, t1_y + 60

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os._exit(1)
            elif event.type == pygame.KEYDOWN:
                run = False

        render()
        displaysurf.blit(text1, (t1_x, t1_y))
        displaysurf.blit(text2, (t2_x, t2_y))
        displaysurf.blit(bomb, (bomb_x, bomb_y))

        pygame.display.flip()
        game_clock.tick(t_fps)
        fps = game_clock.get_fps()
        pygame.display.set_caption('Delta S+ (%.1f fps)' % fps)

# endscreen render
def endscreen(result):
    tela = displaysurf.copy()

    if result == ans:
        text = u'Você ganhou :)'
    else:
        text = u'Você perdeu :P'

    font_obj = pygame.font.Font(os.path.join(verf_exe_py, 'data', 'fonts', 'freesansbold.ttf'), 30)

    text1 = font_obj.render(text, 1, white)
    t1_siz = text1.get_size()
    t1_x, t1_y = (scr_width - t1_siz[0])/2, 150

    text2 = font_obj.render(u'Jogar novamente? [S/N]', 1, white)
    t2_siz = text2.get_size()
    t2_x, t2_y = (scr_width - t2_siz[0])/2, t1_y + 150

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os._exit(1)

        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_s]:
            run = False
        elif tecla[pygame.K_n]:
            os._exit(1)

        displaysurf.blit(tela, (0, 0))
        displaysurf.blit(curtain, (0, 0))
        displaysurf.blit(text1, (t1_x, t1_y))
        displaysurf.blit(text2, (t2_x, t2_y))

        pygame.display.flip()
        game_clock.tick(t_fps)
        fps = game_clock.get_fps()
        pygame.display.set_caption('Delta S+ (%.1f fps)' % fps)
        
# interaction variables
grab = 0

rtp_st = 0
cp_st = 0
pp_st = 0

# answer
ans = (1, 0, 1)

# intro key
intro_key = 0

# main loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os._exit(1)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if player_r.left < event.pos[0] < player_r.right and player_r.top < event.pos[1] < player_r.bottom:
                    grab = 1
                    dist_mb_x, dist_mb_y = event.pos[0] - player_r.left, event.pos[1] - player_r.top
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if grab == 1:
                    grab = 0
                    for pr in pumps_rects:
                        if pr.left < player_r.center[0] < pr.right and pr.top < player_r.center[1] < pr.bottom:
                            pri = pumps_rects.index(pr)
                            if pri == 0:
                                if rtp_st == 0:
                                    rot_pump_s = rot_pump_s2
                                    rtp_st = 1
                                else:
                                    rot_pump_s = rot_pump_s1
                                    rtp_st = 0
                            elif pri == 1:
                                if cp_st == 0:
                                    cent_pump_s = cent_pump_s2
                                    cp_st = 1
                                else:
                                    cent_pump_s = cent_pump_s1
                                    cp_st = 0
                            else:
                                if pp_st == 0:
                                    pist_pump_s = pist_pump_s2
                                    pp_st = 1
                                else:
                                    pist_pump_s = pist_pump_s1
                                    pp_st = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == 13:
                endscreen((rtp_st, cp_st, pp_st))
                grab = 0
                rtp_st = 0
                cp_st = 0
                pp_st = 0
                ans = (1, 0, 1)
                player_r.topleft = (player_xi + 2), (player_yi + 2)
                rot_pump_s = rot_pump_s1
                cent_pump_s = cent_pump_s1
                pist_pump_s = pist_pump_s1

    mouse_p = pygame.mouse.get_pos()
    tecla = pygame.key.get_pressed()

    if intro_key == 0:
        intro()
        intro_key = 1

    if grab == 1:
        player_r.topleft = mouse_p[0] - dist_mb_x, mouse_p[1] - dist_mb_y

    for v in vessel_rects:
        if player_r.colliderect(v):
            endscreen((0, 0, 0))
            grab = 0
            rtp_st = 0
            cp_st = 0
            pp_st = 0
            ans =(1, 0, 1)
            player_r.topleft = (player_xi + 2), (player_yi + 2)
            rot_pump_s = rot_pump_s1
            cent_pump_s = cent_pump_s1
            pist_pump_s = pist_pump_s1

    render()
    displaysurf.blit(rot_pump_s, rot_pump_r)
    displaysurf.blit(cent_pump_s, cent_pump_r)
    displaysurf.blit(pist_pump_s, pist_pump_r)
    displaysurf.blit(player_s, (player_r.topleft[0] - 2, player_r.topleft[1] - 2))

    pygame.display.flip()
    game_clock.tick(t_fps)
    fps = game_clock.get_fps()
    pygame.display.set_caption('Delta S+ (%.1f fps)' % fps)
