# algorithms/base.py
import math

class Grid:
    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            self.grid = [list(line.strip()) for line in f if line.strip()]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.start = self.find_char('S')
        self.end = self.find_char('E')

    def find_char(self, char):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == char:
                    return (r, c)
        raise ValueError(f"{char} not found in grid.")

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_walkable(self, r, c):
        return self.grid[r][c] in ['0', 'E']

    def get_neighbors(self, r, c):
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc) and self.is_walkable(nr, nc):
                yield (nr, nc)

    def manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def euclidean(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])
