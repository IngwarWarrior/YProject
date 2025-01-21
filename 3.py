import pygame
import sys


def draw_rombiki(surface, n):
    width, height = surface.get_size()
    max_x = width // n
    max_y = height // n

    for x in range(max_x):
        for y in range(max_y):
            pygame.draw.polygon(surface, (255, 165, 0), [
                (x * n + n // 2, y * n),
                (x * n + n, y * n + n // 2),
                (x * n + n // 2, y * n + n),
                (x * n, y * n + n // 2)
            ])


def main():
    try:
        n = int(input("Введите целое число n: "))
    except ValueError:
        print("Неправильный формат ввода")
        sys.exit()

    pygame.init()
    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption("Ромбы")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((255, 255, 0))
        draw_rombiki(screen, n)
        pygame.display.flip()


if __name__ == "__main__":
    main()