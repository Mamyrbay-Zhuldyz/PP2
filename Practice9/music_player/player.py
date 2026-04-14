import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        self.playlist = []
        self.current_track_index = 0
        self.is_playing = False
        self.load_playlist()
    
    def load_playlist(self):
        """Загружает все музыкальные файлы из папки"""
        if os.path.exists(self.music_folder):
            files = os.listdir(self.music_folder)
            self.playlist = [f for f in files if f.endswith(('.mp3', '.wav', '.ogg'))]
            print(f"Загружено треков: {len(self.playlist)}")
            if self.playlist:
                print(f"Первый трек: {self.playlist[0]}")
        else:
            print(f"Папка {self.music_folder} не найдена!")
    
    def play(self):
        """Воспроизводит текущий трек"""
        if not self.playlist:
            print("Нет треков в плейлисте!")
            return
        
        track_path = os.path.join(self.music_folder, self.playlist[self.current_track_index])
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        self.is_playing = True
        print(f"Воспроизводится: {self.playlist[self.current_track_index]}")
    
    def stop(self):
        """Останавливает воспроизведение"""
        pygame.mixer.music.stop()
        self.is_playing = False
        print("Воспроизведение остановлено")
    
    def next_track(self):
        """Переключает на следующий трек"""
        if not self.playlist:
            return
        
        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        self.play()
        print(f"Следующий трек: {self.playlist[self.current_track_index]}")
    
    def previous_track(self):
        """Переключает на предыдущий трек"""
        if not self.playlist:
            return
        
        self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
        self.play()
        print(f"Предыдущий трек: {self.playlist[self.current_track_index]}")
    
    def get_current_track_name(self):
        """Возвращает имя текущего трека"""
        if self.playlist:
            return self.playlist[self.current_track_index]
        return "Нет треков"
    
    def get_status(self):
        """Возвращает статус воспроизведения"""
        if self.is_playing:
            return "Playing ▶"
        return "Stopped ■"