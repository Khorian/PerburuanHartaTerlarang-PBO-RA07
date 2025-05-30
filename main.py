import pygame  # Mengimpor modul pygame untuk membuat game
import random  # Mengimpor modul random untuk menghasilkan angka acak
import sys  # Mengimpor modul sys untuk mengakses fungsi sistem
from abc import ABC, abstractmethod

pygame.init()  # Menginisialisasi semua modul pygame
try:
    pygame.mixer.init()  # Menginisialisasi mixer untuk suara
except Exception as e:
    print(f"Error initializing pygame: {e}")  # Menangkap dan mencetak error jika inisialisasi gagal
    sys.exit()  # Keluar dari program jika terjadi error

# Memuat efek suara
SOUND_JUMP = pygame.mixer.Sound("assets/music/sound_effect/lompat.mp3")  # Suara untuk lompatan
SOUND_FIRE = pygame.mixer.Sound("assets/music/sound_effect/tembakan.mp3")  # Suara untuk tembakan
SOUND_START = pygame.mixer.Sound("assets/music/sound_effect/mulai.mp3")  # Suara untuk memulai
SOUND_WIN = pygame.mixer.Sound("assets/music/sound_effect/menang.mp3")  # Suara untuk menang

# Dimensi layar dan warna
WIDTH, HEIGHT = 800, 400  # Lebar dan tinggi layar
WHITE = (255, 255, 255)  # Warna putih
BLACK = (0, 0, 0)  # Warna hitam
RED = (255, 0, 0)  # Warna merah
GOLD = (255, 215, 0)  # Warna emas
FPS = 60  # Frame per detik

# Fungsi untuk memuat gambar
def load_img(path, size):
    return pygame.transform.scale(pygame.image.load(path), size)  # Memuat gambar dan mengubah ukurannya

# Memuat gambar latar menu dan cerita
menu_backgrounds = [load_img(f"assets/background/menu/menu{i}.png", (WIDTH, HEIGHT)) for i in range(1, 7)]  # Memuat gambar latar menu

# Memuat gambar tombol
buttons = {
    'start': load_img("assets/button/start.png", (200, 80)),  # Tombol mulai
    'story': load_img("assets/button/story.png", (200, 80)),  # Tombol cerita
    'exit': load_img("assets/button/exit.png", (200, 80)),  # Tombol keluar
    'back': load_img("assets/button/back_to_menu.png", (200, 60)),  # Tombol kembali
    'next': load_img("assets/button/next_story.png", (200, 60)),  # Tombol lanjut
    'home': load_img("assets/button/home.png", (150, 60)),  # Tombol beranda
    'play_again': load_img("assets/button/play_again.png", (200, 80)),  # Tombol main lagi
    'restart': load_img("assets/button/restart.png", (150, 60)),  # Tombol restart
}

# Memuat gambar cerita
stories = [load_img(f"assets/background/story/story{i}.png", (WIDTH, HEIGHT)) for i in range(1, 6)]  # Memuat gambar cerita

# Memuat gambar gameplay
diam_img = pygame.transform.scale(pygame.image.load("assets/characters/player/diam.png"), (80, 80))  # Gambar diam pemain
jalan1_img = pygame.transform.scale(pygame.image.load("assets/characters/player/jalan1.png"), (100, 100))  # Gambar jalan 1
jalan2_img = pygame.transform.scale(pygame.image.load("assets/characters/player/jalan2.png"), (100, 100))  # Gambar jalan 2
lompat_img = pygame.transform.scale(pygame.image.load("assets/characters/player/lompat.png"), (100, 100))  # Gambar lompat
dragon_open_img = pygame.transform.scale(pygame.image.load("assets/characters/dragon/open.png"), (120, 100))  # Gambar naga terbuka
dragon_close_img = pygame.transform.scale(pygame.image.load("assets/characters/dragon/close.png"), (120, 100))  # Gambar naga tertutup
fire_img = pygame.transform.scale(pygame.image.load("assets/characters/fire.png"), (50, 30))  # Gambar api
treasure_img = pygame.transform.scale(pygame.image.load("assets/characters/treasure.png"), (100, 100))  # Gambar harta
background_img_level_1 = pygame.transform.scale(pygame.image.load("assets/background/level/background_level_1.png"), (800, HEIGHT))  # Gambar latar level 1
background_img_level_2 = pygame.transform.scale(pygame.image.load("assets/background/level/background_level_2.png"), (800, HEIGHT))  # Gambar latar level 2
background_img_level_3 = pygame.transform.scale(pygame.image.load("assets/background/level/background_level_3.png"), (800, HEIGHT))  # Gambar latar level 3
background_img_ending = pygame.transform.scale(pygame.image.load("assets/background/level/background_ending.png"), (800, HEIGHT))  # Gambar latar akhir
papan_ending = pygame.transform.scale(pygame.image.load("assets/background/papan_ending.png"), (600, 400))  # Gambar papan akhir
door_img = pygame.transform.scale(pygame.image.load("assets/characters/door.png"), (120, 120))  # Gambar pintu

# Memetakan level ke gambar latar
background_images = {
    1: background_img_level_1,
    2: background_img_level_2,
    3: background_img_level_3,
    4: background_img_ending,
}

class MovingBackground:
    def __init__(self):
        self._image = background_img_level_1  # Mengatur gambar latar awal
        self.width = self._image.get_width()  # Mendapatkan lebar gambar
        self.offset = 0  # Mengatur offset untuk pergerakan latar

    @property
    def image(self):
        return self._image  # Mengembalikan gambar latar

    @image.setter
    def image(self, img):
        self._image = img  # Mengatur gambar latar baru
        self.width = self._image.get_width()  # Memperbarui lebar gambar

    def update(self, shift):
        self.offset += shift  # Menggeser offset
        if self.offset > self.width:  # Jika offset lebih besar dari lebar gambar
            self.offset -= self.width  # Kembali ke awal
        elif self.offset < -self.width:  # Jika offset lebih kecil dari negatif lebar gambar
            self.offset += self.width  # Kembali ke akhir

    @abstractmethod
    def draw(self, screen):
        # Menggambar gambar latar pada posisi offset dan di kedua sisi untuk efek bergulir
        screen.blit(self._image, (self.offset, 0))
        screen.blit(self._image, (self.offset - self.width, 0))
        screen.blit(self._image, (self.offset + self.width, 0))

class GameObject:
    """Kelas dasar untuk semua objek game"""
    def __init__(self, image, x, y):
        self.image = image  # Mengatur gambar objek
        self.rect = self.image.get_rect()  # Mendapatkan kotak pembatas gambar
        self.rect.x = x  # Mengatur posisi x objek
        self.rect.y = y  # Mengatur posisi y objek
    
    def draw(self, screen):
        """Method untuk menggambar objek ke layar"""
        screen.blit(self.image, self.rect)  # Menggambar objek menggunakan posisi rect
    
    def shift_position(self, shift):
        """Method untuk menggeser posisi objek secara horizontal"""
        self.rect.x += shift  # Menambahkan nilai geser ke posisi x objek

class Character(GameObject):
    """Kelas dasar untuk karakter dalam game"""
    def __init__(self, image, x, y):
        super().__init__(image, x, y)  # Memanggil konstruktor superclass
        self._active = True  # Status aktif karakter
    
    @property
    def active(self):
        return self._active  # Mendapatkan status aktif
    
    @active.setter
    def active(self, value):
        self._active = value  # Mengatur status aktif
    
    def update(self):
        """Method untuk mengupdate logika karakter"""
        pass  # Akan diimplementasikan pada subclass

class Player(Character):
    def __init__(self):
        super().__init__(diam_img, 300, HEIGHT - diam_img.get_rect().height - 30)  # Posisi awal pemain
        self._speed = 5  # Kecepatan horizontal pemain
        self._jump = False  # Status pemain melompat
        self._jump_speed = 10  # Kecepatan lompatan awal
        self._velocity_y = 0  # Kecepatan vertikal saat melompat
        self._gravity = 0.4  # Gaya gravitasi yang menarik ke bawah
        self.direction = 0  # Arah pergeseran latar belakang saat pemain bergerak
        self.walking_frame = 0  # Frame animasi untuk pergerakan berjalan
        self.walking_images = [jalan1_img, jalan2_img]  # Gambar animasi jalan
        self.standing_image = diam_img  # Gambar saat berdiri
        self.jumping_image = lompat_img  # Gambar saat melompat

    @property
    def speed(self):
        return self._speed  # Mendapatkan kecepatan pemain

    @speed.setter
    def speed(self, value):
        self._speed = value  # Mengatur kecepatan pemain

    @property
    def jump(self):
        return self._jump  # Mendapatkan status lompatan

    @jump.setter
    def jump(self, value):
        self._jump = value  # Mengatur status lompatan

    @property
    def velocity_y(self):
        return self._velocity_y  # Mendapatkan kecepatan vertikal

    @velocity_y.setter
    def velocity_y(self, value):
        self._velocity_y = value  # Mengatur kecepatan vertikal

    def move(self, keys):
        self.direction = 0  # Reset arah pergeseran latar belakang
        if keys[pygame.K_RIGHT]:  # Jika tombol panah kanan ditekan
            self.direction = -self.speed  # Gerak ke kiri background (seolah pemain ke kanan)
            self.walking_frame += 1  # Update frame animasi berjalan
            self.image = self.walking_images[(self.walking_frame // 10) % 2]  # Ganti gambar berjalan
        elif keys[pygame.K_LEFT]:  # Jika tombol panah kiri ditekan
            self.direction = self.speed  # Gerak ke kanan background (seolah pemain ke kiri)
            self.walking_frame += 1  # Update frame animasi berjalan
            self.image = self.walking_images[(self.walking_frame // 10) % 2]  # Ganti gambar berjalan
        else:
            if not self.jump:  # Jika tidak sedang melompat
                self.image = self.standing_image  # Set gambar berdiri
            self.walking_frame = 0  # Reset frame animasi berjalan

        if keys[pygame.K_SPACE] and not self.jump:  # Jika tombol spasi ditekan dan tidak sedang melompat
            self.jump = True  # Mulai lompatan
            self.velocity_y = -self._jump_speed  # Set kecepatan lompatan ke atas
            SOUND_JUMP.play()  # Mainkan suara lompat
            self.image = self.jumping_image  # Set gambar lompat

    def apply_gravity(self):
        if self.jump:  # Jika sedang melompat
            self.rect.y += self.velocity_y  # Geser posisi vertikal pemain
            self.velocity_y += self._gravity  # Tambah kecepatan vertikal karena gravitasi
            if self.rect.y >= HEIGHT - self.rect.height - 30:  # Jika pemain menyentuh lantai
                self.rect.y = HEIGHT - self.rect.height - 30  # Set posisi tepat di lantai
                self.jump = False  # Reset status lompat
                self.image = self.standing_image  # Set gambar berdiri kembali
    
    def update(self):
        self.apply_gravity()  # Terapkan efek gravitasi

class Dragon(Character):
    def __init__(self):
        super().__init__(dragon_close_img, 1000, HEIGHT - dragon_close_img.get_rect().height - 30)  # Posisi awal naga
        self._fires = []  # Daftar api yang dilempar
        self._fire_timer = 0  # Timer interval api
        self._fire_interval = 2000  # Interval default api
        self.burst_pattern = [1]  # Pola burst api (berapa kali tembakan per interval)
        self.burst_index = 0  # Indeks untuk pola burst
        self._open_start_time = 0  # Waktu mulai membuka mulut
        self._open_duration = 200  # Lama waktu mulut terbuka
        self.open_image = dragon_open_img  # Gambar mulut terbuka
        self.close_image = dragon_close_img  # Gambar mulut tertutup

    @property
    def fires(self):
        return self._fires  # Mendapatkan daftar api

    @fires.setter
    def fires(self, value):
        self._fires = value  # Mengatur daftar api

    def adjust_fire_parameters(self, level):
        # Menyesuaikan interval dan pola api berdasarkan level
        self._fire_interval = max(800, 4000 - (level * 700))  # Penurunan interval per level tapi minimal 800
        if level == 1:
            self._fire_interval = 1500
            self.burst_pattern = [1,1]  # 1 tembakan per burst
        elif level == 2:
            self._fire_interval = 1200
            self.burst_pattern = [1,1,1]  # 2 burst dengan 1 tembakan masing-masing
        elif level == 3:
            self._fire_interval = 900
            self.burst_pattern = [1,1,1,1]  # 3 burst dengan 1 tembakan masing-masing
        else:
            self._fire_interval = 1500
            self.burst_pattern = [1,1]  # Default burst
        self.burst_index = 0  # Reset burst index

    def update_fire(self, current_time, level):
        # Mengecek apakah sudah waktunya untuk melempar api baru
        if current_time - self._fire_timer > self._fire_interval:
            burst_count = self.burst_pattern[self.burst_index]  # Ambil jumlah api untuk burst sekarang
            for i in range(burst_count):
                fire_rect = fire_img.get_rect()  # Buat rect api baru
                fire_rect.x = self.rect.x  # Posisi x api dari posisi naga
                fire_rect.y = self.rect.y + 20 + i * 15  # Posisi y bergeser per burst
                self._fires.append(fire_rect)  # Tambah api baru ke daftar
            self.burst_index = (self.burst_index + 1) % len(self.burst_pattern)  # Update indeks burst selanjutnya
            self._fire_timer = current_time  # Update timer api
            SOUND_FIRE.play()  # Mainkan suara api
            self._open_start_time = current_time  # Set waktu mulai mulut terbuka

        for fire in self._fires:  # Geser semua api ke kiri (bergerak)
            fire.x -= 7

        self._fires = [fire for fire in self._fires if fire.x > -50]  # Hapus api yang sudah keluar layar

    def check_collision(self, player_rect):
        # Cek apakah ada api yang mengenai pemain
        return any(fire.colliderect(player_rect) for fire in self._fires)

    def draw(self, screen):
        current_time = pygame.time.get_ticks()  # Dapatkan waktu sekarang
        if current_time - self._open_start_time < self._open_duration:  # Jika mulut sedang terbuka
            self.image = self.open_image  # Set gambar terbuka
        else:
            self.image = self.close_image  # Gambar tertutup
        super().draw(screen)  # Panggil fungsi menggambar superclass (gambar naga)
        for fire in self._fires:  # Gambar semua api
            screen.blit(fire_img, fire)

    def shift_position(self, shift):
        super().shift_position(shift)  # Geser posisi naga
        for fire in self._fires:  # Geser semua api agar mengikuti perpindahan naga
            fire.x += shift

class Collectible(GameObject):
    """Kelas dasar untuk objek yang bisa dikumpulkan"""
    def __init__(self, image, x, y):
        super().__init__(image, x, y)  # Memanggil konstruktor superclass
        self._spawned = False  # Status muncul
    
    @property
    def spawned(self):
        return self._spawned  # Mendapatkan status muncul
    
    @spawned.setter
    def spawned(self, value):
        self._spawned = value  # Mengatur status muncul
    
    def check_interaction(self, player_rect):
        # Cek apakah muncul dan mengenai pemain
        return self._spawned and self.rect.colliderect(player_rect)

class Treasure(Collectible):
    def __init__(self):
        super().__init__(treasure_img, 1400, HEIGHT - 70)  # Posisi awal harta
        self._collected_already = False  # Status apakah sudah dikumpulkan
    
    def check_collected(self, player_rect):
        collected = super().check_interaction(player_rect)  # Cek interaksi dengan pemain
        if collected and not self._collected_already:  # Jika baru dikoleksi
            SOUND_WIN.play()  # Mainkan suara menang
            self._collected_already = True  # Tandai sudah dikoleksi
            return True
        return False
    
    @property
    def spawned(self):
        return super().spawned
    
    @spawned.setter
    def spawned(self, value):
        self._spawned = value  # Set status muncul
        if not value:
            self._collected_already = False  # Reset status koleksi jika tidak muncul

class Door(Collectible):
    def __init__(self):
        super().__init__(door_img, 2000, HEIGHT - 150)  # Posisi pintu
    
    def check_entered(self, player_rect):
        return super().check_interaction(player_rect)  # Cek interaksi dengan pemain

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Membuat jendela game
        pygame.display.set_caption("Perburuan Harta Terlarang")  # Judul jendela
        self.clock = pygame.time.Clock()  # Membuat clock untuk mengatur FPS
        self.font = pygame.font.SysFont(None, 36)  # Mengatur font untuk teks
        SOUND_START.play()  # Mainkan suara mulai game
        self.menu_state = "main"  # Status menu saat ini
        self.story_index = 0  # Indeks cerita
        self.menu_bg_index = 0  # Indeks latar menu
        self.last_bg_switch = pygame.time.get_ticks()  # Waktu terakhir ganti latar

        pygame.mixer.music.load("assets/music/backsounds/backsound_menu.mp3")  # Muat musik menu
        pygame.mixer.music.set_volume(1.0)  # Set volume musik
        pygame.mixer.music.play(-1)  # Putar musik berulang

        self._player = None  # Objek pemain
        self._dragon = None  # Objek naga
        self._treasure = None  # Objek harta
        self._door = None  # Objek pintu
        self._background = None  # Objek latar
        self._level = 1  # Level permainan
        self._score = 0  # Skor pemain
        self._game_over = False  # Status game over
        self._game_won = False  # Status game menang
        self._level_start_time = 0  # Waktu mulai level
        self._dragon_visible = True  # Apakah naga terlihat
        self._show_end_buttons = False  # Apakah tombol akhir muncul
        self._hit_by_fire = False  # Status terkena api
        self._show_fire_buttons = False  # Apakah tombol saat terkena api muncul
        self._sound_volume = 1.0  # Volume suara
        self._papan_ending_visible = False  # Status papan akhir terlihat
        self.update_sound_volume()  # Update volume suara

    def update_sound_volume(self):
        # Mengatur volume untuk semua efek suara
        SOUND_JUMP.set_volume(self._sound_volume)
        SOUND_FIRE.set_volume(self._sound_volume)
        SOUND_START.set_volume(self._sound_volume)
        SOUND_WIN.set_volume(self._sound_volume)

    def draw_volume_control(self):
        pygame.draw.rect(self.screen, BLACK, (WIDTH - 210, 10, 200, 20))  # Gambar latar bar volume
        pygame.draw.rect(self.screen, RED, (WIDTH - 210, 10, self._sound_volume * 200, 20))  # Gambar bar volume sesuai level
        volume_text = self.font.render(f"Volume: {int(self._sound_volume * 100)}%", True, BLACK)  # Teks volume
        self.screen.blit(volume_text, (WIDTH - 210, 40))  # Gambar teks volume

    def adjust_volume(self, mouse_pos):
        x, y = mouse_pos  # Posisi klik mouse
        if WIDTH - 210 <= x <= WIDTH - 10 and 10 <= y <= 30:  # Jika klik dalam area bar volume
            self.sound_volume = (x - (WIDTH - 210)) / 200  # Sesuaikan volume berdasarkan posisi klik

    @property
    def player(self):
        return self._player  # Mendapatkan objek pemain

    @player.setter
    def player(self, value):
        self._player = value  # Mengatur objek pemain

    @property
    def dragon(self):
        return self._dragon  # Mendapatkan objek naga

    @dragon.setter
    def dragon(self, value):
        self._dragon = value  # Mengatur objek naga

    @property
    def treasure(self):
        return self._treasure  # Mendapatkan objek harta

    @treasure.setter
    def treasure(self, value):
        self._treasure = value  # Mengatur objek harta

    @property
    def door(self):
        return self._door  # Mendapatkan objek pintu

    @door.setter
    def door(self, value):
        self._door = value  # Mengatur objek pintu

    @property
    def background(self):
        return self._background  # Mendapatkan objek latar

    @background.setter
    def background(self, value):
        self._background = value  # Mengatur objek latar

    @property
    def level(self):
        return self._level  # Mendapatkan level

    @level.setter
    def level(self, value):
        self._level = value  # Mengatur level

    @property
    def score(self):
        return self._score  # Mendapatkan skor

    @score.setter
    def score(self, value):
        self._score = value  # Mengatur skor

    @property
    def game_over(self):
        return self._game_over  # Mendapatkan status game over

    @game_over.setter
    def game_over(self, value):
        self._game_over = value  # Mengatur status game over

    @property
    def game_won(self):
        return self._game_won  # Mendapatkan status game menang

    @game_won.setter
    def game_won(self, value):
        self._game_won = value  # Mengatur status game menang

    @property
    def dragon_visible(self):
        return self._dragon_visible  # Mendapatkan status naga terlihat

    @dragon_visible.setter
    def dragon_visible(self, value):
        self._dragon_visible = value  # Mengatur status naga terlihat

    @property
    def show_end_buttons(self):
        return self._show_end_buttons  # Mendapatkan status tombol akhir terlihat

    @show_end_buttons.setter
    def show_end_buttons(self, value):
        self._show_end_buttons = value  # Mengatur status tombol akhir terlihat

    @property
    def hit_by_fire(self):
        return self._hit_by_fire  # Mendapatkan status terkena api

    @hit_by_fire.setter
    def hit_by_fire(self, value):
        self._hit_by_fire = value  # Mengatur status terkena api

    @property
    def show_fire_buttons(self):
        return self._show_fire_buttons  # Mendapatkan status tombol saat terkena api terlihat

    @show_fire_buttons.setter
    def show_fire_buttons(self, value):
        self._show_fire_buttons = value  # Mengatur status tombol api terlihat

    @property
    def level_start_time(self):
        return self._level_start_time  # Mendapatkan waktu mulai level

    @level_start_time.setter
    def level_start_time(self, value):
        self._level_start_time = value  # Mengatur waktu mulai level

    @property
    def sound_volume(self):
        return self._sound_volume  # Mendapatkan level volume suara

    @sound_volume.setter
    def sound_volume(self, value):
        self._sound_volume = max(0.0, min(value, 1.0))  # Membatasi nilai volume antara 0 dan 1
        self.update_sound_volume()  # Update volume efek suara

    @property
    def papan_ending_visible(self):
        return self._papan_ending_visible  # Mendapatkan status papan akhir terlihat

    @papan_ending_visible.setter
    def papan_ending_visible(self, value):
        self._papan_ending_visible = value  # Mengatur status papan akhir terlihat

    def reset_level(self):
        if self.level < 4:  # Untuk level 1-3
            self.player = Player()  # Buat objek pemain baru
            self.dragon = Dragon()  # Buat objek naga baru
            self.treasure = None  # Harta tidak muncul
            self.door = Door()  # Buat objek pintu baru
        else:  # Level 4 (ending)
            self.player = Player()  # Buat objek pemain baru
            self.dragon = Dragon()  # Buat objek naga baru
            self.treasure = Treasure()  # Buat objek harta baru
            # Atur posisi harta
            self.treasure.rect.x = background_images[4].get_width() - self.treasure.rect.width - 30
            self.treasure.rect.y = HEIGHT - self.treasure.rect.height - 30
            self.treasure.spawned = True  # Tandai harta muncul
            self.treasure._collected_already = False  # Reset status koleksi
            self.door = None  # Tidak ada pintu
        
        self.background = MovingBackground()  # Buat latar bergerak baru
        self.background.image = background_images.get(self.level, background_img_level_1)  # Set gambar latar sesuai level
        self.score = 0  # Reset skor
        self.game_over = False  # Reset status game over
        self.game_won = False  # Reset status menang
        self.level_start_time = pygame.time.get_ticks()  # Simpan waktu mulai level
        self.dragon_visible = True if self.level < 4 else False  # Tampilkan naga hanya untuk level < 4
        self.show_end_buttons = False  # Sembunyikan tombol akhir
        self.hit_by_fire = False  # Reset status terkena api
        self.show_fire_buttons = False  # Sembunyikan tombol api
        self.papan_ending_visible = False  # Sembunyikan papan akhir

    def reset_game(self):
        self.level = 1  # Set level ke awal
        self.score = 0  # Reset skor
        self.game_over = False  # Reset status game over
        self.game_won = False  # Reset status menang
        self.hit_by_fire = False  # Reset status kena api
        self.show_fire_buttons = False  # Sembunyikan tombol api
        self.reset_level()  # Reset level

    def go_home(self):
        pygame.mixer.music.stop()  # Hentikan musik
        pygame.mixer.music.load("assets/music/backsounds/backsound_menu.mp3")  # Muat musik menu
        pygame.mixer.music.set_volume(1.0)  # Set volume music menu
        pygame.mixer.music.play(-1)  # Putar musik menu berulang
        self.menu_state = "main"  # Set status menu ke utama

    def draw_transition(self):
        for i in range(0, WIDTH // 2 + 1, 20):
            self.screen.fill(BLACK)  # Bersihkan layar dengan warna hitam
            pygame.draw.rect(self.screen, BLACK, (0, 0, i, HEIGHT))  # Menggambar efek transisi kiri
            pygame.draw.rect(self.screen, BLACK, (WIDTH - i, 0, i, HEIGHT))  # Menggambar efek transisi kanan
            pygame.display.update()  # Perbarui layar
            pygame.time.delay(10)  # Tunda sebentar untuk efek transisi

    def run_game(self):
        self.reset_level()  # Mulai ulang level

        # Batas skor per level
        score_limits = {
            1: 2000,
            2: 2500,
            3: 3000,
        }

        while True:
            self.clock.tick(FPS)  # Batasi kecepatan frame
            current_time = pygame.time.get_ticks()  # Waktu sekarang
            elapsed_time = (current_time - self.level_start_time) / 1000  # Hitung waktu berlalu dalam detik

            for event in pygame.event.get():  # Loop event pygame
                if event.type == pygame.QUIT:  # Jika window ditutup
                    pygame.quit()  # Keluar pygame
                    sys.exit()  # Keluar program
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Jika klik mouse
                    x, y = event.pos  # Posisi klik
                    if self.show_fire_buttons:  # Jika tombol api muncul
                        home_rect = pygame.Rect(10, HEIGHT - 80, 150, 60)  # Area tombol home
                        restart_rect = pygame.Rect(WIDTH - 160, HEIGHT - 80, 150, 60)  # Area tombol restart
                        if home_rect.collidepoint(x, y):  # Klik tombol home
                            self.go_home()  # Kembali ke menu utama
                            return
                        elif restart_rect.collidepoint(x, y):  # Klik tombol restart
                            self.reset_level()  # Mulai ulang level
                            continue
                    elif self.show_end_buttons:  # Jika tombol akhir muncul
                        home_rect = pygame.Rect(10, HEIGHT - 80, 150, 60)  # Area tombol home
                        restart_rect = pygame.Rect(WIDTH - 160, HEIGHT - 80, 150, 60)  # Area tombol restart
                        if home_rect.collidepoint(x, y):  # Klik tombol home
                            self.go_home()  # Kembali ke menu utama
                            return
                        elif restart_rect.collidepoint(x, y):  # Klik tombol restart
                            self.reset_game()  # Mulai ulang game
                            continue
                elif event.type == pygame.KEYDOWN:  # Jika tombol keyboard ditekan
                    if event.key == pygame.K_r:  # Tombol R
                        if self.hit_by_fire or self.game_over:  # Jika terkena api atau game over
                            self.reset_level()  # Mulai ulang level

            keys = pygame.key.get_pressed()  # Ambil input keyboard saat ini

            if self.level < 4:  # Level sebelum ending
                if not self.game_over and not self.game_won and not self.hit_by_fire:  # Jika game sedang berjalan normal
                    # Hitung skor sementara, hanya naik jika belum mencapai batas batasSkor
                    tentative_score = int(elapsed_time * 100)
                    max_score = score_limits.get(self.level, 2000)
                    if tentative_score > max_score:
                        self.score = max_score
                    else:
                        self.score = tentative_score

                    # Jika skor sudah mencapai batas level, tampilkan pintu dan sembunyikan naga
                    if self.score >= max_score:
                        self.dragon_visible = False  # Sembunyikan naga
                        self.door.spawned = True  # Tampilkan pintu

                self.dragon.adjust_fire_parameters(self.level)  # Update parameter api sesuai level

                if self.door.check_entered(self.player.rect) and self.door.spawned and not self.hit_by_fire:
                    # Jika pemain masuk ke pintu dan tidak terkena api
                    if self.level < 3:
                        self.level += 1  # Naik level
                        self.background.image = background_images[self.level]  # Update gambar latar
                        self.reset_level()  # Reset level baru
                        self.draw_transition()  # Tampilkan transisi
                        continue
                    else:
                        self.level = 4  # Menuju level akhir
                        self.reset_level()
                        self.game_won = False
                        self.show_end_buttons = False
                        continue

                if not self.show_end_buttons and not self.show_fire_buttons:
                    self.player.move(keys)  # Gerakkan pemain

                    shift = self.player.direction  # Ambil pergeseran latar
                    self.background.update(shift)  # Geser latar
                    self.dragon.shift_position(shift)  # Geser naga
                    if self.treasure:
                        self.treasure.shift_position(shift)  # Geser harta jika ada
                    self.door.shift_position(shift)  # Geser pintu

                    if not self.game_over and not self.game_won:
                        self.player.update()  # Update status pemain

                        if self.dragon_visible:
                            distance = self.dragon.rect.x - self.player.rect.x  # Hitung jarak naga ke pemain
                            if 0 < distance < 300:
                                self.dragon.rect.x += 4  # Naga maju mendekati pemain
                            self.dragon.update_fire(current_time, self.level)  # Update api naga

                            if self.dragon.check_collision(self.player.rect):
                                self.hit_by_fire = True  # Tandai terkena api
                                self.show_fire_buttons = True  # Tampilkan tombol saat terkena api

            else:  # Level 4, ending
                if not self.show_end_buttons and not self.show_fire_buttons:
                    self.player.move(keys)  # Gerak pemain
                    self.player.rect.x -= self.player.direction  # Geser posisi pemain (koreksi arah)

                self.player.update()  # Update status pemain

                # Batasi posisi pemain agar tidak keluar layar
                if self.player.rect.left < 0:
                    self.player.rect.left = 0
                elif self.player.rect.right > WIDTH:
                    self.player.rect.right = WIDTH

                # Jika pemain mengumpulkan harta
                if self.treasure and self.treasure.check_collected(self.player.rect):
                    if not self.treasure._collected_already:
                        SOUND_WIN.play()  # Putar suara menang sekali
                        self.treasure._collected_already = True
                    self.game_won = True  # Tandai game menang
                    self.show_end_buttons = True  # Tampilkan tombol akhir
                    self.papan_ending_visible = True  # Tampilkan papan akhir

            # Gambar semua elemen di layar
            self.background.draw(self.screen)  # Gambar latar belakang
            if self.level < 4 and self.dragon_visible:
                self.dragon.draw(self.screen)  # Gambar naga jika perlu
            if self.player:
                self.player.draw(self.screen)  # Gambar pemain
            if self.treasure:
                self.treasure.draw(self.screen)  # Gambar harta jika ada
            if self.door and self.level < 4:
                self.door.draw(self.screen)  # Gambar pintu jika ada dan level < 4

            if self.level < 4:  # Tampilkan skor dan level untuk level non-akhir
                score_text = self.font.render(f"Score: {self.score}", True, BLACK)
                level_text = self.font.render(f"Level: {self.level}", True, BLACK)
                self.screen.blit(score_text, (10, 10))
                self.screen.blit(level_text, (10, 50))

            if self.hit_by_fire:  # Jika terkena api
                hit_text = self.font.render("Kamu Terkena Api!", True, RED)
                self.screen.blit(hit_text, (WIDTH // 2 - 120, HEIGHT // 2 - 50))  # Tampilkan pesan
                home_x = 10
                restart_x = WIDTH - 160
                button_y = HEIGHT - 80
                self.screen.blit(buttons['home'], (home_x, button_y))  # Tampilkan tombol home
                self.screen.blit(buttons['restart'], (restart_x, button_y))  # Tampilkan tombol restart

            elif self.show_end_buttons:  # Jika tombol akhir muncul
                if self.level == 4 and self.papan_ending_visible:
                    papan_x = (WIDTH - papan_ending.get_width()) // 2
                    papan_y = HEIGHT // 2 - papan_ending.get_height() // 2
                    self.screen.blit(papan_ending, (papan_x, papan_y))  # Tampilkan papan akhir

                home_x = 10
                restart_x = WIDTH - 160
                button_y = HEIGHT - 80
                self.screen.blit(buttons['home'], (home_x, button_y))  # Tampilkan tombol home
                self.screen.blit(buttons['restart'], (restart_x, button_y))  # Tampilkan tombol restart

            pygame.display.update()  # Perbarui layar

    def run(self):
        while True:
            self.clock.tick(FPS)  # Batasi frame rate
            current_time = pygame.time.get_ticks()  # Waktu sekarang

            for event in pygame.event.get():  # Loop event
                if event.type == pygame.QUIT:  # Jika window ditutup
                    pygame.quit()  # Keluar pygame
                    sys.exit()  # Keluar program
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Jika mouse diklik
                    x, y = event.pos  # Posisi klik
                    # Menu utama
                    if self.menu_state == "main":
                        if 200 <= x <= 400 and 180 <= y <= 260:  # Tombol mulai
                            self.menu_state = "game"  # Ganti status ke game
                            self.adjust_volume(event.pos)  # Sesuaikan volume
                            pygame.mixer.music.stop()  # Stop musik menu
                            pygame.mixer.music.load("assets/music/backsounds/backsound.mp3")  # Muat musik game
                            pygame.mixer.music.set_volume(1.0)  # Set volume musik
                            pygame.mixer.music.play(-1)  # Putar musik game berulang
                            self.reset_game()  # Reset game
                            self.run_game()  # Jalankan game
                        elif 420 <= x <= 620 and 180 <= y <= 260:  # Tombol cerita
                            self.menu_state = "story"  # Ganti status ke cerita
                            self.story_index = 0  # Reset indeks cerita
                        elif 300 <= x <= 500 and 280 <= y <= 360:  # Tombol keluar
                            pygame.quit()  # Keluar pygame
                            sys.exit()  # Keluar program
                    # Menu cerita
                    elif self.menu_state == "story":
                        if 20 <= x <= 220 and 320 <= y <= 380:  # Tombol kembali
                            self.menu_state = "main"  # Kembali ke menu utama
                        elif 580 <= x <= 780 and 320 <= y <= 380:  # Tombol next cerita
                            self.story_index = min(self.story_index + 1, len(stories) - 1)  # Next cerita

            self.screen.fill(WHITE)  # Bersihkan layar dengan putih
            if self.menu_state == "main":  # Jika di menu utama
                if current_time - self.last_bg_switch > 600:  # Jika waktunya ganti background
                    self.menu_bg_index = (self.menu_bg_index + 1) % len(menu_backgrounds)  # Ganti index gambar latar
                    self.last_bg_switch = current_time  # Reset timer pergantian
                self.screen.blit(menu_backgrounds[self.menu_bg_index], (0, 0))  # Gambar latar menu
                # Gambar tombol menu utama
                self.screen.blit(buttons['start'], (200, 180))
                self.screen.blit(buttons['story'], (420, 180))
                self.screen.blit(buttons['exit'], (300, 280))
            elif self.menu_state == "story":  # Jika di menu cerita
                self.screen.blit(stories[self.story_index], (0, 0))  # Gambar background cerita
                self.screen.blit(buttons['back'], (20, 320))  # Gambar tombol kembali
                if self.story_index < len(stories) - 1:  # Jika tidak story terakhir
                    self.screen.blit(buttons['next'], (580, 320))  # Gambar tombol next

            pygame.display.update()  # Perbarui layar setiap loop frame

if __name__ == "__main__":
    game = Game()  # Membuat game instance
    game.run()  # Menjalankan game


 