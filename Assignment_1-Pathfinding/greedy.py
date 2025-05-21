import heapq
from utilities import Grid

def run(filepath, heuristic='manhattan'):
    g = Grid(filepath)
    parent = {}  # Keeps track of each node's parent for path reconstruction
    open_heap = []  # Priority queue (min-heap) storing (heuristic value, node)
    closed = set()  # Set of visited nodes to avoid revisiting
    h = g.manhattan if heuristic == 'manhattan' else g.euclidean  # Choose heuristic function

    # Initial state is pushed with its heuristic score (h(start, goal))
    heapq.heappush(open_heap, (h(g.start, g.end), g.start))

    while open_heap:
        # Node with the lowest heuristic estimate is selected
        _, current = heapq.heappop(open_heap)

        if current in closed:
            continue

        closed.add(current)

        # If goal is reached, exit the loop
        if current == g.end:
            break

        # Explore each neighbor of the current node
        for neighbor in g.get_neighbors(*current):
            if neighbor not in closed:
                # Update parent pointer for path reconstruction
                parent[neighbor] = current

                # Score = h(n), where n = neighbor
                # This is the Greedy Best-First part: score is ONLY heuristic,
                # no actual path cost (g(n)) is tracked
                heapq.heappush(open_heap, (h(neighbor, g.end), neighbor))

    # Output file naming
    name = f"Greedy Best-First ({heuristic.title()})"
    filename = f"greedy_{heuristic.lower()}_output.txt"

    # Reconstruct and save output
    result = reconstruct(name, g, parent, closed, open_heap)
    write_output(g.grid, result['path'], closed, filename)
    return result


# Reconstruct the path from end to start using the parent pointers
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
        'cost': len(path) - 1,  # Total number of steps in path
        'explored': len(closed),  # How many nodes were visited
        'remaining': len(open_heap)  # Nodes still in grid space when goal found
    }

# Marks the path on the output grid with '.'
def mark_path(grid, path):
    for r, c in path:
        if grid[r][c] == '0':
            grid[r][c] = '.'

# Marks all explored but non-path nodes with '*'
def mark_explored(grid, path, closed):
    path_set = set(path)
    for r, c in closed:
        if (r, c) not in path_set and grid[r][c] == '0':
            grid[r][c] = '*'

# Writes final grid to a file with visual indicators
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
