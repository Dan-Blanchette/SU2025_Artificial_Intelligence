import time
import os
from collections import deque

class BFSPathFinder:
    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            self.grid = [list(line.strip()) for line in f if line.strip()]

        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.start = self.find_char('S')
        self.end = self.find_char('E')
        self.parent = {}
        self.open_list = deque()
        self.closed_list = set()
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
        self.path_cost = len(path) - 1
        return path

    def search(self, animate=False, delay=0.01):
      self.open_list.append(self.start)

      while self.open_list:
         current = self.open_list.popleft()
         self.closed_list.add(current)

         if current != self.start and current != self.end:
               self.grid[current[0]][current[1]] = 'C'
               if animate:
                  self.print_grid(highlight=current)
                  time.sleep(delay)

         if current == self.end:
               return self.reconstruct_path()

         for neighbor in self.get_neighbors(*current):
               if neighbor not in self.closed_list and neighbor not in self.open_list:
                  self.parent[neighbor] = current
                  self.open_list.append(neighbor)

                  # Animate each individual node as it’s added to the open list
                  if neighbor != self.end:
                     self.grid[neighbor[0]][neighbor[1]] = 'O'
                  if animate:
                     self.print_grid(highlight=neighbor)
                     time.sleep(delay)
               return None


    def mark_path(self, path):
        for r, c in path:
            if self.grid[r][c] == '0':
                self.grid[r][c] = '.'

    def print_grid(self, highlight=None):
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen for animation
        for r, row in enumerate(self.grid):
            line = ''
            for c, val in enumerate(row):
                if highlight and (r, c) == highlight:
                    line += '\033[1;33m@\033[0m'  # Highlight current cell with '@' in yellow
                else:
                    line += val
            print(line)
        print()

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



# === Entry point
if __name__ == "__main__":
    solver = BFSPathFinder("pathFindingMap.txt")
    path = solver.search(animate=True, delay=1)  # Set animate=True to see animation

    if path:
        print("Path found!")
        solver.mark_path(path)
        solver.print_grid()
        solver.print_stats()
    else:
        print("No path found.")
        solver.print_stats()
