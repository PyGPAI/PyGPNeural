#everything is from https://stackoverflow.com/a/2459541/782170


import numpy as np

import vtk

#todo: create 3d testing library for point clouds
class MockModel(object):
    def __init__(self):
        self.dots = []

    def add_block(self, position):
        self.dots.append((*position,))

    def batch_blocks(self, array_in):
        self.dots = array_in


    def show_cloud(self):
        points = vtk.vtkPoints()

        vertices = vtk.vtkCellArray()

        for d in self.dots:
            p = points.InsertNextPoint((d[0], d[1], d[2]))
            vertices.InsertNextCell(1)
            vertices.InsertCellPoint(p)

        cloud = vtk.vtkPolyData()

        cloud.SetPoints(points)
        cloud.SetVerts(vertices)

        # Visualize
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(cloud)
        else:
            mapper.SetInputData(cloud)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetPointSize(2)

        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        renderer.AddActor(actor)

        renderWindow.Render()
        renderWindowInteractor.Start()


import math as m

def cartesian_to_hex(x, y, scale=1.0/6.0):
    b = (y/2)/(3*scale)
    r = (m.sqrt(3)*x - y)/(3*scale)
    return b,r

def hex_to_cartesian(b, r, scale=6.0):
    y = (3*scale*b)/2
    x = (m.sqrt(3)*scale)*(b/2 + r)
    return x,y

if __name__ == '__main__':
    mod = MockModel()
    for b in range(0,10):
        for r in range(0,10):
            x,y = hex_to_cartesian(b,r)
            mod.add_block((x,y,0))
    mod.show_cloud()

