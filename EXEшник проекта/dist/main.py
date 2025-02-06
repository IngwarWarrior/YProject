import time
from math import acos, pi
from random import randint, choice

import pygame as pg


class MainMenu(pg.sprite.Sprite):
    running = True
    choosing = False
    ch_level = False
    pause = False
    main_menu = True
    ending = False

    def __init__(self):
        super().__init__()

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                MainMenu.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    MainMenu.main_menu = False
                    MainMenu.ch_level = True
                    self.kill()
                if event.key == pg.K_2:
                    MainMenu.running = False
                if event.key == pg.K_ESCAPE:
                    MainMenu.running = False


class MainCharacter(pg.sprite.Sprite):
    def __init__(self):
        self.ans = [[pg.image.load('charsu1.png'), pg.image.load('charsu2.png')],
                    [pg.image.load('charru1.png'), pg.image.load('charru2.png')],
                    [pg.image.load('charrd1.png'), pg.image.load('charrd2.png')],
                    [pg.image.load('charsd1.png'), pg.image.load('charsd2.png')],
                    [pg.image.load('charld1.png'), pg.image.load('charld2.png')],
                    [pg.image.load('charlu1.png'), pg.image.load('charlu2.png')]]
        self.cur = self.ans[3]
        super().__init__()
        self.image = pg.image.load('Character.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 475, 450
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.mask = pg.mask.from_surface(self.image)
        self.hitf = {}

    def update(self):
        if move_right:
            if move_up:
                self.cur = self.ans[1]
            else:
                self.cur = self.ans[2]
        elif move_left:
            if move_up:
                self.cur = self.ans[5]
            else:
                self.cur = self.ans[4]
        else:
            if move_up:
                self.cur = self.ans[0]
            else:
                self.cur = self.ans[3]
        self.image = self.cur[(count // 25) % 2]
        for i in enemies:
            if pg.sprite.collide_mask(self, i) and i not in self.hitf:
                self.hitf[i] = 0
                hearts.minus()
            elif i in self.hitf and not pg.sprite.collide_mask(self, i):
                self.hitf.pop(i)
        popkeys = []
        for i in self.hitf:
            self.hitf[i] += 1
            if self.hitf[i] == 50:
                popkeys.append(i)
        for i in popkeys:
            self.hitf.pop(i)
        if pg.sprite.spritecollide(self, hill, dokill=True):
            hearts.plus()
        if pg.sprite.spritecollide(self, gears, dokill=True):
            MainMenu.choosing = True


class Enemy(pg.sprite.Sprite):
    animations = [[pg.image.load('Slime1.png'), pg.image.load('Slime2.png'), pg.image.load('Slime3.png'),
                   pg.image.load('Slime4.png'), pg.image.load('Slime5.png')],
                  [pg.image.load('Slime13.png'), pg.image.load('Slime23.png'), pg.image.load('Slime33.png'),
                   pg.image.load('Slime43.png'), pg.image.load('Slime53.png')],
                  [pg.image.load('Slime12.png'), pg.image.load('Slime22.png'), pg.image.load('Slime32.png'),
                   pg.image.load('Slime42.png'), pg.image.load('Slime52.png')]]
    num = 0

    def __init__(self):
        super().__init__()
        self.list = Enemy.animations[randint(0, 2)]
        self.count = [count, randint(0, 4)]
        self.image = self.list[self.count[1]]
        self.rect = self.image.get_rect()
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.mask = pg.mask.from_surface(self.image)
        self.rect.x, self.rect.y = randint(0, 970), randint(0, 950)
        self.distance = ((485 - self.rect.x) ** 2 + (475 - self.rect.y) ** 2) ** 0.5
        self.speed = [int((485 - self.rect.x) / ((self.distance + 1) / (speed - 2 - diff))),
                      int((475 - self.rect.y) / ((self.distance + 1) / (speed - 2 - diff)))]
        self.f = 0
        self.hp = (level.level * 5 + 5) * diff
        self.hitf = {}

    def update(self):
        if (count - self.count[0]) % 10 == 0:
            self.count[1] = (self.count[1] + 1) % 5
            self.image = self.list[self.count[1]]
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        for i in enemies:
            if pg.sprite.collide_mask(self, i) and i != self:
                self.rect.x -= self.speed[0]
                self.rect.y -= self.speed[1]
        self.distance = ((485 - self.rect.x) ** 2 + (475 - self.rect.y) ** 2) ** 0.5
        self.speed = [int((485 - self.rect.x) / ((self.distance + 1) / (speed - 2 - diff))),
                      int((475 - self.rect.y) / ((self.distance + 1) / (speed - 2 - diff)))]
        if self.rect.x < 485 and not self.f:
            self.f = 1
            self.image = pg.transform.flip(self.image, True, False)
        if self.rect.x > 485 and self.f:
            self.f = 0
            self.image = pg.transform.flip(self.image, True, False)

        for i in projectiles:
            if pg.sprite.collide_mask(self, i) and i not in self.hitf:
                self.hitf[i] = 0
                self.hp -= i.damage
                i.life -= 1
            elif i in self.hitf and not pg.sprite.collide_mask(self, i):
                self.hitf.pop(i)
        if self.hp <= 0:
            Enemy.num += 1
            self.kill()
        popkeys = []
        for i in self.hitf:
            self.hitf[i] += 1
            if self.hitf[i] == 25:
                popkeys.append(i)
        for i in popkeys:
            self.hitf.pop(i)
        if self.rect.x >= 5000 or self.rect.x <= -4000 or self.rect.y >= 5000 or self.rect.y <= - 4000:
            self.kill()


class Bullet(pg.sprite.Sprite):
    life = 1
    damage = 10
    number = 1

    def __init__(self):
        super().__init__()
        self.life = Bullet.life  # ОБРАТИ ВНИМАНИЕ!!! ХП нужны для пробивания врагов!
        self.damage = Bullet.damage
        self.image = pg.image.load('bullet.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 500, 500
        self.sp = 20
        mx, my = 5000, 5000
        for i in enemies:
            if ((i.rect.x + 15) - 500) ** 2 + ((i.rect.y + 25) - 500) ** 2 < (mx - 500) ** 2 + (my - 500) ** 2:
                mx, my = i.rect.x + 5, i.rect.y + 15
        distance = ((mx - 500) ** 2 + (my - 500) ** 2) ** 0.5

        if (my <= 500 <= mx) or (mx <= 500 <= my):
            self.image = pg.transform.rotate(self.image, acos(abs(self.rect.x - mx) / distance) * 180 / pi % 91)
        else:
            self.image = pg.transform.rotate(self.image, 0 - acos(abs(self.rect.x - mx) / distance) * 180 / pi % 91)
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.mask = pg.mask.from_surface(self.image)
        self.speed = [int((mx - 500) / ((distance + 1) / self.sp)),
                      int((my - 500) / ((distance + 1) / self.sp))]

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        if self.rect.x >= 5000 or self.rect.x <= -4000 or self.rect.y >= 5000 or self.rect.y <= - 4000:
            self.kill()
        if self.life == 0:
            self.kill()


class Stopwatch:
    def __init__(self, screen):
        self.screen = screen
        self.image = pg.image.load('table.png')
        self.image = pg.transform.rotate(self.image, 90)
        self.image = pg.transform.scale(self.image, (300, 200))
        self.font = pg.font.Font("Comic Sans MS.ttf", 25)  # Шрифт для отображения времени
        self.running = True  # Флаг для управления работой секундомера
        self.start_time = time.time()  # Время запуска секундомера

    def update(self):
        if self.running:
            elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(int(elapsed_time), 60)

            timer_display = f"{minutes:02}:{seconds:02}"

            # Отображение времени в правом верхнем углу
            text_surface = self.font.render(timer_display, True, (255, 255, 255))
            text_rect = text_surface.get_rect(topright=(self.screen.get_width() - 30, 55))
            self.screen.blit(text_surface, text_rect)

    def stop(self):
        self.running = False  # Остановка секундомера

    def time(self):
        elapsed_time = time.time() - self.start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        return minutes, seconds


class Level:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.Font("Comic Sans MS.ttf", 25)  # Шрифт для текста
        self.level = 1
        self.max_level = 25
        self.start_time = time.time()  # Запоминаем время начала
        self.level_up_interval = 30  # Интервал повышения уровня в секундах

    def update(self):
        # Проверяем, прошло ли 30 секунд с последнего повышения уровня
        current_time = time.time()
        if current_time - self.start_time >= self.level_up_interval:
            if self.level < self.max_level:
                self.level += 1
            self.start_time = current_time  # Обновляем время

    def get_color(self):
        # Плавное изменение цвета от зеленого к красному
        ratio = (self.level - 1) / (self.max_level - 1)
        blue = int(255 * (1 - ratio))  # Зеленый уменьшается
        red = int(255 * ratio)  # Красный увеличивается
        return (red, 0, blue)

    def color(self):
        color = self.get_color()
        text_surface = self.font.render(f'Level: {self.level}', True, color)
        text_rect = text_surface.get_rect(topright=(self.screen.get_width() - 180, 55))
        self.screen.blit(text_surface, text_rect)


class Hearts:
    def __init__(self, screen):
        self.screen = screen
        self.max_hearts = 5
        self.current_hearts = 5
        self.heart_image = pg.image.load("heart.png")  # Загрузка изображения сердечка
        self.heart_image = pg.transform.scale(self.heart_image, (40, 40))  # Изменение размера изображения
        self.heart_spacing = 5  # Промежуток между сердечками

    def plus(self):
        if self.current_hearts < self.max_hearts:
            self.current_hearts += 1

    def minus(self):
        if self.current_hearts > 0:
            self.current_hearts -= 1

    def draw(self):
        for i in range(self.current_hearts):
            x = self.screen.get_width() - (i + 1) * (self.heart_image.get_width() + self.heart_spacing) - 36
            y = 100  # Расположение по вертикали
            self.screen.blit(self.heart_image, (x, y))


class Gear(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('gear.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = choice(
            [(randint(-500, 250), randint(-500, 250)), (randint(-500, 250), randint(750, 1500)),
             (randint(750, 1500), randint(-500, 250)), (randint(750, 1500), randint(750, 1500))])
        self.mask = pg.mask.from_surface(self.image)


class Hill(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 1000
        self.height = 1000
        sprite_image = pg.image.load('hill.png')
        self.image = pg.transform.scale(sprite_image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = randint(0, self.width - self.image.get_width()), randint(0,
                                                                                            self.height - self.image.get_height())


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
            field_image = pg.image.load('field.png')
            field.image = field_image
            field.rect = field.image.get_rect()
            field.rect.x = 1000 * i - 1000
            field.rect.y = 1000 * j - 1000
            a.append(field)
        land[i] = a

    fps = 50
    count = 1
    bcount = 0
    clock = pg.time.Clock()
    stopwatch = Stopwatch(screen)
    level = Level(screen)
    hearts = Hearts(screen)
    diff = 1

    mm = MainMenu()
    menuim = pg.image.load('field.png')
    font = pg.font.Font("Comic Sans MS.ttf", 50)
    name = font.render('SlimeKill', True, (0, 0, 240))
    btt = pg.transform.scale(pg.image.load('button.png'), (800, 233))
    clbtt = pg.transform.scale(pg.image.load('button.png'), (800, 150))
    tf = pg.font.Font("Comic Sans MS.ttf", 30)
    tut = tf.render('''Управление на WASD. Пауза на Escape. Ваша цель - выжить''', True, (0, 0, 240))
    fbutton = font.render('1. Начать', True, (0, 0, 240))
    sbutton = font.render('2. Выйти', True, (0, 0, 240))

    rating = open('top5.txt', 'r')
    rates = list(map(lambda x:[x.split()[0], int(x.split()[1]), int(x.split()[2])], rating.readlines()))
    rating.close()
    rf = pg.font.Font("Comic Sans MS.ttf", 20)
    rtext = rf.render('Время        Убито      Счет             Лучших пяти забегов', True, (0, 0, 240))

    chbtt = pg.transform.scale(pg.image.load('button.png'), (800, 200))
    chtext1 = font.render('1. Увеличить пробивание пуль', True, (0, 0, 240))
    chtext2 = font.render('2. Увеличить количество пуль', True, (0, 0, 240))
    chtext3 = font.render('3. Увеличить урон пуль', True, (0, 0, 240))

    ea = font.render('1. Легко', True, (0, 0, 240))
    me = font.render('2. Средне', True, (0, 0, 240))
    ha = font.render('3. Сложно', True, (0, 0, 240))

    pbtt = pg.transform.scale(pg.image.load('button.png'), (800, 800))
    ptext = font.render('Нажмите 1, чтобы продолжить', True, (0, 0, 240))
    ptext1 = font.render('Нажмите Escape, чтобы выйти', True, (0, 0, 240))
    ptext2 = font.render('из игры', True, (0, 0, 240))

    collectibles_group = pg.sprite.Group()
    enemies = pg.sprite.Group()
    enemy_time = 50 - level.level
    projectiles = pg.sprite.Group()
    hill = pg.sprite.Group()
    gears = pg.sprite.Group()
    gears.add(Gear())
    while MainMenu.running:
        if MainMenu.main_menu:
            screen.blit(menuim, (0, 0))
            screen.blit(name, (440, 50))
            screen.blit(tut, (75, 140))
            screen.blit(btt, (100, 300))
            screen.blit(btt, (100, 600))
            screen.blit(fbutton, (125, 325))
            screen.blit(sbutton, (125, 625))
            mm.update()
            pg.display.flip()
        elif MainMenu.ch_level:
            screen.blit(menuim, (0, 0))
            screen.blit(name, (440, 50))
            screen.blit(tut, (75, 140))
            screen.blit(clbtt, (100, 200))
            screen.blit(ea, (100, 225))
            screen.blit(clbtt, (100, 425))
            screen.blit(me, (100, 450))
            screen.blit(clbtt, (100, 650))
            screen.blit(ha, (100, 675))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    MainMenu.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        MainMenu.ch_level = False
                        diff = 1
                    if event.key == pg.K_2:
                        MainMenu.ch_level = False
                        diff = 2
                    if event.key == pg.K_3:
                        MainMenu.ch_level = False
                        diff = 3
                    if event.key == pg.K_ESCAPE:
                        MainMenu.main_menu = True
                        MainMenu.ch_level = False
            pg.display.flip()
        elif MainMenu.pause:
            screen.blit(pbtt, (100, 100))
            screen.blit(ptext, (125, 350))
            screen.blit(ptext1, (125, 550))
            screen.blit(ptext2, (125, 650))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    MainMenu.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        MainMenu.pause = False
                    if event.key == pg.K_ESCAPE:
                        MainMenu.running = False
            pg.display.flip()
        elif MainMenu.choosing:
            screen.blit(chbtt, (100, 100))
            screen.blit(chbtt, (100, 400))
            screen.blit(chbtt, (100, 700))
            screen.blit(chtext1, (125, 125))
            screen.blit(chtext2, (125, 425))
            screen.blit(chtext3, (125, 725))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    MainMenu.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        Bullet.life += 1
                        MainMenu.choosing = False
                    if event.key == pg.K_2:
                        Bullet.number += 1
                        MainMenu.choosing = False
                    if event.key == pg.K_3:
                        Bullet.damage += 5
                        MainMenu.choosing = False
                    if event.key == pg.K_ESCAPE:
                        MainMenu.running = False
            pg.display.flip()
        elif MainMenu.ending:
            screen.blit(pbtt, (100, 100))
            screen.blit(rtext, (125, 150))
            for i in range(5):
                screen.blit(rates[i], (125, 200 + 40 * i))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    MainMenu.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        MainMenu.running = False

            pg.display.flip()
        else:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    MainMenu.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:
                        move_up = True
                    if event.key == pg.K_a:
                        move_left = True
                    if event.key == pg.K_s:
                        move_down = True
                    if event.key == pg.K_d:
                        move_right = True
                    if event.key == pg.K_ESCAPE:
                        MainMenu.pause = True
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
            if count % enemy_time == 0:
                enemies.add(Enemy())
                for i in range(0, randint(0, level.level // 2)):
                    enemies.add(Enemy())
                enemy_time = 50 - level.level

            if bcount and count % 5 == 0:
                projectiles.add(Bullet())
                bcount -= 1
            if count % 60 == 0 and not bcount:
                projectiles.add(Bullet())
                bf = True
                bcount = Bullet.number - 1
            if count % 250 == 0:
                chance = randint(1, 100)
                if chance > 83 + diff * 2:
                    gears.add(Gear())
                elif chance > 72 + diff * 3:
                    hill.add(Hill())

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
            for i in hill:
                i.rect.x -= speed * int(move_right) - speed * int(move_left)
                i.rect.y -= speed * int(move_down) - speed * int(move_up)
            for i in gears:
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
                    screen.blit(j.image, (j.rect.x, j.rect.y))  #
            screen.blit(main_char.image, (width // 2 - main_char.rect.width // 2, height // 2 - main_char.rect.height // 2))
            main_char.update()
            if hearts.current_hearts == 0:
                MainMenu.ending = False
                elapsed_time = time.time() - stopwatch.start_time
                total = [':'.join(map(str, divmod(int(elapsed_time), 60))), Enemy.num, level.level * Enemy.num]
                rates.append(total)
                rates.sort(key= lambda x: x[2], reverse=True)
                with open('top5.txt', 'w') as fi:
                    st = ''
                    for i in rates[:5]:
                        st += '        '.join(map(str, i)) + '\n'
                    fi.write(st)
                for i in range(5):
                    rates[i] = rf.render('              '.join(map(str, rates[i])), True, (0, 0, 240))
                MainMenu.ending = True

            enemies.update()
            enemies.draw(screen)
            projectiles.update()
            projectiles.draw(screen)
            screen.blit(stopwatch.image, (700, 0))
            stopwatch.update()
            level.update()
            level.color()
            hearts.draw()
            hill.update()
            hill.draw(screen)
            gears.draw(screen)
            pg.display.flip()
            clock.tick(fps)
    pg.quit()
