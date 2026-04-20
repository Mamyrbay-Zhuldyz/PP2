import pygame
import sys
import os
from game import Player, Enemy, Coin

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer - Собирай монеты!")
clock = pygame.time.Clock()

# Функция для безопасной загрузки звука
def load_sound(file_path):
    try:
        if os.path.exists(file_path):
            sound = pygame.mixer.Sound(file_path)
            print(f"Звук загружен: {file_path}")
            return sound
        else:
            print(f"Файл не найден: {file_path}")
            return None
    except Exception as e:
        print(f"Ошибка загрузки звука {file_path}: {e}")
        return None

# Загружаем звуки с проверкой
crash_sound = load_sound("sound/crash.wav")
coin_sound = load_sound("sound/coin.wav")

# Фоновая музыка
try:
    if os.path.exists("sound/background.wav"):
        pygame.mixer.music.load("sound/background.wav")
        pygame.mixer.music.play(-1)  # -1 = бесконечно
        pygame.mixer.music.set_volume(0.5)
        print("Фоновая музыка играет")
    else:
        print("Файл фоновой музыки не найден: sound/background.wav")
except Exception as e:
    print(f"Ошибка с фоновой музыкой: {e}")

def draw_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Coins: {score}", True, BLACK)
    pygame.draw.rect(screen, WHITE, (WIDTH - 130, 10, 100, 35))
    pygame.draw.rect(screen, BLACK, (WIDTH - 130, 10, 100, 35), 2)
    screen.blit(text, (WIDTH - 125, 15))

def draw_road():
    try:
        road = pygame.image.load("images/AnimatedStreet.png")
        road = pygame.transform.scale(road, (WIDTH, HEIGHT))
        screen.blit(road, (0, 0))
    except:
        # Простая дорога
        pygame.draw.rect(screen, (50, 50, 50), (WIDTH//2 - 50, 0, 100, HEIGHT))
        pygame.draw.line(screen, WHITE, (WIDTH//2 - 50, 0), (WIDTH//2 - 50, HEIGHT), 5)
        pygame.draw.line(screen, WHITE, (WIDTH//2 + 50, 0), (WIDTH//2 + 50, HEIGHT), 5)
        for y in range(0, HEIGHT, 40):
            pygame.draw.rect(screen, WHITE, (WIDTH//2 - 5, y, 10, 20))

def main():
    player = Player(WIDTH//2 - 30, HEIGHT - 120)
    enemies = []
    coins = []
    score = 0
    
    enemy_timer = 0
    coin_timer = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        player.move(keys, WIDTH)
        
        # Создание врагов
        enemy_timer += 1
        if enemy_timer > 30:
            enemies.append(Enemy(WIDTH))
            enemy_timer = 0
        
        # Создание монет
        coin_timer += 1
        if coin_timer > 20:
            coins.append(Coin(WIDTH))
            coin_timer = 0
        
        # Движение врагов
        for enemy in enemies[:]:
            enemy.move()
            if enemy.is_off_screen(HEIGHT):
                enemies.remove(enemy)
        
        # Движение монет
        for coin in coins[:]:
            coin.move()
            if coin.is_off_screen(HEIGHT):
                coins.remove(coin)
        
        player_rect = player.get_rect()
        
        # Проверка столкновения с врагами
        for enemy in enemies:
            if player_rect.colliderect(enemy.get_rect()):
                if crash_sound:
                    crash_sound.play()
                running = False
        
        # Проверка сбора монет
        for coin in coins[:]:
            if player_rect.colliderect(coin.get_rect()):
                coins.remove(coin)
                score += 1
                if coin_sound:
                    coin_sound.play()
        
        # Отрисовка
        draw_road()
        player.draw(screen)
        
        for enemy in enemies:
            enemy.draw(screen)
        for coin in coins:
            coin.draw(screen)
        
        draw_score(score)
        pygame.display.flip()
        clock.tick(60)
    
    # Game Over
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    game_over = font.render("GAME OVER", True, RED)
    screen.blit(game_over, (WIDTH//2 - 150, HEIGHT//2 - 60))
    
    font_small = pygame.font.Font(None, 36)
    final_score = font_small.render(f"Total Coins: {score}", True, BLACK)
    screen.blit(final_score, (WIDTH//2 - 80, HEIGHT//2 + 20))
    
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()