import pygame
import sys
from ball import Ball  # Импортируем класс Ball

# Инициализация
pygame.init()

# Размеры окна
WIDTH = 800
HEIGHT = 600
BALL_RADIUS = 25
MOVE_DISTANCE = 20

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Создаем окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

# Создаем мяч в центре экрана
ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, RED)

# Часы
clock = pygame.time.Clock()

# Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ball.move_left(MOVE_DISTANCE, WIDTH)
            elif event.key == pygame.K_RIGHT:
                ball.move_right(MOVE_DISTANCE, WIDTH)
            elif event.key == pygame.K_UP:
                ball.move_up(MOVE_DISTANCE, HEIGHT)
            elif event.key == pygame.K_DOWN:
                ball.move_down(MOVE_DISTANCE, HEIGHT)
            elif event.key == pygame.K_ESCAPE:
                running = False
    
    # Отрисовка
    screen.fill(WHITE)
    ball.draw(screen)  # Рисуем мяч через метод класса
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()