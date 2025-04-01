import pygame
import numpy as np
import time
import os
from maze import generate_maze
from pathfinding import astar

# Constants
CELL_SIZE = 20  # size of each cell in the grid
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PLAYER_COLOR = (255, 0, 0)
TEXT_COLOR = (0, 0, 255)
AUTO_SOLVE_COLOR = (255, 165, 0)
LEADERBOARD_FILE = "scores.txt"

# Initialize Pygame
pygame.init()

# Global screen variable
screen = None  # Will be initialized in the main loop

def set_screen_size(rows, cols):
    global screen
    screen = pygame.display.set_mode((cols * CELL_SIZE, rows * CELL_SIZE))

# Generate Maze
def generate_game(level):
    if level == "Easy":
        size = 25
    elif level == "Medium":
        size = 25
    else:
        size = 30
    return generate_maze(size, size), (1, 1), (size-2, size-2)

# Leaderboard Functions
def save_score(time_taken):
    with open(LEADERBOARD_FILE, "a") as file:
        file.write(f"{time_taken:.2f}\n")

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as file:
        scores = [float(line.strip()) for line in file.readlines()]
    return sorted(scores)[:5]  # Show top 5 scores

# Draw Functions
def draw_text(text, x, y, color=TEXT_COLOR):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_maze(maze, start, end, player_pos, auto_solve, solution_path, is_winning):
    rows, cols = maze.shape
    screen.fill(WHITE)
    
    # Draw each cell in the maze
    for x in range(rows):
        for y in range(cols):
            color = BLACK if maze[x, y] == 1 else WHITE
            pygame.draw.rect(screen, color, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw start point (blue) and end point (green)
    pygame.draw.rect(screen, BLUE, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw the exit (green) and keep it green if the player wins
    if is_winning:
        pygame.draw.rect(screen, GREEN, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    else:
        pygame.draw.rect(screen, GREEN, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw the auto-solve path if enabled
    if auto_solve and solution_path:
        for (px, py) in solution_path:
            pygame.draw.rect(screen, AUTO_SOLVE_COLOR, (py * CELL_SIZE, px * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    
    # Draw the player
    pygame.draw.rect(screen, PLAYER_COLOR, (player_pos[1] * CELL_SIZE, player_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def show_leaderboard():
    screen.fill(WHITE)
    draw_text("Leaderboard (Top Scores)", 150, 50)
    scores = load_leaderboard()
    if scores:
        for i, score in enumerate(scores, start=1):
            draw_text(f"{i}. {score} sec", 150, 100 + (i * 40))
    else:
        draw_text("No scores yet!", 150, 150)
    draw_text("Press any key to return", 150, 500)
    pygame.display.update()
    wait_for_key()

def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                return

def game_over_menu(time_taken):
    save_score(time_taken)  # Store the player's time
    while True:
        screen.fill(WHITE)
        draw_text(f"You Won! Time: {time_taken:.2f} sec", 100, 100)
        draw_text("1. Restart", 100, 200)
        draw_text("2. Back to Menu", 100, 250)
        draw_text("3. Quit", 100, 300)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "restart"
                elif event.key == pygame.K_2:
                    return "menu"
                elif event.key == pygame.K_3:
                    pygame.quit()
                    exit()

def game_loop(level):
    maze, start, end = generate_game(level)
    player_x, player_y = start
    auto_solve = False
    solution_path = []
    is_winning = False
    start_time = time.time()
    rows, cols = maze.shape
    set_screen_size(rows, cols)  # Set screen size dynamically
    running = True

    while running:
        draw_maze(maze, start, end, (player_x, player_y), auto_solve, solution_path, is_winning)
        draw_text(f"Time: {time.time() - start_time:.2f} sec", 10, 10)
        pygame.display.update()

        # Auto-solve mode
        if auto_solve and solution_path:
            for (px, py) in solution_path:
                player_x, player_y = px, py
                draw_maze(maze, start, end, (player_x, player_y), auto_solve, solution_path, is_winning)
                pygame.display.update()
                pygame.time.delay(100)
            total_time = time.time() - start_time
            return game_over_menu(total_time)

        # Player input handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_s:
                    auto_solve = True
                    solution_path = astar(maze, start, end)
                else:
                    new_x, new_y = player_x, player_y
                    if event.key == pygame.K_UP:
                        new_x -= 1
                    elif event.key == pygame.K_DOWN:
                        new_x += 1
                    elif event.key == pygame.K_LEFT:
                        new_y -= 1
                    elif event.key == pygame.K_RIGHT:
                        new_y += 1
                    if 0 <= new_x < maze.shape[0] and 0 <= new_y < maze.shape[1] and maze[new_x, new_y] == 0:
                        player_x, player_y = new_x, new_y
                    if (player_x, player_y) == end:
                        is_winning = True
                        total_time = time.time() - start_time
                        return game_over_menu(total_time)

def choose_level():
    while True:
        screen.fill(WHITE)
        draw_text("Choose Difficulty Level:", 150, 100)
        draw_text("1. Easy", 150, 200)
        draw_text("2. Medium", 150, 250)
        draw_text("3. Hard", 150, 300)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "Easy"
                elif event.key == pygame.K_2:
                    return "Medium"
                elif event.key == pygame.K_3:
                    return "Hard"

def main_menu():
    set_screen_size(30 ,30)  # Set default size for the menu
    while True:
        screen.fill(WHITE)
        draw_text("Maze Game", 200, 100)
        draw_text("1. Start Game", 200, 200)
        draw_text("2. Leaderboard", 200, 250)
        draw_text("3. Quit", 200, 300)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "start"
                elif event.key == pygame.K_2:
                    return "leaderboard"
                elif event.key == pygame.K_3:
                    pygame.quit()
                    exit()

# Main Loop
while True:
    menu_choice = main_menu()
    if menu_choice == "leaderboard":
        show_leaderboard()
    elif menu_choice == "start":
        level = choose_level()
        while True:
            result = game_loop(level)
            if result == "menu":
                break
            elif result == "restart":
                break
