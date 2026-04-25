import pygame
import sys
from snake import Snake, NormalFood, SpecialFood

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Змейка")
clock = pygame.time.Clock()

def draw_score_level(score, level):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    
    # Прозрачный фон для текста
    pygame.draw.rect(screen, WHITE, (5, 5, 110, 65))
    pygame.draw.rect(screen, BLACK, (5, 5, 110, 65), 2)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

def main():
    snake = Snake(WIDTH, HEIGHT, CELL_SIZE)
    normal_food = NormalFood(snake.body, WIDTH, HEIGHT, CELL_SIZE)
    special_food = None
    score = 0
    level = 1
    speed = 5
    special_food_timer = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")
        
        snake.move()
        
        if snake.check_collision():
            running = False
        
        # Проверка съедания обычной еды
        if snake.get_head() == normal_food.get_position():
            score += normal_food.get_points()
            snake.grow()
            normal_food = NormalFood(snake.body, WIDTH, HEIGHT, CELL_SIZE)
            
            if score >= level * 5:
                level += 1
                speed += 2
        
        # Проверка съедания особой еды
        if special_food:
            if snake.get_head() == special_food.get_position():
                points = special_food.get_points()
                score += points
                snake.grow()
                special_food = None
                special_food_timer = 0
                
                if score >= level * 5:
                    level += 1
                    speed += 2
        
        # Спавн особой еды
        special_food_timer += 1
        if not special_food and special_food_timer > 300:
            special_food = SpecialFood(snake.body, WIDTH, HEIGHT, CELL_SIZE)
            special_food_timer = 0
        
        if special_food and special_food.is_expired():
            special_food = None
            special_food_timer = 0
        
        # Отрисовка (чистый фон, без клеток)
        screen.fill(WHITE)
        
        snake.draw(screen, GREEN)
        normal_food.draw(screen)
        if special_food:
            special_food.draw(screen)
        
        draw_score_level(score, level)
        pygame.display.flip()
        clock.tick(speed)
    
    # Game Over
    screen.fill(WHITE)
    font = pygame.font.Font(None, 72)
    game_over = font.render("GAME OVER", True, BLACK)
    screen.blit(game_over, (WIDTH//2 - 150, HEIGHT//2 - 50))
    
    font_small = pygame.font.Font(None, 36)
    final_score = font_small.render(f"Score: {score}", True, BLACK)
    screen.blit(final_score, (WIDTH//2 - 60, HEIGHT//2 + 20))
    
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()