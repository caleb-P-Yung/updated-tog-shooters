import os
# r= True
# while r:
#     i=input("Are you on linux? (y/n) ")
#     if i.lower() == "y" or i.lower() == "yes":
#         i2 = input("Are you using PulseAudio? (y/n) ")
#         if i2.lower() =="y" or i2.lower() == "yes":
#             os.environ["SDL_AUDIODRIVER"] = "pulseaudio"
#             r=False
#         if i2.lower() == "n" or i.lower == "no":
#             i3= input("Are You Use ALSA?")
#             if i3.lower() =="y" or i3.lower() == "yes":
#                 os.environ["SDL_AUDIODRIVER"] = "alsa"
#                 r=False
#             if i3.lower() == "n" or i3.lower() == "no":
#                 i4=input("Are you using PipeWire?")
#                 if i4.lower() =="y" or i4.lower() == "yes":
#                     os.environ["SDL_AUDIODRIVER"] = "pipewire"
#                     r=False
#     elif i.lower() == "n" or i.lower() == "no":
#         os.environ["SDL_AUDIODRIVER"] = "directaudio"
#         r=False
#     print("n\n\n\n\n\n ANSWER THE QUESTION!!!!!\n")
import pygame
import pygame_menu
import pygame_menu.events
import random
import json
import sys
import pygamepopup
from Bullet import Bullet
from Player import Player
from Enemy import Enemy
from spike import Spikes
from pygamepopup.components import Button, InfoBox
from pygamepopup.menu_manager import MenuManager
# setup:


def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath("./")

    return os.path.join(base_path, path)
pygame.font.init()
Comic_sans = pygame.font.SysFont('Comic Sans MS', 30)
pygame.init()
sound_enabled = True
try:
    pygame.mixer.init()
except pygame.error as e:
    sound_enabled = False

isFullscreen = False
end_score=4
player = Player(100, resource_path("assets/Images/Conky-Bob.png"))
if sound_enabled:
    kill_sound = pygame.mixer.Sound(resource_path("assets/sounds/Killed.wav"))
else:
    kill_sound =None
background_img_path= resource_path("assets/Images/background.jpeg")
backgrong_img=pygame.image.load(background_img_path)
width, height = pygame.display.set_mode((900, 900)).get_size()
display = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygamepopup.init()
bullet_image = pygame.image.load(resource_path("assets/Images/bullet.png")).convert_alpha()
bullet_pygame = pygame.transform.scale(bullet_image, (50, 50))
amount =1
bullets = []
bullet_speed = 2
fire_cooldown = 300
last_shot_time = 0
menu_manager = MenuManager(display)
start_menu = pygame_menu.Menu('ierhgfbdhyvf', width, height, theme=pygame_menu.themes.THEME_BLUE)
pregame_menu=pygame_menu.Menu('ierhgfbdhyvf', width, height, theme=pygame_menu.themes.THEME_BLUE)
pygame.display.flip()
# Load Player Image
bob = pygame.image.load(player.image).convert_alpha()
BIG_BOB = pygame.transform.scale(bob, (100, 100))

# ----------------- FUNCTIONS -----------------

def randx(sx):
    rx=random.randrange(100,sx)
    lx=random.randrange(sx-100,sx)
    return  random.randrange(rx,lx)
def randy(sy):
    ry=random.randrange(100,sy)
    ly=random.randrange(sy-100,sy)
    return random.randrange(ry,ly)
def quit_game():
    pygame.quit()
    exit()

win_popup = InfoBox(
    "You Win!",
    [
        [
            Button(quit_game,title="Quit")

        ]
    ]
)
lose_popup = InfoBox(
    "You Lost",
    [
        [
            Button(quit_game,title="Quit")

        ]
    ]
)
def Spawn_Ememies(A,enemies):
    for _ in range(A):
        enemies.append(Enemy(random.randint(0, 800), random.randint(0, 800)))
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


def save_score(username, score, filename=resource_path("assets/scores.json")):
    if not os.path.exists(filename):
        data = {}
    else:
        with open(filename, "r") as f:
            data = json.load(f)

    if username not in data or score > data[username]["Highscore"]:
        data[username] = {"Highscore": score}

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def get_score(username, filename=resource_path("assets/scores.json")):
    if not os.path.exists(filename):
        return "bob"
    with open(filename, "r") as f:
        data = json.load(f)
    return data.get(username)

def shoot_bullet(enemies,bobx,boby):
    global last_shot_time
    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time >= fire_cooldown and enemies:
        e = enemies[0]  # shoot nearest enemy
        dx = e.x - bobx
        dy = e.y - boby
        dist = max((dx**2 + dy**2)**0.5, 0.001)

        new_bullet = Bullet(bobx, boby, (dx/dist) * bullet_speed, (dy/dist) * bullet_speed)
        bullets.append(new_bullet)
        last_shot_time = current_time

# ----------------- MAIN GAME LOOP -----------------

def Main(player_name):
    fullscreen()
    game_won = False
    popup_shown = False
    game_lost = False
    player_speed = 1
    spikes=[]
    screen_w, screen_h = display.get_size()
    # spikes.append(spike(randx(screen_w),randy(screen_h),100))
    spikes.append(Spikes(screen_w,screen_h))

        # MULTIPLE ENEMIES
    enemies = []
    pygame.key.set_repeat()
    # Spawn_Ememies(1,enemies)
    bobx, boby = 100, 100
    score = 0
    r=100
    running = True
    save_score(player_name,score)
    # =================== GAME LOOP =====================
    while running:
            left_click_held = False
            highscore=get_score(player_name)
            string2=f"Your HighScore is {highscore["Highscore"]}"
            string = f"Your current score is {score}"
            text2=Comic_sans.render(string2, False, (0, 0, 0))
            text = Comic_sans.render(string, False, (0, 0, 0))
            global current_time
            current_time = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:  # left button held
                shoot_bullet(enemies,bobx,boby)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEMOTION:
                    menu_manager.motion(event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    menu_manager.click(event.button, event.pos)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    left_click_held = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    left_click_held = False
                        



            # ------------- PLAYER MOVEMENT LIMITS ----------------
            
            if keys[pygame.K_ESCAPE]:
                    quit_game()
            if not menu_manager.active_menu and not game_lost:
                if keys[pygame.K_a] and bobx > 10:
                    bobx -= player_speed
                if keys[pygame.K_d] and bobx < screen_w - 110:
                    bobx += player_speed
                if keys[pygame.K_w] and boby > 10:
                    boby -= player_speed
                if keys[pygame.K_s] and boby < 900:
                    boby += player_speed
                if left_click_held:
                    shoot_bullet(enemies,bobx,boby)
                # ------------- SHOOTING ----------------

            # ------------- FILL SCREEN & DRAW PLAYER ----------------
            display.blit(pygame.transform.scale(backgrong_img,(screen_w,screen_h)))
            display.blit(text, text.get_rect(center=(screen_w/2, 10)))
            display.blit(text2, text2.get_rect(center=(screen_w/2, 40)))
            display.blit(BIG_BOB, (bobx, boby))

            # ------------- ENEMY MOVEMENT + DAMAGE TO PLAYER ----------------
            for e in enemies[:]:
                e.move_toward(bobx, boby)
                e.draw(display)
                draw_health_bar(display, e.x-10, e.y-20, e.health, 100)
                # Damage player on touch
                if abs(e.x - bobx) < 30 and abs(e.y - boby) < 30:
                    player.health -= 0.05

                # Player dead
                if player.health <= 0:
                    game_lost = True

            # ------------- BULLET MOVEMENT + ENEMY COLLISION ----------------
            for bullet in bullets[:]:
                bullet.x += bullet.vel_x
                bullet.y += bullet.vel_y

                display.blit(bullet_pygame, (bullet.x, bullet.y))
                
                # Off screen delete
                if bullet.x < 0 or bullet.x > screen_w or bullet.y < 0 or bullet.y > 1000:
                    bullets.remove(bullet)
                    continue

                # Check bullet → enemy collision
                for e in enemies[:]:
                    if abs(bullet.x - e.x) < 20 and abs(bullet.y - e.y) < 20:
                        e.health -= 10
                        bullets.remove(bullet)
                        break
            for s in spikes:
                s.draw(display)
                if s.x +r <= bobx and bobx >=s.x -r or s.y +r >= boby and boby >=s.y -r:
                    player.health -=0.05
                print(f"spike x: {s.x} spike y: {s.y} damage radius: {r}")
                # Remove dead enemies
            for e in enemies[:]:
                    if e.health <= 0:
                        enemies.remove(e)
                        score += 1
                        
                        
                        try:
                            kill_sound.set_volume(1.0)
                            kill_sound.play()
                            print(f"Just Played:{kill_sound}")
                            print("The lenegh of the Sound was:", kill_sound.get_length())
                        except AttributeError:
                            print("You did : \n 1.choose the wrong audio driver \n 2. your system doesn't support audio ")
                        

                        
                        # Respawn new enemy
                        
                        save_score(player_name, score)
                        if score==end_score/4:
                            
                            Spawn_Ememies(2,enemies)
                        if score==end_score/2:
                            
                            Spawn_Ememies(2,enemies)
                        elif score < end_score:
                            Spawn_Ememies(1,enemies)
            if not enemies:
                    game_won = True

            if game_won and not popup_shown:
                menu_manager.open_menu(win_popup)
                popup_shown = True
            if game_lost and not popup_shown:
                menu_manager.open_menu(lose_popup)
                popup_shown = True

                    
            menu_manager.display()        

        # ------------- HEALTH BARS ----------------
            draw_health_bar(display, bobx-10, boby-20, player.health, 100)
                
            pygame.display.flip()



# ----------------- MENU SETUP -----------------

def start_buttons():
    start_menu.add.text_input("type your name: ", copy_paste_enable=True, onreturn=Main)
    start_menu.add.button("Quit if you're not brave enough", pygame_menu.events.EXIT)
    
start_buttons()
pygame.display.flip()
start_menu.mainloop(display)
pygame.quit()
