# Dan Blanchette
# Assignment #3
# CS 5701 Artificial Intelligence
# Dr. Soule

# Credit: ChatGPT 
# Artificial Intelligence: A Modern Approach
from csp_utils import load_graph, count_conflicts, visualize_coloring
import random  

# Define the Min-Conflicts algorithm for solving graph coloring
def min_conflicts(graph, num_colors, max_steps=10000):
    # Step 1: Start with a random assignment of colors to all nodes
    assignment = {v: random.randint(0, num_colors - 1) for v in graph}

    # Step 2: Iterate up to max_steps to reduce conflicts
    for _ in range(max_steps):
        # Identify all variables (nodes) that are in conflict
        conflicted = [
            var for var in graph
            if any(assignment[var] == assignment[neighbor] for neighbor in graph[var])
        ]

        # If there are no conflicts, return the current assignment as a solution
        if not conflicted:
            return assignment

        # Step 3: Choose a conflicted variable at random
        var = random.choice(conflicted)

        # Step 4: For each possible color, compute the total number of conflicts
        conflicts = [
            (count_conflicts(graph, {**assignment, var: c}), c)
            for c in range(num_colors)
        ]

        # Step 5: Assign the color that results in the fewest conflicts
        assignment[var] = min(conflicts)[1]

    # If no solution is found within the allowed steps, return None
    return None

def main():
    graph = load_graph()  # Load the graph from the utility function
    for k in range(2, 11):  # Try from 2 to 10 colors
        result = min_conflicts(graph, k)
        if result:
            print(f"Min-Conflicts: Solved with {k} colors.")
            visualize_coloring(graph, result, f"Min-Conflicts: {k} Colors")  # Show the result
            break  # Stop when a valid coloring is found

# Run the algorithm if the script is executed directly
if __name__ == "__main__":
    main()