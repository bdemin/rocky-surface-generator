import vtk

import numpy as np

from vtk import vtkPoints, vtkCellArray, vtkTriangle, \
    vtkPolyData, vtkLookupTable, vtkCleanPolyData, \
    vtkUnsignedCharArray, vtkLoopSubdivisionFilter, \
    vtkPolyDataMapper, vtkActor


def get_3dsurface_actor():
    size_x = 200
    size_y = 100
    x_data = np.linspace(-100, 100, size_x)
    y_data = np.linspace(-3, 3, size_y)
    z_data = np.zeros((size_x, size_y))
    
    m = z_data.shape[0]
    n = z_data.shape[1]
    
    # Define points, triangles and colors
    points = vtkPoints()
    triangles = vtkCellArray()
    
    # Build the meshgrid:
    #need to try Delauney
    count = 0
    for i in range(m-1):
        for j in range(n-1):
            z1 = z_data[i][j]
            z2 = z_data[i][j+1]
            z3 = z_data[i+1][j]
    
            # Triangle 1
            points.InsertNextPoint(x_data[i], y_data[j], z1)
            points.InsertNextPoint(x_data[i], y_data[j+1], z2)
            points.InsertNextPoint(x_data[i+1], y_data[j], z3)
    
            triangle = vtkTriangle()
            triangle.GetPointIds().SetId(0, count)
            triangle.GetPointIds().SetId(1, count + 1)
            triangle.GetPointIds().SetId(2, count + 2)
    
            triangles.InsertNextCell(triangle)
            
            z1 = z_data[i][j+1]
            z2 = z_data[i+1][j+1]
            z3 = z_data[i+1][j]
    
            # Triangle 2  
            points.InsertNextPoint(x_data[i], y_data[j+1], z1)
            points.InsertNextPoint(x_data[i+1], y_data[j+1], z2)
            points.InsertNextPoint(x_data[i+1], y_data[j], z3)
            
            triangle = vtkTriangle()
            triangle.GetPointIds().SetId(0, count + 3)
            triangle.GetPointIds().SetId(1, count + 4)
            triangle.GetPointIds().SetId(2, count + 5)
    
            count += 6
            triangles.InsertNextCell(triangle)
    
    # Create a polydata object
    PolyData = vtkPolyData()
    
    # Add the geometry and topology to the polydata
    PolyData.SetPoints(points)
    PolyData.SetPolys(triangles)
    

    # Clean the polydata so that the edges are shared !
    cleanPolyData = vtkCleanPolyData()
    cleanPolyData.SetInputData(PolyData)
    
    # Use a filter to smooth the data (will add triangles and smooth)
    smooth_loop = vtkLoopSubdivisionFilter()
    smooth_loop.SetNumberOfSubdivisions(3)
    smooth_loop.SetInputConnection(cleanPolyData.GetOutputPort())
    
    # Create a mapper and actor for smoothed dataset
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(smooth_loop.GetOutputPort())
    
    actor_loop = vtkActor()
    actor_loop.SetMapper(mapper)
    

    return actor_loop




inputPolyData = vtk.vtkPolyData()

sphereSource = vtk.vtkSphereSource()
sphereSource.SetRadius(1)
sphereSource.SetThetaResolution(100)
sphereSource.SetPhiResolution(100)
sphereSource.Update()
inputPolyData = sphereSource.GetOutput()

reduction = 0.999 # 90% reduction

colors = vtk.vtkNamedColors()

decimate = vtk.vtkDecimatePro()
decimate.SetInputData(inputPolyData)
decimate.SetTargetReduction(reduction)
decimate.PreserveTopologyOff()
decimate.SplittingOn()
decimate.BoundaryVertexDeletionOn()
decimate.Update()

decimated = vtk.vtkPolyData()
decimated.ShallowCopy(decimate.GetOutput())

decimatedPoints = []
for i in range(decimated.GetNumberOfPoints()):
    point = decimated.GetPoint(i)
    if point[2] >= 0:
        decimatedPoints.append(point)
    # print(decimated.GetPoint(i))



backFace = vtk.vtkProperty()
backFace.SetColor(colors.GetColor3d("gold"))


decimatedMapper = vtk.vtkPolyDataMapper()
decimatedMapper.SetInputData(decimated)

decimatedActor = vtk.vtkActor()
decimatedActor.SetMapper(decimatedMapper)
decimatedActor.GetProperty().SetColor(colors.GetColor3d("flesh"))
decimatedActor.GetProperty().SetInterpolationToFlat()
decimatedActor.SetBackfaceProperty(backFace)

# There will be one render window
renderWindow = vtk.vtkRenderWindow()
renderWindow.SetSize(600, 300)

# And one interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)


renderer = vtk.vtkRenderer()
renderWindow.AddRenderer(renderer)
renderer.SetBackground(.4, .5, .6)

# Add the sphere to the left and the cube to the right
renderer.AddActor(decimatedActor)
renderer.AddActor(get_3dsurface_actor())

# Shared camera
# Shared camera looking down the -y axis
camera = vtk.vtkCamera()
camera.SetPosition (0, -1, 0)
camera.SetFocalPoint (0, 0, 0)
camera.SetViewUp (0, 0, 1)
camera.Elevation(30)
camera.Azimuth(30)

renderer.SetActiveCamera(camera)

renderer.ResetCamera()

renderWindow.Render()
interactor.Start()