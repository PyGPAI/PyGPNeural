import random
import numpy as np
from vtk_classes.vtk_animation_timer_callback import VTKAnimationTimerCallback
from vtk_classes.vtk_displayer import VTKDisplayer


def show_landscape(point_displayer):
    from opensimplex import OpenSimplex
    import random

    simplex_r = OpenSimplex(seed=364)
    simplex_g = OpenSimplex(seed=535)
    simplex_b = OpenSimplex(seed=656)

    for i in range(100000):
        x = random.randint(0, 1000, 4237842 + i)
        y = random.randint(0, 1000, 5437474 + i)

        r1 = .0009765625 * (simplex_g.noise2d(x=x, y=y))
        r2 = .001953125 * (simplex_r.noise2d(x=x / 2.0, y=y / 2.0))
        r3 = .00390625 * (simplex_b.noise2d(x=x / 4.0, y=y / 4.0, ))
        r4 = .0078125 * (simplex_g.noise2d(x=x / 8.0, y=y / 8.0))
        r5 = .015625 * (simplex_r.noise2d(x=x / 16.0, y=y / 16.0))
        r6 = .03125 * (simplex_b.noise2d(x=x / 32.0, y=y / 32.0))
        r7 = .0625 * (simplex_g.noise2d(x=x / 64.0, y=y / 64.0))
        r8 = .125 * (simplex_r.noise2d(x=x / 128.0, y=y / 128.0))
        r9 = .25 * (simplex_b.noise2d(x=x / 256.0, y=y / 256.0))
        normalization_factor = .5
        val = ((r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8 + r9) / 2.0)
        if val > 0:
            p = 1.0
        else:
            p = -1.0
        norm_val = (abs(val) ** normalization_factor) * p
        pos_val = (norm_val + 1.0) / 2.0
        z = pos_val * 254.0

        point_displayer.add_point([x - 100, y - 100, z - 100], [160, int(z), 20])


def show_cloud(point_displayer):
    from opensimplex import OpenSimplex
    import math
    import random

    simplex_r = OpenSimplex(seed=364)
    simplex_g = OpenSimplex(seed=535)
    simplex_b = OpenSimplex(seed=656)

    for i in range(100000):

        x = random.randint(0, 1000)
        y = random.randint(0, 1000)
        z = random.randint(0, 1000)

        d = math.sqrt((x - 500) ** 2 + (y - 500) ** 2 + (z - 500) ** 2) / 500.0

        r1 = .0009765625 * (simplex_g.noise3d(x=x, y=y, z=z))
        r2 = .001953125 * (simplex_r.noise3d(x=x / 2.0, y=y / 2.0, z=z / 2.0))
        r3 = .00390625 * (simplex_b.noise3d(x=x / 4.0, y=y / 4.0, z=z / 4.0))
        r4 = .0078125 * (simplex_g.noise3d(x=x / 8.0, y=y / 8.0, z=z / 8.0))
        r5 = .015625 * (simplex_r.noise3d(x=x / 16.0, y=y / 16.0, z=z / 16.0))
        r6 = .03125 * (simplex_b.noise3d(x=x / 32.0, y=y / 32.0, z=z / 32.0))
        r7 = .0625 * (simplex_g.noise3d(x=x / 64.0, y=y / 64.0, z=z / 64.0))
        r8 = .125 * (simplex_r.noise3d(x=x / 128.0, y=y / 128.0, z=z / 128.0))
        r9 = .25 * (simplex_b.noise3d(x=x / 256.0, y=y / 256.0, z=z / 256.0))
        r10 = .5 * (simplex_g.noise3d(x=x / 512.0, y=y / 512.0, z=z / 512.0))
        r11 = (simplex_r.noise3d(x=x / 1024.0, y=y / 1024.0, z=z / 1024.0))
        val = ((r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8 + r9) / 2.0)
        if val > 0:
            p = 1.0
        else:
            p = -1.0

        # use ^d for cumulus clouds,
        # use distance from a certain height for a sky of clouds
        # use constant power <1 for endless 3d field of clouds
        # use distance from sets of points or lines for other shapes

        norm_val = (abs(val) ** d) * p
        pos_val = (norm_val + 1.0) / 2.0
        r = int(pos_val * 254.0)
        # r5 = int((r5)*255.0/2.0)
        # lim octaves->inf gives 1/2^x sum (=1)
        if r > 160:
            point_displayer.add_point([x, y, z], [r, r, r])


def show_rand_line_cube(point_displayer):
    import random as rand

    line_a = rand.sample(range(0, 500), 500)
    line_b = rand.sample(range(500, 1000), 500)

    for i in range(len(line_a)):
        r = rand.randint(0, 255, 5453476 + i)
        g = rand.randint(0, 255, 5983279 + i)
        b = rand.randint(0, 255, 9827312 + i)
        point_displayer.add_line(line_a[i], line_b[i], [r, g, b])


class PointLineTester(VTKAnimationTimerCallback):
    def __init__(self):
        # super().__init__()
        super(PointLineTester, self).__init__()

    def loop(self, obj, event):
        rand_points = [2, random.randint(0, 40 * 40 * 2 - 1), random.randint(0, 40 * 40 * 2 - 1)]

        if len(self.line_id_array) > 0 and random.randint(0, 10) < 9:
            self.del_lines(0)
        self.add_lines(rand_points, [128, 99, 21])

        self.add_points([[random.randint(-50,50),random.randint(-50,50),random.randint(-50,50)]],[[0,0,0]])

        if random.randint(0, 40) == 1:
            self.del_all_lines()
            self.set_all_point_colors([int(128), int(66), int(21)])

        rand_points = np.array([random.randint(0, 40 * 40 * 2 - 1) for x in range(20)])
        rand_colors = np.array([[85, 36, 0] for x in range(10)])
        rand_colors = np.append(rand_colors, [([212, 151, 106]) for x in range(10)], axis=0)

        self.set_point_colors(rand_colors, rand_points)


def display_test_point_loop():
    point_displayer = VTKDisplayer(PointLineTester)
    add_array(point_displayer, [40, 40, 2], [0, 1, 0], [0, 1, 0], [int(128), int(66), int(21)])
    point_displayer.set_poly_data()
    point_displayer.visualize()

if __name__ == '__main__':
    display_test_point_loop()