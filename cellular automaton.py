from tkinter import *
import time
from random import randint


class Life_Controller:
    def __init__(self, cols, rows, alive_cells_for_start):
        self.alive_generation = set()

        while alive_cells_for_start > 0:
            cords = (randint(0, rows), randint(0, cols))
            if cords not in self.alive_generation:
                self.alive_generation.add(cords)
                alive_cells_for_start -= 1

        self.prev_generation = set()

    def keep_cell_alive(self, neighbors_number, cords):
        if cords in self.alive_generation:
            return neighbors_number in (2, 3)
        return neighbors_number == 3

    @staticmethod
    def get_neighbors_cords(x, y):
        return {
            (x-1, y-1), (x-1, y), (x-1, y+1),
            (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)
        }

    def _get_cell_neighbors_count(self, x, y):
        neighbors_cords = Life_Controller.get_neighbors_cords(x, y)
        alive_neighbors = self.alive_generation & neighbors_cords
        return len(alive_neighbors)

    def is_alive(self, *cords):
        return tuple(cords) in self.alive_generation

    def prepaire_next_generation(self):
        next_generation = set()
        for cords in self.field_cords:
            cell_neighbors_count = self._get_cell_neighbors_count(*cords)
            if self.keep_cell_alive(cell_neighbors_count, cords):
                next_generation.add(cords)
        self.prev_generation = self.alive_generation
        self.alive_generation = next_generation

    def is_stopped_life(self):
        # conditions for exit: if no alive left or if generations are same
        return (
            len(self.alive_generation) == 0 or
            self.prev_generation == self.alive_generation
        )


class Game_Controller(Life_Controller):
    def __init__(self, root, field_size, cell_size, alive_cells_for_start):

        self.field_size = field_size
        self.cell_size = cell_size

        self.rows = self.cols = int(field_size / cell_size)
        self.canvas = Canvas(root, width=field_size, height=field_size)
        self.canvas.pack()

        Life_Controller.__init__(
            self, self.rows, self.cols, alive_cells_for_start)

        self.field_cords = []
        self._create_field_cords()
        self._prepaire_field_with_life()

    def _create_field_cords(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.field_cords.append((row, col))

    def _prepaire_field_with_life(self):
        for cords in self.field_cords:
            row, col = cords
            self._create_cell(row, col)
        self.canvas.update()

    def _create_cell(self, row, col):
        color = 'green' if self.is_alive(row, col) else 'white'
        top, left, right, bottom = self._calc_cell_position(row, col)
        self.canvas.create_rectangle(top, left, right, bottom, fill=color)

    def _calc_cell_position(self, row, col):
        c = self.cell_size
        f = self.field_size
        return (c*col, c*row, f+(c*col), f+(c*row))

    def next_frame(self):
        self.prepaire_next_generation()
        self._prepaire_field_with_life()


class Window:
    def __init__(self, field_size, cell_size, alive_cells_for_start):

        self.root = Tk()
        self.root.geometry(f"{field_size}x{field_size}+500+10")

        self.game_controller = Game_Controller(
            self.root, field_size, cell_size, alive_cells_for_start
        )

    def start(self):
        while True:
            time.sleep(1)
            if self.game_controller.is_stopped_life():
                break
            self.game_controller.next_frame()
        self.root.quit()


window = Window(
    field_size=700,
    cell_size=50,
    alive_cells_for_start=50
)

window.start()
