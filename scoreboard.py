# Import modul pygame untuk font dan grup sprite.
import pygame.font
from pygame.sprite import Group

# Import kelas Ship untuk menampilkan jumlah kapal yang tersisa.
from ship import Ship

class Scoreboard:
    """
    Kelas untuk menampilkan informasi skor dan level.
    """

    def __init__(self, ai_settings, screen, stats):
        """
        Menginisialisasi atribut yang berhubungan dengan skor.
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Pengaturan font untuk teks skor.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Persiapan tampilan awal skor, level, dan sisa nyawa.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """
        Mengubah skor menjadi gambar yang ditampilkan di layar.
        """
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color
        )

        # Menampilkan skor di pojok kanan atas.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """
        Mengubah skor tertinggi menjadi gambar yang ditampilkan di layar.
        """
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color
        )

        # Menampilkan skor tertinggi di tengah atas layar.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """
        Mengubah level menjadi gambar yang ditampilkan di layar.
        """
        self.level_image = self.font.render(
            str(self.stats.level), True, self.text_color
        )

        # Menampilkan level di bawah skor.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """
        Menampilkan jumlah nyawa (pesawat) yang tersisa.
        """
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """
        Menggambar skor, level, dan sisa nyawa di layar.
        """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
