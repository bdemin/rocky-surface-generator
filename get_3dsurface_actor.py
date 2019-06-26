import numpy as np

from vtk import vtkPoints, vtkCellArray, vtkTriangle, \
    vtkPolyData, vtkLookupTable, vtkCleanPolyData, \
    vtkUnsignedCharArray, vtkLoopSubdivisionFilter, \
    vtkPolyDataMapper, vtkActor


color_map = True
color_map = False
def get_3dsurface_actor(path_directory):
    path_directory = path_directory
    x_data = np.loadtxt(path_directory + 'x.txt', delimiter = ',')
    y_data = np.loadtxt(path_directory + 'y.txt', delimiter = ',')
    z_data = np.loadtxt(path_directory + 'z.txt', delimiter = ',')
    z_data -= 0.1 #fix ground clipping
    
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
    
    if color_map:
        #%% Create colormap
        bounds= 6*[0.0]
        PolyData.GetBounds(bounds)

        # Find min and max z
        minz = bounds[4]
        maxz = bounds[5]

        colorLookupTable = vtkLookupTable()
        colorLookupTable.SetTableRange(minz, maxz)
        colorLookupTable.Build()

        # Generate the colors for each point based on the color map
        colors = vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)
        colors.SetName("Colors")
            
        for i in range(0, PolyData.GetNumberOfPoints()):
            p= 3*[0.0]
            PolyData.GetPoint(i,p)

            dcolor = 3*[0.0]
            colorLookupTable.GetColor(p[2], dcolor)

            color=3*[0.0]
            for j in range(0,3):
                color[j] = int(255.0 * dcolor[j])

            try:
                colors.InsertNextTupleValue(color)
            except AttributeError:
                # For compatibility with new VTK generic data arrays.
                colors.InsertNextTypedTuple(color)


        PolyData.GetPointData().SetScalars(colors)

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
    
#    actor_loop.GetProperty().SetColor(0.929, 0.788, 0.686)
#    actor_loop.GetProperty().SetAmbient(0.1)
#    actor_loop.GetProperty().SetAmbientColor(0.3,0.3,0.3)
    
#    actor_loop.GetProperty().SetDiffuse(0.1)
#    actor_loop.GetProperty().SetDiffuseColor(0.396, 0.263, 0.129)
#    actor_loop.GetProperty().SetInterpolationToPhong()
#    actor_loop.GetProperty().SetSpecular(0.6)
#    actor_loop.GetProperty().SetSpecularPower(10)
#    actor_loop.GetProperty().EdgeVisibilityOn()
    
#    actor_loop.GetProperty().SetLineWidth(0.2)

    return actor_loop