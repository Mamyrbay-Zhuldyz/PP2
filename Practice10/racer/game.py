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
    def __init__(self, WIDTH):
        self.image = pygame.image.load("images/Enemy.png")
        self.image = pygame.transform.scale(self.image, (60, 100))
        self.x = random.randint(0, WIDTH - 60)
        self.y = -100
        self.width = 60
        self.height = 100
        self.speed = 5
    
    def move(self):
        self.y += self.speed
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def is_off_screen(self, HEIGHT):
        return self.y > HEIGHT
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Coin:
    def __init__(self, WIDTH):
        self.x = random.randint(0, WIDTH - 30)
        self.y = -30
        self.width = 30
        self.height = 30
        self.speed = 4
    
    def move(self):
        self.y += self.speed
    
    def draw(self, screen):
        # Рисуем золотую монету
        pygame.draw.circle(screen, (255, 215, 0), (self.x + 15, self.y + 15), 15)
        pygame.draw.circle(screen, (255, 255, 0), (self.x + 15, self.y + 15), 10)
        pygame.draw.circle(screen, (255, 200, 0), (self.x + 10, self.y + 10), 5)
    
    def is_off_screen(self, HEIGHT):
        return self.y > HEIGHT
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)