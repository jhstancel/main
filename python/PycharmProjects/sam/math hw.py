import numpy as np
import matplotlib.pyplot as plt

# Generate x values from 0 to 2*pi for one full cycle
x = np.linspace(0, 2 * np.pi, 1000)

# Compute the function values for y = cos(x)
y = np.cos(x)

# Create the plot
plt.figure(figsize=(8, 6))
plt.plot(x, y, label=r'$y = \cos(x)$', color='blue')
plt.title('Graph of y = cos(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')
plt.axvline(0, color='black', linewidth=0.5, linestyle='--')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.show()
