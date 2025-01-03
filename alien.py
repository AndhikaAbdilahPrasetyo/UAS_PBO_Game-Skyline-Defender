# Import module pygame untuk membuat game 2D.
import pygame
from pygame.sprite import Sprite  # Import Sprite untuk mempermudah pengelolaan objek game.


class Alien(Sprite):
    """
    Kelas yang merepresentasikan satu alien dalam permainan.
    """

    def __init__(self, ai_settings, screen):
        """
        Inisialisasi alien dan atur posisi awalnya.
        """
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Memuat gambar alien dan menetapkan posisinya.
        self.image = pygame.image.load("alien.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Menyimpan posisi horizontal alien.
        self.x = float(self.rect.x)

    def check_edges(self):
        """
        Memeriksa apakah alien berada di tepi layar.
        """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """
        Menggerakkan alien ke kanan atau ke kiri.
        """
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        """
        Menampilkan alien di layar.
        """
        self.screen.blit(self.image, self.rect)

