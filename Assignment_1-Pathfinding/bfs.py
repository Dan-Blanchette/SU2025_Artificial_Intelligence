from collections import deque
from utilities import Grid

def bfs(filepath):
    g = Grid(filepath)  # Load the grid from file (walls, start, end, etc.)
    parent = {}  # Tracks each node's predecessor for reconstructing the path
    open_list = deque([g.start])  # BFS uses a queue (FIFO) for the frontier
    closed = set()  # Set of already visited nodes

    while open_list:
        # Pop the oldest node added to the queue (FIFO order)
        current = open_list.popleft()
        closed.add(current)

        # Stop when goal is reached
        if current == g.end:
            break

        # Look at each valid neighbor of the current node
        for neighbor in g.get_neighbors(*current):
            # Only add unexplored neighbors to the queue
            if neighbor not in closed and neighbor not in open_list:
                parent[neighbor] = current  # Track how we got to this node
                open_list.append(neighbor)  # Add neighbor to be explored later

    # Once the search is complete, reconstruct and output the result
    result = reconstruct("BFS", g, parent, closed, open_list)
    write_output(g.grid, result['path'], closed, "bfs_output.txt")
    return result


# Reconstructs the path from goal to start using parent links
def reconstruct(name, g, parent, closed, open_list):
    current = g.end

    # If the goal was never reached, return empty path
    if current not in parent:
        return {'name': name, 'path': [], 'cost': "-", 'explored': len(closed), 'remaining': len(open_list)}

    # Walk backwards from the goal to the start
    path = []
    while current != g.start:
        path.append(current)
        current = parent[current]
    path.append(g.start)
    path.reverse()  # Convert from end-to-start to start-to-end

    return {
        'name': name,
        'path': path,
        'cost': len(path) - 1,  # Cost is number of steps in the path
        'explored': len(closed),  # Total number of nodes explored
        'remaining': len(open_list)  # Nodes left in queue after termination
    }


# Marks the final path on the grid using '.'
def mark_path(grid, path):
    for r, c in path:
        if grid[r][c] == '0':
            grid[r][c] = '.'


# Marks all explored (but non-path) nodes with '*'
def mark_explored(grid, path, closed):
    path_set = set(path)
    for r, c in closed:
        if (r, c) not in path_set and grid[r][c] == '0':
            grid[r][c] = '*'


# Writes the modified grid to a text file for visualization
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
