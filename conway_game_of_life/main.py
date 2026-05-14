import numpy as np
from system import MultiAgent
from simulation import Simulation
from pygame_session import PygameSession

STEPS_IN_SIMULATION = 300
ROWS_NUMBER = 50
COLUMNS_NUMBER = 50

glider_gun_init_state_cells = [
    (22, 8),
    (12, 7),
    (36, 7),
    (17, 9),
    (11, 8),
    (1, 9),
    (25, 4),
    (2, 8),
    (16, 7),
    (25, 10),
    (21, 6),
    (23, 9),
    (14, 6),
    (36, 6),
    (22, 7),
    (14, 12),
    (17, 8),
    (11, 10),
    (25, 9),
    (35, 7),
    (1, 8),
    (18, 9),
    (22, 6),
    (21, 8),
    (23, 5),
    (12, 11),
    (17, 10),
    (11, 9),
    (35, 6),
    (25, 5),
    (2, 9),
    (13, 6),
    (13, 12),
    (15, 9),
    (16, 11),
    (21, 7),
]

init_state = np.zeros((ROWS_NUMBER, COLUMNS_NUMBER))

for x, y in glider_gun_init_state_cells:
    init_state[y][x] = 1


# init_state = np.random.choice(2, (ROWS_NUMBER, COLUMNS_NUMBER)) # np.zeros((ROWS_NUMBER, COLUMNS_NUMBER))

system = MultiAgent(init_state, finite=True)

simulation = Simulation(system, STEPS_IN_SIMULATION)

session = PygameSession(simulation=simulation, by_mouse=False, rendering_duration=0.1)

session.draw_simulation()
