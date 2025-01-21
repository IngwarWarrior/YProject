import pygame as pg
from random import randint

# Инициализация Pygame
pg.init()

# Настройки экрана
screen_width, screen_height = 1000, 1000
screen = pg.display.set_mode((screen_width, screen_height))


# Класс врага
class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('enemy.png')
        colorkey = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkey)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = randint(0, screen_width - self.rect.width), randint(0,
                                                                                       screen_height - self.rect.height)
        self.speed = [2, 2]  # Задайте начальную скорость

    def update(self):
        # Логика движения врага
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        # Проверка границ экрана
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed[0] *= -1
        if self.rect.top < 0 or self.rect.bottom > screen_height:
            self.speed[1] *= -1

    def kill_enemy(self):
        self.kill()  # Удаляет спрайт из всех групп


# Основной игровой цикл
def main():
    clock = pg.time.Clock()
    enemies = pg.sprite.Group()

    # Создание врагов
    for _ in range(5):  # Создайте 5 врагов
        enemy = Enemy()
        enemies.add(enemy)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # Обновление всех врагов
        enemies.update()

        # Проверка столкновений (пример с игроком)
        # player_rect - это прямоугольник вашего игрока (замените на ваш код)
        # player_rect = pg.Rect(500, 500, 50, 50)  # Пример прямоугольника игрока
        for enemy in enemies:
            if enemy.rect.colliderect(player_rect):  # Если враг столкнулся с игроком
                enemy.kill_enemy()  # Уничтожаем врага

        # Отрисовка
        screen.fill((255, 255, 255))  # Очистка экрана
        enemies.draw(screen)  # Рисуем врагов
        pg.display.flip()  # Обновление экрана

        clock.tick(60)  # Ограничение FPS

    pg.quit()


if __name__ == "__main__":
    main()
