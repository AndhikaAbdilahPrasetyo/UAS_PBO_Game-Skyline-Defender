# Import modul pygame untuk pengelolaan suara.
import pygame

# Inisialisasi mixer untuk menangani pemutaran suara.
pygame.mixer.init()

# Memuat file suara untuk berbagai efek dalam permainan.
bullet_sound = pygame.mixer.Sound('bullet_sound.wav')  # Suara peluru.
explosion_sound = pygame.mixer.Sound('explosion.wav')  # Suara ledakan.
