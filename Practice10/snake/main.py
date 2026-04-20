import pygame
import sys
from snake import Snake, Food

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Змейка с уровнями")
clock = pygame.time.Clock()

def draw_score_level(score, level):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

def main():
    snake = Snake(WIDTH, HEIGHT, CELL_SIZE)
    food = Food(snake.body, WIDTH, HEIGHT, CELL_SIZE)
    score = 0
    level = 1
    speed = 5
    
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
        
        if snake.get_head() == food.get_position():
            snake.grow()
            score += 1
            food = Food(snake.body, WIDTH, HEIGHT, CELL_SIZE)
            
            if score % 3 == 0:
                level += 1
                speed += 1
        
        screen.fill(WHITE)
        snake.draw(screen, GREEN)
        food.draw(screen, RED)
        draw_score_level(score, level)
        pygame.display.flip()
        clock.tick(speed)
    
    # Game Over
    font = pygame.font.Font(None, 72)
    game_over = font.render("GAME OVER", True, RED)
    screen.blit(game_over, (WIDTH//2 - 150, HEIGHT//2 - 50))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()