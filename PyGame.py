from random import randint
from math import acos, pi
import pygame as pg


class MainCharacter(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('Character.png')
        self.rect = self.image.get_rect()
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.land = [[], [], []]
        self.la_x = 0
        self.la_y = 0
        # for i in range(3):
        #    a = []
        #    for j in range(3):
        #        field = pg.sprite.Sprite()
        #        field_image = pg.image.load('check_field.png')
        #        field.image = field_image
        #        field.rect = field.image.get_rect()
        #        field.rect.x = 1000 * i - 1000
        #        field.rect.y = 1000 * j - 1000
        #        a.append(field)
        #    self.land[i] = a


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('enemy.png')
        self.rect = self.image.get_rect()
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.rect.x, self.rect.y = randint(0, 970), randint(0, 950)
        distance = ((500 - self.rect.x) ** 2 + (500 - self.rect.y) ** 2) ** 0.5
        self.speed = [int((500 - self.rect.x) / (distance / (speed - 2))),
                      int((500 - self.rect.y) / (distance / (speed - 2)))]
        self.f = 0

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        distance = ((500 - self.rect.x) ** 2 + (500 - self.rect.y) ** 2) ** 0.5
        self.speed = [int((500 - self.rect.x) / (distance / (speed - 2))),
                      int((500 - self.rect.y) / (distance / (speed - 2)))]
        if self.rect.x < 500 and not self.f:
            self.f = 1
            self.image = pg.transform.flip(self.image, True, False)
        if self.rect.x > 500 and self.f:
            self.f = 0
            self.image = pg.transform.flip(self.image, True, False)


class Bullet(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.life = 1  # ОБРАТИ ВНИМАНИЕ!!! ХП нужны для пробивания врагов!
        self.image = pg.image.load('bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 500, 500
        # self.image = pg.transform.rotate(self.image, 45)
        self.sp = 20
        mx, my = 5000, 5000
        for i in enemies:
            if (i.rect.x - 500) ** 2 + (i.rect.y - 500) ** 2 < (mx - 500) ** 2 + (my - 500) ** 2:
                mx, my = i.rect.x, i.rect.y
        distance = ((mx - 500) ** 2 + (my - 500) ** 2) ** 0.5

        self.image = pg.transform.rotate(self.image, acos((self.rect.x - mx) / distance) * 180 / pi % 91)
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.speed = [int((mx - 500) / (distance / self.sp)),
                      int((my - 500) / (distance / self.sp))]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]


if __name__ == '__main__':
    pg.init()

    width = 1000
    height = 1000
    screen = pg.display.set_mode((width, height))

    move_up, move_down, move_left, move_right = False, False, False, False
    tp_l, tp_r, tp_u, tp_d = False, False, False, False
    speed = 7

    main_char = MainCharacter()
    land = [[], [], []]
    la_x = 0
    la_y = 0
    for i in range(3):
        a = []
        for j in range(3):
            field = pg.sprite.Sprite()
            field_image = pg.image.load('check_field.png')
            field.image = field_image
            field.rect = field.image.get_rect()
            field.rect.x = 1000 * i - 1000
            field.rect.y = 1000 * j - 1000
            a.append(field)
        land[i] = a

    fps = 50
    count = 1
    clock = pg.time.Clock()
    running = True

    enemies = pg.sprite.Group()
    projectiles = pg.sprite.Group()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    move_up = True
                if event.key == pg.K_a:
                    move_left = True
                if event.key == pg.K_s:
                    move_down = True
                if event.key == pg.K_d:
                    move_right = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_w:
                    move_up = False
                if event.key == pg.K_a:
                    move_left = False
                if event.key == pg.K_s:
                    move_down = False
                if event.key == pg.K_d:
                    move_right = False
        count += 1
        if count % 50 == 0:
            enemies.add(Enemy())
        if count % 60 == 0:
            projectiles.add(Bullet())

        for i in land:
            for j in i:
                j.rect.x -= speed * int(move_right) - speed * int(move_left)
                j.rect.y -= speed * int(move_down) - speed * int(move_up)
        for i in enemies:
            i.rect.x -= speed * int(move_right) - speed * int(move_left)
            i.rect.y -= speed * int(move_down) - speed * int(move_up)
        for i in projectiles:
            i.rect.x -= speed * int(move_right) - speed * int(move_left)
            i.rect.y -= speed * int(move_down) - speed * int(move_up)

        screen.fill('black')
        if land[1][1].rect.x >= 1000:
            tp_l = True
        elif land[1][1].rect.x <= -1000:
            tp_r = True
        if land[1][1].rect.y >= 1000:
            tp_u = True
        elif land[1][1].rect.y <= -1000:
            tp_d = True
        for i in range(3):
            for j in range(3):
                land[i][j].rect.x += int(tp_r) * 1000 - int(tp_l) * 1000
                land[i][j].rect.y += int(tp_d) * 1000 - int(tp_u) * 1000
        tp_l, tp_r, tp_u, tp_d = False, False, False, False
        for i in land:
            for j in i:
                screen.blit(j.image, (j.rect.x, j.rect.y))
        screen.blit(main_char.image, (width // 2 - main_char.rect.width // 2, height // 2 - main_char.rect.height // 2))
        enemies.update()
        enemies.draw(screen)
        projectiles.update()
        projectiles.draw(screen)
        pg.display.flip()
        clock.tick(fps)
    pg.quit()
