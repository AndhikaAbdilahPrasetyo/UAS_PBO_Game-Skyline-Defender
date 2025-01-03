# Import module pygame untuk membuat game 2D.
import pygame
from pygame.sprite import Sprite  # Import Sprite untuk mempermudah pengelolaan objek peluru.

class Bullet(Sprite):
    """
    Kelas untuk mengelola peluru yang ditembakkan oleh pesawat.
    """

    def __init__(self, ai_settings, screen, ship):
        """
        Membuat objek peluru di posisi pesawat saat ini.
        """
        super(Bullet, self).__init__()
        self.screen = screen

        # Mengatur ukuran dan posisi awal peluru.
        self.rect = pygame.Rect(
            0, 0, ai_settings.bullet_width, ai_settings.bullet_height
        )
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Menyimpan posisi vertikal peluru.
        self.y = float(self.rect.y)

        # Mengatur warna dan kecepatan peluru.
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """
        Menggerakkan peluru ke atas layar.
        """
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """
        Menampilkan peluru di layar.
        """
        pygame.draw.rect(self.screen, self.color, self.rect)

