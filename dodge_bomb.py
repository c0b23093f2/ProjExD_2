import os
import sys
import pygame as pg
from random import *
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
        pg.K_UP: (0, -5), 
        pg.K_DOWN: (0, 5), 
        pg.K_LEFT: (-5, 0), 
        pg.K_RIGHT: (5, 0)
        }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとん，または，爆弾のRect
    戻り値：真理値タプル（横判定結果，縦判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate
def game_over(screen):
    go_img = pg.Surface((WIDTH,HEIGHT))

    pg.draw.rect(go_img,(0,0,0),(0,0,WIDTH,HEIGHT))
    go_rct =go_img.get_rect()
    go_rct.center =WIDTH/2,HEIGHT/2
    go_img.set_alpha(100)
    crying_img = pg.image.load("fig/8.png")
    crying2_img = pg.image.load("fig/8.png")
    crying_rct = crying_img.get_rect(center=(WIDTH // 2-190, HEIGHT // 2))
    crying2_rct = crying2_img.get_rect(center=(WIDTH // 2+190, HEIGHT // 2))
    font = pg.font.Font(None, 80)
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    text_rect = game_over_text.get_rect(center=(WIDTH // 2-10, HEIGHT // 2))

    screen.blit(go_img,go_rct)

    screen.blit(crying_img, crying_rct)
    screen.blit(crying2_img, crying2_rct)
    screen.blit(game_over_text, text_rect)
    pg.display.update()
    time.sleep(5)


def main():
    rotate = {(0, -5):90,(5,0):180,(0,5):270,(-5,0):0,(5,-5):135,(5,5):225,(-5,5):315,(-5,-5):45}
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    num = 0
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    R_size = 50
    tm = 0
    bb = pg.Surface((R_size, R_size))
    pg.draw.circle(bb, (255, 0, 0), (20, 20), 10 + tm)
    bb.set_colorkey((0, 0, 0))
    bb_rct = bb.get_rect()
    bb_rct.centerx = randint(0, WIDTH)
    bb_rct.centery = randint(0, HEIGHT)
    vx, vy = 5, 5
    

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):  # 衝突判定
            
            return game_over(screen)

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横方向
                sum_mv[1] += tpl[1]  # 縦方向]
        #if sum_mv[0] != 0 or sum_mv[1] != 0:
        #    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), rotate[tuple(sum_mv)], 0.9)


        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        


        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb, bb_rct)

     

        pg.display.update()
        tmr += 1
        clock.tick(50)




if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
