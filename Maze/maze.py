import numpy as np
import random

def generate_maze(rows, cols):
    # Create a maze grid initialized to walls (1)
    maze = np.ones((rows, cols), dtype=int)
    stack = [(1, 1)]
    maze[1, 1] = 0  # Starting point

    # Function to get neighbors to explore
    def neighbors(x, y):
        dirs = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Directions to explore
        random.shuffle(dirs)
        return [(x + dx, y + dy, x + dx // 2, y + dy // 2) for dx, dy in dirs]

    # Maze generation using backtracking algorithm
    while stack:
        x, y = stack[-1]
        valid_neighbors = [(nx, ny, mx, my) for nx, ny, mx, my in neighbors(x, y)
                           if 0 <= nx < rows and 0 <= ny < cols and maze[nx, ny] == 1]
        if valid_neighbors:
            nx, ny, mx, my = valid_neighbors.pop()
            maze[mx, my] = 0  # Remove wall
            maze[nx, ny] = 0   # Remove wall
            stack.append((nx, ny))
        else:
            stack.pop()  # Backtrack if no valid neighbors
    
    # Ensure the exit point is always reachable
    maze[rows - 2, cols - 2] = 0  # Exit point
    # Check if the exit is blocked and un-block if necessary
    if maze[rows - 3, cols - 2] == 1 and maze[rows - 2, cols - 3] == 1:
        maze[rows - 3, cols - 2] = 0  # Create a path if blocked
    
    return maze