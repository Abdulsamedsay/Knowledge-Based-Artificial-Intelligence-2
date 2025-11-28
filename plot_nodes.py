#Abdulsamed Say (s1146476)
#Ismail Vatansever (s1152889)

import matplotlib.pyplot as plt
import numpy as np

# Circuits and node counts (taken from test_all.py output)
circuits = np.arange(1, 8)
nodes_smallest = [6, 6, 3, 9, 6, 13, 21]
nodes_mostfreq = [6, 6, 3, 9, 6, 13, 21]

# --- Plot setup ---
width = 0.35  # bar width
plt.figure(figsize=(7, 4))

# Bar positions
plt.bar(circuits - width/2, nodes_smallest, width, label='Smallest-Conflict', color='steelblue')
plt.bar(circuits + width/2, nodes_mostfreq, width, label='Most-Frequent', color='orange')

# Labels and title
plt.xlabel('Circuit Number')
plt.ylabel('Nodes Expanded')
plt.title('Nodes Expanded per Circuit for Both Heuristics')
plt.xticks(circuits)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# --- Save as PNG ---
plt.tight_layout()
plt.savefig('nodes_per_circuit.png', dpi=300)
plt.show()
