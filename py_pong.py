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
scored = 0  # score state - Ball.move method returns 1 for player score or -1 if CPU scores
in_play = False

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
        self.speed = 8
        self.speed_ai = 4.5
        self.rect = pygame.Rect(self.x, self.y, self.height, self.length)

    def draw(self):
        pygame.draw.rect(self.screen, self.colour, self.rect, 0)

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top > MARGIN:
            self.rect.move_ip(0, -1 * self.speed)
        if key[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT:
            self.rect.move_ip(0, self.speed)

    def ai_move(self):
        # To make the AI possible to defeat we need to mix it's response speed up
        # And on occasions make it too slow to return the ball
        # if the ball is in the players half randomise the CPU response speed
        #ai_response_speed = self.speed_ai
        #print(ball.rect.centerx)

        if self.rect.centery > ball.rect.bottom and self.rect.top > MARGIN:
            if ball.rect.centerx == 380:
                self.speed_ai = self.ai_speed_mixer()
            #print(self.speed_ai)
            self.rect.move_ip(0, -1 * self.speed_ai)
        elif self.rect.centery < ball.rect.top and self.rect.bottom < WINDOW_HEIGHT:
            if ball.rect.centerx == 380:
                self.speed_ai = self.ai_speed_mixer()
            #print(self.speed_ai)
            self.rect.move_ip(0, self.speed_ai)

    def ai_speed_mixer(self):
        return random.uniform(2.9, 5.5)


class Ball:
    def __init__(self, x, y, colour, size):
        self.reset(x, y, colour, size)

    def draw(self):
        pygame.draw.circle(screen, self.colour, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)

    def move(self):
        # Check collision with walls
        if self.rect.top < MARGIN:
            self.speed_y = - self.ball_speed_mixer()
            self.speed_y *= -1
        if self.rect.bottom > WINDOW_HEIGHT:
            self.speed_y = self.ball_speed_mixer()
            self.speed_y *= -1
        # Out of bounds
        if self.rect.left < 0:
            self.scored = 1
        if self.rect.right > WINDOW_WIDTH:
            self.scored = -1

        # Collides with paddles
        if self.rect.colliderect(cpu_paddle.rect):
            self.speed_x = - self.ball_speed_mixer()
            print(self.speed_x)
            self.speed_x *= -1
        if self.rect.colliderect(player_paddle.rect):
            self.speed_x = self.ball_speed_mixer()
            print(self.speed_x)
            self.speed_x *= -1

        # Move the ball
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        return self.scored

    def reset(self, x, y, colour, size):
        self.x = x
        self.y = y
        self.screen = screen
        self.radius = size
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        self.colour = colour
        self.speed_x = -4
        self.speed_y = 4
        self.scored = 0

    def ball_speed_mixer(self):
        return random.uniform(3, 7)


# Create Paddles
player_paddle = Paddle(WINDOW_WIDTH - 40, WINDOW_HEIGHT // 2, WHITE, 80)
cpu_paddle = Paddle(40, WINDOW_HEIGHT // 2, WHITE, 80)

# Create Ball
ball = Ball(WINDOW_WIDTH - 60, WINDOW_HEIGHT // 2, RED, 6)

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

    if in_play and scored == 0:
        # Move Paddles
        player_paddle.move()
        cpu_paddle.ai_move()

        # Draw Ball
        ball.draw()

        # Move Ball
        scored = ball.move()

        # Check scored state
        if scored == -1:
            score_cpu += 1
            in_play = False
        elif scored == 1:
            score_player += 1
            in_play = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            ball.reset(WINDOW_WIDTH - 60, WINDOW_HEIGHT // 2, RED, 8)
            in_play = True
            scored = 0

    pygame.display.update()

