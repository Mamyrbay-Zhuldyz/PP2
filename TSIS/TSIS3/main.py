import pygame
import random
import sys
import os
from persistence import load_settings, save_settings, load_leaderboard, add_score
from ui import init_ui, show_menu, show_settings_screen, show_game_over, show_leaderboard_screen

pygame.init()
pygame.mixer.init()

# Paths
BASE_DIR = os.path.dirname(__file__)
ASSETS = os.path.join(BASE_DIR, "assets")

# Constants
WIDTH, HEIGHT = 400, 600
LANE_COUNT = 3
LANE_WIDTH = WIDTH // LANE_COUNT
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# State
STATE_MENU = "MENU"
STATE_SETTINGS = "SETTINGS"
STATE_GAME = "GAME"
STATE_GAMEOVER = "GAMEOVER"
STATE_LEADERBOARD = "LEADERBOARD"

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")
clock = pygame.time.Clock()
font_small = pygame.font.SysFont("Verdana", 16)
font_medium = pygame.font.SysFont("Verdana", 24)

init_ui(screen)
settings = load_settings()

# Load images
bg_image = pygame.image.load(os.path.join(ASSETS, "AnimatedStreet.png")).convert()
player_img = pygame.image.load(os.path.join(ASSETS, "Player.png")).convert_alpha()
enemy_img = pygame.image.load(os.path.join(ASSETS, "Enemy.png")).convert_alpha()

# Load sounds
crash_sound = None
bg_music = None
if os.path.exists(os.path.join(ASSETS, "crash.wav")):
    crash_sound = pygame.mixer.Sound(os.path.join(ASSETS, "crash.wav"))
if os.path.exists(os.path.join(ASSETS, "background.wav")):
    bg_music = os.path.join(ASSETS, "background.wav")

# Game variables
USERNAME = ""
score = 0
distance = 0
coins_collected = 0
current_state = STATE_MENU
game_over = False
difficulty_level = 1
road_offset = 0
road_speed = 5

# Power-ups
powerup_active = False
powerup_type = None
powerup_start_time = 0

# Player
player_lane = 1
player_x = LANE_WIDTH * player_lane + LANE_WIDTH // 2
player_y = HEIGHT - 120
player_speed = 5
player_shield = False
moving_left = False
moving_right = False
SPEED = 5

# Game objects
traffic_cars = []
obstacles = []
coins = []
powerups = []

def spawn_traffic():
    if len(traffic_cars) < 2 + difficulty_level:
        lane = random.randint(0, LANE_COUNT - 1)
        traffic_cars.append({
            "x": lane * LANE_WIDTH + LANE_WIDTH // 2, "y": -100,
            "lane": lane, "speed": 3 + random.randint(0, difficulty_level)
        })

def spawn_obstacle():
    if len(obstacles) < difficulty_level:
        lane = random.randint(0, LANE_COUNT - 1)
        obstacles.append({
            "x": lane * LANE_WIDTH, "y": -30, "lane": lane,
            "type": random.choice(["barrier", "oil", "pothole"])
        })

def spawn_coin():
    if len(coins) < 3:
        lane = random.randint(0, LANE_COUNT - 1)
        coins.append({
            "x": lane * LANE_WIDTH + LANE_WIDTH // 2, "y": -20,
            "lane": lane, "value": random.choice([1, 2, 3])
        })

def spawn_powerup():
    if len(powerups) < 1 and random.random() < 0.003:
        powerups.append({
            "x": random.randint(0, LANE_COUNT - 1) * LANE_WIDTH + LANE_WIDTH // 2,
            "y": -30, "type": random.choice(["nitro", "shield", "repair"])
        })

def reset_game():
    global score, distance, coins_collected, game_over, difficulty_level
    global road_speed, player_lane, player_x, player_shield
    global powerup_active, powerup_type, powerup_start_time
    global traffic_cars, obstacles, coins, powerups
    global moving_left, moving_right

    score = 0
    distance = 0
    coins_collected = 0
    game_over = False
    difficulty_level = 1
    road_speed = 5
    player_lane = 1
    player_x = LANE_WIDTH * player_lane + LANE_WIDTH // 2
    player_shield = False
    moving_left = False
    moving_right = False
    powerup_active = False
    powerup_type = None
    powerup_start_time = 0
    traffic_cars = []
    obstacles = []
    coins = []
    powerups = []

def check_collision(obj):
    car_rect = pygame.Rect(player_x - 22, player_y, 44, 60)
    obj_type = obj.get("type", "")
    if obj_type in ("oil", "barrier"):
        obj_rect = pygame.Rect(obj["x"], obj["y"], LANE_WIDTH, 15)
    elif obj_type == "pothole":
        obj_rect = pygame.Rect(obj["x"] + 20, obj["y"], LANE_WIDTH - 40, 20)
    else:
        obj_rect = pygame.Rect(obj["x"] - 22, obj["y"], 44, 60)
    return car_rect.colliderect(obj_rect)

# Music
if bg_music and settings["sound"]:
    pygame.mixer.music.load(bg_music)
    pygame.mixer.music.play(-1)

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
                elif len(USERNAME) < 15 and event.unicode.isprintable():
                    USERNAME += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn_play, btn_lead, btn_sett, btn_quit = show_menu(USERNAME)
                if btn_play.collidepoint(mouse_pos) and USERNAME:
                    reset_game()
                    current_state = STATE_GAME
                elif btn_lead.collidepoint(mouse_pos):
                    current_state = STATE_LEADERBOARD
                elif btn_sett.collidepoint(mouse_pos):
                    current_state = STATE_SETTINGS
                elif btn_quit.collidepoint(mouse_pos):
                    running = False

        elif current_state == STATE_SETTINGS:
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn_sound, btn_diff, btn_color, btn_back = show_settings_screen(settings)
                if btn_sound.collidepoint(mouse_pos):
                    settings["sound"] = not settings["sound"]
                    if settings["sound"]:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                elif btn_diff.collidepoint(mouse_pos):
                    diffs = ["easy", "normal", "hard"]
                    idx = diffs.index(settings["difficulty"])
                    settings["difficulty"] = diffs[(idx + 1) % 3]
                elif btn_color.collidepoint(mouse_pos):
                    # Change car color randomly
                    pass
                elif btn_back.collidepoint(mouse_pos):
                    save_settings(settings)
                    current_state = STATE_MENU

        elif current_state == STATE_LEADERBOARD:
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn_back = show_leaderboard_screen(load_leaderboard())
                if btn_back.collidepoint(mouse_pos):
                    current_state = STATE_MENU

        elif current_state == STATE_GAMEOVER:
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn_retry, btn_menu = show_game_over(score, distance, coins_collected)
                if btn_retry.collidepoint(mouse_pos):
                    reset_game()
                    current_state = STATE_GAME
                elif btn_menu.collidepoint(mouse_pos):
                    current_state = STATE_MENU

                # Key press - start moving
        if event.type == pygame.KEYDOWN and current_state == STATE_GAME:
            if event.key == pygame.K_LEFT:
                moving_left = True
            elif event.key == pygame.K_RIGHT:
                moving_right = True

        # Key release - stop moving
        if event.type == pygame.KEYUP and current_state == STATE_GAME:
            if event.key == pygame.K_LEFT:
                moving_left = False
            elif event.key == pygame.K_RIGHT:
                moving_right = False

    # Game logic
    if current_state == STATE_GAME and not game_over:
        # Smooth player movement
        if moving_left:
            player_x -= SPEED
        if moving_right:
            player_x += SPEED
        
        # Keep player within screen bounds
        if player_x - 25 < 0:
            player_x = 25
        if player_x + 25 > WIDTH:
            player_x = WIDTH - 25
        
        # Update lane based on position
        player_lane = player_x // LANE_WIDTH
        
        road_offset = (road_offset + road_speed) % HEIGHT
        distance += road_speed // 10

        if distance // 100 > difficulty_level:
            difficulty_level = min(distance // 100 + 1, 10)

        spawn_traffic()
        spawn_obstacle()
        spawn_coin()
        spawn_powerup()

        # Update objects
        for car in traffic_cars[:]:
            car["y"] += car["speed"]
            if car["y"] > HEIGHT + 100:
                traffic_cars.remove(car)
            elif check_collision(car):
                if player_shield:
                    player_shield = False
                    traffic_cars.remove(car)
                else:
                    if crash_sound and settings["sound"]:
                        crash_sound.play()
                    add_score(USERNAME, score, distance)
                    current_state = STATE_GAMEOVER

        for obs in obstacles[:]:
            obs["y"] += road_speed
            if obs["y"] > HEIGHT + 30:
                obstacles.remove(obs)
            elif check_collision(obs):
                if player_shield:
                    player_shield = False
                    obstacles.remove(obs)
                elif powerup_active and powerup_type == "repair":
                    obstacles.remove(obs)
                    powerup_active = False
                else:
                    if crash_sound and settings["sound"]:
                        crash_sound.play()
                    add_score(USERNAME, score, distance)
                    current_state = STATE_GAMEOVER

        for coin in coins[:]:
            coin["y"] += road_speed
            if coin["y"] > HEIGHT + 30:
                coins.remove(coin)
            elif check_collision(coin):
                score += coin["value"]
                coins_collected += 1
                coins.remove(coin)

        for pu in powerups[:]:
            pu["y"] += road_speed
            if pu["y"] > HEIGHT + 30:
                powerups.remove(pu)
            elif check_collision(pu):
                powerup_active = True
                powerup_type = pu["type"]
                powerup_start_time = pygame.time.get_ticks()
                powerups.remove(pu)
                if pu["type"] == "nitro":
                    road_speed += 3
                elif pu["type"] == "shield":
                    player_shield = True

        # Power-up timer
        if powerup_active and pygame.time.get_ticks() - powerup_start_time > 5000:
            if powerup_type == "nitro" and road_speed > 8:
                road_speed -= 3
            powerup_active = False
            powerup_type = None

    # Drawing
    # Background
    screen.blit(bg_image, (0, road_offset - HEIGHT))
    screen.blit(bg_image, (0, road_offset))

    if current_state == STATE_MENU:
        show_menu(USERNAME)
    elif current_state == STATE_SETTINGS:
        show_settings_screen(settings)
    elif current_state == STATE_LEADERBOARD:
        show_leaderboard_screen(load_leaderboard())
    elif current_state == STATE_GAMEOVER:
        show_game_over(score, distance, coins_collected)
    elif current_state == STATE_GAME:
        # Draw traffic
        for car in traffic_cars:
            screen.blit(enemy_img, (car["x"] - 25, car["y"]))

        # Draw obstacles
        for obs in obstacles:
            if obs["type"] == "barrier":
                pygame.draw.rect(screen, ORANGE, (obs["x"], obs["y"], LANE_WIDTH, 15))
            elif obs["type"] == "oil":
                pygame.draw.rect(screen, (50, 50, 50), (obs["x"], obs["y"], LANE_WIDTH, 10))
            elif obs["type"] == "pothole":
                pygame.draw.ellipse(screen, (139, 69, 19), (obs["x"] + 20, obs["y"], LANE_WIDTH - 40, 20))

        # Draw coins
        for coin in coins:
            color = {1: YELLOW, 2: ORANGE, 3: RED}.get(coin["value"], YELLOW)
            pygame.draw.circle(screen, color, (coin["x"], int(coin["y"])), 12)
            pygame.draw.circle(screen, BLACK, (coin["x"], int(coin["y"])), 12, 2)

        # Draw power-ups
        for pu in powerups:
            colors = {"nitro": BLUE, "shield": PURPLE, "repair": GREEN}
            pygame.draw.circle(screen, colors.get(pu["type"], WHITE), (pu["x"], int(pu["y"])), 15)
            letter = font_medium.render(pu["type"][0].upper(), True, WHITE)
            screen.blit(letter, (pu["x"] - 8, int(pu["y"]) - 12))

        # Draw player
        if player_shield:
            pygame.draw.circle(screen, (0, 255, 255), (player_x, player_y + 35), 40, 2)
        screen.blit(player_img, (player_x - 25, player_y))

        # HUD
        score_text = font_small.render(f"Score: {score}", True, WHITE)
        dist_text = font_small.render(f"Dist: {distance}m", True, WHITE)
        coins_text = font_small.render(f"Coins: {coins_collected}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(dist_text, (10, 30))
        screen.blit(coins_text, (10, 50))

        if powerup_active:
            remaining = 5 - (pygame.time.get_ticks() - powerup_start_time) // 1000
            pu_text = font_small.render(f"{powerup_type}: {remaining}s", True, GREEN)
            screen.blit(pu_text, (WIDTH - 150, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()