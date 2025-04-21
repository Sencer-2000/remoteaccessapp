import pygame
import random
import sys
import time
import os

# Windows üzerinde çalışıyorsa pencereyi her zaman üstte yap
if sys.platform == "win32":
    import win32gui
    import win32con

# Pygame başlatma
pygame.init()

# Komut satırından gelen yazı
texttowirte = sys.argv[1]

# Ekran boyutu
screen_width = 1920
screen_height = 1080

# Pencereyi tam ekran ve çerçevesiz başlat
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.NOFRAME)
pygame.display.set_caption("Konfeti Efekti")

# Windows'ta pencereyi her zaman üstte yap
if sys.platform == "win32":
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                          win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Yazı tipi ve yazı ayarları
font = pygame.font.SysFont('Arial', 100)
text = font.render(texttowirte, True, BLACK)

# Konfeti partikül sınıfı
class Confetti:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(5, 10)
        self.speed = random.randint(3, 6)
        self.angle = random.uniform(0, 2 * 3.14159)
        self.velocity_x = self.speed * random.uniform(-0.5, 0.5)
        self.velocity_y = self.speed * random.uniform(-1.5, -2.5)

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.size -= 0.05
        if self.size <= 0:
            self.size = random.randint(5, 10)
            self.x = random.randint(0, screen_width)
            self.y = screen_height

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

# Konfeti renkleri
confetti_colors = [
    (255, 0, 0),     # Kırmızı
    (0, 255, 0),     # Yeşil
    (0, 0, 255),     # Mavi
    (255, 255, 0),   # Sarı
    (255, 165, 0)    # Turuncu
]

# Konfeti listesi
confetti_particles = []

# Yazının büyüme ayarları
text_scale = 1.0
scale_speed = 0.05

# Konfeti oluşturma şansı
confetti_chance = 0.15

# Başlangıç zamanı ve çalışma süresi
start_time = time.time()
run_duration = 5  # saniye

# Ana döngü
clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)

    # Yazıyı büyütme
    if text_scale < 3.0:
        text_scale += scale_speed
    scaled_text = pygame.transform.scale(text, (int(text.get_width() * text_scale), int(text.get_height() * text_scale)))
    screen.blit(scaled_text, (screen_width // 2 - scaled_text.get_width() // 2, screen_height // 2.5 - scaled_text.get_height() // 2))

    # Konfeti güncelleme ve çizme
    for confetti in confetti_particles:
        confetti.update()
        confetti.draw(screen)

    # Konfeti oluştur
    if random.random() < confetti_chance and text_scale >= 2.0:
        color = random.choice(confetti_colors)
        confetti_particles.append(Confetti(random.randint(0, screen_width), screen_height, color))

    # Etkinlikleri kontrol et
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Süreyi kontrol et, 5 saniye sonra çık
    if time.time() - start_time > run_duration:
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
