import pygame
import sys
from game import Player, Enemy, Coin

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer - Монеты разного веса!")
clock = pygame.time.Clock()

def draw_score_and_speed(score, enemy_speed, coins_to_next):
    font = pygame.font.Font(None, 36)
    
    # Счет
    score_text = font.render(f"Score: {score}", True, BLACK)
    pygame.draw.rect(screen, WHITE, (WIDTH - 120, 10, 110, 35))
    pygame.draw.rect(screen, BLACK, (WIDTH - 120, 10, 110, 35), 2)
    screen.blit(score_text, (WIDTH - 115, 15))
    
    # Скорость врага и до следующего увеличения
    speed_text = font.render(f"Enemy Speed: {enemy_speed}", True, BLACK)
    screen.blit(speed_text, (10, 50))
    
    next_text = font.render(f"Next speed up: {5 - coins_to_next} coins", True, BLACK)
    screen.blit(next_text, (10, 85))

def draw_road():
    try:
        road = pygame.image.load("images/AnimatedStreet.png")
        road = pygame.transform.scale(road, (WIDTH, HEIGHT))
        screen.blit(road, (0, 0))
    except:
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
    enemy_speed = 5
    coins_for_speed_up = 0
    
    enemy_timer = 0
    coin_timer = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        player.move(keys, WIDTH)
        
        enemy_timer += 1
        if enemy_timer > 30:
            enemies.append(Enemy(WIDTH, enemy_speed))
            enemy_timer = 0
        
        coin_timer += 1
        if coin_timer > 15:
            coins.append(Coin(WIDTH))
            coin_timer = 0
        
        for enemy in enemies[:]:
            enemy.move()
            if enemy.is_off_screen(HEIGHT):
                enemies.remove(enemy)
        
        for coin in coins[:]:
            coin.move()
            if coin.is_off_screen(HEIGHT):
                coins.remove(coin)
        
        player_rect = player.get_rect()
        
        # Проверка столкновения с врагами
        for enemy in enemies:
            if player_rect.colliderect(enemy.get_rect()):
                running = False
        
        # Проверка сбора монет
        for coin in coins[:]:
            if player_rect.colliderect(coin.get_rect()):
                points = coin.get_points()
                score += points
                coins.remove(coin)
                coins_for_speed_up += points
                
                # Увеличение скорости врага после каждых 5 очков
                if coins_for_speed_up >= 5:
                    enemy_speed += 1
                    coins_for_speed_up = 0
                    print(f"Speed UP! Теперь скорость врага: {enemy_speed}")
                    
                    # Обновляем скорость всех врагов
                    for enemy in enemies:
                        enemy.increase_speed()
        
        # Отрисовка
        draw_road()
        player.draw(screen)
        
        for enemy in enemies:
            enemy.draw(screen)
        for coin in coins:
            coin.draw(screen)
        
        # Показываем счет и скорость врага
        draw_score_and_speed(score, enemy_speed, coins_for_speed_up)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Game Over
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    game_over = font.render("GAME OVER", True, RED)
    screen.blit(game_over, (WIDTH//2 - 150, HEIGHT//2 - 60))
    
    font_small = pygame.font.Font(None, 36)
    final_score = font_small.render(f"Total Score: {score}", True, BLACK)
    screen.blit(final_score, (WIDTH//2 - 80, HEIGHT//2 + 20))
    
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()