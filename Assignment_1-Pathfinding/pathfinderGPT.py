from collections import deque

class BFSPathFinder:
    def __init__(self, filepath):
        # Load the grid from the file
        with open(filepath, 'r') as f:
            self.grid = [list(line.strip()) for line in f if line.strip()]

        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.start = self.find_char('S')
        self.end = self.find_char('E')
        self.parent = {}
        self.open_list = deque()
        self.closed_list = set()

        # Stats counters
        self.path_length = 0
        self.path_cost = 0

    def find_char(self, char):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == char:
                    return (r, c)
        raise ValueError(f"Character '{char}' not found in grid.")

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_walkable(self, r, c):
        return self.grid[r][c] in ['0', 'E']

    def get_neighbors(self, r, c):
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc) and self.is_walkable(nr, nc):
                yield (nr, nc)

    def reconstruct_path(self):
        path = []
        current = self.end
        while current != self.start:
            path.append(current)
            current = self.parent[current]
        path.append(self.start)
        path.reverse()
        self.path_length = len(path)
        self.path_cost = len(path) - 1  # In BFS, each move costs 1
        return path

    def search(self):
        self.open_list.append(self.start)

        while self.open_list:
            current = self.open_list.popleft()
            self.closed_list.add(current)

            if current == self.end:
                return self.reconstruct_path()

            for neighbor in self.get_neighbors(*current):
                if neighbor not in self.closed_list and neighbor not in self.open_list:
                    self.parent[neighbor] = current
                    self.open_list.append(neighbor)

        return None

    def mark_path(self, path):
        # Mark the actual path with '.'
        for r, c in path:
            if self.grid[r][c] == '0':
                self.grid[r][c] = '.'

    def mark_explored(self):
        # Mark explored (checked) nodes with '*', preserving path (.)
        for r, c in self.closed_list:
            if self.grid[r][c] == '0':
                self.grid[r][c] = '*'

    def print_grid(self):
        for row in self.grid:
            print(''.join(row))

    def print_stats(self):
        print("\n Pathfinding Summary (All Algorithms)")
        print(f"{'Algorithm':<25} {'Path Len':<10} {'Cost':<10} {'Explored':<12} {'Remaining'}")
        print("-" * 65)

        # Actual BFS stats
        print(f"{'BFS':<25} {self.path_length:<10} {self.path_cost:<10} {len(self.closed_list):<12} {len(self.open_list)}")

        # Placeholders for other algorithms
        print(f"{'Lowest Cost':<25} {'-':<10} {'-':<10} {'-':<12} {'-'}")
        print(f"{'Greedy Best-First':<25} {'-':<10} {'-':<10} {'-':<12} {'-'}")
        print(f"{'A* (Heuristic 1)':<25} {'-':<10} {'-':<10} {'-':<12} {'-'}")
        print(f"{'A* (Heuristic 2)':<25} {'-':<10} {'-':<10} {'-':<12} {'-'}")

    def write_output(self, filename="output.txt"):
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


# === Run the pathfinding ===
if __name__ == "__main__":
    solver = BFSPathFinder("pathFindingMap.txt")
    path = solver.search()

    if path:
        print(f" Path found! Length: {len(path)}")
        solver.mark_path(path)         # Mark path first
        solver.mark_explored()         # Then mark explored
        solver.print_grid()
        solver.print_stats()
    else:
        print(" No path found.")
        solver.mark_explored()
        solver.print_grid()
        solver.print_stats()

    # Export everything to file
    solver.write_output("BFS_output.txt")
    print("\nGrid with legend and stats written to 'output.txt'")
