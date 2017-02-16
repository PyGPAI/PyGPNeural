import time

import numpy as np
import vtk
from vtk.util import numpy_support

from lib.toolbox.integer import minmax
from lib.toolbox.idarray import IdArray

from lib.toolbox.numpy_helpers import normalize
import math as m

class VTKAnimationTimerCallback(object):
    """This class is called every few milliseconds by VTK based on the set frame rate. This allows for animation.
    I've added several modification functions, such as adding and deleting lines/points, changing colors, etc."""
    __slots__ = ["points", "point_colors", "timer_count", "points_poly",
                 "lines", "lines_poly", "line_colors", "line_id_array"
                                                       "last_velocity_update", "unused_locations",
                 "last_color_velocity_update", "renderer", "last_bg_color_velocity_update",
                 "last_velocity_update", "_loop_time", "remaining_lerp_fade_time", "lerp_multiplier",
                 "line_id_array", "point_id_array", "point_vertices", "interactor_style", "renderer",
                 "interactive_renderer", "_started"
                 ]

    def __init__(self):
        self.timer_count = 0
        self.last_velocity_update = time.clock()
        self.last_color_velocity_update = time.clock()
        self.last_bg_color_velocity_update = time.clock()
        self._loop_time = time.clock()
        self.unused_locations = []
        self.remaining_lerp_fade_time = 0
        self.lerp_multiplier = 1
        self.line_id_array = IdArray()
        self.point_id_array = IdArray()
        self._started=False

    def add_lines(self, lines, line_colors):
        """
        Adds multiple lines between any sets of points.

        Args:
            lines (list, tuple, np.ndarray, np.generic):
                An array in the format of [2, point_a, point_b, 2, point_c, point_d, ...]. The two is needed for VTK's
                  lines.
            line_colors (list, tuple, np.ndarray, np.generic):
                An array in the format of [[r1, g1, b1], [r2, g2, b2], ...], with the same length as the number of
                  lines.
        Returns:
            list: An array containing the memory locations of each of the newly inserted lines.

        """
        assert (isinstance(lines, (list, tuple, np.ndarray, np.generic)))
        assert (isinstance(line_colors, (list, tuple, np.ndarray, np.generic)))

        np_line_data = numpy_support.vtk_to_numpy(self.lines.GetData())
        np_line_color_data = numpy_support.vtk_to_numpy(self.line_colors)

        #todo: add lines in unused locations if possible
        mem_locations = range(int(len(np_line_data) / 3), int((len(np_line_data) + len(lines)) / 3))

        np_line_data = np.append(np_line_data, lines)

        if len(np_line_color_data) > 0:
            np_line_color_data = np.append(np_line_color_data, line_colors, axis=0)
        else:
            np_line_color_data = line_colors

        vtk_line_data = numpy_support.numpy_to_vtkIdTypeArray(np_line_data, deep=True)
        self.lines.SetCells(int(len(np_line_data) / 3), vtk_line_data)

        vtk_line_color_data = numpy_support.numpy_to_vtk(num_array=np_line_color_data,
                                                         deep=True, array_type=vtk.VTK_UNSIGNED_CHAR)
        self.line_colors.DeepCopy(vtk_line_color_data)

        self.lines_poly.Modified()

        self.line_id_array.add_ids(mem_locations)

        return mem_locations

    def del_all_lines(self):
        """
        Deletes all lines.
        """
        vtk_data = numpy_support.numpy_to_vtkIdTypeArray(np.array([], dtype=np.int64), deep=True)
        self.lines.SetCells(0, vtk_data)

        vtk_data = numpy_support.numpy_to_vtk(num_array=np.array([]), deep=True, array_type=vtk.VTK_UNSIGNED_CHAR)
        self.line_colors.DeepCopy(vtk_data)

        self.lines_poly.Modified()

    def del_lines(self, line_indices):
        #todo: change idarray to use tuples of (start,end) locations and set this to delete those partitions
        """
        Delete specific lines.

        Args:
            line_indices (tuple, list, np.ndarray, np.generic):
                An array of integers or a single integer representing line memory locations(s) to delete.
        """
        np_data = numpy_support.vtk_to_numpy(self.lines.GetData())

        np_color_data = numpy_support.vtk_to_numpy(self.line_colors)

        if isinstance(line_indices, (tuple, list, np.ndarray, np.generic)):
            last_loc = -1
            loc = 0
            np_new_data = []
            np_new_color_data = []
            for i in range(len(line_indices)):
                loc = self.line_id_array.pop_id(line_indices[i])
                if loc==None:
                    #todo: put warning here
                    continue

                if len(np_new_data) > 0:
                    np_new_data = np.append(np_new_data, np_data[(last_loc + 1) * 3:loc * 3], axis=0)
                else:
                    np_new_data = np_data[(last_loc + 1) * 3:loc * 3]

                if len(np_new_color_data) > 0:
                    np_new_color_data = np.append(np_new_color_data, np_color_data[(last_loc + 1):loc], axis=0)
                else:
                    np_new_color_data = np_color_data[(last_loc + 1):loc]

                last_loc = loc

            last_loc = loc
            loc = len(np_data) / 3

            np_data = np.append(np_new_data, np_data[(last_loc + 1) * 3:loc * 3], axis=0)

            np_data = np_data.astype(np.int64)

            np_color_data = np.append(np_new_color_data, np_color_data[(last_loc + 1):loc], axis=0)
        else:
            raise TypeError("Deletion list should be tuple, list, np.ndarray, or np.generic")

        vtk_data = numpy_support.numpy_to_vtkIdTypeArray(np_data, deep=True)
        self.lines.SetCells(int(len(np_data) / 3), vtk_data)

        vtk_data = numpy_support.numpy_to_vtk(num_array=np_color_data, deep=True, array_type=vtk.VTK_UNSIGNED_CHAR)
        self.line_colors.DeepCopy(vtk_data)

        self.lines_poly.Modified()

    def del_points(self, point_indices):
        """
        Delete specific points.

        Args:
            point_indices (tuple, list, np.ndarray, np.generic):
                An array of integers or a single integer representing point memory locations(s) to delete.
        """
        np_point_data = numpy_support.vtk_to_numpy(self.points.GetData())
        np_point_color_data = numpy_support.vtk_to_numpy(self.point_colors)
        np_vert_data = numpy_support.vtk_to_numpy(self.point_vertices.GetData())#1,1,1,2,1,3,1,4,1,5,1,6...

        print(len(np_vert_data), len(np_point_data), len(np_point_color_data))

        if isinstance(point_indices, (tuple, list, np.ndarray, np.generic)):
            last_loc = -1
            loc = 0
            subtractor = 0
            np_new_data = []
            np_new_color_data = []
            np_new_verts = []
            for i in range(len(point_indices)):
                loc = self.point_id_array.pop_id(point_indices[i])
                if loc == None:
                    # todo: put warning here
                    continue

                subtractor+=1

                #I could just remove the end of the array, but this keeps the lines attached to the same points
                if len(np_new_verts) >0:
                    np_new_verts = np.append(np_new_verts, np_vert_data[(last_loc+1)*2:loc*2], axis = 0)
                else:
                    np_new_verts = np_vert_data[(last_loc+1)*2: loc*2]

                if len(np_new_data) > 0:
                    np_new_data = np.append(np_new_data, np_point_data[(last_loc + 1):loc], axis=0)
                else:
                    np_new_data = np_point_data[(last_loc + 1):loc]

                if len(np_new_color_data) > 0:
                    np_new_color_data = np.append(np_new_color_data, np_point_color_data[(last_loc + 1)*3:loc*3], axis=0)
                else:
                    np_new_color_data = np_point_color_data[(last_loc + 1):loc]

                last_loc = loc

            if loc == None:
                return

            last_loc = loc
            loc = len(np_point_data)

            np_point_data = np.append(np_new_data, np_point_data[(last_loc + 1):loc], axis=0)

            np_point_color_data = np.append(np_new_color_data, np_point_color_data[(last_loc + 1):loc], axis=0)

            np_vert_data = np.append(np_new_verts, np_vert_data[(last_loc + 1)*2:loc*2], axis = 0)
        else:
            raise TypeError("Deletion list should be tuple, list, np.ndarray, or np.generic")

        vtk_data = numpy_support.numpy_to_vtk(np_point_data, deep=True)
        self.points.SetData(vtk_data)

        vtk_data = numpy_support.numpy_to_vtk(num_array=np_point_color_data, deep=True, array_type=vtk.VTK_UNSIGNED_CHAR)
        self.point_colors.DeepCopy(vtk_data)

        vtk_data = numpy_support.numpy_to_vtkIdTypeArray(np_vert_data, deep=True)
        self.point_vertices.SetCells(int(len(np_vert_data) / 2), vtk_data)

        self.lines_poly.Modified()

    def add_points(self, points, point_colors):
        """
        Adds points in 3d space.

        Args:
            points (tuple, list, np.ndarray, np.generic):
                An array in the format of [[x1,y1,z1], [x2,y2,x2], ..., [xn,yn,zn]]
            point_colors (tuple, list, np.ndarray, np.generic):
                An array in the format of [[r1, g1, b1], [r2, g2, b2], ...], with the same length as the number of
                  points to be added.

        Returns:

        """
        assert (isinstance(points, (list, tuple, np.ndarray, np.generic)))
        assert (isinstance(point_colors, (list, tuple, np.ndarray, np.generic)))

        np_point_data = numpy_support.vtk_to_numpy(self.points.GetData())
        np_point_color_data = numpy_support.vtk_to_numpy(self.point_colors)
        np_vert_data = numpy_support.vtk_to_numpy(self.point_vertices.GetData())

        print(np_vert_data)

        for i in range(len(points)):
            #todo: modify pointer_id_array to set free pointers to deleted data, not deleted data locations
            if len(self.point_id_array.free_pointers)>0:
                np_vert_data = np.append(np_vert_data, [1,self.point_id_array.free_pointers.pop()])
            else:
                np_vert_data = np.append(np_vert_data,[1, len(np_vert_data)/2])

        mem_locations = range(int(len(np_point_data)), int((len(np_point_data) + len(points))))

        if len(np_point_data) > 0:
            np_point_data = np.append(np_point_data, points, axis=0)
        else:
            np_point_data = points

        if len(point_colors) ==1:
            points = np.array(points)
            point_colors = np.tile(point_colors, (points.shape[0], 1))

        if len(np_point_color_data) > 0:
            np_point_color_data = np.append(np_point_color_data, point_colors, axis=0)
        else:
            np_point_color_data = point_colors

        vtk_point_data = numpy_support.numpy_to_vtk(num_array=np_point_data, deep=True, array_type=vtk.VTK_FLOAT)

        self.points.SetData(vtk_point_data)


        vtk_data = numpy_support.numpy_to_vtkIdTypeArray(np_vert_data.astype(np.int64), deep=True)
        self.point_vertices.SetCells(int(len(np_vert_data) / 2), vtk_data)

        vtk_point_color_data = numpy_support.numpy_to_vtk(num_array=np_point_color_data,
                                                         deep=True, array_type=vtk.VTK_UNSIGNED_CHAR)
        self.point_colors.DeepCopy(vtk_point_color_data)

        self.points_poly.Modified()

        self.point_id_array.add_ids(mem_locations)
        #print(self.point_id_array)

        return mem_locations

    def add_point_field(self, widths, normal, center, color):
        """
        Adds a rectangular field of points.
        Args:
            widths (tuple, list, np.ndarray, np.generic):  an array defining the widths of each dimension of the field.
            normal (tuple, list, np.ndarray, np.generic): an array defining the normal to the field. Specifies angle.
            center (tuple, list, np.ndarray, np.generic): an array defining the central position of the field.
            color (tuple, list, np.ndarray, np.generic):
                An array in the format of [[r1, g1, b1], [r2, g2, b2], ...], with the same length as the number of
                  points to be added, or a single color in the form of [[r1, g1, b1]].

        Returns:
            A list of integers representing the memory locations where the points were added.

        """
        true_normal = normalize(normal)
        if not np.allclose(true_normal, [1, 0, 0]):
            zn = np.cross(true_normal, [1, 0, 0])
            xn = np.cross(true_normal, zn)
        else:
            xn = [1, 0, 0]
            zn = [0, 0, 1]
        point_field = np.array([])
        #todo: replace for loops with numpy or gpu ops
        for z in range(-int(m.floor(widths[2] / 2.0)), int(m.ceil(widths[2] / 2.0))):
            for y in range(-int(m.floor(widths[1] / 2.0)), int(m.ceil(widths[1] / 2.0))):
                for x in range(-int(m.floor(widths[0] / 2.0)), int(m.ceil(widths[0] / 2.0))):
                    vector_space_matrix = np.column_stack(
                        (np.transpose(xn), np.transpose(true_normal), np.transpose(zn)))
                    translation = np.matmul([x, y, z], vector_space_matrix)
                    point_location = [center[0], center[1], center[2]] + translation
                    point_location = [point_location]
                    if len(point_field)>0:
                        point_field = np.append(point_field, point_location, axis = 0)
                    else:
                        point_field = point_location
        return self.add_points(point_field, color) #returns ids

    def set_bg_color(self, color):
        """
        Sets the background color of the viewport.

        Args:
            color (tuple, list, np.ndarray, np.generic): a single rgb color in the form of [[int, int, int]]
        """
        r, g, b = color[0]
        r,g,b = (r/255.,g/255.,b/255.)
        self.renderer.SetBackground((minmax(r, 0, 1), minmax(g, 0, 1), minmax(b, 0, 1)))
        self.renderer.Modified()

    def set_all_point_colors(self, color):
        """
        Sets the color of every point.

        Args:
            color (tuple, list, np.ndarray, np.generic): a single rgb color in the form of [[int, int, int]]
        """
        np_color_data = numpy_support.vtk_to_numpy(self.point_colors)
        np_color_data = np.tile(color, (np_color_data.shape[0], 1))
        vtk_data = numpy_support.numpy_to_vtk(num_array=np_color_data, deep=True, array_type=vtk.VTK_UNSIGNED_CHAR)
        self.point_colors.DeepCopy(vtk_data)

    def set_point_colors(self, colors, point_indices=None):
        if point_indices is None:
            if isinstance(colors, (list, tuple, np.ndarray, np.generic)):
                vtk_data = numpy_support.numpy_to_vtk(num_array=colors, deep=True, array_type=vtk.VTK_UNSIGNED_CHAR)
                self.point_colors.DeepCopy(vtk_data)
        elif isinstance(point_indices, (list, tuple, np.ndarray, np.generic)):
            np_color_data = numpy_support.vtk_to_numpy(self.point_colors)
            np_color_data[point_indices] = colors
            vtk_data = numpy_support.numpy_to_vtk(num_array=np_color_data, deep=True, array_type=vtk.VTK_UNSIGNED_CHAR)
            self.point_colors.DeepCopy(vtk_data)

        # self.points_poly.GetPointData().GetScalars().Modified()
        self.points_poly.Modified()

    def setup_lerp_all_point_colors(self, color, fade_time):
        """
        Sets all points to the same color, but uses lerping to slowly change the colors.

        Args:
            color ():
            fade_time ():
        """
        np_color_data = numpy_support.vtk_to_numpy(self.point_colors)
        self.next_colors = np.tile(color, (np_color_data.shape[0], 1))
        self.prev_colors = numpy_support.vtk_to_numpy(self.point_colors)

        self.lerp_fade_time = fade_time
        self.remaining_lerp_fade_time = fade_time

    def lerp_point_colors(self, colors, fade_time, point_indices=None):
        """
        Sets colors for specific points, but uses lerping to slowly change those colors.

        Args:
            colors ():
            fade_time ():
            point_indices ():
        """
        if isinstance(self.next_colors, (np.ndarray, np.generic)):
            if isinstance(point_indices, (list, tuple, np.ndarray, np.generic)):
                self.next_colors[point_indices] = colors
            else:
                self.next_colors = colors
            self.next_color_indices = None
        elif isinstance(point_indices, (list, tuple, np.ndarray, np.generic)) or isinstance(colors, (list, tuple)):
            if self.lerp_fade_time > 0:
                self.next_colors = np.append(self.next_colors, colors)
                if point_indices is not None:
                    self.next_color_indices = np.append(self.next_color_indices, point_indices)
            else:
                self.next_colors = colors
                self.next_color_indices = point_indices
                # must should not already be lerping
                self.prev_colors = numpy_support.vtk_to_numpy(self.point_colors)
        # fade time in seconds, float
        self.lerp_fade_time = fade_time
        self.remaining_lerp_fade_time = fade_time

    def set_lerp_remainder(self, lerp_remainder):
        """
        Sets the portion of color from the previous color set remains after the lerp has been fully run.

        Args:
            lerp_remainder ():
        """
        self.lerp_multiplier = 1 - lerp_remainder

    def _calculate_point_color_lerp(self):
        """
        Linearly interpolates colors. In addition to making animation look smoother, it helps prevent seizures a little.
        Only a little though, and it has to be used correctly. Still, using it at all helps.
        """
        if self.remaining_lerp_fade_time > 0:

            # print(self.lerp_fade_time, self.remaining_lerp_fade_time)

            lerp_val = self.lerp_multiplier * (
            self.lerp_fade_time - self.remaining_lerp_fade_time) / self.lerp_fade_time

            # print(lerp_val)

            diff_array = (self.prev_colors - self.next_colors)

            lerp_diff_array = diff_array * lerp_val

            # print(lerp_diff_array)

            lerp_colors = self.prev_colors - lerp_diff_array

            # print(lerp_colors)

            if isinstance(lerp_colors, (np.ndarray, np.generic)):
                vtk_data = numpy_support.numpy_to_vtk(num_array=lerp_colors, deep=True,
                                                      array_type=vtk.VTK_UNSIGNED_CHAR)
                self.point_colors.DeepCopy(vtk_data)

            # self.points_poly.GetPointData().GetScalars().Modified()
            self.points_poly.Modified()

            self.remaining_lerp_fade_time -= self.loop_change_in_time
            # print(self.remaining_lerp_fade_time)

    def position_points(self, positions, point_indices=None):
        #todo:unit test

        """
        Untested with most recent changes.

        Sets the positions of specific points, all points, or one point.

        Args:
            positions ():
            point_indices ():
        """
        if point_indices == None:
            vtk_data = numpy_support.numpy_to_vtk(num_array=positions, deep=True, array_type=vtk.VTK_FLOAT)
            self.points.DeepCopy(vtk_data)
        elif isinstance(point_indices, (list, tuple)):
            if isinstance(positions, (list, tuple)):
                for i in range(len(point_indices)):
                    x, y, z = positions[i % len(positions)]
                    self.points.SetPoint(point_indices[i], (x, y, z))
            else:
                for i in range(len(point_indices)):
                    x, y, z = positions
                    self.points.SetPoint(point_indices[i], (x, y, z))
        else:
            x, y, z = positions
            self.points.SetPoint(point_indices, (x, y, z))
        self.points_poly.Modified()

    def add_key_input_functions(self, keydic):
        """
        Sets functions to be called when specific keys are pressed, in order from shallowest to deepest dictionaries.

        If a key is already in the dictionary, it will be replaced.

        Args:
            keydic ():
        """
        self.interactor_style.append_input_combinations(keydic)

    def at_start(self):
        """
        Function to be run after class instantiation and vtk start up. Useful for setting things that can only be set
        after VTK is running.
        """
        pass


    def loop(self, obj, event):
        """
        Function called every few milliseconds when VTK is set to call. Variables that need updating like change_in_time
        can be set here.

        Args:
            obj ():
            event ():
        """
        self.loop_change_in_time = time.clock() - self._loop_time
        self._loop_time = time.clock()
        self._calculate_point_color_lerp()
        pass

    def at_end(self):
        """
        Function called when animation is ended.
        """
        self.interactive_renderer.RemoveAllObservers()

    def exit(self):
        # needed to stop previous setups from being run on next class call
        # proper cleanup
        self.interactive_renderer.TerminateApp()

    def execute(self, obj, event):
        """
        Function called to start animation.

        Args:
            obj ():
            event ():
        """
        if not self._started:
            self.at_start()
            self._started = True

        self.loop(obj, event)

        self.points_poly.GetPointData().GetScalars().Modified()
        self.points_poly.Modified()

        self.interactive_renderer = obj
        self.interactive_renderer.GetRenderWindow().Render()
