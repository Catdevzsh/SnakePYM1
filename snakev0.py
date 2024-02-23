import pygame
import sys
import random
from array import array

# Initialize Pygame and Pygame Mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Frame rate
clock = pygame.time.Clock()
FPS = 10

# Snake settings
snake_pos = [[100, 50], [90, 50], [80, 50]]  # Initial snake position
snake_direction = 'RIGHT'
change_to = snake_direction

# Food
food_pos = [random.randrange(1, (SCREEN_WIDTH//10)) * 10, random.randrange(1, (SCREEN_HEIGHT//10)) * 10]
food_spawn = True

# Score
score = 0

# Sound effects
def generate_square_wave(frequency=440, volume=0.1):
    period = int(round(22050 / frequency))
    amplitude = 2 ** (abs(-16) - 1) - 1
    samples = array('h', [amplitude if time < period / 2 else -amplitude for time in range(period)] * int(22050 / period))
    sound = pygame.mixer.Sound(buffer=samples)
    sound.set_volume(volume)
    return sound

eat_sound = generate_square_wave(880, 0.1)
game_over_sound = generate_square_wave(440, 0.1)

# Function to check for direction change
def change_direction(to):
    global snake_direction
    if to == 'RIGHT' and not snake_direction == 'LEFT':
        snake_direction = 'RIGHT'
    if to == 'LEFT' and not snake_direction == 'RIGHT':
        snake_direction = 'LEFT'
    if to == 'UP' and not snake_direction == 'DOWN':
        snake_direction = 'UP'
    if to == 'DOWN' and not snake_direction == 'UP':
        snake_direction = 'DOWN'

# Function to update snake position
def update_snake():
    global score, food_spawn
    # Update snake position
    if snake_direction == 'RIGHT':
        snake_pos.insert(0, [snake_pos[0][0] + 10, snake_pos[0][1]])
    if snake_direction == 'LEFT':
        snake_pos.insert(0, [snake_pos[0][0] - 10, snake_pos[0][1]])
    if snake_direction == 'UP':
        snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] - 10])
    if snake_direction == 'DOWN':
        snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] + 10])
    
    # Snake eating food
    if snake_pos[0] == food_pos:
        score += 1
        food_spawn = False
        eat_sound.play()
    else:
        snake_pos.pop()
    
    # Respawn food
    if not food_spawn:
        food_pos[:] = [random.randrange(1, (SCREEN_WIDTH//10)) * 10, random.randrange(1, (SCREEN_HEIGHT//10)) * 10]
    food_spawn = True

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
    
    # Change direction
    change_direction(change_to)
    
    # Update snake position
    update_snake()
    
    # Game Over conditions
    if snake_pos[0][0] >= SCREEN_WIDTH or snake_pos[0][0] < 0 or snake_pos[0][1] >= SCREEN_HEIGHT or snake_pos[0][1] < 0:
        game_over_sound.play()
        pygame.time.wait(1000)  # Wait a second for sound to finish
        running = False
    for block in snake_pos[1:]:
        if snake_pos[0] == block:
            game_over_sound.play()
            pygame.time.wait(1000)  # Wait a second for sound to finish
            running = False
    
    # Drawing
    screen.fill(BLACK)
    for pos in snake_pos:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
    
    # Update screen and clock
    pygame.display.flip()
    clock.tick(FPS)

# Clean up
pygame.quit()
sys.exit()
