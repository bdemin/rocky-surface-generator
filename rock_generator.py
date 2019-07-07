import numpy as np
from random import gauss

from vtk import (vtkPlane, vtkClipPolyData, vtkSphereSource,\
                vtkPolyData, vtkXMLPolyDataReader,\
                vtkDataSetMapper, vtkStripper, vtkRenderWindowInteractor,\
                vtkFeatureEdges, vtkPolyDataMapper, vtkActor, vtkRenderer,\
                vtkRenderWindow, VTK_MAJOR_VERSION,\
                vtkOrientationMarkerWidget, vtkAxesActor)


class Rock():
    def __init__(self, radius):
        self.sphereSource = vtkSphereSource()
        self.sphereSource.SetThetaResolution(200)
        self.sphereSource.SetPhiResolution(200)
        self.sphereSource.SetRadius(radius)

    def use_chisel(self):
        return cut_with_planes(self.sphereSource)


from vtk import vtkPoints, vtkPlanes, vtkDoubleArray

def cut_with_planes(obj):
    #This function take a obj (vtk source) and cuts it with a plane defined by normal and point.

    num_cuts = 40
    rad_tol = 0.5
    point_min = obj.GetRadius() - rad_tol

    points = vtkPoints()
    normals = vtkDoubleArray()
    normals.SetNumberOfComponents(3)
    for i in range(num_cuts):
        normal = make_rand_vector()
        point = (point_min + np.random.rand(3) * rad_tol/2) * np.sign(normal)
        normals.InsertNextTuple(normal)
        points.InsertNextPoint(*point)

    #Create vtkPlanes object:
    planes = vtkPlanes()
    planes.SetPoints(points)
    planes.SetNormals(normals)
    #Create clipper object:
    clipper = vtkClipPolyData()
    clipper.SetInputConnection(obj.GetOutputPort())
    clipper.SetClipFunction(planes)

    #Cut in the positive side of the plane:
    # clipper.SetValue(0)
    clipper.InsideOutOn()
    clipper.Update()

    #Returned as cut vtkPolyData:
    return clipper.GetOutput()

def make_rand_vector():
    vec = [gauss(0, 1) for i in range(3)]
    mag = sum(x**2 for x in vec) ** .5
    return [x/mag for x in vec]



rock = Rock(1)
polyData = rock.use_chisel()
mapper = vtkDataSetMapper()
mapper.SetInputData(polyData)

clipActor = vtkActor()
clipActor.SetMapper(mapper)
clipActor.GetProperty().SetColor(1.0000, 0.3882, 0.2784)
clipActor.GetProperty().SetInterpolationToFlat()

# Now extract feature edges
boundaryEdges = vtkFeatureEdges()
boundaryEdges.SetInputData(polyData)

boundaryEdges.BoundaryEdgesOn()
boundaryEdges.FeatureEdgesOff()
boundaryEdges.NonManifoldEdgesOff()
boundaryEdges.ManifoldEdgesOff()

boundaryStrips = vtkStripper()
boundaryStrips.SetInputConnection(boundaryEdges.GetOutputPort())
boundaryStrips.Update()

# Change the polylines into polygons
boundaryPoly = vtkPolyData()
boundaryPoly.SetPoints(boundaryStrips.GetOutput().GetPoints())
boundaryPoly.SetPolys(boundaryStrips.GetOutput().GetLines())

boundaryMapper = vtkPolyDataMapper()
boundaryMapper.SetInputData(boundaryPoly)

boundaryActor = vtkActor()
boundaryActor.SetMapper(boundaryMapper)
boundaryActor.GetProperty().SetColor(0.8900, 0.8100, 0.3400)

# create render window, renderer and interactor
renderWindow = vtkRenderWindow()
renderer = vtkRenderer()
renderWindow.AddRenderer(renderer)
iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renderWindow)

# set background color
renderer.SetBackground(.2, .3, .4)
# add our actor to the renderer
renderer.AddActor(clipActor)
renderer.AddActor(boundaryActor)
# Generate an interesting view
renderer.ResetCamera()
# renderer.GetActiveCamera().Azimuth(30)
# renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Dolly(1.2)
renderer.ResetCameraClippingRange()

axesActor = vtkAxesActor()
widget = vtkOrientationMarkerWidget()
widget.SetOrientationMarker(axesActor)
widget.SetInteractor(iren)
widget.SetEnabled(1)
widget.InteractiveOff()



renderWindow.Render()
iren.Start()