import pygame

class Tool:
    def __init__(self):
        self.current_tool = "circle"
        self.current_color = (0, 0, 0)
        self.drawing = False
        self.start_pos = None
    
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

class Button:
    def __init__(self, x, y, width, height, action, action_type, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.action_type = action_type  # "tool" или "color"
        self.color = color
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def create_buttons():
    buttons = []
    # Инструменты
    buttons.append(Button(10, 10, 40, 40, "circle", "tool"))
    buttons.append(Button(60, 10, 40, 40, "rectangle", "tool"))
    buttons.append(Button(110, 10, 40, 40, "eraser", "tool"))
    # Цвета
    buttons.append(Button(170, 10, 30, 30, (255, 0, 0), "color"))
    buttons.append(Button(210, 10, 30, 30, (0, 255, 0), "color"))
    buttons.append(Button(250, 10, 30, 30, (0, 0, 255), "color"))
    buttons.append(Button(290, 10, 30, 30, (0, 0, 0), "color"))
    return buttons

def draw_buttons(screen, buttons, current_tool, current_color):
    # Фон панели
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, 340, 60))
    
    # Кнопка круга
    pygame.draw.rect(screen, (200, 200, 200), (10, 10, 40, 40))
    pygame.draw.circle(screen, (0, 0, 0), (30, 30), 15)
    
    # Кнопка прямоугольника
    pygame.draw.rect(screen, (200, 200, 200), (60, 10, 40, 40))
    pygame.draw.rect(screen, (0, 0, 0), (70, 20, 20, 20))
    
    # Кнопка ластика
    pygame.draw.rect(screen, (200, 200, 200), (110, 10, 40, 40))
    pygame.draw.rect(screen, (255, 255, 255), (120, 20, 20, 20))
    
    # Цвета
    pygame.draw.rect(screen, (255, 0, 0), (170, 10, 30, 30))
    pygame.draw.rect(screen, (0, 255, 0), (210, 10, 30, 30))
    pygame.draw.rect(screen, (0, 0, 255), (250, 10, 30, 30))
    pygame.draw.rect(screen, (0, 0, 0), (290, 10, 30, 30))
    
    # Обводка выбранного инструмента
    if current_tool == "circle":
        pygame.draw.rect(screen, (0, 0, 255), (8, 8, 44, 44), 3)
    elif current_tool == "rectangle":
        pygame.draw.rect(screen, (0, 0, 255), (58, 8, 44, 44), 3)
    elif current_tool == "eraser":
        pygame.draw.rect(screen, (0, 0, 255), (108, 8, 44, 44), 3)
    
    # Обводка выбранного цвета
    if current_color == (255, 0, 0):
        pygame.draw.rect(screen, (0, 0, 255), (168, 8, 34, 34), 3)
    elif current_color == (0, 255, 0):
        pygame.draw.rect(screen, (0, 0, 255), (208, 8, 34, 34), 3)
    elif current_color == (0, 0, 255):
        pygame.draw.rect(screen, (0, 0, 255), (248, 8, 34, 34), 3)
    elif current_color == (0, 0, 0):
        pygame.draw.rect(screen, (0, 0, 255), (288, 8, 34, 34), 3)

def draw_shape(screen, tool, color, start, end):
    if tool == "circle":
        center = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
        radius = max(abs(end[0] - start[0]), abs(end[1] - start[1])) // 2
        pygame.draw.circle(screen, color, center, radius, 0 if tool != "eraser" else -1)
    elif tool == "rectangle":
        rect = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]),
                          abs(end[0] - start[0]), abs(end[1] - start[1]))
        pygame.draw.rect(screen, color, rect, 0 if tool != "eraser" else -1)