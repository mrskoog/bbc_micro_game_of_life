import microbit
import random

DISP_WIDTH = 5
DISP_HEIGHT = 5


class Cell (object):
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.neighbour = 0

    def check_neighbours(self):
        potential_life = []
        hight_range = range(DISP_HEIGHT)
        width_range = range(DISP_WIDTH)
        for x in range(-1, 2):
            for y in range(-1, 2):
                if not (x == 0 and y == 0) and self.x_pos + x in hight_range and self.y_pos + y in width_range:
                    if microbit.display.get_pixel(self.x_pos + x, self.y_pos + y) != 0:
                        self.neighbour = self.neighbour + 1
                    else:
                        potential_life.append([self.x_pos + x, self.y_pos + y])
        return potential_life

    def live_die(self):
        if self.neighbour == 3 or self.neighbour == 2:
            self.neighbour = 0
            return 1  #Cell lives
        else:
            return 0  #Cell dies


class Main (object):
    def __init__(self):
        self.cells = []
        self.next_cells = []

    def add_new_cell(self, pos):
        for i in self.next_cells:
            if i.x_pos == pos[0] and i.y_pos == pos[1]:
                return False
        self.next_cells.append(Cell(pos[0], pos[1]))
        return True

    def next_step(self):
        if len(self.cells) != 0:  #check if list is not empty
            for cell in self.cells:
                p_life = cell.check_neighbours()
                if cell.live_die():  #
                    self.next_cells.append(cell)
                for new_cell in p_life:
                    self.potential_life(new_cell)
            self.cells = list(self.next_cells)
            self.next_cells[:] = []  #clear list
            self.paint_cells()
            return True
        else:
            microbit.display.scroll("END OF LIFE")
            return False

    def potential_life(self, pos):
        neighbour = 0
        hight_range = range(DISP_HEIGHT)
        width_range = range(DISP_WIDTH)
        for x in range(-1, 2):
            for y in range(-1, 2):
                if not (x == 0 and y == 0) and pos[0] + x in hight_range and pos[1] + y in width_range:
                    if microbit.display.get_pixel(pos[0] + x, pos[1] + y) != 0:
                        neighbour = neighbour + 1
        if neighbour == 3:
            self.add_new_cell(pos)

    def paint_cells(self):
        microbit.display.clear()
        if self.cells != None:
            for cell in self.cells:
                microbit.display.set_pixel(cell.x_pos, cell.y_pos, 9)

    def setup(self):
        nbr_of_cells = range(random.randint(0, 20))
        for x in nbr_of_cells:
            self.cells.append(Cell(random.randint(0, 4), random.randint(0, 4)))
        self.paint_cells()

    def run(self):
        running = True
        self.setup()
        while True:
            running = True
            while running:
                microbit.sleep(1000)
                running = self.next_step()
            self.setup()

main = Main()
main.run()