import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as pcm
from matplotlib.patches import Wedge
from matplotlib.collections import PatchCollection

__all__ = ["Pin", "plot_pin", "plot_pins"]


class Pin:
    def __init__(self, radii, thetas, values):
        """
        Initialize Pin instance with `radii`, `thetas`, and `values`.

        `radii` is an iterable object specifying the radii from inner to outer.
        The first radius in `radii` must *not* be 0.

        `thetas` is an iterable object specifying the angles. The first angle
        in `thetas` must be 0.

        `values` is an interable object specifying the value in each mesh.
        """
        self.radii = radii
        self.thetas = thetas
        if len(radii) * len(thetas) != len(values):
            raise ValueError("Value number does not match mesh number.")
        self.values = values

    def get_value(self, radius_index, theta_index):
        return self.values[len(self.thetas) * radius_index + theta_index]


def _get_wedges_colors(pin, center=(0, 0)):
    wedges = []
    colors = []
    for i in range(len(pin.radii)):
        for j in range(len(pin.thetas)):
            if i == 0:
                width = pin.radii[0]
            else:
                width = pin.radii[i] - pin.radii[i-1]
            if j == len(pin.thetas) - 1:
                theta2 = 360.0
            else:
                theta2 = pin.thetas[j+1]
            wedges.append(Wedge(center=center, r=pin.radii[i],
                                width=width, theta1=pin.thetas[j],
                                theta2=theta2, linewidth=0.0))
            colors.append(pin.get_value(i, j))
    return wedges, colors


def plot_pin(pin, *, to_file=None, dpi=600):
    wedges, colors = _get_wedges_colors(pin)
    p = PatchCollection(wedges, cmap=pcm.jet, alpha=1.0, edgecolor="None",
                        linewidth=0.0)
    p.set_array(np.array(colors))

    fig, ax = plt.subplots()
    fig.set_facecolor("blue")
    ax.add_collection(p)
    plt.colorbar(p, shrink=0.8, extend="neither", extendfrac=0.0, format="$%.3f$")
    ax_size = max(pin.radii) + 0.1*max(pin.radii)
    plt.ylim(-ax_size, ax_size)
    plt.xlim(-ax_size, ax_size)
    plt.axis("off")
    if to_file:
        plt.savefig(to_file, dpi=dpi, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
    else:
        plt.show()


def plot_pins(pins, pitch, *, to_file=None, dpi=600):
    row_num = len(pins)
    column_num = len(pins[0])
    all_wedges = []
    all_colors = []
    for i in range(row_num):
        for j in range(column_num):
            if pins[i][j] is None:
                continue
            row = row_num - i - 1
            column = j
            center = (column*pitch, row*pitch)
            wedges, colors = _get_wedges_colors(pins[i][j], center)
            all_wedges += wedges
            all_colors += colors
    p = PatchCollection(all_wedges, cmap=pcm.jet, alpha=1.0, edgecolor="None",
                        linewidth=0.0)
    p.set_array(np.array(all_colors))

    fig, ax = plt.subplots()
    fig.set_facecolor("blue")
    ax.add_collection(p)
    plt.colorbar(p, shrink=0.8, extend="neither", extendfrac=0.0, format="$%.3f$")
    ax_size = max(((row_num-1)*pitch+pitch/2.0, (column_num-1)*pitch+pitch/2.0))
    plt.ylim(-pitch/2.0, ax_size)
    plt.xlim(-pitch/2.0, ax_size)
    plt.axis("off")
    if to_file:
        plt.savefig(to_file, dpi=dpi, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
    else:
        plt.show()


if __name__ == "__main__":
    radii = [i*0.1 for i in range(1, 6)]
    thetas = [i*360.0/4 for i in range(4)]
    pin1 = Pin(radii, thetas, range(20))
    pin2 = Pin(radii, thetas, range(20, 40))
    pin3 = Pin(radii, thetas, range(40, 60))
    pin4 = Pin(radii, thetas, range(60, 80))
    pins = [[pin1, pin3],
            [None, pin4]]
    plot_pins(pins, 1.26)
