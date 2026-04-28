import pygame
import random
import sys
import json
import os
from db import save_game_result, get_leaderboard, get_personal_best, init_db

# Initialize Pygame and Database
pygame.init()
init_db()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
DARK_RED = (139, 0, 0)
BLUE = (0, 100, 255)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Game Constants
WIDTH = 600
HEIGHT = 600
CELL = 30
FPS = 5
SCORE = 0
LEVEL = 1
USERNAME = ""
PERSONAL_BEST = 0

# State Control
STATE_MENU = "MENU"
STATE_GAME = "GAME"
STATE_SETTINGS = "SETTINGS"
STATE_LEADERBOARD = "LEADERBOARD"
STATE_GAMEOVER = "GAMEOVER"
current_state = STATE_MENU

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font_small = pygame.font.SysFont("Verdana", 18)
font_medium = pygame.font.SysFont("Verdana", 24)
font_big = pygame.font.SysFont("Verdana", 48, bold=True)

# Settings
SETTINGS = {"snake_color": [255, 255, 0], "grid": True, "sound": True}

def load_settings():
    if os.path.exists("settings.json"):
        try:
            with open("settings.json", "r") as f:
                return json.load(f)
        except:
            pass
    return SETTINGS.copy()

def save_settings():
    with open("settings.json", "w") as f:
        json.dump(SETTINGS, f)

SETTINGS = load_settings()

# Helper Functions
def draw_button(text, y_pos, width=200, height=50):
    rect = pygame.Rect(WIDTH // 2 - width // 2, y_pos, width, height)
    pygame.draw.rect(screen, GRAY, rect, border_radius=5)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=5)
    btn_text = font_medium.render(text, True, WHITE)
    text_rect = btn_text.get_rect(center=rect.center)
    screen.blit(btn_text, text_rect)
    return rect

def draw_grid():
    if not SETTINGS["grid"]:
        return
    for i in range(0, WIDTH, CELL):
        pygame.draw.line(screen, GRAY, (i, 0), (i, HEIGHT), 1)
    for j in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, GRAY, (0, j), (WIDTH, j), 1)

def draw_status():
    level_text = font_small.render(f"Level: {LEVEL}", True, WHITE)
    score_text = font_small.render(f"Score: {SCORE}", True, WHITE)
    pb_text = font_small.render(f"Best: {PERSONAL_BEST}", True, WHITE)
    screen.blit(level_text, (10, 10))
    screen.blit(score_text, (10, 35))
    screen.blit(pb_text, (WIDTH - 120, 10))

# Game Classes
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
        self.shield = False

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy
        
        # Wall collision - GAME OVER
        if self.body[0].x > WIDTH // CELL - 1:
            if self.shield:
                self.shield = False
                self.body[0].x = WIDTH // CELL - 1
                return True
            return False
        if self.body[0].x < 0:
            if self.shield:
                self.shield = False
                self.body[0].x = 0
                return True
            return False
        if self.body[0].y > HEIGHT // CELL - 1:
            if self.shield:
                self.shield = False
                self.body[0].y = HEIGHT // CELL - 1
                return True
            return False
        if self.body[0].y < 0:
            if self.shield:
                self.shield = False
                self.body[0].y = 0
                return True
            return False
        
        # Self-collision
        for segment in self.body[1:]:
            if self.body[0] == segment:
                if self.shield:
                    self.shield = False
                    return True
                return False
        return True
    
    def draw(self):
        for i, segment in enumerate(self.body):
            color = tuple(SETTINGS["snake_color"]) if i != 0 else RED
            if self.shield:
                color = CYAN
            pygame.draw.rect(screen, color, (segment.x * CELL, segment.y * CELL, CELL, CELL))

class Food:
    def __init__(self, is_poison=False):
        self.pos = Point(0, 0)
        self.is_poison = is_poison
        self.weight = 1
        self.timer = 0
        self.lifetime = 5000  # Only for poison food

    def generate(self, snake_body, obstacles):
        while True:
            self.pos = Point(random.randint(0, WIDTH // CELL - 1), 
                           random.randint(0, HEIGHT // CELL - 1))
            
            # Check obstacles and snake
            if self.pos in snake_body or self.pos in obstacles:
                continue
            
            # Check: not in crowded area
            neighbors = sum(1 for dx in [-1, 0, 1] for dy in [-1, 0, 1]
                          if Point(self.pos.x + dx, self.pos.y + dy) in obstacles)
            
            if neighbors <= 3:  # Not too many obstacles nearby
                break
        
        self.weight = random.randint(1, 3) if not self.is_poison else 0
        if self.is_poison:
            self.timer = pygame.time.get_ticks()

    def update(self):
        # Only poison food disappears after timer
        if self.is_poison:
            return pygame.time.get_ticks() - self.timer > self.lifetime
        return False  # Normal food never disappears

    def draw(self):
        color = DARK_RED if self.is_poison else GREEN
        pygame.draw.rect(screen, color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

class BonusFood:
    def __init__(self):
        self.pos = Point(0, 0)
        self.active = False
        self.timer = 0
        self.lifetime = 7000  # 7 seconds

    def generate(self, snake_body, food_pos, poison_pos, obstacles):
        if random.random() < 0.3:  # 30% chance to spawn
            attempts = 0
            while attempts < 50:
                self.pos = Point(random.randint(0, WIDTH // CELL - 1), 
                                random.randint(0, HEIGHT // CELL - 1))
                # Check: not on snake, other food, obstacles
                if (self.pos not in snake_body and self.pos != food_pos and 
                    self.pos != poison_pos and self.pos not in obstacles):
                    
                    # Check: not in crowded obstacle area
                    neighbors = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            check = Point(self.pos.x + dx, self.pos.y + dy)
                            if check in obstacles:
                                neighbors += 1
                    
                    if neighbors <= 2:  # Not too crowded
                        self.active = True
                        self.timer = pygame.time.get_ticks()
                        break
                attempts += 1
        else:
            self.active = False

    def update(self):
        if self.active:
            return pygame.time.get_ticks() - self.timer > self.lifetime
        return False

    def draw(self):
        if self.active:
            # Gold/Yellow color for bonus food
            cx = self.pos.x * CELL + CELL // 2
            cy = self.pos.y * CELL + CELL // 2
            r = CELL // 2 - 2
            pygame.draw.circle(screen, YELLOW, (cx, cy), r)
            pygame.draw.circle(screen, ORANGE, (cx, cy), r, 2)
            # Draw star/plus inside
            s = r // 2
            pygame.draw.line(screen, RED, (cx - s, cy), (cx + s, cy), 2)
            pygame.draw.line(screen, RED, (cx, cy - s), (cx, cy + s), 2)

class PowerUp:
    def __init__(self):
        self.pos = Point(0, 0)
        self.type = None
        self.timer = 0
        self.lifetime = 8000
        self.active = False
        self.types = ["speed_boost", "slow_motion", "shield"]

    def generate(self, snake_body, food_pos, poison_pos, obstacles):
        self.type = random.choice(self.types)
        while True:
            self.pos = Point(random.randint(0, WIDTH // CELL - 1), random.randint(0, HEIGHT // CELL - 1))
            if self.pos not in snake_body and self.pos != food_pos and self.pos != poison_pos and self.pos not in obstacles:
                break
        self.timer = pygame.time.get_ticks()
        self.active = True

    def update(self):
        if self.active and pygame.time.get_ticks() - self.timer > self.lifetime:
            self.active = False
            return True
        return False

    def draw(self):
        if not self.active:
            return
        colors = {"speed_boost": BLUE, "slow_motion": ORANGE, "shield": PURPLE}
        color = colors.get(self.type, WHITE)
        pygame.draw.rect(screen, color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

class Obstacles:
    def __init__(self):
        self.blocks = []

    def generate(self, snake_body, food_pos, poison_pos, bonus_pos):
        self.blocks = []
        if LEVEL < 3:
            return
        
        # Less obstacles: about 2/3 of original
        count = max(1, (LEVEL - 2))
        
        for _ in range(count):
            attempts = 0
            while attempts < 100:
                p = Point(random.randint(1, WIDTH // CELL - 2), 
                         random.randint(1, HEIGHT // CELL - 2))
                
                # Check: not on snake, food, poison, bonus, or other obstacles
                if (p not in snake_body and p != food_pos and p != poison_pos and 
                    p != bonus_pos and p not in self.blocks):
                    
                    # Check: doesn't block snake's head (head is snake_body[0])
                    head = snake_body[0]
                    # Don't place obstacle directly around the head
                    if not (abs(p.x - head.x) <= 1 and abs(p.y - head.y) <= 1):
                        self.blocks.append(p)
                        break
                attempts += 1

    def draw(self):
        for block in self.blocks:
            pygame.draw.rect(screen, GRAY, (block.x * CELL, block.y * CELL, CELL, CELL))
            # Draw X on obstacle
            cx = block.x * CELL + CELL // 2
            cy = block.y * CELL + CELL // 2
            s = CELL // 4
            pygame.draw.line(screen, DARK_RED, (cx - s, cy - s), (cx + s, cy + s), 3)
            pygame.draw.line(screen, DARK_RED, (cx + s, cy - s), (cx - s, cy + s), 3)

# Screen Functions
def show_menu():
    global USERNAME, PERSONAL_BEST
    screen.fill(BLACK)
    title = font_big.render("SNAKE GAME", True, GREEN)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    name_prompt = font_small.render("Enter username:", True, WHITE)
    screen.blit(name_prompt, (WIDTH // 2 - 80, 140))
    name_text = font_medium.render(USERNAME, True, YELLOW)
    screen.blit(name_text, (WIDTH // 2 - 80, 165))

    btn_play = draw_button("PLAY", 220)
    btn_lead = draw_button("LEADERBOARD", 290)
    btn_sett = draw_button("SETTINGS", 360)
    btn_quit = draw_button("QUIT", 430)
    return btn_play, btn_lead, btn_sett, btn_quit

def show_game_over():
    screen.fill(BLACK)
    title = font_big.render("GAME OVER", True, RED)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    info = font_medium.render(f"Score: {SCORE}  Level: {LEVEL}  Best: {PERSONAL_BEST}", True, WHITE)
    screen.blit(info, (WIDTH // 2 - info.get_width() // 2, 200))
    btn_retry = draw_button("RETRY", 300)
    btn_menu = draw_button("MAIN MENU", 370)
    return btn_retry, btn_menu

def show_leaderboard_screen():
    screen.fill(BLACK)
    title = font_big.render("TOP 10", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    scores = get_leaderboard()
    y = 80
    header = font_small.render(f"{'Rank':<5} {'Name':<15} {'Score':<8} {'Level':<6}", True, WHITE)
    screen.blit(header, (50, y))
    y += 25
    for i, row in enumerate(scores):
        text = font_small.render(f"{i+1:<5} {row[0]:<15} {row[1]:<8} {row[2]:<6}", True, WHITE)
        screen.blit(text, (50, y))
        y += 25
    btn_back = draw_button("BACK", 500)
    return btn_back

def show_settings_screen():
    screen.fill(BLACK)
    title = font_big.render("SETTINGS", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    grid_status = "ON" if SETTINGS["grid"] else "OFF"
    sound_status = "ON" if SETTINGS["sound"] else "OFF"
    snake_color = tuple(SETTINGS["snake_color"])
    btn_grid = draw_button(f"Grid: {grid_status}", 150)
    btn_sound = draw_button(f"Sound: {sound_status}", 220)
    color_preview = font_small.render(f"Snake Color: RGB{snake_color}", True, WHITE)
    screen.blit(color_preview, (WIDTH // 2 - 80, 280))
    pygame.draw.rect(screen, snake_color, (WIDTH // 2 - 15, 300, 30, 30))
    btn_color = draw_button("Change Color", 340)
    btn_back = draw_button("SAVE & BACK", 450)
    return btn_grid, btn_sound, btn_color, btn_back

def reset_game():
    global SCORE, LEVEL, FPS, game_over, powerup_active, powerup_type, powerup_start_time
    SCORE = 0
    LEVEL = 1
    FPS = 5
    game_over = False
    powerup_active = False
    powerup_type = None
    powerup_start_time = 0
    snake.__init__()
    food.generate(snake.body, obs.blocks)
    poison.generate(snake.body, obs.blocks)
    bonus.active = False
    powerup.active = False
    obs.blocks = []

# Initialize Game Objects
snake = Snake()
food = Food()
poison = Food(is_poison=True)
bonus = BonusFood
powerup = PowerUp()
obs = Obstacles()
game_over = False
powerup_active = False
powerup_type = None
powerup_start_time = 0

# Main Loop
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if current_state == STATE_MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    USERNAME = USERNAME[:-1]
                elif event.key == pygame.K_RETURN:
                    PERSONAL_BEST = get_personal_best(USERNAME)
                else:
                    if len(USERNAME) < 15 and event.unicode.isprintable():
                        USERNAME += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn_play, btn_lead, btn_sett, btn_quit = show_menu()
                if btn_play.collidepoint(mouse_pos):
                    if USERNAME:
                        PERSONAL_BEST = get_personal_best(USERNAME)
                        reset_game()
                        current_state = STATE_GAME
                elif btn_lead.collidepoint(mouse_pos):
                    current_state = STATE_LEADERBOARD
                elif btn_sett.collidepoint(mouse_pos):
                    current_state = STATE_SETTINGS
                elif btn_quit.collidepoint(mouse_pos):
                    running = False

        elif current_state == STATE_GAMEOVER:
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn_retry, btn_menu = show_game_over()
                if btn_retry.collidepoint(mouse_pos):
                    reset_game()
                    current_state = STATE_GAME
                elif btn_menu.collidepoint(mouse_pos):
                    current_state = STATE_MENU

        elif current_state == STATE_LEADERBOARD:
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn_back = show_leaderboard_screen()
                if btn_back.collidepoint(mouse_pos):
                    current_state = STATE_MENU

        elif current_state == STATE_SETTINGS:
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn_grid, btn_sound, btn_color, btn_back = show_settings_screen()
                if btn_grid.collidepoint(mouse_pos):
                    SETTINGS["grid"] = not SETTINGS["grid"]
                elif btn_sound.collidepoint(mouse_pos):
                    SETTINGS["sound"] = not SETTINGS["sound"]
                elif btn_color.collidepoint(mouse_pos):
                    r = random.randint(0, 255)
                    g = random.randint(0, 255)
                    b = random.randint(0, 255)
                    SETTINGS["snake_color"] = [r, g, b]
                elif btn_back.collidepoint(mouse_pos):
                    save_settings()
                    current_state = STATE_MENU

        if event.type == pygame.KEYDOWN and current_state == STATE_GAME:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx, snake.dy = 1, 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx, snake.dy = -1, 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx, snake.dy = 0, 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx, snake.dy = 0, -1

    # Game Logic
    if current_state == STATE_GAME and not game_over:
        if not snake.move():
            game_over = True

        head = snake.body[0]

        # Obstacle collision
        if any(head == b for b in obs.blocks):
            if snake.shield:
                snake.shield = False
            else:
                game_over = True

        # Food
        if head == food.pos:
            SCORE += food.weight
            snake.body.append(Point(snake.body[-1].x, snake.body[-1].y))
            food.generate(snake.body, obs.blocks)
            # Spawn bonus after eating normal food (small chance)
            if random.random() < 0.3 and not bonus.active:
                bonus.generate(snake.body, food.pos, poison.pos, obs.blocks)
            
            if SCORE // 5 >= LEVEL:
                LEVEL += 1
                FPS += 1
                if LEVEL >= 3:
                    obs.generate(snake.body, food.pos, poison.pos, bonus.pos)
                if LEVEL % 2 == 0 and not powerup.active:
                    powerup.generate(snake.body, food.pos, poison.pos, obs.blocks)

        # Bonus Food
        if bonus.active and head == bonus.pos:
            SCORE += 3  # 3 points bonus!
            snake.body.append(Point(snake.body[-1].x, snake.body[-1].y))
            bonus.active = False

        # Poison
        if head == poison.pos:
            if len(snake.body) > 3:
                snake.body.pop()
                snake.body.pop()
            else:
                game_over = True
            poison.generate(snake.body, obs.blocks)

        # Power-up
        if powerup.active and head == powerup.pos:
            powerup_type = powerup.type
            powerup_start_time = pygame.time.get_ticks()
            powerup_active = True
            powerup.active = False
            if powerup_type == "speed_boost":
                FPS += 3
            elif powerup_type == "slow_motion":
                FPS = max(2, FPS - 3)
            elif powerup_type == "shield":
                snake.shield = True

        # Power-up timer
        if powerup_active:
            elapsed = pygame.time.get_ticks() - powerup_start_time
            if elapsed > 5000:
                if powerup_type == "speed_boost":
                    FPS -= 3
                elif powerup_type == "slow_motion":
                    FPS += 3
                powerup_active = False
                powerup_type = None

                # Food timers
        # Normal food does NOT disappear - no need to call food.update()
        if poison.update():
            poison.generate(snake.body, obs.blocks)
        if powerup.update():
            pass

        # Game Over
        if game_over:
            save_game_result(USERNAME, SCORE, LEVEL)
            PERSONAL_BEST = get_personal_best(USERNAME)
            current_state = STATE_GAMEOVER

    # Rendering
    screen.fill(BLACK)

    if current_state == STATE_MENU:
        show_menu()
    elif current_state == STATE_GAMEOVER:
        show_game_over()
    elif current_state == STATE_LEADERBOARD:
        show_leaderboard_screen()
    elif current_state == STATE_SETTINGS:
        show_settings_screen()
    elif current_state == STATE_GAME:
        draw_grid()
        obs.draw()
        snake.draw()
        food.draw()
        poison.draw()
        if bonus.active:
            bonus.draw()
        if powerup.active:
            powerup.draw()
        draw_status()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()