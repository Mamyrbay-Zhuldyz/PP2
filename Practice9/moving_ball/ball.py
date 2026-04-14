import pygame

class Ball:
    def __init__(self, x, y, radius, color):
        """Конструктор мяча"""
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    
    def draw(self, screen):
        """Рисует мяч на экране"""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    def move_left(self, distance, screen_width):
        """Двигает мяч влево, если не выходит за границу"""
        if self.x - self.radius - distance >= 0:
            self.x -= distance
            return True
        return False
    
    def move_right(self, distance, screen_width):
        """Двигает мяч вправо, если не выходит за границу"""
        if self.x + self.radius + distance <= screen_width:
            self.x += distance
            return True
        return False
    
    def move_up(self, distance, screen_height):
        """Двигает мяч вверх, если не выходит за границу"""
        if self.y - self.radius - distance >= 0:
            self.y -= distance
            return True
        return False
    
    def move_down(self, distance, screen_height):
        """Двигает мяч вниз, если не выходит за границу"""
        if self.y + self.radius + distance <= screen_height:
            self.y += distance
            return True
        return False
    
    def get_position(self):
        """Возвращает позицию мяча"""
        return (self.x, self.y)