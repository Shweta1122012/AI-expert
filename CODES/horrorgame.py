import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Night Shift Protocol")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 40)

# Colors
BLACK = (0,0,0)
GRAY = (40,40,40)
RED = (200,0,0)
GREEN = (0,200,0)
WHITE = (255,255,255)

# Game variables
power = 100
hour = 12
night_timer = 0
game_over = False
win = False

left_door_closed = False
right_door_closed = False
camera_on = False

# Monster states
monster_position = "stage"
monster_timer = 0

def draw_office():
    screen.fill(GRAY)

    # Doors
    if left_door_closed:
        pygame.draw.rect(screen, RED, (0,0,100,HEIGHT))
    else:
        pygame.draw.rect(screen, BLACK, (0,0,100,HEIGHT))

    if right_door_closed:
        pygame.draw.rect(screen, RED, (WIDTH-100,0,100,HEIGHT))
    else:
        pygame.draw.rect(screen, BLACK, (WIDTH-100,0,100,HEIGHT))

def draw_ui():
    power_text = font.render(f"Power: {power}%", True, GREEN)
    hour_text = font.render(f"{hour} AM", True, WHITE)

    screen.blit(power_text, (20,20))
    screen.blit(hour_text, (WIDTH-200,20))

def monster_ai():
    global monster_position, game_over

    if monster_position == "stage" and random.randint(0,1000) < 5:
        monster_position = "left_hall"

    elif monster_position == "left_hall":
        if not left_door_closed:
            monster_position = "office"
        else:
            monster_position = "stage"

    if monster_position == "office":
        game_over = True

while True:
    clock.tick(60)
    night_timer += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                left_door_closed = not left_door_closed
            if event.key == pygame.K_d:
                right_door_closed = not right_door_closed
            if event.key == pygame.K_SPACE:
                camera_on = not camera_on

    if not game_over and not win:

        # Power drain
        drain = 0.02
        if left_door_closed: drain += 0.05
        if right_door_closed: drain += 0.05
        if camera_on: drain += 0.03

        power -= drain

        if power <= 0:
            game_over = True

        # Time system
        if night_timer % 600 == 0:
            hour += 1
            if hour == 6:
                win = True

        monster_ai()

        draw_office()
        draw_ui()

        if camera_on:
            pygame.draw.rect(screen, BLACK, (200,100,500,400))
            cam_text = font.render("CAMERA FEED", True, WHITE)
            screen.blit(cam_text, (350,120))

            pos_text = font.render(f"Monster: {monster_position}", True, RED)
            screen.blit(pos_text, (300,200))

    elif game_over:
        screen.fill(RED)
        text = font.render("JUMPSCARE!", True, BLACK)
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2))

    elif win:
        screen.fill(BLACK)
        text = font.render("6 AM - YOU SURVIVED", True, GREEN)
        screen.blit(text, (WIDTH//2 - 250, HEIGHT//2))

    pygame.display.update()
