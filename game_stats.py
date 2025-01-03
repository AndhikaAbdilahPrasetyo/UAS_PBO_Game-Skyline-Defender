class GameStats:
    """
    Kelas untuk melacak statistik permainan.
    """

    def __init__(self, ai_settings):
        """
        Menginisialisasi statistik permainan.
        """
        self.ai_settings = ai_settings
        self.reset_stats()

        # Memulai permainan dalam keadaan tidak aktif.
        self.game_active = False

        # Skor tertinggi tidak boleh di-reset.
        self.high_score = 0

    def reset_stats(self):
        """
        Mengatur ulang statistik yang dapat berubah selama permainan berlangsung.
        """
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
