import vtk
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from vtk_animation_timer_callback import VTKAnimationTimerCallback
from vtk_keypress_interactor_style import VTKKeyPressInteractorStyle


class VTKDisplayer:
    # adapted from:
    # http://www.vtk.org/Wiki/VTK/Examples/Python/GeometricObjects/Display/Point
    def __init__(self, callback_class, *args, **kwargs):
        self.points = vtk.vtkPoints()
        self.vertices = vtk.vtkCellArray()

        self.point_colors = vtk.vtkUnsignedCharArray()
        self.point_colors.SetNumberOfComponents(3)
        self.point_colors.SetName("Colors")

        self.lines = vtk.vtkCellArray()

        self.line_colors = vtk.vtkUnsignedCharArray()
        self.line_colors.SetNumberOfComponents(3)
        self.line_colors.SetName("Colors")

        assert issubclass(callback_class, VTKAnimationTimerCallback)
        self.callback_class = callback_class
        self.callback_class_args = args
        self.callback_class_kwargs = kwargs

        self._set_poly_data()

    def _set_poly_data(self):

        self.points_poly = vtk.vtkPolyData()
        self.points_poly.SetPoints(self.points)
        self.points_poly.SetVerts(self.vertices)

        self.points_poly.GetPointData().SetScalars(self.point_colors)

        self.lines_poly = vtk.vtkPolyData()
        self.lines_poly.SetPoints(self.points)
        self.lines_poly.SetLines(self.lines)

        self.lines_poly.GetCellData().SetScalars(self.line_colors)

    def visualize(self):
        point_mapper = vtk.vtkPolyDataMapper()
        line_mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            point_mapper.SetInput(self.points_poly)
            line_mapper.SetInput(self.lines_poly)
        else:
            point_mapper.SetInputData(self.points_poly)
            line_mapper.SetInputData(self.lines_poly)

        point_actor = vtk.vtkActor()
        line_actor = vtk.vtkActor()

        point_actor.SetMapper(point_mapper)
        line_actor.SetMapper(line_mapper)
        point_actor.GetProperty().SetPointSize(60)  # todo:allow modification
        # actor.GetProperty().SetPointColor

        renderer = vtk.vtkRenderer()

        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)
        render_window_interactor = vtk.vtkRenderWindowInteractor()
        interactor_style = VTKKeyPressInteractorStyle(camera=renderer.GetActiveCamera(),
                                                      render_window=render_window,
                                                      parent=render_window_interactor)
        render_window_interactor.SetInteractorStyle(
            interactor_style
        )

        render_window_interactor.SetRenderWindow(render_window)

        renderer.AddActor(point_actor)
        renderer.AddActor(line_actor)

        # light brown = .6,.6,.4
        # light brown = .2,.2,.1
        # dark brown = .2, .1, 0
        # dusk = .05, .05, .1
        # calm blue sky = .1, .2, .4
        # day blue sky = .2, .4, .8
        # bright blue sky = .6, .8, 1.0 (bg attention activation)
        renderer.SetBackground(66 / 255.0, 132 / 255.0, 125 / 255.0)

        render_window.Render()

        render_window_interactor.Initialize()

        cb = self.callback_class(*self.callback_class_args, **self.callback_class_kwargs)
        cb.interactor_style = interactor_style  # allows adding/removing input functions
        cb.renderer = renderer
        cb.points = self.points
        cb.point_vertices = self.vertices
        cb.points_poly = self.points_poly
        cb.point_colors = self.point_colors
        cb.lines = self.lines
        cb.lines_poly = self.lines_poly
        cb.line_colors = self.line_colors

        render_window_interactor.AddObserver('TimerEvent', cb.execute)
        timer_id = render_window_interactor.CreateRepeatingTimer(10)
        render_window_interactor.Start()

        # cleanup after loop
        cb.at_end()
