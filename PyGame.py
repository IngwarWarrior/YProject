import time
from math import acos, pi
from random import randint, choice

import pygame as pg


class MainCharacter(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('Character.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 475, 450
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.mask = pg.mask.from_surface(self.image)
        self.hitf = {}


    def update(self):
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


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('enemy.png')
        self.rect = self.image.get_rect()
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.mask = pg.mask.from_surface(self.image)
        self.rect.x, self.rect.y = randint(0, 970), randint(0, 950)
        self.distance = ((485 - self.rect.x) ** 2 + (475 - self.rect.y) ** 2) ** 0.5
        self.speed = [int((485 - self.rect.x) / ((self.distance + 1) / (speed - 2))),
                      int((475 - self.rect.y) / ((self.distance + 1) / (speed - 2)))]
        self.f = 0
        self.hp = level.level * 5 + 5
        self.hitf = {}

    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]
        self.distance = ((485 - self.rect.x) ** 2 + (475 - self.rect.y) ** 2) ** 0.5
        self.speed = [int((485 - self.rect.x) / ((self.distance + 1) / (speed - 2))),
                      int((475 - self.rect.y) / ((self.distance + 1) / (speed - 2)))]
        if self.rect.x < 485 and not self.f:
            self.f = 1
            self.image = pg.transform.flip(self.image, True, False)
        if self.rect.x > 485 and self.f:
            self.f = 0
            self.image = pg.transform.flip(self.image, True, False)

        for i in projectiles:
            if pg.sprite.collide_mask(self, i) and i not in self.hitf:
                self.hitf[i] = 0
                self.hp -= 10
            elif i in self.hitf and not pg.sprite.collide_mask(self, i):
                self.hitf.pop(i)
        if self.hp <= 0:
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

    def __init__(self):
        super().__init__()
        self.life = Bullet.life  # ОБРАТИ ВНИМАНИЕ!!! ХП нужны для пробивания врагов!
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


class Collectible(pg.sprite.Sprite):  # Класс подбираемых штук. Из него выйдут аптечки и прокачки
    def __init__(self):
        super().__init__()
        self.x, self.y = choice([(randint(-500, 250), randint(-500, 250)), (randint(-500, 250), randint(750, 1500)),
                                 (randint(750, 1500), randint(-500, 250)), (randint(750, 1500), randint(750, 1500))])


class Medkit(Collectible):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('medkit.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 500, 500
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.mask = pg.mask.from_surface(self.image)



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
    stopwatch = Stopwatch(screen)
    level = Level(screen)
    hearts = Hearts(screen)

    collectibles_group = pg.sprite.Group()
    enemies = pg.sprite.Group()
    enemy_time = 50 - level.level
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
        if count % enemy_time == 0:
            enemies.add(Enemy())
            for i in range(0, randint(0, level.level // 2)):
                enemies.add(Enemy())
            enemy_time = 50 - level.level

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
                screen.blit(j.image, (j.rect.x, j.rect.y))  #
        screen.blit(main_char.image, (width // 2 - main_char.rect.width // 2, height // 2 - main_char.rect.height // 2))
        main_char.update()
        if hearts.current_hearts == 0:
            running = False
        enemies.update()
        enemies.draw(screen)
        projectiles.update()
        projectiles.draw(screen)
        screen.blit(stopwatch.image, (700, 0))
        stopwatch.update()
        level.update()
        level.color()
        hearts.draw()
        pg.display.flip()
        clock.tick(fps)
    pg.quit()
