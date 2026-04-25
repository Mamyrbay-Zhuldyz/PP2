import pygame
import random

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("images/Player.png")
        self.image = pygame.transform.scale(self.image, (60, 100))
        self.x = x
        self.y = y
        self.width = 60
        self.height = 100
        self.speed = 5
    
    def move(self, keys, WIDTH):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Enemy:
    def __init__(self, WIDTH, base_speed=5):
        self.image = pygame.image.load("images/Enemy.png")
        self.image = pygame.transform.scale(self.image, (60, 100))
        self.x = random.randint(0, WIDTH - 60)
        self.y = -100
        self.width = 60
        self.height = 100
        self.speed = base_speed
    
    def move(self):
        self.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def is_off_screen(self, HEIGHT):
        return self.y > HEIGHT
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def increase_speed(self, amount=1):
        self.speed += amount

class Coin:
    # Типы монет: (название, цвет, очки, размер)
    COIN_TYPES = [
        {"name": "gold", "color": (255, 215, 0), "inner_color": (255, 255, 100), "points": 3, "size": 20},
        {"name": "silver", "color": (150, 150, 150), "inner_color": (200, 200, 200), "points": 2, "size": 18},
        {"name": "bronze", "color": (180, 100, 50), "inner_color": (220, 140, 80), "points": 1, "size": 15}
    ]
    
    def __init__(self, WIDTH):
        self.coin_type = random.choice(self.COIN_TYPES)
        self.x = random.randint(0, WIDTH - self.coin_type["size"] * 2)
        self.y = -self.coin_type["size"] * 2
        self.width = self.coin_type["size"] * 2
        self.height = self.coin_type["size"] * 2
        self.speed = 4
    
    def move(self):
        self.y += self.speed
    
    def draw(self, screen):
        color = self.coin_type["color"]
        inner_color = self.coin_type["inner_color"]
        size = self.coin_type["size"]
        x, y = self.x + size, self.y + size
        
        # Внешний круг (обводка для видимости)
        pygame.draw.circle(screen, (0, 0, 0), (x, y), size + 2)  # черная обводка
        # Основной цвет монеты
        pygame.draw.circle(screen, color, (x, y), size)
        # Внутренний блик
        pygame.draw.circle(screen, inner_color, (x - size//4, y - size//4), size//3)
        
        # Рисуем звездочку или символ на монете
        font = pygame.font.Font(None, size)
        if self.coin_type["name"] == "gold":
            symbol = "★"
        elif self.coin_type["name"] == "silver":
            symbol = "●"
        else:
            symbol = "♦"
        
        text = font.render(symbol, True, (255, 255, 255))
        screen.blit(text, (x - size//2, y - size//2))
    
    def is_off_screen(self, HEIGHT):
        return self.y > HEIGHT
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_points(self):
        return self.coin_type["points"]