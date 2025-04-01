import heapq

# A* Algorithm
def astar(maze, start, end):
    rows, cols = maze.shape
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: abs(start[0] - end[0]) + abs(start[1] - end[1])}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor] == 0:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1])
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

# Backtracking Algorithm
def backtracking_solve(maze, start, end):
    ROWS, COLS = maze.shape
    visited = set()
    path = []

    def backtrack(x, y):
        if (x, y) in visited or maze[x, y] == 1:
            return False
        visited.add((x, y))
        path.append((x, y))

        if (x, y) == end:
            return True

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            if backtrack(x + dx, y + dy):
                return True

        path.pop()
        return False

    backtrack(*start)
    return path