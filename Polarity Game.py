import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Polarity Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

# Font setup
font = pygame.font.Font(None, 36)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5
        self.polarity = 1  # 1 for positive (red), -1 for negative (blue)
        self.last_polarity_switch = pygame.time.get_ticks()  # Time since the last polarity switch

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Switch polarity
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and current_time - self.last_polarity_switch > 200:  # Add a small delay to prevent rapid switching
            self.polarity *= -1
            self.last_polarity_switch = current_time
            # Change color based on polarity
            if self.polarity == 1:
                self.image.fill(RED)
                print("Polarity changed to positive (RED)")
            else:
                self.image.fill(BLUE)
                print("Polarity changed to negative (BLUE)")

        # Check for collisions with platforms
        collided_platforms = pygame.sprite.spritecollide(self, platforms, False)
        for platform in collided_platforms:
            if (self.polarity == 1 and platform.color == BLUE) or (self.polarity == -1 and platform.color == RED):
                return True  # Collision with wrong polarity
        return False

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((100, 20))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Levels with mandatory polarity-switching barriers
levels = [
    [
        Platform(200, 500, RED), Platform(400, 400, BLUE),
        Platform(200, 300, RED), Platform(400, 200, BLUE)
    ],
    [
        Platform(100, 500, BLUE), Platform(300, 400, RED),
        Platform(500, 300, BLUE), Platform(300, 200, RED)
    ],
    [
        Platform(150, 500, RED), Platform(350, 400, BLUE),
        Platform(550, 300, RED), Platform(350, 200, BLUE)
    ]
]

current_level = 0
score = 0

# Load level function
def load_level(level):
    global all_sprites, platforms
    all_sprites.empty()
    platforms.empty()
    all_sprites.add(player)
    for platform in level:
        platforms.add(platform)
        all_sprites.add(platform)
    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
    print(f"Loaded level {current_level + 1}")

# Load the first level
load_level(levels[current_level])

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sprites
    all_sprites.update(platforms)

    # Check for collisions with wrong polarity
    if player.update(platforms):
        score = 0
        current_level = 0
        load_level(levels[current_level])
        continue

    # Check if player reached the end of the level
    if player.rect.y < 0:
        score += 10
        current_level += 1
        if current_level >= len(levels):
            print("You won the game with a score of:", score)
            running = False
        else:
            load_level(levels[current_level])

    # Draw everything
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Display level
    level_text = font.render(f"Level: {current_level + 1}", True, WHITE)
    screen.blit(level_text, (10, 50))

    # Display instructions
    instructions_text = font.render("Use arrow keys to move, spacebar to switch polarity", True, WHITE)
    screen.blit(instructions_text, (10, SCREEN_HEIGHT - 30))

    # Refresh the screen
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
