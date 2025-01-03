# Import module pygame untuk membuat game 2D
import pygame
from pygame.sprite import Group  # Import Group untuk mengelola sekumpulan objek (seperti peluru dan alien)
import sys  # Digunakan untuk keluar dari program

# Import file lain dalam proyek yang berisi kelas atau fungsi tambahan
from settings import Settings  # Pengaturan umum game (misalnya, ukuran layar, kecepatan, dll.)
from game_stats import GameStats  # Untuk melacak statistik game (misalnya, skor, status permainan aktif)
from scoreboard import Scoreboard  # Untuk menampilkan skor di layar
from button import Button  # Untuk membuat tombol Play
from ship import Ship  # Kelas pesawat pemain
import game_functions as gf  # Modul berisi fungsi-fungsi utama game (seperti event handler)


def run_game():
    """
    Fungsi utama untuk menjalankan game Skyline Defender.
    """

    # Inisialisasi pygame dan pengaturan game
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Skyline Defender")

    # Membuat elemen utama dalam game
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Membuat formasi alien
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Loop utama game
    while True:
        # Mengelola input pemain
        gf.check_events(
            ai_settings, screen, stats, sb, play_button, ship, aliens, bullets
        )

        # Memproses logika permainan jika aktif
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)

        # Memperbarui tampilan layar
        gf.update_screen(
            ai_settings, screen, stats, sb, ship, aliens, bullets, play_button
        )

# Memulai game
run_game()

