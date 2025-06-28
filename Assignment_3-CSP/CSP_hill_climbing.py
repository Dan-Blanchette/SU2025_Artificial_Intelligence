from csp_utils import load_graph, count_conflicts, visualize_coloring
import random

def hill_climbing(graph, num_colors, max_steps=2000):
    assignment = {v: random.randint(0, num_colors - 1) for v in graph}
    for _ in range(max_steps):
        if count_conflicts(graph, assignment) == 0:
            return assignment
        var = random.choice(list(graph))
        best_color = assignment[var]
        min_conflict = count_conflicts(graph, assignment)
        for c in range(num_colors):
            if c != assignment[var]:
                assignment[var] = c
                conf = count_conflicts(graph, assignment)
                if conf < min_conflict:
                    best_color = c
                    min_conflict = conf
        assignment[var] = best_color
    return None

if __name__ == "__main__":
    graph = load_graph()
    for k in range(2, 11):
        result = hill_climbing(graph, k)
        if result:
            print(f"Hill Climbing: Solved with {k} colors.")
            visualize_coloring(graph, result, f"Hill Climbing: {k} Colors")
            break
