"""
Another small step towards understending, how the complexity organizes itself
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, TextBox

from model import Automaton


# init model
init_state = np.array([0] * 121)
init_state[61] = 1

initial_rule_number = 10

auto = Automaton(
    steps_in_cycle=65, init_state=init_state, rule_number=initial_rule_number
)


# init visualization
STEPS_IN_SIMULATION = 5000
DURATION_OF_ANIMATION = STEPS_IN_SIMULATION / 10  # seconds
FRAMES_NUMBER = STEPS_IN_SIMULATION
DELAY_BETWEEN_FRAMES = 1000 * DURATION_OF_ANIMATION / FRAMES_NUMBER  # in milliseconds

FIGURE_SIZE = (8, 8)
SCENE_WIDTH = FIGURE_SIZE[1]
SCENE_HEIGHT = FIGURE_SIZE[0]
SCATTER_SIZE = 5

SIMULATION_NAME = "Wolfram Rules"

paused = [True]

fig_animation, ax_scatter = plt.subplots(figsize=FIGURE_SIZE)
fig_animation.suptitle(SIMULATION_NAME, fontsize=14)

ax_scatter.set_xticks([])
ax_scatter.set_yticks([])
ax_scatter.set_aspect("equal")
ax_scatter.set_xlim(-SCENE_WIDTH / 2, SCENE_WIDTH / 2)
ax_scatter.set_ylim(-SCENE_HEIGHT / 2, SCENE_HEIGHT / 2)

scatter_of_grid = ax_scatter.scatter([], [], SCATTER_SIZE)


def grid_to_scatter():

    grid_state = auto.state()

    height, width = grid_state.shape
    dots_margin_x = SCENE_WIDTH / width
    dots_margin_y = SCENE_HEIGHT / height
    coordinates = []
    colors = []
    for y in range(height):
        for x in range(width):
            coordinates.append(
                [
                    (x - width / 2 + 1 / 2) * dots_margin_x,
                    (y - height / 2 + 1 / 2) * dots_margin_y,
                ]
            )
            cell_state = grid_state[y][x].item()
            if cell_state:
                rgb = [0.4, 0.8, 0.9]
            else:
                rgb = [1, 1, 1]
            colors.append(rgb)
    coordinates = np.array(coordinates)
    colors = np.array(colors)
    return coordinates, colors


def init_plot():

    coordinates, colors = grid_to_scatter()
    scatter_of_grid.set_offsets(coordinates)
    scatter_of_grid.set_color(colors)
    return (scatter_of_grid,)


def update_plot(frame):

    if not paused[0]:
        auto.step()  # here the simulation step heppens

    coordinates, colors = grid_to_scatter()
    scatter_of_grid.set_offsets(coordinates)
    scatter_of_grid.set_color(colors)
    return (scatter_of_grid,)


# init widgets

# button
button_ax = plt.axes([0.8, 0.025, 0.1, 0.04])  # x, y, width, height
button = Button(button_ax, "Play", hovercolor="0.975")


def toggle(event):
    paused[0] = not paused[0]
    button.label.set_text("Play" if paused[0] else "Pause")


button.on_clicked(toggle)

# text box
text_ax = plt.axes([0.18, 0.025, 0.1, 0.04])  # x, y, width, height
text = TextBox(text_ax, label="Rule: ", initial=initial_rule_number)  # color


def update_rule(event):
    rule_number = int(text.text)
    if 0 <= rule_number <= 255:
        update_rule_table(rule_number)
        auto.set_rule(rule_number)


text.on_submit(update_rule)


# table
# --- Wolfram Rule Function ---
def get_rule_table(rule_number):
    """Return mapping table for given rule number (0-255)."""
    binary = np.binary_repr(rule_number, 8)
    return np.array([int(b) for b in binary], dtype=int)


# --- Update Rule Table ---
def update_rule_table(rule_number):
    global rule_table
    table_vals = get_rule_table(rule_number)

    # Clear old table if exists
    for t in rule_table.get_celld().values():
        t.set_text_props(text="")

    # Fill with new values
    for i, pattern in enumerate(patterns):
        rule_table[0, i].get_text().set_text(pattern)
        rule_table[1, i].get_text().set_text(str(table_vals[i]))

    fig_animation.canvas.draw_idle()


# --- Rule Table ---
patterns = ["111", "110", "101", "100", "011", "010", "001", "000"]
rule_table = plt.table(
    cellText=[patterns, [""] * 8],
    cellLoc="center",
    loc="bottom",
    bbox=[1.2, 0.01, 4.8, 2],
)  # [left, bottom, width, height]

# Make fonts readable
rule_table.auto_set_font_size(False)  # disable automatic shrinking
rule_table.set_fontsize(14)  # pick a good size (try 14–18)

"""
# vertical arrow "time"
ax_scatter.annotate(
    "time",
    xy=(0, 1),
    xycoords="axes fraction",
    xytext=(0, 0),
    textcoords="axes fraction",
    arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
    ha="right",
    va="center",
    rotation=90,
    fontsize=12,
)
"""

# Draw a straight vertical arrow on the left
ax_scatter.annotate(
    "",
    xy=(0, 1),
    xycoords="axes fraction",
    xytext=(0, 0),
    textcoords="axes fraction",
    arrowprops=dict(arrowstyle="->", color="black", lw=1.5),
)

# Add vertical label "time" to the left of the arrow
ax_scatter.text(
    -0.08,
    0.5,
    "time",
    transform=ax_scatter.transAxes,
    rotation=90,
    va="center",
    ha="center",
    fontsize=12,
)


if __name__ == "__main__":

    animation = FuncAnimation(
        fig=fig_animation,
        func=update_plot,
        frames=FRAMES_NUMBER,
        init_func=init_plot,
        blit=True,
        interval=DELAY_BETWEEN_FRAMES,
        repeat=False,
        # save_count=FRAMES_NUMBER
    )

    fig_animation.show()
