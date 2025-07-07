# Dan Blanchette
# Assignment #3
# CS 5701 Artificial Intelligence
# Dr. Soule

# Credit: ChatGPT, 
# GeeksForGeeks: https://www.geeksforgeeks.org/artificial-intelligence/introduction-hill-climbing-artificial-intelligence/
from csp_utils import load_graph, count_conflicts, visualize_coloring
import random  

# Define the Hill Climbing algorithm for graph coloring
def hill_climbing(graph, num_colors, max_steps=2000):
    # Initialize a random color assignment for each vertex
    assignment = {v: random.randint(0, num_colors - 1) for v in graph}

    # Iterate up to a maximum number of steps to try improving the solution
    for _ in range(max_steps):
        # If there are no conflicts, return the current assignment
        if count_conflicts(graph, assignment) == 0:
            return assignment

        # Randomly choose a variable (node) to modify
        var = random.choice(list(graph))

        # Initialize with the current color and current conflict count
        best_color = assignment[var]
        min_conflict = count_conflicts(graph, assignment)

        # Try all other colors to find the one that reduces conflicts the most
        for c in range(num_colors):
            if c != assignment[var]:
                assignment[var] = c
                conf = count_conflicts(graph, assignment)
                if conf < min_conflict:
                    best_color = c
                    min_conflict = conf

        # Assign the best color found
        assignment[var] = best_color

    # Return None if no solution is found within the step limit
    return None

def main():
    graph = load_graph()  # Load the graph structure
    for k in range(2, 11):  # Try increasing number of colors from 2 to 10
        result = hill_climbing(graph, k)  # Attempt to solve the coloring problem
        if result:
            print(f"Hill Climbing: Solved with {k} colors.")
            visualize_coloring(graph, result, f"Hill Climbing: {k} Colors")  # Display result
            break  # Stop once a valid coloring is found

# Main block to run the hill climbing on a loaded graph
if __name__ == "__main__":
    main()

