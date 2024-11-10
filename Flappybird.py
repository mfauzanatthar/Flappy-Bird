import pygame
import random

# Inisialisasi pygame
pygame.init()

# Ukuran layar
screen_width, screen_height = 400, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Memuat gambar burung untuk animasi sayap
bird_up_image = pygame.image.load("bird_up.png")  # Burung dengan sayap naik
bird_down_image = pygame.image.load("bird_down.png")  # Burung dengan sayap turun

# Memuat gambar latar belakang dan pipa
background_image = pygame.image.load("background.png")  # Latar belakang
pipe_top_image = pygame.image.load("pipe_top.png")  # Pipa atas (gambarnya harus terbalik)
pipe_bottom_image = pygame.image.load("pipe_bottom.png")  # Pipa bawah

# Stretch background untuk mengisi layar
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Ukuran pipa setelah distretch
pipe_width = pipe_top_image.get_width()  # Menggunakan lebar gambar pipa asli
pipe_height = 0

# Gap antar pipa
gap = 150


class Bird:
    def __init__(self):
        self.x = 50
        self.y = 300
        self.gravity = 0.5
        self.lift = -10
        self.velocity = 0
        self.image = bird_up_image  # Mulai dengan gambar sayap naik
        self.rect = self.image.get_rect()  # Menyimpan rect untuk posisi burung
        self.frame_count = 0  # Counter untuk animasi sayap
        self.flap_rate = 10  # Setiap 10 frame, burung akan mengganti posisi sayap

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        self.rect.y = self.y  # Memperbarui posisi burung berdasarkan perhitungan gravitasi

        if self.y > screen_height - 50:  # Jatuh ke tanah
            self.y = screen_height - 50
            self.velocity = 0

        # Ganti gambar burung setiap beberapa frame untuk animasi sayap
        self.frame_count += 1
        if self.frame_count >= self.flap_rate:
            self.frame_count = 0  # Reset hitungan frame
            if self.image == bird_up_image:
                self.image = bird_down_image  # Ganti ke gambar sayap turun
            else:
                self.image = bird_up_image  # Ganti ke gambar sayap naik

    def flap(self):
        self.velocity += self.lift

    def get_rect(self):
        return self.rect  # Kembalikan rect dari gambar burung


class Pipe:
    def __init__(self):
        # Set tinggi pipa atas acak, dengan batasan agar pipa bawah tidak melampaui layar
        self.height = random.randint(100, screen_height - gap - pipe_height)
        self.x = screen_width
        self.width = pipe_width  # Lebar pipa
        self.speed = 5
        self.passed = False

        # Mengatur posisi pipa bawah agar tidak tumpang tindih dan tidak keluar dari layar
        self.bottom_height = screen_height - (self.height + gap)  # Pipa bawah berada di bawah gap

    def update(self):
        self.x -= self.speed
        if self.x < -self.width:  # Pipa keluar dari layar
            self.x = screen_width  # Pipa kembali muncul dari kanan
            self.height = random.randint(100, screen_height - gap - pipe_height)  # Set tinggi pipa atas acak
            self.bottom_height = screen_height - (self.height + gap)  # Update posisi pipa bawah
            self.passed = False

    def get_rects(self):
        # Pipa atas dan bawah dengan memastikan tidak melebihi layar
        top_rect = pygame.Rect(self.x, 0, self.width, self.height)  # Pipa atas
        bottom_rect = pygame.Rect(self.x, self.height + gap, self.width, self.bottom_height)  # Pipa bawah
        return top_rect, bottom_rect


# Fungsi untuk menggambar skor
def draw_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))


# Fungsi untuk game over
def game_over():
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("Game Over", True, RED)
    screen.blit(game_over_text, (100, 250))
    pygame.display.update()
    pygame.time.wait(2000)


# Fungsi untuk menampilkan menu utama
def show_menu():
    font = pygame.font.Font(None, 60)
    title_text = font.render("Flappy Bird", True, BLACK)
    start_text = pygame.font.Font(None, 40).render("Press ENTER to Start", True, GREEN)
    quit_text = pygame.font.Font(None, 40).render("Press ESC to Quit", True, GREEN)

    screen.fill(WHITE)
    screen.blit(title_text, (100, 100))
    screen.blit(start_text, (80, 250))
    screen.blit(quit_text, (80, 300))

    pygame.display.update()


# Fungsi untuk menangani menu dan input
def handle_menu():
    menu_active = True
    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Tekan Enter untuk mulai
                    menu_active = False
                elif event.key == pygame.K_ESCAPE:  # Tekan ESC untuk keluar
                    pygame.quit()
                    exit()

        show_menu()
        clock.tick(60)


# Fungsi untuk menampilkan layar pause
def show_pause():
    font = pygame.font.Font(None, 60)
    pause_text = font.render("PAUSED", True, RED)
    instruction_text = pygame.font.Font(None, 30).render("Press P to Resume", True, BLACK)

    screen.fill(WHITE)
    screen.blit(pause_text, (120, 250))
    screen.blit(instruction_text, (110, 300))

    pygame.display.update()


# Fungsi utama untuk menjalankan permainan
def game_loop():
    bird = Bird()
    pipes = [Pipe(), Pipe()]  # Mulai dengan dua pipa
    score = 0
    live = 3
    clock = pygame.time.Clock()
    paused = False  # Variabel untuk mengecek apakah game sedang di-pause

    while live > 0:
        # Reset permainan setiap kali hidup baru
        bird = Bird()
        pipes = [Pipe()]  # Reset pipa
        score = 0
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Burung terbang
                        bird.flap()
                    if event.key == pygame.K_p:  # Tekan P untuk pause
                        paused = not paused  # Toggle status pause

            if paused:
                show_pause()  # Jika game di-pause, tampilkan layar pause
                pygame.display.update()
                continue  # Skip update game jika dalam kondisi pause

            bird.update()
            for pipe in pipes:
                pipe.update()

            # Periksa tabrakan
            bird_rect = bird.get_rect()
            for pipe in pipes:
                top_rect, bottom_rect = pipe.get_rects()
                if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                    running = False  # Tabrakan terjadi, game berakhir

            # Skor dan pipa melewati burung
            for pipe in pipes:
                if pipe.x + pipe.width < bird.x and not pipe.passed:
                    pipe.passed = True
                    score += 1

                if pipe.x < 0:
                    print("pipe", pipe.x)
                if pipe.x < -20:
                    pipes.remove(pipe)

            # Jika pipa terakhir sudah keluar layar, tambahkan pipa baru
            if pipes[-1].x < screen_width - 150:
                pipes.append(Pipe())

            # Gambar elemen game
            screen.fill(WHITE)
            screen.blit(background_image, (0, 0))  # Gambar latar belakang stretch

            screen.blit(bird.image, bird.rect)  # Menampilkan burung dengan gambar yang berubah
            for pipe in pipes:
                # Stretch gambar pipa sesuai tinggi yang dihitung
                screen.blit(pygame.transform.scale(pipe_top_image, (pipe_width, pipe.height)), (pipe.x, 0))
                screen.blit(pygame.transform.scale(pipe_bottom_image, (pipe_width, pipe.bottom_height)), (pipe.x, pipe.height + gap))

            draw_score(score)

            pygame.display.update()
            clock.tick(30)

        live -= 1
        game_over()  # Tampilkan game over setelah satu nyawa habis


# Inisialisasi pygame dan masuk ke menu utama
pygame.init()
clock = pygame.time.Clock()

# Tampilkan menu utama sebelum permainan dimulai
handle_menu()

# Mulai permainan setelah menu
game_loop()

pygame.quit()
