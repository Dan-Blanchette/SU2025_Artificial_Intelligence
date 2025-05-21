from collections import deque
from utilities import Grid

def bfs(filepath):
    g = Grid(filepath)
    parent = {}
    open_list = deque([g.start])
    closed = set()

    while open_list:
        current = open_list.popleft()
        closed.add(current)
        if current == g.end:
            break
        for neighbor in g.get_neighbors(*current):
            if neighbor not in closed and neighbor not in open_list:
                parent[neighbor] = current
                open_list.append(neighbor)

    result = reconstruct("BFS", g, parent, closed, open_list)
    write_output(g.grid, result['path'], closed, "bfs_output.txt")
    return result

def reconstruct(name, g, parent, closed, open_list):
    current = g.end
    if current not in parent:
        return {'name': name, 'path': [], 'cost': "-", 'explored': len(closed), 'remaining': len(open_list)}
    path = []
    while current != g.start:
        path.append(current)
        current = parent[current]
    path.append(g.start)
    path.reverse()
    return {
        'name': name,
        'path': path,
        'cost': len(path) - 1,
        'explored': len(closed),
        'remaining': len(open_list)
    }

# Shared utilities
def mark_path(grid, path):
    for r, c in path:
        if grid[r][c] == '0':
            grid[r][c] = '.'

def mark_explored(grid, path, closed):
    path_set = set(path)
    for r, c in closed:
        if (r, c) not in path_set and grid[r][c] == '0':
            grid[r][c] = '*'

def write_output(grid, path, closed, filename):
    grid_copy = [row.copy() for row in grid]
    mark_path(grid_copy, path)
    mark_explored(grid_copy, path, closed)
    with open(filename, "w") as f:
        f.write("=== Final Grid with Path and Explored States ===\n")
        for row in grid_copy:
            f.write(''.join(row) + '\n')
        f.write("\n=== Legend ===\n")
        f.write("S = Start\nE = End\n0 = Unvisited walkable space\n")
        f.write("X = Wall/blocked cell\n'.' = Final path from S to E\n'*' = Explored during search\n")
