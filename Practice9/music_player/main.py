import pygame
import sys
from player import MusicPlayer

# Инициализация Pygame и микшера для музыки
pygame.init()
pygame.mixer.init()

# Размеры окна
WIDTH = 600
HEIGHT = 400

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)
GREEN = (100, 255, 100)
RED = (255, 100, 100)

# Создаем окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player - Музыкальный плеер")

# Шрифты
font_title = pygame.font.Font(None, 48)
font_text = pygame.font.Font(None, 32)
font_small = pygame.font.Font(None, 24)

# Создаем плеер (укажи путь к папке с музыкой)
player = MusicPlayer("music")

# Загружаем первый трек автоматически
if player.playlist:
    player.play()

# Часы
clock = pygame.time.Clock()

# Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Play
                if player.is_playing:
                    pygame.mixer.music.unpause()
                    print("Воспроизведение возобновлено")
                else:
                    player.play()
            
            elif event.key == pygame.K_s:  # Stop
                player.stop()
            
            elif event.key == pygame.K_n:  # Next
                player.next_track()
            
            elif event.key == pygame.K_b:  # Back (Previous)
                player.previous_track()
            
            elif event.key == pygame.K_q:  # Quit
                running = False
            
            elif event.key == pygame.K_SPACE:  # Pause
                if player.is_playing:
                    pygame.mixer.music.pause()
                    print("Пауза")
                    player.is_playing = False
                else:
                    pygame.mixer.music.unpause()
                    print("Воспроизведение продолжено")
                    player.is_playing = True
    
    # Отрисовка
    screen.fill(WHITE)
    
    # Заголовок
    title = font_title.render("MUSIC PLAYER", True, BLUE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 30))
    
    # Информация о текущем треке
    track_text = font_text.render(f"Current Track:", True, BLACK)
    screen.blit(track_text, (50, 120))
    
    track_name = font_text.render(player.get_current_track_name(), True, GREEN)
    screen.blit(track_name, (50, 160))
    
    # Статус
    status = font_text.render(f"Status: {player.get_status()}", True, BLACK)
    screen.blit(status, (50, 220))
    
    # Управление (инструкция)
    controls_y = 280
    controls_title = font_small.render("CONTROLS:", True, BLACK)
    screen.blit(controls_title, (50, controls_y))
    
    controls = [
        "P - Play / Resume",
        "S - Stop",
        "N - Next Track",
        "B - Previous Track",
        "SPACE - Pause",
        "Q - Quit"
    ]
    
    for i, control in enumerate(controls):
        control_text = font_small.render(control, True, GRAY)
        screen.blit(control_text, (70, controls_y + 30 + i * 25))
    
    # Обновляем экран
    pygame.display.flip()
    clock.tick(60)

# Очистка
pygame.mixer.music.stop()
pygame.quit()
sys.exit()