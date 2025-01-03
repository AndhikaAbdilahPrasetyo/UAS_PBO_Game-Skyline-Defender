# Import module pygame untuk membuat game 2D dan modul font untuk teks.
import pygame.font

class Button:
    """
    Kelas untuk membuat tombol di layar.
    """

    def __init__(self, ai_settings, screen, msg):
        """
        Menginisialisasi atribut tombol.
        """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Mengatur dimensi dan properti tombol.
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)  # Warna tombol (hijau).
        self.text_color = (255, 255, 255)  # Warna teks (putih).
        self.font = pygame.font.SysFont(None, 48)  # Font dan ukuran teks.

        # Membuat objek tombol dan memusatkannya di layar.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Mempersiapkan pesan tombol.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """
        Mengubah pesan menjadi gambar yang dirender dan memusatkan teks di tombol.
        """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """
        Menampilkan tombol dan teksnya di layar.
        """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
