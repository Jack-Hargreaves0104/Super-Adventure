import pygame
import sys

def handle_vertical_movement(char_x, char_y, char_width, char_height, char_vel_y, platforms, height):
    on_ground = False
    pixels_to_move = int(char_vel_y)
    remainder = char_vel_y - pixels_to_move

    for _ in range(abs(pixels_to_move)):
        char_y += 1 if pixels_to_move > 0 else -1
        char_rect = pygame.Rect(char_x, char_y, char_width, char_height)
        if char_y + char_height >= height:
            char_y = height - char_height
            char_vel_y = 0
            on_ground = True
            break
        for plat in platforms:
            if char_rect.colliderect(plat) and pixels_to_move > 0:
                char_y = plat.top - char_height
                char_vel_y = 0
                on_ground = True
                break
        if on_ground:
            break

    char_y += remainder
    char_rect = pygame.Rect(char_x, char_y, char_width, char_height)
    return char_y, char_vel_y, on_ground, char_rect

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Super Adventure!")

# Load your sprite image at original size
sprite_original = pygame.image.load("greenGuy.png").convert_alpha()
sprite = pygame.transform.scale(
    sprite_original,
    (sprite_original.get_width(), sprite_original.get_height())
)
char_width = sprite.get_width()
char_height = sprite.get_height()
char_x = width // 2
char_y = height // 2
char_speed = 5

char_vel_y = 0           # Vertical velocity
gravity = 0.5            # Gravity strength

# Define platforms as a list of pygame.Rect objects
platforms = [
    pygame.Rect(100, 500, 400, 40),
    pygame.Rect(550, 350, 200, 40),
    pygame.Rect(50, 200, 300, 40)
]

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        char_x -= char_speed
    if keys[pygame.K_RIGHT]:
        char_x += char_speed

    char_vel_y += gravity
    char_vel_y = min(char_vel_y, 20)  # Cap fall speed

    char_y, char_vel_y, on_ground, char_rect = handle_vertical_movement(
        char_x, char_y, char_width, char_height, char_vel_y, platforms, height
    )

    # Optional: Jumping
    if keys[pygame.K_UP] and on_ground:
        char_vel_y = -15  # Jump strength

    window.fill((30, 30, 30))
    window.blit(sprite, (char_x, char_y))  # Draw your sprite

    # Draw platforms
    for plat in platforms:
        pygame.draw.rect(window, (100, 200, 100), plat)

    pygame.draw.rect(window, (255, 0, 0), char_rect, 2)  # Red collision box

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second

pygame.quit()
sys.exit()