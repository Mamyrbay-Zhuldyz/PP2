import pygame
import random

WIDTH, HEIGHT = 400, 600
LANE_COUNT = 3
LANE_WIDTH = WIDTH // LANE_COUNT
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)
CYAN = (0, 255, 255)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)

class Player:
    def __init__(self):
        self.lane = 1
        self.x = LANE_WIDTH * self.lane + LANE_WIDTH // 2
        self.y = HEIGHT - 100
        self.width = 50
        self.height = 70
        self.shield = False
        self.color = (0, 255, 0)

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.x = LANE_WIDTH * self.lane + LANE_WIDTH // 2

    def move_right(self):
        if self.lane < LANE_COUNT - 1:
            self.lane += 1
            self.x = LANE_WIDTH * self.lane + LANE_WIDTH // 2

    def draw(self, screen):
        color = CYAN if self.shield else self.color
        rect = pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)
        pygame.draw.rect(screen, color, rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, rect, 2, border_radius=5)
        # Windows
        pygame.draw.rect(screen, BLACK, (self.x - 15, self.y + 10, 30, 20), border_radius=3)

    def collide(self, obj):
        car_rect = pygame.Rect(self.x - self.width // 2, self.y, self.width, self.height)
        if obj.get("type") == "oil":
            obj_rect = pygame.Rect(obj["x"], obj["y"], LANE_WIDTH, 20)
        elif obj.get("type") == "pothole":
            obj_rect = pygame.Rect(obj["x"] + 20, obj["y"], LANE_WIDTH - 40, 20)
        else:
            obj_rect = pygame.Rect(obj["x"] - 25, obj["y"], 50, 70)
        return car_rect.colliderect(obj_rect)

class RacerGame:
    def __init__(self):
        self.road_offset = 0
        self.road_speed = 5
        self.score = 0
        self.distance = 0
        self.coins_collected = 0
        self.difficulty_level = 1
        self.traffic_cars = []
        self.obstacles = []
        self.coins = []
        self.powerups = []
        self.powerup_active = False
        self.powerup_type = None
        self.powerup_start_time = 0

    def spawn_traffic(self):
        if len(self.traffic_cars) < 2 + self.difficulty_level:
            lane = random.randint(0, LANE_COUNT - 1)
            self.traffic_cars.append({
                "x": lane * LANE_WIDTH + LANE_WIDTH // 2, "y": -50,
                "lane": lane, "speed": 3 + random.randint(0, self.difficulty_level)
            })

    def spawn_obstacle(self):
        if len(self.obstacles) < self.difficulty_level:
            lane = random.randint(0, LANE_COUNT - 1)
            self.obstacles.append({
                "x": lane * LANE_WIDTH, "y": -30, "lane": lane,
                "type": random.choice(["barrier", "oil", "pothole"])
            })

    def spawn_coin(self):
        if len(self.coins) < 3:
            lane = random.randint(0, LANE_COUNT - 1)
            self.coins.append({
                "x": lane * LANE_WIDTH + LANE_WIDTH // 2, "y": -20,
                "lane": lane, "value": random.choice([1, 2, 3])
            })

    def spawn_powerup(self):
        if len(self.powerups) < 1 and random.random() < 0.003:
            self.powerups.append({
                "x": random.randint(0, LANE_COUNT - 1) * LANE_WIDTH + LANE_WIDTH // 2,
                "y": -30, "type": random.choice(["nitro", "shield", "repair"])
            })

    def update(self):
        self.road_offset = (self.road_offset + self.road_speed) % 40
        self.distance += self.road_speed // 10

        if self.distance // 100 > self.difficulty_level:
            self.difficulty_level = min(self.distance // 100 + 1, 10)

        for car in self.traffic_cars[:]:
            car["y"] += car["speed"]
            if car["y"] > HEIGHT + 50:
                self.traffic_cars.remove(car)

        for obs in self.obstacles[:]:
            obs["y"] += self.road_speed
            if obs["y"] > HEIGHT + 30:
                self.obstacles.remove(obs)

        for coin in self.coins[:]:
            coin["y"] += self.road_speed
            if coin["y"] > HEIGHT + 20:
                self.coins.remove(coin)

        for pu in self.powerups[:]:
            pu["y"] += self.road_speed
            if pu["y"] > HEIGHT + 30:
                self.powerups.remove(pu)

        if self.powerup_active and pygame.time.get_ticks() - self.powerup_start_time > 5000:
            self.powerup_active = False
            self.powerup_type = None
            if self.road_speed > 10:
                self.road_speed -= 3

    def draw_road(self, screen):
        screen.fill(BLACK)
        for i in range(LANE_COUNT - 1):
            x = (i + 1) * LANE_WIDTH
            for y in range(-40, HEIGHT, 40):
                pygame.draw.rect(screen, WHITE, (x - 2, y + self.road_offset, 4, 20))

    def draw_objects(self, screen, player):
        for car in self.traffic_cars:
            rect = pygame.Rect(car["x"] - 25, car["y"], 50, 70)
            pygame.draw.rect(screen, RED, rect, border_radius=5)
            pygame.draw.rect(screen, BLACK, (car["x"] - 15, car["y"] + 10, 30, 20), border_radius=3)

        for obs in self.obstacles:
            if obs["type"] == "barrier":
                pygame.draw.rect(screen, ORANGE, (obs["x"], obs["y"], LANE_WIDTH, 15))
            elif obs["type"] == "oil":
                pygame.draw.rect(screen, (50, 50, 50), (obs["x"], obs["y"], LANE_WIDTH, 15))
            elif obs["type"] == "pothole":
                pygame.draw.ellipse(screen, BROWN, (obs["x"] + 20, obs["y"], LANE_WIDTH - 40, 20))

        for coin in self.coins:
            color = {1: YELLOW, 2: ORANGE, 3: RED}.get(coin["value"], YELLOW)
            pygame.draw.circle(screen, color, (coin["x"], int(coin["y"])), 12)
            pygame.draw.circle(screen, WHITE, (coin["x"], int(coin["y"])), 12, 2)

        for pu in self.powerups:
            colors = {"nitro": BLUE, "shield": PURPLE, "repair": GREEN}
            pygame.draw.circle(screen, colors.get(pu["type"], WHITE), (pu["x"], int(pu["y"])), 15)
            first_letter = font_small.render(pu["type"][0].upper(), True, WHITE)
            screen.blit(first_letter, (pu["x"] - 5, int(pu["y"]) - 8))
            player.draw(screen)

    def reset(self):
        self.__init__()