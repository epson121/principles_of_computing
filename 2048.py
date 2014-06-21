"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    res = []
    for elem in line:
        res.append(0)
    counter = 0
    for elem in line:
        if elem == 0:
            pass
        else:
            res[counter] = elem
            counter += 1
    res2 = []
    counter = 0
    while counter < len(res):
        if counter+1 < len(res) and res[counter] == res[counter+1]:
            res2.append(res[counter]*2)
            counter += 2
        else:
            res2.append(res[counter])
            counter += 1
    while len(res2) < len(res):
        res2.append(0)
    return res2

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.grid = self.reset()
        self.initial_tiles = self.compute_initial_tiles()

    def compute_initial_tiles(self):
        """
        Docstring
        """
        initial_up = [[0, x] for x in range(self.grid_width)]
        initial_down = [[self.grid_height-1, x] for x in range(self.grid_width)]
        initial_left = [[x, 0] for x in range(self.grid_height)]
        initial_right = [[x, self.grid_width-1] for x in range(self.grid_height)]
        return {UP: initial_up, LEFT : initial_left, RIGHT : initial_right, DOWN : initial_down}

    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        grid = []
        for _ in range (0, self.grid_height):
            row = []
            for _ in range(0, self.grid_width):
                row.append(0)
            grid.append(row)
        return grid

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        res = ""
        for elem2 in range (0, self.grid_height):
            for elem in range(0, self.grid_width):
                res = res + str(self.grid[elem2][elem]) + " "
            res += "\n"
        return res

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        changed = False
        for elem2 in self.initial_tiles[direction]:
            if self.apply_offset(elem2, direction):
                changed = True
        if changed:
            self.new_tile()
            changed = False

    def apply_offset(self, cell, direction):
        """
        Docstring
        """
        changed = False
        limit =  self.grid_height if direction == UP or direction == DOWN else self.grid_width
        indices = [[cell[0], cell[1]]]
        values = []
        for elem in range(0, limit-1):
            x_temp = indices[-1][0] + OFFSETS[direction][0]
            y_temp = indices[-1][1] + OFFSETS[direction][1]
            indices.append([x_temp, y_temp])
        for elem in indices:
            values.append(self.get_tile(elem[0], elem[1]))
        values_new = merge(values)
        if (values_new != values):
            changed = True
        count = 0
        for elem in indices:
            self.grid[elem[0]][elem[1]] = values_new[count]
            count+=1
        return changed

    def get_empty_cells(self):
        """
        Docstring
        """
        res = []
        for elem in range (0, self.grid_height):
            for elem2 in range(0, self.grid_width):
                if (self.grid[elem][elem2] == 0):
                    empty_cell = [elem, elem2]
                    res.append(empty_cell)
        return res

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty_cells = self.get_empty_cells()
        random_cell = empty_cells[random.randrange(len(empty_cells))]
        random_num = 4 if random.choice('0123456789') == '4' else 2
        self.grid[random_cell[0]][random_cell[1]] = random_num

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
