#!/usr/bin/env python3
"""
Simple Tetris Game
A classic Tetris implementation in Python using pygame.
"""

import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]


class Tetromino:
    def __init__(self):
        self.shape_index = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_index]
        self.color = SHAPE_COLORS[self.shape_index]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        """Rotate the tetromino 90 degrees clockwise"""
        self.shape = list(zip(*self.shape[::-1]))


class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.game_over = False
        self.score = 0
        self.fall_time = 0
        self.fall_speed = 500  # milliseconds

    def check_collision(self, piece, offset_x=0, offset_y=0):
        """Check if the piece collides with the grid or boundaries"""
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x + offset_x
                    new_y = piece.y + y + offset_y

                    # Check boundaries
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return True

                    # Check grid collision
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return True
        return False

    def lock_piece(self):
        """Lock the current piece into the grid"""
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_x = self.current_piece.x + x
                    grid_y = self.current_piece.y + y
                    if grid_y >= 0:
                        self.grid[grid_y][grid_x] = self.current_piece.color

    def clear_lines(self):
        """Clear completed lines and update score"""
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
            else:
                y -= 1

        if lines_cleared > 0:
            self.score += lines_cleared * 100

    def move(self, dx, dy):
        """Move the current piece"""
        if not self.check_collision(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False

    def rotate_piece(self):
        """Rotate the current piece"""
        old_shape = self.current_piece.shape
        self.current_piece.rotate()

        if self.check_collision(self.current_piece):
            self.current_piece.shape = old_shape

    def drop_piece(self):
        """Drop the piece all the way down"""
        while self.move(0, 1):
            pass

    def draw_grid(self):
        """Draw the grid and locked pieces"""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, self.grid[y][x], rect)
                pygame.draw.rect(self.screen, GRAY, rect, 1)

    def draw_piece(self, piece):
        """Draw the current piece"""
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        (piece.x + x) * BLOCK_SIZE,
                        (piece.y + y) * BLOCK_SIZE,
                        BLOCK_SIZE,
                        BLOCK_SIZE
                    )
                    pygame.draw.rect(self.screen, piece.color, rect)
                    pygame.draw.rect(self.screen, GRAY, rect, 1)

    def draw_text(self, text, size, color, x, y):
        """Draw text on screen"""
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def run(self):
        """Main game loop"""
        while not self.game_over:
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        self.move(0, 1)
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        self.drop_piece()

            # Auto fall
            if self.fall_time >= self.fall_speed:
                self.fall_time = 0
                if not self.move(0, 1):
                    self.lock_piece()
                    self.clear_lines()
                    self.current_piece = Tetromino()

                    # Check game over
                    if self.check_collision(self.current_piece):
                        self.game_over = True

            # Draw everything
            self.screen.fill(BLACK)
            self.draw_grid()
            self.draw_piece(self.current_piece)
            self.draw_text(f'Score: {self.score}', 30, WHITE, SCREEN_WIDTH // 2, 10)
            pygame.display.flip()

        # Game over screen
        self.screen.fill(BLACK)
        self.draw_text('GAME OVER', 50, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
        self.draw_text(f'Final Score: {self.score}', 30, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.draw_text('Press any key to exit', 25, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        pygame.display.flip()

        # Wait for key press to exit
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    waiting = False

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    print("Starting Tetris...")
    print("Controls:")
    print("  LEFT/RIGHT: Move piece")
    print("  DOWN: Soft drop")
    print("  UP: Rotate piece")
    print("  SPACE: Hard drop")
    print()

    game = Tetris()
    game.run()
