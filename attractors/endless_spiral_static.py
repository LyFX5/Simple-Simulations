import math
import random
import matplotlib.pyplot as plt

# 1. Define the 'Little Man' (Condensation Set)
# This could be a list of (x, y) coordinates forming the shape.
little_man_points = []

# Head (circle)
cx, cy, r = 0.0, 1.2, 0.5
for t in range(40):
    angle = 2 * math.pi * t / 40
    x = cx + r * math.cos(angle)
    y = cy + r * math.sin(angle)
    little_man_points.append((x, y))

# Eyes
little_man_points += [
    (-0.15, 1.3),
    (0.15, 1.3),
]

# Smile (arc)
for t in range(10):
    angle = math.pi * (0.2 + 0.6 * t / 10)
    x = 0.25 * math.cos(angle)
    y = 1.1 - 0.15 * math.sin(angle)
    little_man_points.append((x, y))

# Body (vertical line)
for t in range(15):
    little_man_points.append((0.0, 0.7 - t * 0.08))

# Arms
for t in range(10):
    little_man_points.append((0.0 - t * 0.07, 0.4 + t * 0.05))  # left
    little_man_points.append((0.0 + t * 0.07, 0.4 + t * 0.05))  # right

# Legs
for t in range(10):
    little_man_points.append((0.0 - t * 0.05, -0.5 - t * 0.07))  # left
    little_man_points.append((0.0 + t * 0.05, -0.5 - t * 0.07))  # right

# Antenna (spiral curl)
for t in range(20):
    angle = 0.3 * t + math.pi / 2
    radius = 0.02 * t
    x = -0.22 + radius * math.cos(angle)
    y = 2 - radius * math.sin(angle)
    little_man_points.append((x, y))


scale = 0.35  # try 0.5–0.7 depending on taste

little_man_points = [(scale * x, scale * y) for (x, y) in little_man_points]


# 2. Define the Spiral Transformation (Similitude)
# w1(x, y) = [a b; c d][x; y] + [e; f]
# For a spiral: r is scaling, theta is rotation
def w1(x, y, r=0.92, theta=0.4, tx=0.5, ty=0.5):
    new_x = r * (x * math.cos(theta) - y * math.sin(theta)) + tx
    new_y = r * (x * math.sin(theta) + y * math.cos(theta)) + ty
    return new_x, new_y


# 3. Simulation Loop
x, y = 0, 0
plot_x, plot_y = [], []
num_iterations = 30000

for n in range(num_iterations):
    # Randomly choose between condensation (the man) or the spiral map
    # p0 is the probability of picking a point from the man
    if random.random() < 0.05:
        x, y = random.choice(little_man_points)
    else:
        x, y = w1(x, y)

    # Ignore first few points to allow convergence [17]
    if n > 10:
        plot_x.append(x)
        plot_y.append(y)

plt.figure(figsize=(8, 8))
plt.scatter(plot_x, plot_y, s=0.05)

plt.gca().set_aspect("equal", adjustable="box")
plt.axis("off")

plt.show()
