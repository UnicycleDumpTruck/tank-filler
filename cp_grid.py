"""Neopixel matrix that acts as 'gas mixing' readout."""
from random import choice


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

    def remove_pxls(self, number, color):
        for _ in range(number):
            if len(self.locations[color]):
                row, col = choice(self.locations[color])
                self.grid[row][col] = Mtx.colors['off']
                self.locations[color].remove((row, col))
                self.locations['off'].append((row, col))
            else:
                print(f"No more {color} pixels left.")


if __name__ == "__main__":
    mat = Mtx(8, 8)
    print("Starting Matrix, all off:")
    mat.print_grid()
    print("\nMatrix with 10 blue added randomly:")
    mat.add_pxls(10, 'blue')
    mat.print_grid()
    print("\nMatrix after 5 of those removed:")
    mat.remove_pxls(5, 'blue')
    mat.print_grid()
