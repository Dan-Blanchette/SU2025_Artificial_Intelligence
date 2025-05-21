# Author: Dan Blanchette
# Date Started: 5-13-25
# Extended: 5-20-25

from collections import deque  # for BFS queue
import heapq                   # for priority queue in Dijkstra, A*, and Greedy
import math                    # for Euclidean heuristic

class BFSPathFinder:
    """
    Implements multiple pathfinding algorithms—BFS, Dijkstra, Greedy Best-First Search,
    and A*—on a 2D grid loaded from a text file. Supports path visualization, cost tracking,
    and search space statistics.
    """
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
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc) and self.is_walkable(nr, nc):
                yield (nr, nc)

    def get_cell_cost(self, r, c):
        return 1 if self.grid[r][c] in ['0', 'E'] else float('inf')

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

    def dijkstra(self):
        open_heap = [(0, self.start)]
        cost_so_far = {self.start: 0}
        self.parent = {}
        self.closed_list = set()
        while open_heap:
            current_cost, current = heapq.heappop(open_heap)
            if current in self.closed_list:
                continue
            self.closed_list.add(current)
            if current == self.end:
                self.path_cost = current_cost
                return self.reconstruct_path()
            for neighbor in self.get_neighbors(*current):
                new_cost = current_cost + self.get_cell_cost(*neighbor)
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(open_heap, (new_cost, neighbor))
                    self.parent[neighbor] = current
        return None

    def manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def euclidean(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def greedy_best_first(self, heuristic='manhattan'):
        open_heap = []
        self.parent = {}
        self.closed_list = set()
        h_func = self.manhattan if heuristic == 'manhattan' else self.euclidean
        heapq.heappush(open_heap, (h_func(self.start, self.end), self.start))
        while open_heap:
            _, current = heapq.heappop(open_heap)
            if current in self.closed_list:
                continue
            self.closed_list.add(current)
            if current == self.end:
                return self.reconstruct_path()
            for neighbor in self.get_neighbors(*current):
                if neighbor not in self.closed_list:
                    self.parent[neighbor] = current
                    heapq.heappush(open_heap, (h_func(neighbor, self.end), neighbor))
        return None

    def a_star(self, heuristic='manhattan'):
        open_heap = []
        self.parent = {}
        self.closed_list = set()
        g_cost = {self.start: 0}
        h_func = self.manhattan if heuristic == 'manhattan' else self.euclidean
        f_start = h_func(self.start, self.end)
        heapq.heappush(open_heap, (f_start, self.start))
        while open_heap:
            _, current = heapq.heappop(open_heap)
            if current in self.closed_list:
                continue
            self.closed_list.add(current)
            if current == self.end:
                self.path_cost = g_cost[current]
                return self.reconstruct_path()
            for neighbor in self.get_neighbors(*current):
                tentative_g = g_cost[current] + self.get_cell_cost(*neighbor)
                if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                    g_cost[neighbor] = tentative_g
                    f_score = tentative_g + h_func(neighbor, self.end)
                    heapq.heappush(open_heap, (f_score, neighbor))
                    self.parent[neighbor] = current
        return None

    def reconstruct_path(self):
        path = []
        current = self.end
        while current != self.start:
            path.append(current)
            current = self.parent[current]
        path.append(self.start)
        path.reverse()
        self.path_length = len(path)
        if self.path_cost == 0:
            self.path_cost = self.path_length - 1
        return path

    def mark_path(self, path):
        for r, c in path:
            if self.grid[r][c] == '0':
                self.grid[r][c] = '.'

    def mark_explored(self):
        for r, c in self.closed_list:
            if self.grid[r][c] == '0':
                self.grid[r][c] = '*'

    def print_grid(self):
        for row in self.grid:
            print(''.join(row))

    def print_stats(self, algorithm="BFS"):
        print("\nPathfinding Summary")
        print(f"{'Algorithm':<30} {'Path Len':<10} {'Cost':<10} {'Explored':<12}")
        print("-" * 65)
        print(f"{algorithm:<30} {self.path_length:<10} {self.path_cost:<10} {len(self.closed_list):<12}")

    def write_output(self, filename="output.txt", summary_table=None):
        with open(filename, 'w') as f:
            f.write("=== Final Grid with Path and Explored States ===\n")
            for row in self.grid:
                f.write(''.join(row) + '\n')
            f.write("\n=== Legend ===\n")
            f.write("S = Start\n")
            f.write("E = End\n")
            f.write("0 = Unvisited walkable space\n")
            f.write("X = Wall/blocked cell\n")
            f.write("'.' = Final path from S to E\n")
            f.write("'*' = Explored during search\n")
            if summary_table:
                f.write("\n=== Pathfinding Summary (All Algorithms) ===\n")
                f.write(f"{'Algorithm':<30} {'Path Len':<10} {'Cost':<10} {'Explored':<12}\n")
                f.write("-" * 65 + "\n")
                for entry in summary_table:
                    f.write(f"{entry['Algorithm']:<30} {entry['Path Len']:<10} {entry['Cost']:<10} {entry['Explored']:<12}\n")

# === Unified Runner for All Algorithms ===
def run_all_algorithms(filepath="pathFindingMap.txt"):
    """
    Executes all implemented search algorithms (BFS, Dijkstra, Greedy Best-First, A*)
    on the provided grid file. Each algorithm's path and explored nodes are marked,
    and a comprehensive performance summary is printed to the console and written
    to an output file.
    """
    summary = []

    def run_method(name, method_func):
        solver = BFSPathFinder(filepath)
        path = method_func(solver)
        if path:
            solver.mark_path(path)
        solver.mark_explored()
        output_filename = name.replace(" ", "_").replace("(", "").replace(")", "").replace("-", "") + "_output.txt"
        solver.write_output(output_filename)
        summary.append({
            "Algorithm": name,
            "Path Len": solver.path_length if path else "-",
            "Cost": solver.path_cost if path else "-",
            "Explored": len(solver.closed_list)
        })

    def bfs_runner(s):
        return s.search()
    run_method("BFS", bfs_runner)
    def dijkstra_runner(s):
        return s.dijkstra()
    run_method("Dijkstra (Lowest Cost)", dijkstra_runner)
    def greedy_manhattan_runner(s):
        return s.greedy_best_first("manhattan")
    run_method("Greedy Best-First (Manhattan)", greedy_manhattan_runner)
    def a_star_manhattan_runner(s):
        return s.a_star("manhattan")
    run_method("A* (Manhattan)", a_star_manhattan_runner)
    def a_star_euclidean_runner(s):
        return s.a_star("euclidean")
    run_method("A* (Euclidean)", a_star_euclidean_runner)

    print("\n=== Pathfinding Summary (All Algorithms) ===")
    print(f"{'Algorithm':<30} {'Path Len':<10} {'Cost':<10} {'Explored':<12}")
    print("-" * 65)
    for row in summary:
        print(f"{row['Algorithm']:<30} {row['Path Len']:<10} {row['Cost']:<10} {row['Explored']:<12}")

    solver = BFSPathFinder(filepath)
    solver.write_output("summary_output.txt", summary)
    print("\nSummary written to 'summary_output.txt'")

# === Entry Point ===
if __name__ == "__main__":
    run_all_algorithms()
