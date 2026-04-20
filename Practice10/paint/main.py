import pygame
import sys
from paint import Tool, create_buttons, draw_buttons, draw_shape

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint - Рисовалка")
clock = pygame.time.Clock()

screen.fill(WHITE)

tool_manager = Tool()
buttons = create_buttons()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            clicked = False
            
            for button in buttons:
                if button.is_clicked(pos):
                    if button.action_type == "tool":
                        tool_manager.set_tool(button.action)
                    elif button.action_type == "color":
                        tool_manager.set_color(button.action)
                    clicked = True
                    break
            
            if not clicked and pos[1] > 60:
                tool_manager.start_draw(pos)
        
        if event.type == pygame.MOUSEBUTTONUP:
            if tool_manager.drawing:
                draw_shape(screen, tool_manager.current_tool, 
                          tool_manager.current_color, 
                          tool_manager.start_pos, event.pos)
            tool_manager.stop_draw()
        
        if event.type == pygame.MOUSEMOTION and tool_manager.drawing:
            if tool_manager.current_tool == "eraser":
                pygame.draw.circle(screen, WHITE, event.pos, 20)
    
    draw_buttons(screen, buttons, tool_manager.current_tool, tool_manager.current_color)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()