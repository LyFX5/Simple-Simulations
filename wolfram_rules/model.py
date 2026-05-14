from abc import ABC
import numpy as np


class Wolfram:

    @classmethod
    def to_binary(cls, decimal: int) -> str:
        binary_str = ""
        while decimal > 0:
            binary_str = str(decimal % 2) + binary_str
            decimal //= 2
        return "0" + binary_str  # TODO fix hardcode (8 bits)

    @classmethod
    def from_binary(cls, binary: int) -> int:
        decimal, power = 0, 0
        while binary:
            decimal += (binary % 10) * (2**power)
            binary //= 10
            power += 1
        return decimal

    @classmethod
    def rule(cls, rule_number: int):
        assert (
            0 <= rule_number <= 255
        ), f"rule number must fit in [0, 255]. {rule_number=}"
        rule_bin = Wolfram.to_binary(rule_number)
        return rule_bin


class System(ABC):

    def reset(self) -> None: ...

    def get_rule(self) -> str: ...

    def set_rule(self, rule_number: int) -> None: ...

    def state(self) -> np.ndarray: ...

    def step(self) -> None: ...


class Automaton(System):

    def __init__(
        self, steps_in_cycle: int, init_state: np.ndarray, rule_number: int = 90
    ):
        assert (
            init_state.ndim == 1
        ), f"automaton lives in first dimension. {init_state.dim=}"
        assert np.array_equal(
            init_state, init_state.astype(bool)
        ), f"automaton must be binary"
        self._steps_in_cycle = steps_in_cycle
        self._init_state = init_state
        self.set_rule(rule_number)
        self.reset()

    def reset(self):
        self._step_number = 0
        self._grid = np.zeros((self._steps_in_cycle, len(self._init_state))).astype(int)
        self._grid[0, :] = self._init_state

    def get_rule(self) -> str:
        return self._rule

    def set_rule(self, rule_number: int) -> None:
        self._rule = Wolfram.rule(rule_number)

    def state(self) -> np.ndarray:
        return self._grid

    def local_step(self, l: int, m: int, r: int) -> int:
        bin_str = str(l) + str(m) + str(r)
        code = Wolfram.from_binary(int(bin_str))
        rule_len = len(self._rule)
        cell_next_state = int(self._rule[rule_len - 1 - code])
        return cell_next_state

    def step(self) -> None:
        height = self._grid.shape[0]
        width = self._grid.shape[1]
        for x in range(width):
            l = self._grid[self._step_number % height][(x - 1) % width]
            m = self._grid[self._step_number % height][x]
            r = self._grid[self._step_number % height][(x + 1) % width]
            self._grid[(self._step_number + 1) % height][x] = self.local_step(l, m, r)
        self._step_number += 1
        if self._step_number >= self._steps_in_cycle:
            self.reset()

    def simulate(self, steps_number):
        for _ in range(steps_number):
            print(self.state())
            self.step()
