import numpy as np

from vtk import (vtkPlane, vtkClipPolyData)


class Rock():
    def __init__(self):
        self.rad = np.random.randint(0,100) * 0.1

        phi = np.linspace(0, np.pi, 20)
        theta = np.linspace(0, 2 * np.pi, 40)
        x = np.outer(np.sin(theta), np.cos(phi))
        y = np.outer(np.sin(theta), np.sin(phi))
        z = np.outer(np.cos(theta), np.ones_like(phi))


def cut_with_plane(obj, normal, point):
    #This function take a obj (vtk source) and cuts it with a plane defined by normal and point

    #Create vtkPlane object:
    plane = vtkPlane()
    plane.SetNormal(*normal)
    plane.SetOrigin(*point)

    #Create clipper object:
    clipper = vtkClipPolyData()
    clipper.SetInputConnection(obj.GetOutputPort())
    clipper.SetClipFunction(plane)

    #Cut in the positive side of the plane:
    clipper.InsideOutOn()
    clipper.Update()

    #Returned as cut vtkPolyData:
    return clipper.GetOutput()