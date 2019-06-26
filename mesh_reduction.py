#include <vtkXMLPolyDataReader.h>
#include <vtkPolyData.h>
#include <vtkSphereSource.h>
#include <vtkTriangleFilter.h>
#include <vtkDecimatePro.h>
#include <vtkSmartPointer.h>
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkRenderer.h>
#include <vtkCamera.h>

#include <vtkNamedColors.h>
import vtk


def main(argc, argv):
    inputPolyData = vtk.vtkPolyData()
    if argc > 1:
        reader = vtk.vtkXMLPolyDataReader() 
        reader.SetFileName(argv[1])
        triangles = vtk.vtkTriangleFilter() 
        triangles.SetInputConnection(reader.GetOutputPort())
        triangles.Update()
        inputPolyData = triangles.GetOutput()
    else:
        sphereSource = vtk.vtkSphereSource()
        sphereSource.SetThetaResolution(100)
        sphereSource.SetPhiResolution(100)
        sphereSource.Update()
        inputPolyData = sphereSource.GetOutput()

    reduction = 0.999 # 90% reduction
    if argc > 2:
        reduction = float(argv[2])

    colors = vtk.vtkNamedColors()
    print("Before decimation")
    print("There are ", inputPolyData.GetNumberOfPoints(), " points.")
    print("There are ", inputPolyData.GetNumberOfPolys(), " polygons.")

    decimate = vtk.vtkDecimatePro()
    decimate.SetInputData(inputPolyData)
    decimate.SetTargetReduction(reduction)
    decimate.PreserveTopologyOff()
    decimate.SplittingOn()
    decimate.BoundaryVertexDeletionOn()
    decimate.Update()

    decimated = vtk.vtkPolyData()
    decimated.ShallowCopy(decimate.GetOutput())

    print("After decimation")
    print("There are ", decimated.GetNumberOfPoints() ," points.")
    print("There are ", decimated.GetNumberOfPolys(), " polygons.")
    print("Reduction: ", ((inputPolyData.GetNumberOfPolys() - decimated.GetNumberOfPolys())) / (inputPolyData.GetNumberOfPolys()))

    inputMapper = vtk.vtkPolyDataMapper()
    inputMapper.SetInputData(inputPolyData)

    backFace = vtk.vtkProperty()
    backFace.SetColor(colors.GetColor3d("gold"))

    inputActor = vtk.vtkActor()
    inputActor.SetMapper(inputMapper)
    inputActor.GetProperty().SetInterpolationToFlat()
    inputActor.GetProperty().SetColor(colors.GetColor3d("flesh"))
    inputActor.SetBackfaceProperty(backFace)

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

    # Define viewport ranges
    # (xmin, ymin, xmax, ymax)
    leftViewport = [0.0, 0.0, 0.5, 1.0]
    rightViewport = [0.5, 0.0, 1.0, 1.0]

    # Setup both renderers
    leftRenderer = vtk.vtkRenderer()
    renderWindow.AddRenderer(leftRenderer)
    leftRenderer.SetViewport(leftViewport)
    leftRenderer.SetBackground(.6, .5, .4)

    rightRenderer = vtk.vtkRenderer()
    renderWindow.AddRenderer(rightRenderer)
    rightRenderer.SetViewport(rightViewport)
    rightRenderer.SetBackground(.4, .5, .6)

    # Add the sphere to the left and the cube to the right
    leftRenderer.AddActor(inputActor)
    rightRenderer.AddActor(decimatedActor)

    # Shared camera
    # Shared camera looking down the -y axis
    camera = vtk.vtkCamera()
    camera.SetPosition (0, -1, 0)
    camera.SetFocalPoint (0, 0, 0)
    camera.SetViewUp (0, 0, 1)
    camera.Elevation(30)
    camera.Azimuth(30)
    
    leftRenderer.SetActiveCamera(camera)
    rightRenderer.SetActiveCamera(camera)

    leftRenderer.ResetCamera()
    leftRenderer.ResetCameraClippingRange()

    renderWindow.Render()
    interactor.Start()

if __name__ == '__main__':
    main(1, 90)