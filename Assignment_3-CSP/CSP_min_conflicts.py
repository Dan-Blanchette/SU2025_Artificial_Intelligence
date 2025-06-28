from csp_utils import load_graph, count_conflicts, visualize_coloring
import random

def min_conflicts(graph, num_colors, max_steps=10000):
    assignment = {v: random.randint(0, num_colors - 1) for v in graph}
    for _ in range(max_steps):
        conflicted = [
            var for var in graph
            if any(assignment[var] == assignment[neighbor] for neighbor in graph[var])
        ]
        if not conflicted:
            return assignment
        var = random.choice(conflicted)
        conflicts = [(count_conflicts(graph, {**assignment, var: c}), c)
                     for c in range(num_colors)]
        assignment[var] = min(conflicts)[1]
    return None

if __name__ == "__main__":
    graph = load_graph()
    for k in range(2, 11):
        result = min_conflicts(graph, k)
        if result:
            print(f"Min-Conflicts: Solved with {k} colors.")
            visualize_coloring(graph, result, f"Min-Conflicts: {k} Colors")
            break
