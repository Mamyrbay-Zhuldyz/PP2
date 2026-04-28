import pygame, sys, datetime
from paint import Tool, create_buttons, draw_buttons, draw_shape, flood_fill

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pro Paint")
clock = pygame.time.Clock()

# Initialize text font
font_text = pygame.font.SysFont("Arial", 24)
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

tool_manager = Tool()
buttons = create_buttons()
# List including the new straight line tool
SHAPE_TOOLS = ["rectangle", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus", "line"]

running = True
while running:
    curr_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        
        if event.type == pygame.KEYDOWN:
            # Size switching shortcuts
            if event.key == pygame.K_1: tool_manager.set_size(2)
            elif event.key == pygame.K_2: tool_manager.set_size(5)
            elif event.key == pygame.K_3: tool_manager.set_size(10)
            
            # Save Canvas shortcut
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                fn = f"paint_{datetime.datetime.now().strftime('%H%M%S')}.png"
                pygame.image.save(canvas, fn)

            # Text Tool interaction
            if tool_manager.current_tool == "text" and tool_manager.text_pos:
                if event.key == pygame.K_RETURN: # Render permanently
                    canvas.blit(font_text.render(tool_manager.text_buffer, True, tool_manager.current_color), tool_manager.text_pos)
                    tool_manager.text_buffer = ""; tool_manager.text_pos = None
                elif event.key == pygame.K_ESCAPE: # Cancel
                    tool_manager.text_buffer = ""; tool_manager.text_pos = None
                elif event.key == pygame.K_BACKSPACE: tool_manager.text_buffer = tool_manager.text_buffer[:-1]
                else: tool_manager.text_buffer += event.unicode # Real-time typing

        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked_ui = False
            for btn in buttons:
                if btn.is_clicked(event.pos):
                    if btn.action_type == "tool": tool_manager.set_tool(btn.action)
                    elif btn.action_type == "color": tool_manager.set_color(btn.action)
                    elif btn.action_type == "size": tool_manager.set_size(btn.action)
                    clicked_ui = True
            
            if not clicked_ui and event.pos[1] > 60:
                if tool_manager.current_tool == "fill": 
                    flood_fill(canvas, event.pos[0], event.pos[1], tool_manager.current_color)
                elif tool_manager.current_tool == "text": 
                    tool_manager.text_pos = event.pos #
                else:
                    tool_manager.start_draw(event.pos)
        
        if event.type == pygame.MOUSEBUTTONUP:
            if tool_manager.drawing:
                if tool_manager.current_tool in SHAPE_TOOLS:
                    draw_shape(canvas, tool_manager.current_tool, tool_manager.current_color, tool_manager.start_pos, event.pos, tool_manager.brush_size)
                tool_manager.stop_draw()

        if event.type == pygame.MOUSEMOTION and tool_manager.drawing:
            # Pencil with brush thickness
            if tool_manager.current_tool == "pencil":
                pygame.draw.line(canvas, tool_manager.current_color, tool_manager.last_pos, event.pos, tool_manager.brush_size)
                tool_manager.last_pos = event.pos
            elif tool_manager.current_tool == "eraser":
                pygame.draw.line(canvas, (255, 255, 255), tool_manager.last_pos, event.pos, tool_manager.brush_size * 5)
                tool_manager.last_pos = event.pos

    # --- RENDER ---
    screen.blit(canvas, (0, 0)) 
    # Live preview for drag-and-drop shapes
    if tool_manager.drawing and tool_manager.current_tool in SHAPE_TOOLS:
        draw_shape(screen, tool_manager.current_tool, tool_manager.current_color, tool_manager.start_pos, curr_pos, tool_manager.brush_size)
    # Live text preview
    if tool_manager.text_pos:
        screen.blit(font_text.render(tool_manager.text_buffer + "|", True, tool_manager.current_color), tool_manager.text_pos)
    
    draw_buttons(screen, buttons, tool_manager.current_tool, tool_manager.current_color, tool_manager.brush_size)
    pygame.display.flip()
    clock.tick(120)

pygame.quit()