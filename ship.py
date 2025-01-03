# Import modul pygame untuk grafis dan Sprite untuk pengelolaan objek bergerak.
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """
    Kelas untuk mengelola pesawat pemain.
    """

    def __init__(self, ai_settings, screen):
        """
        Menginisialisasi pesawat dan menetapkan posisi awalnya.
        """
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Memuat gambar pesawat dan mendapatkan ukurannya.
        self.image = pygame.image.load("pesawattempur.png")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Menempatkan pesawat di bagian bawah-tengah layar.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Menyimpan posisi decimal untuk pergerakan yang halus.
        self.center = float(self.rect.centerx)
        self.top = float(self.rect.top)

        # Mengatur flag untuk pergerakan.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def center_ship(self):
        """
        Mengatur pesawat kembali ke posisi tengah bawah layar.
        """
        self.center = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def update(self):
        """
        Memperbarui posisi pesawat berdasarkan input pemain.
        """
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.top -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.top += self.ai_settings.ship_speed_factor

        # Memperbarui posisi berdasarkan koordinat.
        self.rect.centerx = self.center
        self.rect.top = self.top

    def blitme(self):
        """
        Menampilkan pesawat di posisinya saat ini.
        """
        self.screen.blit(self.image, self.rect)

