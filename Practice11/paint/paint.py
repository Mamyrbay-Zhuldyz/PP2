import pygame
import math

class Tool:
    def __init__(self):
        self.current_tool = "circle"
        self.current_color = (0, 0, 0)
        self.drawing = False
        self.start_pos = None
        self.radius = 10  # для ластика
    
    def set_tool(self, tool):
        self.current_tool = tool
    
    def set_color(self, color):
        self.current_color = color
    
    def start_draw(self, pos):
        self.drawing = True
        self.start_pos = pos
    
    def stop_draw(self):
        self.drawing = False
        self.start_pos = None

def draw_shape(screen, tool, color, start, end):
    """Рисует фигуру от start до end"""
    x1, y1 = start
    x2, y2 = end
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    
    if tool == "circle":
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        radius = max(width, height) // 2
        pygame.draw.circle(screen, color, center, radius, 3)
    
    elif tool == "rectangle":
        rect = pygame.Rect(min(x1, x2), min(y1, y2), width, height)
        pygame.draw.rect(screen, color, rect, 3)
    
    elif tool == "square":
        size = max(width, height)
        rect = pygame.Rect(min(x1, x2), min(y1, y2), size, size)
        pygame.draw.rect(screen, color, rect, 3)
    
    elif tool == "right_triangle":
        # Прямоугольный треугольник
        points = [(x1, y1), (x2, y1), (x1, y2)]
        pygame.draw.polygon(screen, color, points, 3)
    
    elif tool == "equilateral_triangle":
        # Равносторонний треугольник
        side = max(width, height)
        height_triangle = int(side * math.sqrt(3) / 2)
        points = [
            (x1, y2),
            (x1 + side, y2),
            (x1 + side // 2, y2 - height_triangle)
        ]
        pygame.draw.polygon(screen, color, points, 3)
    
    elif tool == "rhombus":
        # Ромб
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        dx = width // 2
        dy = height // 2
        points = [
            (cx, cy - dy),
            (cx + dx, cy),
            (cx, cy + dy),
            (cx - dx, cy)
        ]
        pygame.draw.polygon(screen, color, points, 3)
    
    elif tool == "eraser":
        pygame.draw.circle(screen, (255, 255, 255), end, 20)

class Button:
    def __init__(self, x, y, width, height, text, action_type, action_value):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action_type = action_type
        self.action_value = action_value
        self.active = False
    
    def draw(self, screen, font):
        # Цвет кнопки
        if self.active:
            color = (100, 200, 255)  # активная кнопка
        else:
            color = (220, 220, 220)
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        
        # Текст на кнопке
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)