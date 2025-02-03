import pygame
import random


class Hill:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.sprites = []
        self.load_sprites()

    def load_sprites(self):
        # Загрузка спрайта (замените 'sprite_image.png' на путь к вашему изображению)
        self.sprite_image = pygame.image.load('hill.png').convert_alpha()

    def spawn_sprite(self):
        # Генерация случайных координат для спавна
        x = random.randint(0, self.width - self.sprite_image.get_width()-1)
        y = random.randint(0, self.height - self.sprite_image.get_height()-1)
        sprite_rect = self.sprite_image.get_rect(topleft=(x, y))
        self.sprites.append(sprite_rect)

    def draw(self):
        # Отрисовка всех спрайтов на экране
        for sprite_rect in self.sprites:
            self.screen.blit(self.sprite_image, sprite_rect.topleft)

    def update(self):
        # Обновление состояния игры (например, можно добавлять логику для спауна спрайтов)
        if len(self.sprites) < 10:  # Ограничение на количество спрайтов
            self.spawn_sprite()


def main():
    pygame.init()
    clock = pygame.time.Clock()

    hill = Hill(800, 600)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        hill.update()

        hill.screen.fill((255, 255, 255))  # Очистка экрана белым цветом
        hill.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
