import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT = pygame.font.SysFont("Arial", 30)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Clock for frame rate control
clock = pygame.time.Clock()


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.gravity = 0.5
        self.jump_strength = -7

    def jump(self):
        self.vel = self.jump_strength

    def move(self):
        self.vel += self.gravity
        self.y += self.vel

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (self.x, int(self.y)), 15)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 50
        self.gap = 150
        self.top_height = random.randint(100, 300)
        self.bottom_height = HEIGHT - (self.top_height + self.gap)
        self.speed = 3
        self.passed = False

    def move(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top_height))
        pygame.draw.rect(screen, GREEN, (self.x, HEIGHT - self.bottom_height, self.width, self.bottom_height))

    def collide(self, bird):
        if bird.x + 15 > self.x and bird.x - 15 < self.x + self.width:
            if bird.y - 15 < self.top_height or bird.y + 15 > HEIGHT - self.bottom_height:
                return True
        return False


# Initialize game objects
bird = Bird(WIDTH // 4, HEIGHT // 2)
pipes = [Pipe(WIDTH)]
score = 0
running = True

# Game Loop
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    bird.move()

    if pipes[-1].x < WIDTH // 2:
        pipes.append(Pipe(WIDTH))

    for pipe in pipes:
        pipe.move()
        pipe.draw(screen)
        if pipe.collide(bird):
            running = False  # Game over if collision
        if not pipe.passed and bird.x > pipe.x + pipe.width:
            pipe.passed = True  # Score when bird crosses pipe
            score += 1

    if bird.y > HEIGHT or bird.y < 0:
        running = False  # Game over if bird falls or flies too high

    bird.draw(screen)

    # Display Score
    score_text = FONT.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(20)  # Control frame rate

# Game Over Screen
screen.fill(WHITE)
game_over_text = FONT.render("Game Over!", True, (255, 0, 0))
final_score_text = FONT.render(f"Final Score: {score}", True, (0, 0, 0))
screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 3))
screen.blit(final_score_text, (WIDTH // 4, HEIGHT // 2))
pygame.display.update()
pygame.time.delay(3000)  # Show for 3 seconds

pygame.quit()