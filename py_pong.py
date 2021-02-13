""" py_pong - pong style game with AI
Phil Jones - Feb 2021
Version 1.01
"""

import pygame
import sys
import random

# Initialise Constants
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 0, 255)
CYAN = (0, 255, 255)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 600
MARGIN = 40


# Variables
start = True
fps = 60
score_player = 0
score_cpu = 0

# Pygame Initialise
pygame.init()
pygame.font.init()  # you have to call this at the start,
font = pygame.font.SysFont('Courier New', 20)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()


# Game Functions
def draw_text(text, colour, x, y):
    text_surface = font.render(text, False, colour)
    screen.blit(text_surface, (x, y))


def draw_hud():
    pygame.draw.line(screen, WHITE, (0, MARGIN), (WINDOW_WIDTH, MARGIN))


# Game Objects
class Paddle:
    def __init__(self, x, y, colour, length):
        self.x = x
        self.y = y
        self.length = length
        self.height = 10
        self.screen = screen
        self.colour = colour
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.height, self.length)

    def draw(self):
        pygame.draw.rect(self.screen, self.colour, self.rect, 0)

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top > MARGIN:
            self.rect.move_ip(0, -1 * self.speed)
        if key[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.move_ip(0, self.speed)


class Ball:
    def __init__(self, x, y, colour, size):
        self.x = x
        self.y = y
        self.screen = screen
        self.radius = size
        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)
        self.colour = colour
        self.speed_x = -4
        self.speed_y = 4

    def draw(self):
        pygame.draw.circle(screen, self.colour, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)


# Create Paddles
player_paddle = Paddle(WINDOW_WIDTH - 40, WINDOW_HEIGHT // 2, WHITE, 50)
cpu_paddle = Paddle(40, WINDOW_HEIGHT // 2, WHITE, 50)

# Create Ball
ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, RED, 10)

# Main loop
while start:
    # Set Frame Rate
    clock.tick(fps)

    # Erase Background
    screen.fill(BLACK)

    # Draw Scores to Screen with HUD divider
    draw_hud()
    draw_text("CPU: " + str(score_cpu), WHITE, 20, 5)
    draw_text("P1: " + str(score_player), WHITE, WINDOW_WIDTH - 100, 5)

    # Draw Paddles
    player_paddle.draw()
    cpu_paddle.draw()

    # Move Paddles
    player_paddle.move()

    # Draw Ball
    ball.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False

    pygame.display.update()

