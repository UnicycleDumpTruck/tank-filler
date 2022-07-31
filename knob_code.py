# SPDX-FileCopyrightText: 2021 John Furcean
# SPDX-License-Identifier: MIT

"""I2C rotary encoders in array of Knobs."""

import board
from adafruit_seesaw import seesaw, rotaryio, digitalio

RESOLUTION = 20  # Only change on every nth position.


class Knob():
    def __init__(self, seesaw):
        self.seesaw = seesaw
        seesaw_product = (self.seesaw.get_version() >> 16) & 0xFFFF
        print("Found product {}".format(seesaw_product))
        if seesaw_product != 4991:
            print("Wrong firmware loaded?  Expected 4991")

        self.button = digitalio.DigitalIO(seesaw, 24)
        self.button_held = False
        self.encoder = rotaryio.IncrementalEncoder(self.seesaw)
        self.last_position = 0

    def update(self):
        position = -self.encoder.position
        if position > self.last_position:
            self.last_position = position
            print("Position increased to: {}".format(position))
            if position % RESOLUTION == 0:
                print("ADD "*15)
        elif position < self.last_position:
            self.last_position = position
            print("Position decreased to: {}".format(position))
            if position % RESOLUTION == 0:
                print("REMOVE "*15)
        if not self.button.value and not self.button_held:
            self.button_held = True
            print("Button pressed")
        if self.button.value and self.button_held:
            self.button_held = False
            print("Button released")


knobs = [Knob(seesaw.Seesaw(board.I2C(), addr=0x36))]
knobs.append(Knob(seesaw.Seesaw(board.I2C(), addr=0x37)))
knobs.append(Knob(seesaw.Seesaw(board.I2C(), addr=0x38)))
#knobs.append(Knob(seesaw.Seesaw(board.I2C(), addr=0x39)))
#knobs.append(Knob(seesaw.Seesaw(board.I2C(), addr=0x3a)))
#knobs.append(Knob(seesaw.Seesaw(board.I2C(), addr=0x3b)))
#knobs.append(Knob(seesaw.Seesaw(board.I2C(), addr=0x3c)))
#knobs.append(Knob(seesaw.Seesaw(board.I2C(), addr=0x3d)))


while True:

    for knob in knobs:
        knob.update()
