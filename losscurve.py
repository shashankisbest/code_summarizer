import matplotlib.pyplot as plt
import numpy as np

# Sample loss data (replace with your actual history if available)
epochs = np.arange(1, 51)
training_loss = 2.5 / (1 + 0.1 * epochs) + 0.05 * np.exp(-epochs/10) + 0.02 * np.random.randn(50)
validation_loss = training_loss + 0.05 + 0.02 * np.random.randn(50)

# Ensure smooth curves
training_loss = np.maximum(0.1, training_loss - np.linspace(0, 0.5, 50))
validation_loss = np.maximum(0.15, validation_loss - np.linspace(0, 0.45, 50))

plt.figure(figsize=(10, 6))
plt.plot(epochs, training_loss, 'b-', label='Training Loss', linewidth=2.5, marker='o', markersize=4, markevery=5)
plt.plot(epochs, validation_loss, 'r-', label='Validation Loss', linewidth=2.5, marker='s', markersize=4, markevery=5)

plt.xlabel('Epoch', fontsize=14, fontweight='bold')
plt.ylabel('Loss', fontsize=14, fontweight='bold')
plt.title('Model Training & Validation Loss Curve', fontsize=16, fontweight='bold')
plt.legend(fontsize=12, loc='upper right')
plt.grid(True, alpha=0.3)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)

plt.tight_layout()
plt.savefig('loss_curve.png', dpi=300, bbox_inches='tight')
plt.show()