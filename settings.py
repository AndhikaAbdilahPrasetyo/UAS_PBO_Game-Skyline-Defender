# Import modul pygame untuk menggunakan fitur grafis.
import pygame

class Settings:
    """
    Kelas untuk menyimpan semua pengaturan permainan Skyline Defender.
    """

    def __init__(self):
        """
        Menginisialisasi pengaturan statis game.
        """
        # Pengaturan layar.
        self.screen_width = 1200  
        self.screen_height = 800  
        self.background_image = pygame.image.load("background.jpeg")  

        # Pengaturan kapal.
        self.ship_limit = 3  

        # Pengaturan peluru.
        self.bullet_width = 3  
        self.bullet_height = 15  
        self.bullet_color = (200, 0, 0)  
        self.bullets_allowed = 5  

        # Pengaturan alien.
        self.fleet_drop_speed = 10  

        # Skala percepatan permainan.
        self.speedup_scale = 1.1  
        self.score_scale = 1.5  

        # Inisialisasi pengaturan dinamis.
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """
        Menginisialisasi pengaturan yang berubah selama permainan.
        """
        self.ship_speed_factor = 3.0  
        self.bullet_speed_factor = 3  
        self.alien_speed_factor = 1  

        # Poin awal untuk alien.
        self.alien_points = 50

        # Arah gerakan alien: 1 untuk kanan, -1 untuk kiri.
        self.fleet_direction = 1

    def increase_speed(self):
        """
        Meningkatkan kecepatan permainan dan nilai poin alien.
        """
        self.ship_speed_factor *= self.speedup_scale  
        self.bullet_speed_factor *= self.speedup_scale  
        self.alien_speed_factor *= self.speedup_scale  

        self.alien_points = int(self.alien_points * self.score_scale)  
