import math
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from matplotlib.animation import FFMpegWriter


# 1. Define the 'Little Man' (Condensation Set)
def get_little_man_points():
    points = []
    # Head (circle)
    cx, cy, r = 0.0, 1.2, 0.5
    for t in range(40):
        angle = 2 * math.pi * t / 40
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))

    # Eyes
    points += [(-0.15, 1.3), (0.15, 1.3)]

    # Smile (arc)
    for t in range(10):
        angle = math.pi * (0.2 + 0.6 * t / 10)
        x = 0.25 * math.cos(angle)
        y = 1.1 - 0.15 * math.sin(angle)
        points.append((x, y))

    # Body (vertical line), Arms, Legs, Antenna...
    for t in range(15):
        points.append((0.0, 0.7 - t * 0.08))
    for t in range(10):
        points.append((0.0 - t * 0.07, 0.4 + t * 0.05))
        points.append((0.0 + t * 0.07, 0.4 + t * 0.05))
    for t in range(10):
        points.append((0.0 - t * 0.05, -0.5 - t * 0.07))
        points.append((0.0 + t * 0.05, -0.5 - t * 0.07))
    for t in range(20):
        angle = 0.3 * t + math.pi / 2
        radius = 0.02 * t
        points.append(
            (-0.22 + radius * math.cos(angle), 2 - radius * math.sin(angle))
        )

    scale = 0.35
    return [(scale * x, scale * y) for (x, y) in points]


little_man_points = get_little_man_points()


# 2. Define the Spiral Transformation
def w1(x, y, r=0.94, theta=0.4, tx=0.5, ty=0.5):
    new_x = r * (x * math.cos(theta) - y * math.sin(theta)) + tx
    new_y = r * (x * math.sin(theta) + y * math.cos(theta)) + ty
    return new_x, new_y


# 3. Animation Setup
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_facecolor("#0a0a0a")
fig.patch.set_facecolor("#0a0a0a")
ax.set_aspect("equal")
ax.axis("off")

# We use a line plot with ',' (point marker) for extreme performance
(points_plot,) = ax.plot([], [], ",", color="#00ff88", alpha=0.6, markersize=1)

# Persistent State
app_state = {
    "x": 0.0,
    "y": 0.0,
    "plot_x": [],
    "plot_y": [],
    "iterations_per_frame": 5,  # Control speed here
}

total_frames = 1000


def update(frame):
    x, y = app_state["x"], app_state["y"]

    zoom = 2.8
    bias = 4

    for _ in range(app_state["iterations_per_frame"]):
        if random.random() < 0.08:
            x, y = random.choice(little_man_points)
        else:
            x, y = w1(x, y)

        app_state["plot_x"].append(zoom * x + bias)
        app_state["plot_y"].append(zoom * y - bias)

    app_state["x"], app_state["y"] = x, y

    # Update the data of the plot object
    points_plot.set_data(app_state["plot_x"], app_state["plot_y"])

    # Set plot limits on first frame for a stable view
    if frame == 0:
        ax.set_xlim(-2, 8)
        ax.set_ylim(-5, 5)

    if frame == total_frames // 2:
        app_state["iterations_per_frame"] *= 2

    return (points_plot,)


# Setup the writer (Requires ffmpeg installed on your system)
writer = FFMpegWriter(fps=30, bitrate=1800)

# Create animation
ani = FuncAnimation(fig, update, frames=total_frames, interval=20, blit=True)

plt.show()

# Save the animation
ani.save("little_man_spiral.mp4", writer=writer)
