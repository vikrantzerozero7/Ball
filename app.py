import matplotlib.pyplot as plt
import numpy as np

# Set rotation style to arcball (lock-free)
plt.rcParams['axes3d.mouserotationstyle'] = 'arcball'  # 'sphere', 'trackball', or 'arcball'

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create your 3D object
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = np.outer(np.cos(u), np.sin(v))
y = np.outer(np.sin(u), np.sin(v))
z = np.outer(np.ones(np.size(u)), np.cos(v))

ax.plot_surface(x, y, z, cmap='viridis')
plt.show()
