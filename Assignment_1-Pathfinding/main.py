# runner.py
import bfs, lowestCost, greedy, aStar
import csv

def main(filepath):
    results = [
        bfs.bfs(filepath),
        lowestCost.run(filepath),
        greedy.run(filepath, heuristic='manhattan'),
        aStar.run(filepath, heuristic='manhattan'),
        aStar.run(filepath, heuristic='euclidean')
    ]

    print(f"{'Algorithm':<30} {'Path Len':<10} {'Cost':<10} {'Explored':<12} {'Remaining':<12}")
    print("-" * 80)
    for row in results:
        print(f"{row['name']:<30} {len(row['path']):<10} {row['cost']:<10} {row['explored']:<12} {row['remaining']:<12}")

    with open("summary.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Algorithm", "Path Len", "Cost", "Explored", "Remaining"])
        for row in results:
            writer.writerow([row['name'], len(row['path']), row['cost'], row['explored'], row['remaining']])

if __name__ == "__main__":
    main("pathFindingMap.txt")
