from Bullet import Bullet
from Player import Player
import pygame
import pygame_menu
import pygame_menu.events
from Enemy import Enemy
import random
import json
import os

# setup:
pygame.font.init()
Comic_sans = pygame.font.SysFont('Comic Sans MS', 30)
pygame.mixer.init()
pygame.init()
TEXTURE_PACKS = {
    "TOGS": {
                "player": ("assets/Images/Player-TOGS.png",  (130, 130)),
        "bullet": ("assets/Images/Bullet-TOGS.png",  (70, 70)),
        "enemy":  ("assets/Images/Ememy-TOGS.png",   (120, 120))

    },
    "Normal": {
                "player": ("assets/Images/Player-norm.png",  (100, 100)),
        "bullet": ("assets/Images/Bullet-norm.png",  (50, 50)),
        "enemy":  ("assets/Images/Ememy-norm.png",   (80, 80))
    }
}

current_texture_pack = "Normal"

isFullscreen = False
player = Player(100)

width, height = pygame.display.set_mode((900, 900)).get_size()
display = pygame.display.set_mode((0, 0), pygame.RESIZABLE)

start_menu = pygame_menu.Menu('ierhgfbdhyvf', 900, 900, theme=pygame_menu.themes.THEME_BLUE)
pygame.display.flip()

# Load Player Image


# ----------------- FUNCTIONS -----------------
def switch_textures(selected, index):
    global current_texture_pack
    current_texture_pack = selected   # "Normal" or "TOGS"
    print("Texture pack changed to:", current_texture_pack)

def load_texture(path, size):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(image, size)





def draw_enemy_health_bar(surface, enemy):
    bar_width = 60
    bar_height = 8

    # Position bar above enemy
    x = enemy.x + 20        # center above enemy sprite
    y = enemy.y - 12        # slightly above the image

    # Health ratio
    ratio = enemy.health / 100

    # Background (red)
    pygame.draw.rect(surface, (255, 0, 0), (x, y, bar_width, bar_height))

    # Current health (green)
    pygame.draw.rect(surface, (0, 255, 0), (x, y, bar_width * ratio, bar_height))

    # Border
    pygame.draw.rect(surface, (0, 0, 0), (x, y, bar_width, bar_height), 2)

def fullscreen():
    global isFullscreen, start_menu
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    width, height = screen.get_size()
    pygame_menu.Menu.resize(start_menu, width, height, recursive=True)
    pygame.display.flip()
    isFullscreen = not isFullscreen


def draw_health_bar(surface, x, y, current_health, max_health, width=200, height=25):
    ratio = current_health / max_health
    pygame.draw.rect(surface, (255, 0, 0), (x, y, width, height))
    pygame.draw.rect(surface, (0, 255, 0), (x, y, width * ratio, height))
    pygame.draw.rect(surface, (0, 0, 0), (x, y, width, height), 3)


def save_score(username, score, filename="assets/scores.json"):
    if not os.path.exists(filename):
        data = {}
    else:
        with open(filename, "r") as f:
            data = json.load(f)

    if username not in data or score > data[username]["Highscore"]:
        data[username] = {"Highscore": score}

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def get_score(username, filename="assets/scores.json"):
    if not os.path.exists(filename):
        return None
    with open(filename, "r") as f:
        data = json.load(f)
    return data.get(username)


# ----------------- MAIN GAME LOOP -----------------

def Main(name):
    fullscreen()
    pygame.key.set_repeat()

    # ======= LOAD SELECTED TEXTURES =======
    textures = TEXTURE_PACKS[current_texture_pack]

    player_path, player_size = textures["player"]
    enemy_path, enemy_size = textures["enemy"]
    bullet_path, bullet_size = textures["bullet"]

    BIG_BOB = load_texture(player_path, player_size)

    # BULLET
    bullet_pygame = load_texture(bullet_path, bullet_size)

    # ENEMY (path + size)
    enemy_path, enemy_size = textures["enemy"]

    # ======================================

    killsound = pygame.mixer.Sound("assets/sounds/Killed.wav")
    player_speed = 0.5
    bobx, boby = 100, 100
    running = True
    score = 0
    angle = 1
    fire_cooldown = 300
    last_shot_time = 0

    screen_w, screen_h = display.get_size()

    print(f"Your last High Score: {get_score(name)}")

    # First enemy
    enemies = [
        Enemy(
            random.randint(0, 800),
            random.randint(0, 800),
            enemy_path,
            enemy_size
        )
    ]

    bullets = []
    bullet_speed = 1

    # =================== GAME LOOP =====================
    while running:
        angle += 1
        text = Comic_sans.render(f"Your current score is {score}", False, (0, 0, 0))
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if keys[pygame.K_ESCAPE]:
            running = False

        # Player movement
        if keys[pygame.K_a] and bobx > 10:
            bobx -= player_speed
        if keys[pygame.K_d] and bobx < screen_w - 110:
            bobx += player_speed
        if keys[pygame.K_w] and boby > 10:
            boby -= player_speed
        if keys[pygame.K_s] and boby < 900:
            boby += player_speed

        # Shooting
        if keys[pygame.K_1] and current_time - last_shot_time >= fire_cooldown:
            if enemies:
                e = enemies[0]
                dx = e.x - bobx
                dy = e.y - boby
                dist = max((dx**2 + dy**2)**0.5, 0.001)
                new_bullet = Bullet(bobx, boby, (dx/dist) * bullet_speed, (dy/dist) * bullet_speed)
                bullets.append(new_bullet)
                last_shot_time = current_time

        # Draw background & player
        display.fill("white")
        display.blit(text, text.get_rect(center=(screen_w/2, 10)))
        display.blit(BIG_BOB, (bobx, boby))

        # Enemies
        for e in enemies:
            e.move_toward(bobx, boby)
            e.draw(display)
            draw_enemy_health_bar(display, e)

            if abs(e.x - bobx) < 30 and abs(e.y - boby) < 30:
                player.health -= 0.05

            if player.health <= 0:
                running = False
                print("No more health left :(")

        # Bullets
        for bullet in bullets[:]:
            bullet.x += bullet.vel_x
            bullet.y += bullet.vel_y

            display.blit(pygame.transform.rotate(bullet_pygame, angle), (bullet.x, bullet.y))

            if bullet.x < 0 or bullet.x > screen_w or bullet.y < 0 or bullet.y > 1000:
                bullets.remove(bullet)
                continue

            for e in enemies[:]:
                if abs(bullet.x - e.x) < 20 and abs(bullet.y - e.y) < 20:
                    e.health -= 10
                    bullets.remove(bullet)
                    break

            for e in enemies[:]:
                if e.health <= 0:
                    enemies.remove(e)
                    score += 1
                    killsound.play()

                    enemies.append(Enemy(
                        random.randint(0, 800),
                        random.randint(0, 800),
                        enemy_path,
                        enemy_size
                    ))

                    save_score(name, score)

        draw_health_bar(display, 20, 1050, player.health, 100)
        pygame.draw.rect(display, (0, 0, 0), (0, 0, screen_w, 1000), 5)
        pygame.display.flip()


# ----------------- MENU SETUP -----------------

def start_buttons():
    start_menu.add.selector(
    "Textures: ",
    [("Normal", "Normal"), ("TOGS", "TOGS")],
    onchange=switch_textures
)
    start_menu.add.text_input("type your name: ", copy_paste_enable=True, onreturn=Main)
    start_menu.add.button("Quit if you're not brave enough", pygame_menu.events.EXIT)

start_buttons()
pygame.display.flip()
start_menu.mainloop(display)
pygame.quit()
