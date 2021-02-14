""" py_pong - pong style game with AI
Phil Jones - Feb 2021
Version 1.01 - Added AI to be beatable
version 1.02 - Improve AI to make it move the paddle to a home position in response to next shot
                Also stop paddle hunting when the ball is in P1s half
                Draw court
"""

import pygame
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
pygame.display.set_caption('py_pong V1.0.2')


# Game Functions
def draw_text(text, colour, x, y):
    text_surface = font.render(text, False, colour)
    screen.blit(text_surface, (x, y))


def draw_court():
    pygame.draw.line(screen, WHITE, (0, MARGIN), (WINDOW_WIDTH, MARGIN))
    pygame.draw.line(screen, WHITE, (WINDOW_WIDTH // 2, MARGIN), (WINDOW_WIDTH // 2, WINDOW_HEIGHT))
    pygame.draw.line(screen, WHITE, (0, WINDOW_HEIGHT - 1), (WINDOW_WIDTH, WINDOW_HEIGHT - 1))


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

        if self.rect.centery > ball.rect.bottom and self.rect.top > MARGIN:
            if ball.rect.centerx == 380:
                self.speed_ai = self.ai_speed_mixer()
            if not ball.hit_cpu_paddle and ball.rect.centerx < (WINDOW_WIDTH // 2):
                self.rect.move_ip(0, -1 * self.speed_ai)
            else:
                self.paddle_home()
        elif self.rect.centery < ball.rect.top and self.rect.bottom < WINDOW_HEIGHT:
            if ball.rect.centerx == 380:
                self.speed_ai = self.ai_speed_mixer()
            if not ball.hit_cpu_paddle and ball.rect.centerx < (WINDOW_WIDTH // 2):
                self.rect.move_ip(0, self.speed_ai)
            else:
                self.paddle_home()

    def ai_speed_mixer(self):
        # These need to be tweaked to make the AI harder or easier
        # Easy AI is 2.9, 5.5
        return random.uniform(3.5, 7.5)

    def paddle_home(self):
        if self.rect.centery < WINDOW_HEIGHT // 2:
            self.rect.move_ip(0, self.speed_ai)
        elif self.rect.centery > WINDOW_HEIGHT // 2:
            self.rect.move_ip(0, -1 * self.speed_ai)


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
            self.hit_cpu_paddle = True
            self.speed_x = - self.ball_speed_mixer()
            self.speed_x *= -1
        if self.rect.colliderect(player_paddle.rect):
            self.hit_cpu_paddle = False
            self.speed_x = self.ball_speed_mixer()
            self.speed_x *= -1

        # Move the ball
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Handy way to manage who has scored - or if 0 we're still in play
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
        self.hit_cpu_paddle = False

    def ball_speed_mixer(self):
        # These can be tweaked to give some un-predictable bounces
        # Be nice to add a feature where the speed changes depending where about on the paddle it's hit
        return random.uniform(3, 7)


# Create Paddles
player_paddle = Paddle(WINDOW_WIDTH - 40, WINDOW_HEIGHT // 2, WHITE, 80)
cpu_paddle = Paddle(40, WINDOW_HEIGHT // 2, WHITE, 80)

# Create Ball
ball = Ball(WINDOW_WIDTH - 80, WINDOW_HEIGHT // 2, RED, 6)

# Main loop
while start:
    # Set Frame Rate
    clock.tick(fps)

    # Erase Background
    screen.fill(BLACK)

    # Draw Scores to Screen with HUD divider
    draw_court()
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
        # And increment score
        if scored == -1:
            score_cpu += 1
            in_play = False
        elif scored == 1:
            score_player += 1
            in_play = False
    # We're not in play so someone scored
    # Display who the point went to
    else:
        if scored == 1:
            draw_text("POINT TO P1! PRESS SPACE TO SERVE..", RED, 105, MARGIN - 20)
            draw_text("P1: " + str(score_player), BLUE, WINDOW_WIDTH - 100, 5)
        elif scored == -1:
            draw_text("POINT TO CPU! PRESS SPACE TO SERVE..", RED, 100, MARGIN - 20)
            draw_text("CPU: " + str(score_cpu), RED, 20, 5)
        elif scored == 0:
            draw_text("PRESS SPACE TO SERVE..", RED, 150, MARGIN - 20)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and not in_play:
            ball.reset(WINDOW_WIDTH - 80, WINDOW_HEIGHT // 2, RED, 8)
            in_play = True
            scored = 0

    pygame.display.update()

