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
import platform
import pygame
import pygame_menu
import pygame_menu.events
import random
import json
import sys
import pygamepopup
import math
import time
from datetime import datetime

# Format options: %Y=Year, %m=Month, %d=Day, %H=Hour, %M=Minute, %S=Second
formatted_time = f"({datetime.now().strftime("%m-%d-%Y-%H-%M-%S")})"
from power import powerup
from EBullet import EBullet
from Bullet import Bullet
from Player import Player
from Enemy import Enemy
from spike import Spikes

from pygamepopup.components import Button, InfoBox
from pygamepopup.menu_manager import MenuManager


if not os.path.exists("./Settings.json"):
        default_settings = {"V-sync": True,"Old Potions":True,"Testing":False,"do5thlevel":False,"OutPutlog":False}
        with open("./Settings.json", "w") as f:
            json.dump(default_settings, f, indent=4)
with open("./Settings.json", "r") as f:
            settings = json.load(f)
            OutPutlog = settings.get("OutPutlog", False)
def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath("./")

    return os.path.join(base_path, path)
pygame.font.init()
if platform.system() == "Windows":
    Comic_sans = pygame.font.SysFont('pacificoregular', 30)
else:
      Comic_sans = pygame.font.SysFont('Pacifico', 30)

pygame.init()
sound_enabled = True
try:
    pygame.mixer.init()
except pygame.error as e:
    sound_enabled = False

isFullscreen = False
end_score=4
global player_name

player = Player(100, resource_path("assets/Images/Conky-Bob.png"), 100, 100)
if sound_enabled:
    warning_sound = pygame.mixer.Sound(resource_path("assets/sounds/warning.mp3"))
    background_sound = pygame.mixer.Sound(resource_path("assets/sounds/title.wav"))
    kill_sound = pygame.mixer.Sound(resource_path("assets/sounds/Killed.wav"))
    start_sound = pygame.mixer.Sound(resource_path("assets/sounds/Startup.wav"))
    shutdown_sound = pygame.mixer.Sound(resource_path("assets/sounds/Shutdown.wav"))

else:
    background_sound = None
    kill_sound =None
    start_sound = None
    shutdown_sound = None

lvl1_img=pygame.image.load(resource_path("assets/Images/lvl1.jpeg"))
lvl2_img=pygame.image.load(resource_path("assets/Images/lvl4.jpeg"))
lvl3_img=pygame.image.load(resource_path("assets/Images/lvl3.jpeg"))
lvl4_img=pygame.image.load(resource_path("assets/Images/lvl2.jpeg"))
cat=pygame.image.load(resource_path("assets/Images/cat.JPG"))



width, height = pygame.display.set_mode((900, 900)).get_size()
display = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
pygamepopup.init()
bullet_image = pygame.image.load(resource_path("assets/Images/bullet.png")).convert_alpha()
Ebullet_image = pygame.image.load(resource_path("assets/Images/egg.png")).convert_alpha()
bullet_pygame = pygame.transform.scale(bullet_image, (50, 50))
Ebullet_pygame = pygame.transform.scale(Ebullet_image, (50, 50))
boss_bullet_pygame = pygame.transform.scale(Ebullet_image, (100, 100))
amount =1
bullets = []
Ebullets = []
enemies = []
boss_bullet = []
bullet_speed = 7
fire_cooldown = 1000
boss_fire_cooldown = 10
last_shot_time = 0
menu_manager = MenuManager(display)
start_menu = pygame_menu.Menu('ierhgfbdhyvf', width, height, theme=pygame_menu.themes.THEME_BLUE)
pygame.display.flip()
# Load Player Image
bob = pygame.image.load(player.image).convert_alpha()
BIG_BOB = pygame.transform.scale(bob, (100, 100))
lvl1_unlocked = False
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
    try:
                            background_sound.fadeout(0)
                            shutdown_sound.set_volume(1.0)
                            shutdown_sound.play()

    except AttributeError:
            if not os.path.exists("./log.txt") and OutPutlog:
                default_settings = f"{formatted_time}: sys: Error: womp womp your system doesn't support audio \n"
                with open("./log.txt", "w") as f:
                    f.write(default_settings)
            elif  os.path.exists("./log.txt") and OutPutlog:
                default_settings = f"{formatted_time}: sys: Error: womp womp your system doesn't support audio \n"
                with open("./log.txt", "w") as f:
                    f.write(default_settings)
    if not os.path.exists("./log.txt") and OutPutlog:
        default_settings = f"{formatted_time}: sys: quited the game\n"
        with open("./log.txt", "a") as f:
            f.write(default_settings)
    else:
        if OutPutlog:
            default_settings = f"{formatted_time}: sys: quited the game\n"
            with open("./log.txt", "a") as f:
                f.write(default_settings)
    time.sleep(3.2036733627319336)
    
    pygame.quit()
    os._exit(0)

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
def Spawn(A,l,screen_w,screen_h,r,x,y):
    for _ in range(A):
            l.append(Spikes(screen_w, screen_h))
            for s in l:
                if (s.x - r <= x <= s.x + r) and (s.y - r <= y <= s.y + r):
                    l.remove(s)
def Spawn_e(A,l,c):
    for _ in range(A):
            l.append(c(random.randint(0, 800), random.randint(0, 800)))

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
def shoot_enemy_bullet(enemy):
    current_time = pygame.time.get_ticks()

    if current_time - enemy.last_shot_time >= fire_cooldown :
        e = player  # target player
        dx = e.x - (enemy.x + random.randint(-500, 500))
        dy = e.y - (enemy.y + random.randint(-500, 500))
        dist = max((dx**2 + dy**2)**0.5, 0.001)

        new_bullet = EBullet(
            enemy.x,
            enemy.y,
            (dx/dist) * bullet_speed,
            (dy/dist) * bullet_speed
        )

        Ebullets.append(new_bullet)
        enemy.last_shot_time = current_time
def shoot_boss_bullet(enemy):
    current_time = pygame.time.get_ticks()

    if current_time - enemy.last_shot_time >= boss_fire_cooldown :
        e = player  # target player
        dx = e.x - (enemy.x + random.randint(-500, 500))
        dy = e.y - (enemy.y + random.randint(-500, 500))
        dist = max((dx**2 + dy**2)**0.5, 0.001)

        new_bullet = EBullet(
            enemy.x,
            enemy.y,
            (dx/dist) * bullet_speed,
            (dy/dist) * bullet_speed
        )

        boss_bullet.append(new_bullet)
        enemy.last_shot_time = current_time
def close_menu():
    paused_menu.disable()

# ----------------- MAIN GAME LOOP -----------------

def Main(player_name):
    if not os.path.exists("./Settings.json"):
        default_settings = {"V-sync": True,"Old Potions":True,"Testing":False,"do5thlevel":False,"OutPutlog":False}
        with open("./Settings.json", "w") as f:
            json.dump(default_settings, f, indent=4)
    with open("./Settings.json", "r") as f:
        settings = json.load(f)
    Vsync = settings.get("V-sync", True)
    doOldPotions = settings.get("Old Potions", True)
    testing = settings.get("Testing", False)
    do5thlevel = settings.get("do5thlevel", False)
    OutPutlog = settings.get("OutPutlog", False)
    if not os.path.exists("./log.txt") and OutPutlog:
        default_settings = f"{formatted_time}: {player_name}: launched main function and got settings from Settings.json\n"
        with open("./log.txt", "a") as f:
            f.write(default_settings)
    else:
        if OutPutlog:
            default_settings = f"{formatted_time}: {player_name}: launched main function and got settings from Settings.json\n"
            with open("./log.txt", "a") as f:
                f.write(default_settings)
    paused = False
    global paused_menu
    paused_menu = pygame_menu.Menu('Paused', width, height, theme=pygame_menu.themes.THEME_BLUE)
   
    

    
    try:
                            start_sound.set_volume(1.0)
                            start_sound.play()
    except AttributeError:
            if not os.path.exists("./log.txt") and OutPutlog:
                default_settings = f"{formatted_time}: {player_name}: Error:womp womp your system doesn't support audio \n"
                with open("./log.txt", "a") as f:
                    f.write(default_settings)
            else:
                if OutPutlog:
                    default_settings = f"{formatted_time}: {player_name}: Error:womp womp your system doesn't support audio \n"
                    with open("./log.txt", "a") as f:
                        f.write(default_settings)
    

    fullscreen()
    
    isStunCol = False
    SpowerCol= False
    isSpeedCol=False

    game_won = False
    popup_shown = False
    game_lost = False

    player_speed = 2
    player_speed_temp=0.25

    SpowerCoolDown=1
    StpowerCoolDown=1
    SppowerCoolDown=1

    inventory = []
    powerupsoptions=[]
    powerups=[]
    spikes=[]
    boss=[]

    screen_w, screen_h = display.get_size()
    # spikes.append(spike(randx(screen_w),randy(screen_h),100))
    powerupsoptions.append("s")
    powerups.append(powerup(screen_w,screen_h,"h",doOldPotions))
    powerups.append(powerup(screen_w,screen_h,"h",doOldPotions))
    powerups.append(powerup(screen_w,screen_h,"h",doOldPotions))
    powerups.append(powerup(screen_w,screen_h,"sp",doOldPotions))
        # MULTIPLE ENEMIES
    time.sleep(4.814058780670166)
    # if not background_sound_channel.get_busy() and not start_sound_channel.get_busy() and not shutdown_sound_channel.get_busy() and not SoundPlayed:
    lvl1_inc = 0
    lvl2_inc = 0
    lvl3_inc = 0
    lvl4_inc = 0
    score = 0

    r=100
    try:
                    # background_sound.play(loops=-1)
                    pass
                    
    except AttributeError:
            if not os.path.exists("./log.txt") and OutPutlog:
                default_settings = f"{formatted_time}: {player_name}: Error: womp womp your system doesn't support audio \n"
                with open("./log.txt", "a") as f:
                    f.write(default_settings)
            else:
                if OutPutlog:
                    default_settings = f"{formatted_time}: {player_name}: Error: womp womp your system doesn't support audio \n"
                    with open("./log.txt", "a") as f:
                        f.write(default_settings)
    
    pygame.key.set_repeat()
    Spawn_e(1,enemies,Enemy)
    bobx, boby = player.x, player.y
    
    paused_menu.add.label(f"Score: {score}","score")
    paused_menu.add.label("")
    paused_menu.add.button('Resume',close_menu)
    paused_menu.add.button('Quit Game',quit_game)
    Spawn(3,spikes,screen_w,screen_h-290,r,bobx,boby)
    running = True
    save_score(player_name,score)
    # =================== GAME LOOP =====================
    clock=pygame.time.Clock()
    e= Enemy(random.randint(0, 800), random.randint(0, 800))
    w=screen_w
    h=screen_h
    spin=0
    Ememy_cooldown=0
    boss_cooldown=0
    if not os.path.exists("./log.txt") and OutPutlog:
        default_settings = f"{formatted_time}: {player_name}: Launching main loop\n"
        with open("./log.txt", "a") as f:
            f.write(default_settings)
    else:
        if OutPutlog:
            default_settings = f"{formatted_time}: {player_name}: Launching main loop\n"
            with open("./log.txt", "a") as f:
                f.write(default_settings)
    while running:
            label = paused_menu.get_widget("score")
            label.set_title(f"Score: {score}")
            clock.tick()
            Ememy_cooldown+=1
            boss_cooldown+=0.5
            item_images = {
    "s": pygame.transform.scale(pygame.image.load(resource_path("assets/Images/strengh.png")).convert_alpha(), (50, 50)),
    "st": pygame.transform.scale(pygame.image.load(resource_path("assets/Images/stun.png")).convert_alpha(), (50, 50)),
    "h": pygame.transform.scale(pygame.image.load(resource_path("assets/Images/health.png")).convert_alpha(), (50, 50)),
    "sp": pygame.transform.scale(pygame.image.load(resource_path("assets/Images/speed.png")).convert_alpha(), (50, 50)),
}
            spin+=1
            player.x, player.y = bobx,boby
            
            if Vsync:
                clock.tick(60)
            if SpowerCol:
                SpowerCoolDown+=1
                if SpowerCoolDown >= 1000:
                    
                    SpowerCoolDown = not SpowerCol
                    SpowerCol = False
            if isStunCol:
                StpowerCoolDown+=1
                if not testing:
                    if StpowerCoolDown >= 1000:
                        StpowerCoolDown = 0
                        isStunCol = False

            if isSpeedCol:
                SppowerCoolDown+=1
                if SppowerCoolDown == 1:
                    player_speed = player_speed+player_speed_temp
                if SppowerCoolDown >= 1000:
                    player_speed = player_speed-player_speed_temp
                    SppowerCoolDown = 0
                    isSpeedCol = False
            left_click_held = False
            highscore=get_score(player_name)
            boss_string="WARNING John Cena is coming!"
            boss_text=Comic_sans.render(boss_string, False, (255, 0, 0))
            boss_string2="WARNING John Cena is HERE!"
            boss_text2=Comic_sans.render(boss_string2, False, (255, 0, 0))
            string2=f"Your HighScore is {highscore["Highscore"]}"
            string = f"Your current score is {score}"
            disFPS= f"FPS:{math.ceil(clock.get_fps())}"
            text2=Comic_sans.render(string2, False, (0, 0, 0))
            text = Comic_sans.render(string, False, (0, 0, 0))
            disFPST = Comic_sans.render(disFPS, False, (0, 0, 0))
            global current_time
            current_time = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            mouse_buttons = pygame.mouse.get_pressed()
            if not menu_manager.active_menu and not game_lost:
                if mouse_buttons[0]:  # left button held
                    shoot_bullet(enemies,bobx,boby)
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        
                        running = False
                        paused_menu.mainloop(display)
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        paused = True
                        paused_menu.enable()
                        paused_menu.mainloop(display)
                        paused = False
                    if event.type == pygame.MOUSEMOTION:
                        menu_manager.motion(event.pos)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        menu_manager.click(event.button, event.pos)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        left_click_held = True
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        left_click_held = False
                    if event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_u and not paused:
                            
                            for i in range(len(inventory)):
                                if not (inventory[i] is None):
                                    if not os.path.exists("./log.txt") and OutPutlog:
                                            default_settings = f"{formatted_time}: {player_name}: using powerup:{inventory[i].type} \n"
                                            with open("./log.txt", "a") as f:
                                                f.write(default_settings)
                                    else:
                                        if OutPutlog:
                                            default_settings = f"{formatted_time}: {player_name}: using powerup:{inventory[i].type} \n"
                                            with open("./log.txt", "a") as f:
                                                f.write(default_settings)
                                if inventory[i] is None:
                                    if not os.path.exists("./log.txt") and OutPutlog:
                                        default_settings = f"{formatted_time}: {player_name}: Error: Invalid powerup \n"
                                        with open("./log.txt", "a") as f:
                                            f.write(default_settings)
                                    else:
                                        if OutPutlog:
                                            default_settings = f"{formatted_time}: {player_name}: Error: Invalid powerup \n"
                                            with open("./log.txt", "a") as f:
                                                f.write(default_settings)
                                    continue

                                if inventory[i].type == "h" and player.health <= 80:
                                    player.health += 20
                                    inventory[i] = None
                                    break

                                elif inventory[i].type == "s":
                                    SpowerCol = True
                                    inventory[i] = None
                                    break

                                elif inventory[i].type == "st":
                                    isStunCol = True
                                    inventory[i] = None
                                    break

                                elif inventory[i].type == "sp":
                                    isSpeedCol = True
                                    inventory[i] = None
                                    break

                            # Compact inventory
                            inventory = [item for item in inventory if item is not None]

                            while len(inventory) < len(slots):
                                inventory.append(None)


                        



            # ------------- PLAYER MOVEMENT LIMITS ----------------
            if not menu_manager.active_menu and not game_lost and not paused:

                if keys[pygame.K_a] and bobx > 0:
                    bobx -= player_speed
                if keys[pygame.K_a] and bobx <= 10:
                    bobx=screen_w-108
                    bobx -= player_speed

                if keys[pygame.K_d] and bobx < screen_w:
                    bobx += player_speed
                if keys[pygame.K_d] and bobx >= screen_w-109:
                    bobx = 10
                    bobx += player_speed

                if keys[pygame.K_w]:
                    boby -= player_speed
                if keys[pygame.K_w] and boby <= 100 and not doOldPotions:
                    boby=screen_h-290
                    boby -= player_speed
                elif  keys[pygame.K_w] and boby <= 100 and doOldPotions:
                    boby=screen_h-109
                    boby -= player_speed
                if keys[pygame.K_s]:
                    boby += player_speed
                if keys[pygame.K_s] and boby >= screen_h-290 and not doOldPotions:
                    boby=99
                    boby += player_speed
                if keys[pygame.K_s] and boby >= screen_h-110 and doOldPotions:
                    boby=99
                    boby += player_speed

                if left_click_held:
                    shoot_bullet(enemies,bobx-1,boby+1)
                

                # ------------- SHOOTING ----------------

            # ------------- FILL SCREEN & DRAW PLAYER ----------------

            if score < 20:
                display.blit(pygame.transform.scale(lvl1_img,(screen_w,screen_h)),(0,0))
            if score >= 20 and score < 40:
                lvl1_inc +=1
                if lvl1_inc == 1:
                    if not os.path.exists("./log.txt") and OutPutlog:
                        default_settings = f"{formatted_time}: {player_name}: Leveling up to Level 2\n"
                        with open("./log.txt", "a") as f:
                            f.write(default_settings)
                    else:
                        if OutPutlog:
                            default_settings = f"{formatted_time}: {player_name}: Leveling up to Level 2\n"
                            with open("./log.txt", "a") as f:
                                f.write(default_settings)
                    boss.append(Enemy(random.randint(0, 800), random.randint(0, 800),0.6,100,"boss"))
                display.blit(pygame.transform.scale(lvl2_img,(w,h)),(0,0))
            if score >= 40 and score < 60:
                lvl2_inc +=1

                if lvl2_inc == 1:
                    if not os.path.exists("./log.txt") and OutPutlog:
                        default_settings = f"{formatted_time}: {player_name}: Leveling up to Level 3\n"
                        with open("./log.txt", "a") as f:
                            f.write(default_settings)
                    else:
                        if OutPutlog:
                            default_settings = f"{formatted_time}: {player_name}: Leveling up to Level 3\n"
                            with open("./log.txt", "a") as f:
                                f.write(default_settings)
                    boss.append(Enemy(random.randint(0, 800), random.randint(0, 800), type="boss"))
                display.blit(pygame.transform.scale(lvl3_img,(w,h)),(0,0))
            if score >= 60 and score < 80:
                lvl3_inc +=1
                if lvl3_inc == 1:
                    if not os.path.exists("./log.txt") and OutPutlog:
                        default_settings = f"{formatted_time}: {player_name}: Leveling up to Level 4\n"
                        with open("./log.txt", "a") as f:
                            f.write(default_settings)
                    else:
                        if OutPutlog:
                            default_settings = f"{formatted_time}: {player_name}: Leveling up to Level 4\n"
                            with open("./log.txt", "a") as f:
                                f.write(default_settings)
                        boss.append(Enemy(random.randint(0, 800), random.randint(0, 800), type="boss"))
                display.blit(pygame.transform.scale(lvl4_img,(w,h)),(0,0))
            if score >= 80 and do5thlevel:
                lvl4_inc +=1
                if lvl4_inc == 1:
                    if not os.path.exists("./log.txt") and OutPutlog:
                        default_settings = f"{formatted_time}: {player_name}: Leveling up to Level 5\n"
                        with open("./log.txt", "a") as f:
                            f.write(default_settings)
                    else:
                        if OutPutlog:
                            default_settings = f"{formatted_time}: {player_name}: Leveling up to Level 5\n"
                            with open("./log.txt", "a") as f:
                                f.write(default_settings)
                        boss.append(Enemy(random.randint(0, 800), random.randint(0, 800), type="boss"))
                display.blit(pygame.transform.scale(cat,(w,h)),(0,0))

            
            display.blit(BIG_BOB, (bobx, boby))
            if not doOldPotions:

                rect_w = w*0.5
                rect_h=100
                main_rect = pygame.Rect(0, 0, rect_w, rect_h)
                main_rect.center = (w/2, h*0.9)
                pygame.draw.rect(display, (128, 128, 128), main_rect)
                slot1x= main_rect.x + 10
                slot1y= main_rect.y + 10
                slot2x= main_rect.x + 10 + rect_h
                slot2y= main_rect.y + 10
                slot3x= main_rect.x + 10 + 2*rect_h
                slot3y= main_rect.y + 10
                slot4x= main_rect.x + 10 + 3*rect_h
                slot4y= main_rect.y + 10
                slot5x= main_rect.x + 10 + 4*rect_h
                slot5y= main_rect.y + 10
                slot6x= main_rect.x + 10 + 5*rect_h
                slot6y= main_rect.y + 10
                slot7x= main_rect.x + 10 + 6*rect_h
                slot7y= main_rect.y + 10
                slot8x= main_rect.x + 10 + 7*rect_h
                slot8y= main_rect.y + 10
                slot9x= main_rect.x + 10 + 8*rect_h
                slot9y= main_rect.y + 10
                slots = [
        (slot1x, slot1y),
        (slot2x, slot2y),
        (slot3x, slot3y),
        (slot4x, slot4y),
        (slot5x, slot5y),
        (slot6x, slot6y),
        (slot7x, slot7y),
        (slot8x, slot8y),
        (slot9x, slot9y),
    ]
                slot1= pygame.Rect(slot1x, slot1y, rect_h-20, rect_h-20)
                slot2= pygame.Rect(slot2x, slot2y, rect_h-20, rect_h-20)
                slot3= pygame.Rect(slot3x, slot3y, rect_h-20, rect_h-20)
                slot4= pygame.Rect(slot4x, slot4y, rect_h-20, rect_h-20)
                slot5= pygame.Rect(slot5x, slot5y, rect_h-20, rect_h-20)
                slot6= pygame.Rect(slot6x, slot6y, rect_h-20, rect_h-20)
                slot7= pygame.Rect(slot7x, slot7y, rect_h-20, rect_h-20)
                slot8= pygame.Rect(slot8x, slot8y, rect_h-20, rect_h-20)
                slot9= pygame.Rect(slot9x, slot9y, rect_h-20, rect_h-20)
                pygame.draw.rect(display, (255, 255, 255), slot1)
                pygame.draw.rect(display, (255, 255, 255), slot2)
                pygame.draw.rect(display, (255, 255, 255), slot3)
                pygame.draw.rect(display, (255, 255, 255), slot4)
                pygame.draw.rect(display, (255, 255, 255), slot5)
                pygame.draw.rect(display, (255, 255, 255), slot6)
                pygame.draw.rect(display, (255, 255, 255), slot7)
                pygame.draw.rect(display, (255, 255, 255), slot8)
                pygame.draw.rect(display, (255, 255, 255), slot9)
            for p in powerups:
                p.draw(display)
                if (p.x - r/2 <= bobx <= p.x + r/2) and (p.y - r/2 <= boby <= p.y + r/2):
                    if not os.path.exists("./log.txt") and OutPutlog:
                        default_settings = f"{formatted_time}: {player_name}: Appended powerup: {p.type}\n"
                        with open("./log.txt", "a") as f:
                            f.write(default_settings)
                    else:
                        if OutPutlog:
                            default_settings = f"{formatted_time}: {player_name}: Appended powerup: {p.type}\n"
                            with open("./log.txt", "a") as f:
                                f.write(default_settings)
                if p.type == "s":
                    if (p.x - r/2 <= bobx <= p.x + r/2) and (p.y - r/2 <= boby <= p.y + r/2):
                        if not doOldPotions:
                            inventory.append(p)
                        else:
                            SpowerCol = True
                        powerups.remove(p)
                if p.type == "h":
                    if (p.x - r <= bobx <= p.x + r) and (p.y - r <= boby <= p.y + r) and player.health <100:
                        if not doOldPotions:
                            inventory.append(p)
                        else:
                            player.health += 20
                        powerups.remove(p)
                if p.type=="sp":
                     if (p.x - r/2 <= bobx <= p.x + r/2) and (p.y - r/2 <= boby <= p.y + r/2):
                        if not doOldPotions:
                            inventory.append(p)
                        else:
                            isSpeedCol = True
                        powerups.remove(p)
                if p.type=="st":
                     if (p.x - r/2 <= bobx <= p.x + r/2) and (p.y - r/2 <= boby <= p.y + r/2):
                        if not doOldPotions:
                            inventory.append(p)
                        else:
                            isSpeedCol = True
                        powerups.remove(p)

            # ------------- ENEMY MOVEMENT + DAMAGE TO PLAYER ----------------
            for e in enemies[:]:                                    
                if (not isStunCol or not testing and Ememy_cooldown%2==0) and not paused:shoot_enemy_bullet(enemy=e)
            for e in boss[:]:                                    
                if (not isStunCol or not testing and Ememy_cooldown%2==0) and not paused:shoot_boss_bullet(enemy=e)

            for e in enemies[:]:
                e.move_toward(bobx, boby,isStunCol,testing,paused)
                e.draw(display)
                draw_health_bar(display, e.x-10, e.y-20, e.health, 100)
                # Damage player on touch
                if abs(e.x - bobx) < 30 and abs(e.y - boby) < 30:
                    player.health -= 0.05

                # Player dead
                if player.health <= 0:
                    game_lost = True
            for e in boss[:]:
                e.move_toward(bobx, boby,isStunCol,testing,paused)
                e.draw(display)
                draw_health_bar(display, e.x-10, e.y-20, e.health, 200)
                # Damage player on touch
                if abs(e.x - bobx) < 30 and abs(e.y - boby) < 30:
                    player.health -= 0.05

                # Player dead
                if player.health <= 0:
                    game_lost = True

            # ------------- BULLET MOVEMENT + ENEMY COLLISION ----------------
            for e in boss[:]:
                    for s in spikes:
                        s.draw(display)
                        if (s.x - r <= e.x <= s.x + r) and (s.y - r <= e.y <= s.y + r):
                            if e.health <200:
                                e.health+=0.05
                    if e.health <= 0:
                        boss.remove(e)
                        score += 10
                        
                        
                        try:
                            kill_sound.set_volume(1.0)
                            kill_sound.play()
                        except AttributeError:
                            if not os.path.exists("./log.txt"):
                                default_settings = f"{formatted_time}: {player_name}: Error: womp womp your system doesn't support audio \n"
                                with open("./log.txt", "a") as f:
                                    f.write(default_settings)
                        

                        
                        # Respawn new enemy
                        
                        save_score(player_name, score)
                        if not os.path.exists("./log.txt") and OutPutlog:
                            default_settings = f"{formatted_time}: {player_name}: saved score for {player_name}: {score}\n"
                            with open("./log.txt", "a") as f:
                                f.write(default_settings)
                        else:
                            if OutPutlog:
                                default_settings = f"{formatted_time}: {player_name}: saved score for {player_name}: {score}\n"
                                with open("./log.txt", "a") as f:
                                    f.write(default_settings)
                        if str(abs(score))[0] == "5" or str(abs(score))[0] == "0":
                            powerups.append(powerup(screen_w,screen_h,"s",doOldPotions))
                        if score %4 == 0:
                            powerups.append(powerup(screen_w,screen_h,"st",doOldPotions))
                        #     Spawn_e(2,enemies,Enemy)
                        if score % 2 ==0:
                            Spawn(1,spikes,screen_w,screen_h-290,r,bobx,boby)
                            
                        Spawn_e(2,enemies,Enemy)
            for bullet in bullets[:]:
                bullet.x += bullet.vel_x
                bullet.y += bullet.vel_y
                
                display.blit(pygame.transform.rotate(bullet_pygame,spin), (bullet.x, bullet.y))

                # Off screen delete
                if bullet.x < 0 or bullet.x > screen_w or bullet.y < 0 or bullet.y > screen_h:
                    if not os.path.exists("./log.txt") and OutPutlog:
                        default_settings = f"{formatted_time}: {player_name}: deleted bullet:{bullet}\n"
                        with open("./log.txt", "a") as f:
                            f.write(default_settings)
                    else:
                        if OutPutlog:
                            default_settings = f"{formatted_time}: {player_name}: deleted bullet:{bullet}\n"
                            with open("./log.txt", "a") as f:
                                f.write(default_settings)
                    bullets.remove(bullet)
                    
                    continue

                # Check bullet → enemy collision
                for e in boss[:]:

                    if abs(bullet.x - e.x) < 20 and abs(bullet.y - e.y) < 20:
                            
                            if SpowerCol:
                                
                                e.health -= 20
                                bullets.remove(bullet)
                            else:
                                e.health -= 10
                                bullets.remove(bullet)
                                break
                for e in enemies[:]:

                    if abs(bullet.x - e.x) < 20 and abs(bullet.y - e.y) < 20:
                            
                            if SpowerCol:
                                
                                e.health -= 15
                                bullets.remove(bullet)
                            else:
                                e.health -= 5
                                bullets.remove(bullet)
                                break
            
            for bullet in Ebullets[:]:
                if not paused:
                    bullet.x += bullet.vel_x
                    bullet.y += bullet.vel_y

                display.blit(pygame.transform.rotate(Ebullet_pygame,spin), (bullet.x, bullet.y))
                
                # Off screen delete
                if bullet.x < 0 or bullet.x > screen_w or bullet.y < 0 or bullet.y > screen_h:
                    # bullets.remove(bullet)
                    continue

                # Check bullet → enemy collision
                if abs(bullet.x - bobx) < 20 and abs(bullet.y - boby) < 20:
                                player.health -= 0.5
                                Ebullets.remove(bullet)
                                break
            for bullet in boss_bullet[:]:
                if not paused:
                    bullet.x += bullet.vel_x
                    bullet.y += bullet.vel_y

                display.blit(pygame.transform.rotate(boss_bullet_pygame,spin), (bullet.x, bullet.y))
                
                # Off screen delete
                if bullet.x < 0 or bullet.x > screen_w or bullet.y < 0 or bullet.y > screen_h:
                    # bullets.remove(bullet)
                    continue

                # Check bullet → enemy collision
                if abs(bullet.x - bobx) < 20 and abs(bullet.y - boby) < 20:
                                player.health -= 0.75
                                boss_bullet.remove(bullet)
                                break
            for s in spikes:
                s.draw(display)
                if (s.x - r <= bobx <= s.x + r) and (s.y - r <= boby <= s.y + r):
                    player.health -=0.05


            for index, item in enumerate(inventory):
                if index >= len(slots):
                    break  # don't overflow hotbar

                if item is None:
                    continue

                if item.type in item_images:
                    display.blit(item_images[item.type], slots[index])
                            # Remove dead enemies
            for e in enemies[:]:
                    for s in spikes:
                        s.draw(display)
                        if (s.x - r <= e.x <= s.x + r) and (s.y - r <= e.y <= s.y + r):
                            if e.health <100:
                                e.health+=0.05
                    if e.health <= 0:
                        enemies.remove(e)
                        score += 1
                        
                        
                        try:
                            kill_sound.set_volume(1.0)
                            kill_sound.play()
                        except AttributeError:
                            if not os.path.exists("./log.txt"):
                                default_settings = f"{formatted_time}: {player_name}: Error: womp womp your system doesn't support audio \n"
                                with open("./log.txt", "w") as f:
                                    f.write(default_settings)
                        

                        
                        # Respawn new enemy
                        
                        save_score(player_name, score)
                        if not os.path.exists("./log.txt") and OutPutlog:
                            default_settings = f"{formatted_time}: {player_name}: saved score for {player_name}: {score}\n"
                            with open("./log.txt", "a") as f:
                                f.write(default_settings)
                        else:
                            if OutPutlog:
                                default_settings = f"{formatted_time}: {player_name}: saved score for {player_name}: {score}\n"
                                with open("./log.txt", "a") as f:
                                    f.write(default_settings)
                        if str(abs(score))[0] == "5" or str(abs(score))[0] == "0":
                            powerups.append(powerup(screen_w,screen_h,"s",doOldPotions))
                        if score %4 == 0:
                            powerups.append(powerup(screen_w,screen_h,"st",doOldPotions))
                        #     Spawn_e(2,enemies,Enemy)
                        if score % 2 ==0:
                            Spawn(1,spikes,screen_w,screen_h-290,r,bobx,boby)
                            
                        Spawn_e(2,enemies,Enemy)
                        # elif score < end_score:
                        #     Spawn_e(1,enemies,Enemy)
            # if not enemies:
            #         game_won = True

            if game_won and not popup_shown:
                menu_manager.open_menu(win_popup)
                popup_shown = True
            if game_lost and not popup_shown:
                menu_manager.open_menu(lose_popup)
                popup_shown = True

                    
            menu_manager.display()        

        # ------------- HEALTH BARS ----------------
            if doOldPotions:
                draw_health_bar(display, bobx-10, boby-20, player.health, 100)
            elif not doOldPotions:
                draw_health_bar(display, 150, screen_h -150, player.health, 100)
            display.blit(text, text.get_rect(center=(screen_w/2, 10)))
            display.blit(text2, text2.get_rect(center=(screen_w/2, 40)))
            display.blit(disFPST, disFPST.get_rect(center=(screen_w/2, 70)))
            if score == 19 or score == 39 or score == 59 or score == 79:
                warning_sound.play(-1)
                display.blit(boss_text, boss_text.get_rect(center=(screen_w/2, 100)))
            else:
                warning_sound.stop()
            if score == 20 or score == 40 or score == 60 or score == 80:
                display.blit(boss_text2, boss_text2.get_rect(center=(screen_w/2, 100)))
            pygame.display.flip()
            



# ----------------- MENU SETUP -----------------
if not os.path.exists("./Settings.json"):
        default_settings = {"V-sync": True,"Old Potions":True,"Testing":False,"do5thlevel":False,"OutPutlog":False}
        with open("./Settings.json", "w") as f:
            json.dump(default_settings, f, indent=4)
        with open("./Settings.json", "r") as f:
            settings = json.load(f)
            OutPutlog = settings.get("OutPutlog", False)
def start_buttons():
    start_menu.add.text_input("type your name: ", copy_paste_enable=True, onreturn=Main)
    start_menu.add.button("Quit if you're not brave enough", pygame_menu.events.EXIT)
try:
                            start_sound.set_volume(1.0)
                            start_sound.play()
except AttributeError:
            if not os.path.exists("./log.txt"):
                default_settings = f"{formatted_time}: sys: Error: womp womp your system doesn't support audio \n"
                with open("./log.txt", "w") as f:
                    f.write(default_settings)

start_buttons()
pygame.display.flip()
start_menu.mainloop(display)
pygame.quit()
# if not os.path.exists("./log.txt") and OutPutlog:
#     default_settings = "\n"
#     with open("./log.txt", "a") as f:
#         f.write(default_settings)
# else:
#     if OutPutlog:
#         default_settings = "\n"
#         with open("./log.txt", "a") as f:
#             f.write(default_settings)