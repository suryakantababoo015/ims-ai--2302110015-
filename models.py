from dataclasses import dataclass
from cadquery import func as cf


@dataclass
class CellSpec:
    r_cell: float  # mm
    h_cell: float  # mm


def make_cell(spec):
    return cf.cylinder(d=2 * spec.r_cell, h=spec.h_cell)


def tray(spec, n=3, clearance=0.3, wall=4.0, thickness=6.0, depth=3.0):
    pocket_r = spec.r_cell + clearance
    pitch = 2 * pocket_r + wall
    plate = cf.box(n * pitch + wall, 2 * pocket_r + 2 * wall, thickness)
    pocket = cf.cylinder(d=2 * pocket_r, h=depth + 1).moved(z=thickness - depth)
    for i in range(n):
        plate = plate - pocket.moved(x=(i - (n - 1) / 2) * pitch)
    return plate


cells = {
    "18650": CellSpec(9.0, 65.0),
    "21700": CellSpec(10.5, 70.0),
    "4680": CellSpec(23.0, 80.0),
    # My upgrade: a new cell format from a real datasheet (26650 = O26 x 65 mm)
    "26650": CellSpec(13.0, 65.0),
}


if __name__ == "__main__":
    for name, spec in cells.items():
        t = tray(spec)
        print(name, t.isValid(), round(t.Volume(), 1))
        t.exportStl(f"tray_{name}.stl")
