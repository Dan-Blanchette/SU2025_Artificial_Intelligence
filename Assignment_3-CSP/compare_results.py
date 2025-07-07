from CSP_hill_climbing import hill_climbing
from CSP_min_conflicts import min_conflicts
from csp_utils import load_graph, count_conflicts
import time
import pandas as pd

graph = load_graph()

def run_algorithm(name, algorithm, max_colors=10, max_steps=10000):
    results = []

    for k in range(2, max_colors + 1):
        total_steps = 0
        start = time.perf_counter()
        result = algorithm(graph, k, max_steps=max_steps)
        end = time.perf_counter()

        if result:
            conflicts = count_conflicts(graph, result)
            success = conflicts == 0
        else:
            success = False

        results.append({
            "Algorithm": name,
            "Colors": k,
            "Success": success,
            "Time (s)": round(end - start, 10),
            "Steps": max_steps if not success else "≤ " + str(max_steps)
        })

    return pd.DataFrame(results)

# Run and collect data
hill_df = run_algorithm("Hill Climbing", hill_climbing)
minconf_df = run_algorithm("Min-Conflicts", min_conflicts)

# Combine results
combined = pd.concat([hill_df, minconf_df], ignore_index=True)

# Show table
# Show results in terminal
print(combined.to_string(index=False))

# Save to file
combined.to_csv("csp_algorithm_results.csv", index=False)

