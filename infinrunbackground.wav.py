import pygame


pygame.mixer.init()
background_sound = pygame.mixer.Sound("assets/sounds/title.wav")
background_sound.play(-1)  # Play indefinitely
try:
    while True:
        pass  # Keep the program running to allow the sound to play
except KeyboardInterrupt as e:
    background_sound.stop()  # Stop the sound when the program is interrupted