# Mengimpor modul dan dependensi yang diperlukan.
import sys  # Untuk keluar dari program.
from time import sleep  # Untuk jeda waktu.
import sound as se  # Modul untuk mengatur suara.
import pygame  # Modul utama untuk membuat game.
from bullet import Bullet  # Kelas untuk objek peluru.
from alien import Alien  # Kelas untuk objek alien.

# Fungsi untuk menangani penekanan tombol.
def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """
    Merespons penekanan tombol.
    """
    if event.key == pygame.K_RIGHT: 
        ship.moving_right = True
    elif event.key == pygame.K_LEFT: 
        ship.moving_left = True
    elif event.key == pygame.K_UP:  
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:  
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:  
        fire_bullet(ai_settings, screen, ship, bullets) 
    elif event.key == pygame.K_ESCAPE:  
        sys.exit()

# Fungsi untuk menangani pelepasan tombol.
def check_keyup_events(event, ship):
    """
    Merespons pelepasan tombol.
    """
    if event.key == pygame.K_RIGHT:  
        ship.moving_right = False
    elif event.key == pygame.K_LEFT: 
        ship.moving_left = False
    elif event.key == pygame.K_UP:  
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:  
        ship.moving_down = False

# Fungsi utama untuk memeriksa semua jenis peristiwa.
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """
    Merespons peristiwa seperti penekanan tombol dan klik mouse.
    """
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            pygame.quit()  
            sys.exit()  
        elif event.type == pygame.KEYDOWN:  
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP: 
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            mouse_x, mouse_y = pygame.mouse.get_pos()  
            check_play_button(
                ai_settings, 
                screen,  
                stats,  
                sb,  
                play_button, 
                ship,  
                aliens,  
                bullets,  
                mouse_x, 
                mouse_y,  
            )



# Fungsi untuk menangani klik tombol Play.
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """
    Memulai permainan baru ketika pemain mengklik tombol Play.
    """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)  
    if button_clicked and not stats.game_active:
        # Reset pengaturan permainan.
        ai_settings.initialize_dynamic_settings()

        # Sembunyikan kursor mouse.
        pygame.mouse.set_visible(False)

        # Reset statistik permainan.
        stats.reset_stats()
        stats.game_active = True

        # Reset gambar papan skor.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Kosongkan daftar alien dan peluru.
        aliens.empty()
        bullets.empty()

        # Buat armada alien baru dan pusatkan kapal.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

# Fungsi untuk menembakkan peluru.
def fire_bullet(ai_settings, screen, ship, bullets):
    """
    Menembakkan peluru jika batas belum tercapai.
    """
    # Periksa apakah jumlah peluru yang ada kurang dari batas.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)  
        bullets.add(new_bullet)  
        se.bullet_sound.play()  

# Fungsi untuk memperbarui tampilan layar.
def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """
    Memperbarui gambar di layar dan mengganti ke layar baru.
    """
    # Gambar ulang latar belakang.
    screen.blit(ai_settings.background_image, [0, 0])

    # Gambar ulang semua peluru di belakang kapal dan alien.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()  
    aliens.draw(screen)  

    # Gambar informasi skor.
    sb.show_score()

    # Gambar tombol Play jika permainan tidak aktif.
    if not stats.game_active:
        play_button.draw_button()

    # Buat layar terbaru terlihat.
    pygame.display.flip()


# Fungsi untuk memperbarui posisi peluru dan menghapus peluru yang sudah tidak terlihat.
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Memperbarui posisi peluru dan menghapus peluru lama.
    """
    # Perbarui posisi setiap peluru.
    bullets.update()

    # Hapus peluru yang keluar dari layar.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    # Periksa tabrakan peluru dengan alien.
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

# Fungsi untuk memeriksa dan memperbarui skor tertinggi.
def check_high_score(stats, sb):
    """
    Periksa apakah ada skor tertinggi baru.
    """
    if stats.score > stats.high_score:
        stats.high_score = stats.score  
        sb.prep_high_score() 

# Fungsi untuk menangani tabrakan antara peluru dan alien.
def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Menangani tabrakan antara peluru dan alien.
    """
    # Periksa tabrakan antara peluru dan alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        se.explosion_sound.play()  # Mainkan efek suara ledakan.
        for aliens in collisions.values():
            # Tambahkan skor berdasarkan jumlah alien yang hancur.
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()  
        check_high_score(stats, sb)  

    # Jika semua alien telah dihancurkan, tingkatkan level permainan.
    if len(aliens) == 0:
        bullets.empty()  # Hapus semua peluru yang tersisa.
        ai_settings.increase_speed()  # Tingkatkan kecepatan permainan.

        # Tingkatkan level.
        stats.level += 1
        sb.prep_level()  # Perbarui tampilan level.

        # Buat armada alien baru.
        create_fleet(ai_settings, screen, ship, aliens)

# Fungsi untuk memeriksa apakah ada alien yang mencapai tepi layar.
def check_fleet_edges(ai_settings, aliens):
    """
    Menanggapi jika ada alien yang mencapai tepi layar.
    """
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)  # Ubah arah armada alien.
            break

# Fungsi untuk mengubah arah armada alien.
def change_fleet_direction(ai_settings, aliens):
    """
    Menurunkan posisi armada dan mengubah arah gerakan mereka.
    """
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed  # Turunkan posisi alien.
    ai_settings.fleet_direction *= -1  # Balik arah gerakan armada.


# Fungsi untuk menangani ketika kapal terkena alien.
def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Menanggapi situasi ketika kapal terkena oleh alien.
    """
    if stats.ships_left > 0:
        # Kurangi jumlah kapal yang tersisa.
        stats.ships_left -= 1

        # Perbarui tampilan jumlah kapal di papan skor.
        sb.prep_ships()
    else:
        # Jika tidak ada kapal tersisa, hentikan permainan.
        stats.game_active = False
        pygame.mouse.set_visible(True)  # Tampilkan kursor mouse.

    # Kosongkan daftar alien dan peluru.
    aliens.empty()
    bullets.empty()

    # Buat armada alien baru dan pusatkan kapal.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # Beri jeda sementara sebelum melanjutkan permainan.
    sleep(0.5)

# Fungsi untuk memeriksa apakah ada alien yang mencapai bagian bawah layar.
def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Periksa apakah ada alien yang mencapai dasar layar.
    Jika iya, perlakukan ini seperti kapal yang terkena.
    """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Perlakukan ini sama seperti kapal yang terkena.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

# Fungsi untuk memperbarui posisi alien dan memeriksa tabrakan.
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """
    Perbarui posisi semua alien dan periksa tabrakan atau kejadian tertentu.
    """
    # Periksa apakah armada alien telah mencapai tepi layar.
    check_fleet_edges(ai_settings, aliens)
    aliens.update()  # Perbarui posisi semua alien.

    # Periksa tabrakan antara kapal dan alien.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Periksa apakah ada alien yang mencapai bagian bawah layar.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)



def get_number_aliens_x(ai_settings, alien_width):
    """
    Menentukan jumlah alien yang dapat muat dalam satu baris.
    """
    # Menghitung ruang horizontal yang tersedia untuk alien.
    available_space_x = ai_settings.screen_width - 2 * alien_width
    # Menghitung jumlah alien yang muat dalam ruang tersebut.
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """
    Menentukan jumlah baris alien yang dapat muat pada layar.
    """
    # Menghitung ruang vertikal yang tersedia untuk alien.
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    # Menghitung jumlah baris alien yang muat dalam ruang tersebut.
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """
    Membuat alien dan menempatkannya di posisi yang tepat dalam baris.
    """
    # Membuat objek alien baru.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width  # Mendapatkan lebar alien.
    
    # Menentukan posisi horizontal alien dalam baris.
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    
    # Menentukan posisi vertikal alien dalam baris.
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    
    # Menambahkan alien ke grup aliens.
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """
    Membuat armada alien lengkap (baris dan kolom alien).
    """
    # Membuat alien pertama untuk menghitung berapa banyak alien yang bisa muat dalam satu baris dan satu kolom.
    alien = Alien(ai_settings, screen)
    
    # Menentukan jumlah alien yang muat dalam satu baris.
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    
    # Menentukan jumlah baris alien.
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Membuat armada alien (baris dan kolom).
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


