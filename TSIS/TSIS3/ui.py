import pygame

pygame.init()

WIDTH, HEIGHT = 400, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)

font_small = pygame.font.SysFont("Verdana", 16)
font_medium = pygame.font.SysFont("Verdana", 24)
font_big = pygame.font.SysFont("Verdana", 40, bold=True)

screen = None

def init_ui(display_surface):
    global screen
    screen = display_surface

def draw_button(text, y_pos, width=220, height=50):
    rect = pygame.Rect(WIDTH // 2 - width // 2, y_pos, width, height)
    pygame.draw.rect(screen, GRAY, rect, border_radius=8)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
    btn_text = font_medium.render(text, True, WHITE)
    text_rect = btn_text.get_rect(center=rect.center)
    screen.blit(btn_text, text_rect)
    return rect

def show_menu(username=""):
    screen.fill(BLACK)
    title = font_big.render("RACER GAME", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))
    name_prompt = font_small.render("Enter username:", True, WHITE)
    screen.blit(name_prompt, (WIDTH // 2 - 80, 130))
    name_text = font_medium.render(username, True, CYAN)
    screen.blit(name_text, (WIDTH // 2 - 80, 155))
    return draw_button("PLAY", 220), draw_button("LEADERBOARD", 290), draw_button("SETTINGS", 360), draw_button("QUIT", 430)

def show_settings_screen(settings):
    screen.fill(BLACK)
    title = font_big.render("SETTINGS", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
    btn_sound = draw_button(f"Sound: {'ON' if settings['sound'] else 'OFF'}", 130)
    btn_diff = draw_button(f"Difficulty: {settings['difficulty'].upper()}", 200)
    btn_color = draw_button("Car Color", 270)
    btn_back = draw_button("SAVE & BACK", 400)
    return btn_sound, btn_diff, btn_color, btn_back

def show_game_over(score, distance, coins):
    screen.fill(BLACK)
    title = font_big.render("GAME OVER", True, RED)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))
    for i, (label, value) in enumerate([("Score", score), ("Distance", f"{distance}m"), ("Coins", coins)]):
        text = font_medium.render(f"{label}: {value}", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 160 + i * 35))
    return draw_button("RETRY", 300), draw_button("MAIN MENU", 370)

def show_leaderboard_screen(leaderboard):
    screen.fill(BLACK)
    title = font_big.render("TOP 10", True, YELLOW)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    y = 80
    header = font_small.render(f"{'Rank':<5} {'Name':<12} {'Score':<8} {'Dist':<6}", True, WHITE)
    screen.blit(header, (30, y))
    y += 25
    for entry in leaderboard[:10]:
        text = font_small.render(f"{entry['rank']:<5} {entry['name']:<12} {entry['score']:<8} {entry['distance']:<6}m", True, WHITE)
        screen.blit(text, (30, y))
        y += 25
    return draw_button("BACK", 500)