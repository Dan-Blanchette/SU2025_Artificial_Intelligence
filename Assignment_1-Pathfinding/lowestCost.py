import heapq
from utilities import Grid

def run(filepath):
    g = Grid(filepath)  # Load grid: includes map, start, and end
    parent = {}  # For reconstructing the path at the end
    open_heap = [(0, g.start)]  # Priority queue storing (cumulative cost, node)
    cost_so_far = {g.start: 0}  # Maps each node to the lowest known cost to reach it
    closed = set()  # Visited/explored nodes

    while open_heap:
        # Get the node with the lowest known path cost so far
        _, current = heapq.heappop(open_heap)

        if current in closed:
            continue
        closed.add(current)

        # Stop the search once the end is reached
        if current == g.end:
            break

        # Check each neighbor of the current node
        for neighbor in g.get_neighbors(*current):
            # Assuming uniform step cost of 1
            new_cost = cost_so_far[current] + 1

            # If this path is better than any previously recorded path
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost  # Update cost
                heapq.heappush(open_heap, (new_cost, neighbor))  # Prioritize cheaper paths
                parent[neighbor] = current  # Track the path

    # Reconstruct and output result
    result = reconstruct("Dijkstra (Lowest Cost)", g, parent, closed, open_heap)
    write_output(g.grid, result['path'], closed, "lowestCost_output.txt")
    return result


# Reconstructs the path from the end node to the start node using parent pointers
def reconstruct(name, g, parent, closed, open_heap):
    current = g.end

    # If the goal was not reached (not in parent), return empty results
    if current not in parent:
        return {
            'name': name,
            'path': [],
            'cost': "-",
            'explored': len(closed),
            'remaining': len(open_heap)
        }

    path = []
    while current != g.start:
        path.append(current)
        current = parent[current]
    path.append(g.start)
    path.reverse()  # Reverse to get start → end order

    return {
        'name': name,
        'path': path,
        'cost': len(path) - 1,  # Total number of steps from start to end
        'explored': len(closed),
        'remaining': len(open_heap)
    }


# Marks the final path on the grid with '.'
def mark_path(grid, path):
    for r, c in path:
        if grid[r][c] == '0':
            grid[r][c] = '.'


# Marks all visited (explored) cells not on the final path with '*'
def mark_explored(grid, path, closed):
    path_set = set(path)
    for r, c in closed:
        if (r, c) not in path_set and grid[r][c] == '0':
            grid[r][c] = '*'


# Writes the final grid state to a file for visualization
def write_output(grid, path, closed, filename):
    grid_copy = [row.copy() for row in grid]  # Copy grid so original isn't altered
    mark_path(grid_copy, path)
    mark_explored(grid_copy, path, closed)
    with open(filename, "w") as f:
        f.write("=== Final Grid with Path and Explored States ===\n")
        for row in grid_copy:
            f.write(''.join(row) + '\n')
        f.write("\n=== Legend ===\n")
        f.write("S = Start\nE = End\n0 = Unvisited walkable space\n")
        f.write("X = Wall/blocked cell\n'.' = Final path from S to E\n'*' = Explored during search\n")
