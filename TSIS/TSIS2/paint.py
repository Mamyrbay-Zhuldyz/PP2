import pygame, math

class Tool:
    def __init__(self):
        self.current_tool = "pencil" 
        self.current_color = (0, 0, 0)
        self.brush_size = 2 # Default thickness
        self.drawing = False
        self.start_pos = None
        self.last_pos = None
        # Text tool state
        self.text_buffer = ""
        self.text_pos = None

    def set_tool(self, tool): self.current_tool = tool
    def set_color(self, color): self.current_color = color
    def set_size(self, size): self.brush_size = size

    def start_draw(self, pos):
        self.drawing = True
        self.start_pos = pos
        self.last_pos = pos
    
    def stop_draw(self):
        self.drawing = False
        self.start_pos = None

class Button:
    def __init__(self, x, y, width, height, action, action_type):
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.action_type = action_type # "tool", "color", or "size"
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def flood_fill(surface, x, y, new_color):
    """Fills a closed region starting from (x, y)."""
    try:
        target_color = surface.get_at((x, y))
    except IndexError: return
    
    if target_color == new_color: return

    pixels = [(x, y)]
    while pixels:
        px, py = pixels.pop()
        # Stay within canvas and avoid the toolbar (y > 60)
        if 0 <= px < surface.get_width() and 60 <= py < surface.get_height():
            if surface.get_at((px, py)) == target_color:
                surface.set_at((px, py), new_color) #
                pixels.extend([(px+1, py), (px-1, py), (px, py+1), (px, py-1)])

def create_buttons():
    buttons = []
    # Tools
    buttons.append(Button(10, 10, 40, 40, "pencil", "tool"))
    buttons.append(Button(60, 10, 40, 40, "line", "tool"))
    buttons.append(Button(110, 10, 40, 40, "rectangle", "tool"))
    buttons.append(Button(160, 10, 40, 40, "circle", "tool"))
    buttons.append(Button(210, 10, 40, 40, "fill", "tool"))
    buttons.append(Button(260, 10, 40, 40, "text", "tool"))
    buttons.append(Button(310, 10, 40, 40, "eraser", "tool"))
    
    # Brush Sizes
    buttons.append(Button(370, 15, 30, 30, 2, "size"))
    buttons.append(Button(410, 15, 30, 30, 5, "size"))
    buttons.append(Button(450, 15, 30, 30, 10, "size"))

    # Geometric Shapes from Practice 10-11
    buttons.append(Button(500, 10, 35, 35, "square", "tool"))
    buttons.append(Button(540, 10, 35, 35, "right_triangle", "tool"))
    buttons.append(Button(580, 10, 35, 35, "equilateral_triangle", "tool"))
    buttons.append(Button(620, 10, 35, 35, "rhombus", "tool"))

    # Colors
    buttons.append(Button(680, 15, 25, 25, (255, 0, 0), "color")) # Red
    buttons.append(Button(715, 15, 25, 25, (0, 255, 0), "color")) # Green
    buttons.append(Button(750, 15, 25, 25, (0, 0, 0), "color"))   # Black
    return buttons

def draw_buttons(screen, buttons, current_tool, current_color, current_size):
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, 800, 60))
    pygame.draw.line(screen, (150, 150, 150), (0, 60), (800, 60), 2)

    for btn in buttons:
        if btn.action_type == "tool":
            pygame.draw.rect(screen, (180, 180, 180), btn.rect)
            # Drawing the toolbar icons so they are visible
            if btn.action == "pencil": pygame.draw.line(screen, (0,0,0), (btn.rect.x+10, btn.rect.y+30), (btn.rect.x+30, btn.rect.y+10), 2)
            elif btn.action == "line": pygame.draw.line(screen, (0,0,0), (btn.rect.x+10, btn.rect.y+10), (btn.rect.x+30, btn.rect.y+30), 2)
            elif btn.action == "rectangle": pygame.draw.rect(screen, (0,0,0), (btn.rect.x+10, btn.rect.y+10, 20, 20), 1)
            elif btn.action == "circle": pygame.draw.circle(screen, (0,0,0), btn.rect.center, 10, 1)
            elif btn.action == "text": 
                f = pygame.font.SysFont("Arial", 20, bold=True)
                screen.blit(f.render("T", True, (0,0,0)), (btn.rect.x+12, btn.rect.y+10))
            elif btn.action == "square": pygame.draw.rect(screen, (0,0,0), (btn.rect.x+12, btn.rect.y+12, 16, 16), 1)
            elif btn.action == "right_triangle": pygame.draw.polygon(screen, (0,0,0), [(btn.rect.x+10, btn.rect.y+10), (btn.rect.x+10, btn.rect.y+30), (btn.rect.x+30, btn.rect.y+30)], 1)
            elif btn.action == "equilateral_triangle": pygame.draw.polygon(screen, (0,0,0), [(btn.rect.x+17, btn.rect.y+10), (btn.rect.x+10, btn.rect.y+30), (btn.rect.x+24, btn.rect.y+30)], 1)
            elif btn.action == "rhombus": pygame.draw.polygon(screen, (0,0,0), [(btn.rect.x+17, btn.rect.y+10), (btn.rect.x+24, btn.rect.y+20), (btn.rect.x+17, btn.rect.y+30), (btn.rect.x+10, btn.rect.y+20)], 1)
        elif btn.action_type == "color":
            pygame.draw.rect(screen, btn.action, btn.rect)
        elif btn.action_type == "size":
            pygame.draw.rect(screen, (200, 200, 200), btn.rect)
            pygame.draw.circle(screen, (0,0,0), btn.rect.center, btn.action // 2 + 1)

    # Highlighting selected tools/colors/sizes
    for btn in buttons:
        if btn.action == current_tool or btn.action == current_color or (btn.action_type == "size" and btn.action == current_size):
            pygame.draw.rect(screen, (0, 0, 255), btn.rect.inflate(4, 4), 3)

def draw_shape(surface, tool, color, start, end, width):
    """Draws shapes using the brush size as width."""
    x1, y1 = start
    x2, y2 = end
    if tool == "line": pygame.draw.line(surface, color, start, end, width) #
    elif tool == "rectangle": pygame.draw.rect(surface, color, (min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1)), width)
    elif tool == "circle":
        r = int(((x2-x1)**2 + (y2-y1)**2)**0.5) // 2
        if r > 0: pygame.draw.circle(surface, color, ((x1+x2)//2, (y1+y2)//2), r, width)
    elif tool == "square":
        s = max(abs(x2-x1), abs(y2-y1))
        pygame.draw.rect(surface, color, (min(x1, x2), min(y1, y2), s, s), width)
    elif tool == "right_triangle":
        pygame.draw.polygon(surface, color, [(x1, y1), (x1, y2), (x2, y2)], width)
    elif tool == "equilateral_triangle":
        h = (x2 - x1) * (math.sqrt(3) / 2)
        pygame.draw.polygon(surface, color, [(x1, y2), (x2, y2), ((x1 + x2) / 2, y2 - h)], width)
    elif tool == "rhombus":
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        pygame.draw.polygon(surface, color, [(mx, y1), (x2, my), (mx, y2), (x1, my)], width)