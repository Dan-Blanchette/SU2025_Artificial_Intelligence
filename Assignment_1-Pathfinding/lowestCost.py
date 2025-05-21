import heapq
from utilities import Grid

def run(filepath):
    g = Grid(filepath)
    parent = {}
    open_heap = [(0, g.start)]
    cost_so_far = {g.start: 0}
    closed = set()

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        closed.add(current)
        if current == g.end:
            break
        for neighbor in g.get_neighbors(*current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(open_heap, (new_cost, neighbor))
                parent[neighbor] = current

    result = reconstruct("Dijkstra (Lowest Cost)", g, parent, closed, open_heap)
    write_output(g.grid, result['path'], closed, "dijkstra_output.txt")
    return result

# Reconstruct and utilities same as in bfs.py
def reconstruct(name, g, parent, closed, open_heap):
    current = g.end
    if current not in parent:
        return {'name': name, 'path': [], 'cost': "-", 'explored': len(closed), 'remaining': len(open_heap)}
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
        'remaining': len(open_heap)
    }

# Utilities 
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