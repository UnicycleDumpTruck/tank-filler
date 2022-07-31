# SPDX-FileCopyrightText: 2021 John Furcean
# SPDX-License-Identifier: MIT

"""I2C rotary encoders in array of Knobs."""

from random import choice
import board
from adafruit_seesaw import seesaw, rotaryio, digitalio

RESOLUTION = 20  # Only change on every nth position.


class Mtx():
    colors = {'off': (0, 0, 0), 'red': (255, 0, 0),
              'green': (0, 255, 0), 'blue': (0, 0, 255)}

    def __init__(self, height, width):
        self.grid = [[Mtx.colors['off']
                      for _ in range(width)] for _ in range(height)]
        self.locations = {key: [] for key in Mtx.colors.keys()}
        self.locations['off'] = [(row, col)
                                 for col in range(width) for row in range(height)]
        # print(self.locations)

    def print_grid(self):
        for row in self.grid:
            for column in row:
                print(str(column).strip(), end="  ")
            print("")

    def add_pxls(self, number, color):
        for _ in range(number):
            if len(self.locations['off']):
                row, col = choice(self.locations['off'])
                self.grid[row][col] = Mtx.colors[color]
                self.locations['off'].remove((row, col))
                self.locations[color].append((row, col))
            else:
                print("No off pixels.")
        self.print_grid()

    def remove_pxls(self, number, color):
        for _ in range(number):
            if len(self.locations[color]):
                row, col = choice(self.locations[color])
                self.grid[row][col] = Mtx.colors['off']
                self.locations[color].remove((row, col))
                self.locations['off'].append((row, col))
            else:
                print(f"No more {color} pixels left.")
        self.print_grid()


mat = Mtx(8, 8)


class Knob():
    def __init__(self, seesaw, matrix: Mtx, color):
        self.seesaw = seesaw
        self.matrix = matrix
        self.color = color
        seesaw_product = (self.seesaw.get_version() >> 16) & 0xFFFF
        print(f"Found product {seesaw_product}")
        if seesaw_product != 4991:
            print("Wrong firmware loaded?  Expected 4991")

        self.button = digitalio.DigitalIO(seesaw, 24)
        self.button_held = False
        self.encoder = rotaryio.IncrementalEncoder(self.seesaw)
        self.last_position = 0
        self.last_change = 0

    def update(self):
        position = -self.encoder.position
        if position > self.last_position:
            print(f"Position increased to: {position}, diff {position - self.last_position}")
            if ((position - self.last_change) > RESOLUTION):
                print("ADD "*15)
                self.matrix.add_pxls(1, self.color)
                self.last_change = position
            self.last_position = position
        elif position < self.last_position:
            print(f"Position decreased to: {position}, diff {self.last_position - position}")
            if ((self.last_change - position) > RESOLUTION):
                print("REMOVE "*15)
                self.matrix.remove_pxls(1, self.color)
                self.last_change = position
            self.last_position = position
        if not self.button.value and not self.button_held:
            self.button_held = True
            print("Button pressed")
        if self.button.value and self.button_held:
            self.button_held = False
            print("Button released")


knobs = [Knob(seesaw.Seesaw(board.I2C(), addr=0x36), mat, 'red')]
#knobs.append(Knob(seesaw.Seesaw(board.I2C(), addr=0x37)))
#knobs.append(Knob(seesaw.Seesaw(board.I2C(), addr=0x38)))
#knobs.append(Knob(seesaw.Seesaw(board.I2C(), addr=0x39)))
#knobs.append(Knob(seesaw.Seesaw(board.I2C(), addr=0x3a)))
#knobs.append(Knob(seesaw.Seesaw(board.I2C(), addr=0x3b)))
#knobs.append(Knob(seesaw.Seesaw(board.I2C(), addr=0x3c)))
#knobs.append(Knob(seesaw.Seesaw(board.I2C(), addr=0x3d)))

# if __name__ == "__main__":

while True:

    for knob in knobs:
        knob.update()
