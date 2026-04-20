import pygame
import random

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
        # Столкновение со стенами
        if (head[0] < 0 or head[0] >= self.WIDTH or 
            head[1] < 0 or head[1] >= self.HEIGHT):
            return True
        # Столкновение с собой
        if head in self.body[1:]:
            return True
        return False
    
    def draw(self, screen, GREEN):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], self.CELL_SIZE, self.CELL_SIZE))
    
    def get_head(self):
        return self.body[0]

class Food:
    def __init__(self, snake_body, WIDTH, HEIGHT, CELL_SIZE):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.CELL_SIZE = CELL_SIZE
        self.position = self.random_position(snake_body)
    
    def random_position(self, snake_body):
        while True:
            x = random.randint(0, (self.WIDTH // self.CELL_SIZE) - 1) * self.CELL_SIZE
            y = random.randint(0, (self.HEIGHT // self.CELL_SIZE) - 1) * self.CELL_SIZE
            if [x, y] not in snake_body:
                return [x, y]
    
    def draw(self, screen, RED):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], self.CELL_SIZE, self.CELL_SIZE))
    
    def get_position(self):
        return self.position