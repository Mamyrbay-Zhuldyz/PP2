import pygame
import datetime
import math

class MickeyClock:
    def __init__(self, screen, center_x, center_y):
        self.screen = screen
        self.center_x = center_x
        self.center_y = center_y
        self.clock_face = None
        self.left_hand = None   # левая рука (секунды)
        self.right_hand = None  # правая рука (минуты)
    
    def load_images(self, face_path, left_hand_path, right_hand_path):
        """Загружает изображения циферблата и рук Микки"""
        # Загружаем циферблат
        self.clock_face = pygame.image.load(face_path)
        self.clock_face = pygame.transform.scale(self.clock_face, (400, 400))
        
        # Загружаем левую руку (секундная стрелка)
        self.left_hand = pygame.image.load(left_hand_path)
        self.left_hand = pygame.transform.scale(self.left_hand, (480, 560))
        
        # Загружаем правую руку (минутная стрелка)
        self.right_hand = pygame.image.load(right_hand_path)
        self.right_hand = pygame.transform.scale(self.right_hand, (320, 400))
        
        print("Все изображения загружены успешно!")
    
    def get_time_angles(self):
        """Получает текущее время и возвращает углы для стрелок"""
        now = datetime.datetime.now()
        seconds = now.second
        minutes = now.minute
        
        # Угол для секундной стрелки (левая рука) - 6 градусов в секунду
        seconds_angle = seconds * 6
        # Угол для минутной стрелки (правая рука) - 6 градусов в минуту
        minutes_angle = (minutes + seconds / 60) * 6
        
        return seconds_angle, minutes_angle
    
    def rotate_hand(self, image, angle, center):
        """Поворачивает изображение руки вокруг центра"""
        rotated_image = pygame.transform.rotate(image, -angle)
        new_rect = rotated_image.get_rect(center=center)
        return rotated_image, new_rect
    
    def draw(self):
        """Отрисовывает часы с руками Микки Мауса"""
        # Получаем углы для стрелок
        seconds_angle, minutes_angle = self.get_time_angles()
        
        # Рисуем циферблат
        face_rect = self.clock_face.get_rect(center=(self.center_x, self.center_y))
        self.screen.blit(self.clock_face, face_rect)
        
        # Рисуем левую руку (секунды)
        left_rotated, left_rect = self.rotate_hand(
            self.left_hand, seconds_angle, (self.center_x, self.center_y))
        self.screen.blit(left_rotated, left_rect)
        
        # Рисуем правую руку (минуты)
        right_rotated, right_rect = self.rotate_hand(
            self.right_hand, minutes_angle, (self.center_x, self.center_y))
        self.screen.blit(right_rotated, right_rect)
    
    def draw_digital_time(self):
        """Рисует цифровое время внизу"""
        now = datetime.datetime.now()
        font = pygame.font.Font(None, 48)
        time_text = font.render(f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}", 
                                True, (0, 0, 0))
        text_rect = time_text.get_rect(center=(self.center_x, self.center_y + 220))
        self.screen.blit(time_text, text_rect)