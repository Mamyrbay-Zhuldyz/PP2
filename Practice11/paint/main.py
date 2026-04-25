import pygame
import sys
from paint import Tool, draw_shape, Button

pygame.init()

# Размеры окна
WIDTH, HEIGHT = 1000, 700
WHITE = (255, 255, 255)
COLORS = [
    ("RED", (255, 0, 0)),
    ("GREEN", (0, 255, 0)),
    ("BLUE", (0, 0, 255)),
    ("BLACK", (0, 0, 0)),
    ("YELLOW", (255, 255, 0)),
    ("PURPLE", (128, 0, 128))
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint - Рисовалка")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)

# Создаем инструменты
tool_manager = Tool()

# Создаем кнопки инструментов
tools_buttons = [
    Button(10, 10, 70, 40, "Круг", "tool", "circle"),
    Button(90, 10, 70, 40, "Квадрат", "tool", "square"),
    Button(170, 10, 70, 40, "Прям-к", "tool", "rectangle"),
    Button(250, 10, 90, 40, "Прям. треуг", "tool", "right_triangle"),
    Button(350, 10, 90, 40, "Равн. треуг", "tool", "equilateral_triangle"),
    Button(450, 10, 70, 40, "Ромб", "tool", "rhombus"),
    Button(530, 10, 70, 40, "Ластик", "tool", "eraser"),
]

# Создаем кнопки цветов
color_buttons = []
x = 10
for i, (name, color) in enumerate(COLORS):
    color_buttons.append(Button(x, 60, 50, 35, name, "color", color))
    x += 60

# Фоновая панель
def draw_panel():
    pygame.draw.rect(screen, (240, 240, 240), (0, 0, WIDTH, 110))
    pygame.draw.line(screen, (0, 0, 0), (0, 110), (WIDTH, 110), 2)

# Обновление активных кнопок
def update_active_buttons():
    for btn in tools_buttons:
        btn.active = (btn.action_value == tool_manager.current_tool)
    
    for btn in color_buttons:
        btn.active = (btn.action_value == tool_manager.current_color)

# Очистка экрана
def clear_screen():
    screen.fill(WHITE)
    draw_panel()
    update_active_buttons()
    for btn in tools_buttons + color_buttons:
        btn.draw(screen, font)

# Главный цикл
def main():
    screen.fill(WHITE)
    draw_panel()
    update_active_buttons()
    
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Нажатие мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                
                # Проверка нажатия на кнопки
                clicked = False
                
                # Кнопки инструментов
                for btn in tools_buttons:
                    if btn.is_clicked(pos):
                        tool_manager.set_tool(btn.action_value)
                        update_active_buttons()
                        clicked = True
                        break
                
                # Кнопки цветов
                if not clicked:
                    for btn in color_buttons:
                        if btn.is_clicked(pos):
                            tool_manager.set_color(btn.action_value)
                            update_active_buttons()
                            clicked = True
                            break
                
                # Если нажали на область рисования
                if not clicked and pos[1] > 110:
                    tool_manager.start_draw(pos)
            
            # Отпускание мыши
            if event.type == pygame.MOUSEBUTTONUP:
                if tool_manager.drawing:
                    draw_shape(screen, tool_manager.current_tool, 
                              tool_manager.current_color, 
                              tool_manager.start_pos, event.pos)
                tool_manager.stop_draw()
                update_active_buttons()
            
            # Движение мыши (для ластика)
            if event.type == pygame.MOUSEMOTION and tool_manager.drawing:
                if tool_manager.current_tool == "eraser":
                    pygame.draw.circle(screen, WHITE, event.pos, 20)
                    tool_manager.start_pos = event.pos
        
        # Перерисовка кнопок
        draw_panel()
        for btn in tools_buttons + color_buttons:
            btn.draw(screen, font)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()