from vtk import (vtkPolyData, vtkXMLPolyDataReader, vtkSphereSource, vtkPlane,\
    vtkClipPolyData, vtkDataSetMapper, vtkStripper, vtkRenderWindowInteractor,\
    vtkFeatureEdges, vtkPolyDataMapper, vtkActor, vtkRenderer, vtkRenderWindow, VTK_MAJOR_VERSION,\
    vtkOrientationMarkerWidget, vtkAxesActor)


planeNorm = (0,0,-1)
planePoint = (0,0,-1)
sphere_rad = 5

# Create a sphere
sphereSource = vtkSphereSource()
sphereSource.SetThetaResolution(2000)
sphereSource.SetPhiResolution(1000)
sphereSource.SetRadius(sphere_rad)

plane = vtkPlane()
plane.SetOrigin(planePoint)
plane.SetNormal(planeNorm)

clipper1 = vtkClipPolyData()
clipper1.SetInputConnection(sphereSource.GetOutputPort())
clipper1.SetClipFunction(plane)

# clipper1.SetValue(0)
clipper1.InsideOutOn()
clipper1.Update()


plane2 = vtkPlane()
plane2.SetOrigin((1,1,0))
plane2.SetNormal((1,1,1))
clipper2 = vtkClipPolyData()
clipper2.SetInputConnection(clipper1.GetOutputPort())
clipper2.SetClipFunction(plane2)
clipper2.InsideOutOn()
clipper2.Update()

plane3 = vtkPlane()
plane3.SetOrigin((1,1,1))
plane3.SetNormal((2,1,2))
clipper3 = vtkClipPolyData()
clipper3.SetInputConnection(clipper2.GetOutputPort())
clipper3.SetClipFunction(plane3)
clipper3.InsideOutOn()
clipper3.Update()



polyData = clipper3.GetOutput()



clipMapper = vtkDataSetMapper()
clipMapper.SetInputData(polyData)

clipActor = vtkActor()
clipActor.SetMapper(clipMapper)
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