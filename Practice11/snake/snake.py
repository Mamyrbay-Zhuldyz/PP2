import pygame
import random
import time

class Snake:
    def __init__(self, WIDTH, HEIGHT, CELL_SIZE):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.CELL_SIZE = CELL_SIZE
        self.body = [[WIDTH//2, HEIGHT//2]]
        self.direction = "RIGHT"
        self.grow_flag = False
    
    def move(self):
        head = self.body[0].copy()
        if self.direction == "RIGHT":
            head[0] += self.CELL_SIZE
        elif self.direction == "LEFT":
            head[0] -= self.CELL_SIZE
        elif self.direction == "UP":
            head[1] -= self.CELL_SIZE
        elif self.direction == "DOWN":
            head[1] += self.CELL_SIZE
        
        self.body.insert(0, head)
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False
    
    def grow(self):
        self.grow_flag = True
    
    def change_direction(self, new_dir):
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        if opposites[new_dir] != self.direction:
            self.direction = new_dir
    
    def check_collision(self):
        head = self.body[0]
        if (head[0] < 0 or head[0] >= self.WIDTH or 
            head[1] < 0 or head[1] >= self.HEIGHT):
            return True
        if head in self.body[1:]:
            return True
        return False
    
    def draw(self, screen, GREEN):
        for i, segment in enumerate(self.body):
            if i == 0:
                pygame.draw.rect(screen, (0, 150, 0), (segment[0], segment[1], self.CELL_SIZE, self.CELL_SIZE))
            else:
                pygame.draw.rect(screen, GREEN, (segment[0], segment[1], self.CELL_SIZE, self.CELL_SIZE))
    
    def get_head(self):
        return self.body[0]

class NormalFood:
    def __init__(self, snake_body, WIDTH, HEIGHT, CELL_SIZE):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.CELL_SIZE = CELL_SIZE
        self.position = self.random_position(snake_body)
        self.points = 1
        self.color = (255, 0, 0)
    
    def random_position(self, snake_body):
        while True:
            x = random.randint(0, (self.WIDTH // self.CELL_SIZE) - 1) * self.CELL_SIZE
            y = random.randint(0, (self.HEIGHT // self.CELL_SIZE) - 1) * self.CELL_SIZE
            if [x, y] not in snake_body:
                return [x, y]
    
    def draw(self, screen):
        x, y = self.position
        size = self.CELL_SIZE
        pygame.draw.rect(screen, self.color, (x, y, size, size))
        pygame.draw.circle(screen, (255, 255, 255), (x + size//3, y + size//3), size//6)
        pygame.draw.ellipse(screen, (0, 255, 0), (x + size//2, y - 3, size//4, size//3))
    
    def get_points(self):
        return self.points
    
    def get_position(self):
        return self.position

class SpecialFood:
    def __init__(self, snake_body, WIDTH, HEIGHT, CELL_SIZE):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.CELL_SIZE = CELL_SIZE
        self.position = self.random_position(snake_body)
        self.points = random.choice([3, 4, 5])
        self.spawn_time = time.time()
        self.lifetime = 5
        if self.points == 3:
            self.color = (255, 165, 0)
        elif self.points == 4:
            self.color = (255, 255, 0)
        else:
            self.color = (255, 0, 255)
    
    def random_position(self, snake_body):
        while True:
            x = random.randint(0, (self.WIDTH // self.CELL_SIZE) - 1) * self.CELL_SIZE
            y = random.randint(0, (self.HEIGHT // self.CELL_SIZE) - 1) * self.CELL_SIZE
            if [x, y] not in snake_body:
                return [x, y]
    
    def draw(self, screen):
        x, y = self.position
        size = self.CELL_SIZE
        pygame.draw.rect(screen, self.color, (x, y, size, size))
        pygame.draw.circle(screen, (255, 255, 255), (x + size//2, y + size//2), size//3)
        
        remaining = max(0, self.lifetime - (time.time() - self.spawn_time))
        ratio = remaining / self.lifetime
        pygame.draw.arc(screen, (0, 0, 0), (x + 2, y + 2, size - 4, size - 4), 
                        0, 2 * 3.14159 * ratio, 3)
    
    def is_expired(self):
        return time.time() - self.spawn_time > self.lifetime
    
    def get_points(self):
        return self.points
    
    def get_position(self):
        return self.position