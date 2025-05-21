from collections import deque  # Used for fast FIFO queue in BFS

class BFSPathFinder:
    # === Member Function Block ===
    def __init__(self, filepath):
        # === Load the map/grid from a file ===
        with open(filepath, 'r') as f:
            self.grid = [list(line.strip()) for line in f if line.strip()]

        # Grid dimensions
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        # Locate start ('S') and end ('E') positions
        self.start = self.find_char('S')
        self.end = self.find_char('E')

        # For tracking the search process
        self.parent = {}              # Maps each node to its parent node
        self.open_list = deque()      # Queue for BFS exploration
        self.closed_list = set()      # Set of already explored nodes

        # Search statistics
        self.path_length = 0
        self.path_cost = 0

    def find_char(self, char):
        # === Locate a character in the grid (e.g., 'S' or 'E') ===
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == char:
                    return (r, c)
        raise ValueError(f"Character '{char}' not found in grid.")

    def in_bounds(self, r, c):
        # === Check if (r, c) is within the grid bounds ===
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_walkable(self, r, c):
        # === Check if the cell is walkable (not a wall) ===
        return self.grid[r][c] in ['0', 'E']

    def get_neighbors(self, r, c):
        # === Yield valid, walkable neighbors (up/down/left/right) ===
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc) and self.is_walkable(nr, nc):
                yield (nr, nc)

    def search(self):
        # === Perform BFS to find shortest path from start to end ===
        self.open_list.append(self.start)

        while self.open_list:
            current = self.open_list.popleft()  # Get the next node to explore
            self.closed_list.add(current)       # Mark it as explored

            if current == self.end:
                return self.reconstruct_path()  # Found the goal, build the path

            for neighbor in self.get_neighbors(*current):
                if neighbor not in self.closed_list and neighbor not in self.open_list:
                    self.parent[neighbor] = current
                    self.open_list.append(neighbor)

        return None  # No path found

    def reconstruct_path(self):
        # === Rebuild the path from end to start using the parent map ===
        path = []
        current = self.end

        while current != self.start:
            path.append(current)               # Add current node
            current = self.parent[current]     # Move backward to the parent

        path.append(self.start)                # Finally add the start node
        path.reverse()                         # Reverse to get start -> end

        self.path_length = len(path)
        self.path_cost = len(path) - 1         # Each step = 1 cost
        return path

    def mark_path(self, path):
        # === Mark the final path on the grid with '.' ===
        for r, c in path:
            if self.grid[r][c] == '0':         # Don't overwrite S or E
                self.grid[r][c] = '.'

    def mark_explored(self):
        # === Mark explored (visited) nodes with '*' ===
        for r, c in self.closed_list:
            if self.grid[r][c] == '0':
                self.grid[r][c] = '*'

    def print_grid(self):
        # === Print the current state of the grid ===
        for row in self.grid:
            print(''.join(row))

    def print_stats(self):
        # === Print BFS statistics and summary ===
        print("\n Pathfinding Summary (All Algorithms)")
        print(f"{'Algorithm':<25} {'Path Len':<10} {'Cost':<10} {'Explored':<12} {'Remaining'}")
        print("-" * 65)
        print(f"{'BFS':<25} {self.path_length:<10} {self.path_cost:<10} {len(self.closed_list):<12} {len(self.open_list)}")
        print(f"{'Lowest Cost':<25} {'-':<10} {'-':<10} {'-':<12} {'-'}")
        print(f"{'Greedy Best-First':<25} {'-':<10} {'-':<10} {'-':<12} {'-'}")
        print(f"{'A* (Heuristic 1)':<25} {'-':<10} {'-':<10} {'-':<12} {'-'}")
        print(f"{'A* (Heuristic 2)':<25} {'-':<10} {'-':<10} {'-':<12} {'-'}")

    def write_output(self, filename="output.txt"):
        # === Save the final grid, legend, and stats to a text file ===
        with open(filename, 'w') as f:
            f.write("=== Final Grid with Path and Explored States ===\n")
            for row in self.grid:
                f.write(''.join(row) + '\n')

            f.write("\n=== Legend ===\n")
            f.write("S = Start\n")
            f.write("E = End\n")
            f.write("0 = Unvisited walkable space\n")
            f.write("1 = Wall/blocked cell\n")
            f.write("'.' = Final path from S to E\n")
            f.write("'*' = Explored during BFS\n")

            f.write("\n=== Pathfinding Summary ===\n")
            f.write(f"Algorithm: BFS\n")
            f.write(f"Path Length: {self.path_length}\n")
            f.write(f"Path Cost: {self.path_cost}\n")
            f.write(f"Nodes Explored: {len(self.closed_list)}\n")
            f.write(f"Remaining in Queue: {len(self.open_list)}\n")


# === Function Block ===
def run_bfs(filepath="pathFindingMap.txt"):
    # create an instance of the BFS class
    solver = BFSPathFinder(filepath)
    path = solver.search()

    if path:
        print(f" Path found! Length: {len(path)}")
        solver.mark_path(path)       # Mark the shortest path with '.'
        solver.mark_explored()       # Mark explored cells with '*'
        solver.print_grid()          # Show the updated grid
        solver.print_stats()         # Print performance metrics
    else:
        print(" No path found.")
        solver.mark_explored()
        solver.print_grid()
        solver.print_stats()

    solver.write_output("BFS_output.txt")
    print("\nGrid with legend and stats written to 'BFS_output.txt'")


# === Entry point for running the script ===
if __name__ == "__main__":
    run_bfs()
