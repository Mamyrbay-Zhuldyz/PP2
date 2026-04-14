import pygame
import sys
from clock import MickeyClock

# Инициализация
pygame.init()

# Размеры окна
WIDTH = 800
HEIGHT = 600

# Цвета
WHITE = (255, 255, 255)

# Создаем окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock - Часы Микки Мауса")

# Создаем часы в центре экрана
mickey_clock = MickeyClock(screen, WIDTH // 2, HEIGHT // 2)

# Загружаем изображения (укажи правильные пути к файлам!)
try:
    mickey_clock.load_images(
        "images/mickeyclock.png",   # циферблат
        "images/left_hand.png",      # левая рука (секунды)
        "images/right_hand.png"      # правая рука (минуты)
    )
except Exception as e:
    print(f"Ошибка загрузки изображений: {e}")
    print("Проверь, что файлы находятся в папке images/")
    print("И что имена файлов написаны правильно!")
    sys.exit()

# Часы для контроля FPS
clock = pygame.time.Clock()

# Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Отрисовка
    screen.fill(WHITE)
    mickey_clock.draw()              # Рисуем часы с руками Микки
    mickey_clock.draw_digital_time() # Рисуем цифровое время
    pygame.display.flip()
    
    # Обновляем 30 раз в секунду
    clock.tick(30)

pygame.quit()
sys.exit()