import heapq
from utilities import Grid

def run(filepath, heuristic='manhattan'):
    g = Grid(filepath)
    parent = {}
    g_cost = {g.start: 0}
    open_heap = []
    closed = set()
    h = g.manhattan if heuristic == 'manhattan' else g.euclidean

    heapq.heappush(open_heap, (h(g.start, g.end), g.start))

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        closed.add(current)
        if current == g.end:
            break
        for neighbor in g.get_neighbors(*current):
            tentative_g = g_cost[current] + 1
            if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                g_cost[neighbor] = tentative_g
                f_score = tentative_g + h(neighbor, g.end)
                heapq.heappush(open_heap, (f_score, neighbor))
                parent[neighbor] = current

    name = f"A* ({heuristic.title()})"
    filename = f"astar_{heuristic.lower()}_output.txt"
    result = reconstruct(name, g, parent, closed, open_heap)
    write_output(g.grid, result['path'], closed, filename)
    return result

# Reconstruct & utilities
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