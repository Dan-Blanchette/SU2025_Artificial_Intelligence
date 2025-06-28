# Dan Blanchette
# Assignment # 4 Robot Decision Tree
# CS 5701 Artficial Intelligence
# Dr. Soule
# Date: 6-28-25

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("Problem4DecisionTreeData.CSV")

# Drop Examples (No bearing on decision tree outcomes)
df = df.drop(columns=['Example'])

# Separate features and target
X = df.drop(columns=['Decision'])
# Encode yes and no to match data convetion to 1 or 2
y = df['Decision'].map({'Yes': 1, 'No': 0})  

# Sample list for testing
training_sizes = [2, 5, 10, 20, 50]
test_accuracies = []

# Set seed for reproducibility
random_seed = 42
np.random.seed(random_seed)

# Create directory for saving images
os.makedirs("decision_tree_images_bigger", exist_ok=True)

# Run experiments for different training sizes
for size in training_sizes:
    # Shuffle data: returns a new array list configuration based
    # on exisiting indice values.
    shuffled_indices = np.random.permutation(len(X))
    # update both data paramters for train and test data with
    # shuffled values
    X_shuffled = X.iloc[shuffled_indices]
    y_shuffled = y.iloc[shuffled_indices]

    # Split data
    X_train = X_shuffled.iloc[:size]
    y_train = y_shuffled.iloc[:size]
    X_test = X_shuffled.iloc[size:]
    y_test = y_shuffled.iloc[size:]

    # Train decision tree
    clf = DecisionTreeClassifier(max_depth=5, random_state=random_seed)
    clf.fit(X_train, y_train)

    # Predict and evaluate
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    test_accuracies.append(accuracy)

    print(f"Training size: {size}, Test accuracy: {accuracy:.2f}")

    # Plot and save the decision tree
    plt.figure(figsize=(20, 10))
    plot_tree(
        clf,
        max_depth=5,
        feature_names=X.columns,
        class_names=['No', 'Yes'],
        filled=True,
        rounded=True
    )
    plt.title(f"Decision Tree Trained on {size} Examples")
    tree_filename = f"decision_tree_images_bigger/tree_{size}_examples.png"
    plt.savefig(tree_filename)
    plt.close()
    print(f"Saved tree image to: {tree_filename}")

# Plot and save the accuracy graph
plt.figure(figsize=(10, 6))
plt.plot(training_sizes, test_accuracies, marker='o')
plt.title("Robot Help-Request Decision Accuracy vs. Training Size")
plt.xlabel("Training Set Size")
plt.ylabel("Test Set Accuracy")
plt.grid(True)
accuracy_graph_path = "decision_tree_images/accuracy_vs_training_size.png"
plt.savefig(accuracy_graph_path)
plt.close()

print(f"Saved accuracy graph to: {accuracy_graph_path}")
