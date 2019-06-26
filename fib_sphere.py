add_library('hemesh')
 
phi = (sqrt(5) + 1) / 2 - 1 #Golden Ratio
angle = phi * 2 * PI #Golden Angle
n_points, radius, t = 200, 200, 0
liste = []
 
def setup():
    global triangles, render
    size(600, 600, P3D)
    smooth(8)
 
    render = WB_Render(this)
 
    for p in range(n_points):
        lon = angle * p
        lon /= 2 * PI; lon -= floor(lon); lon *= 2 * PI
        if lon > PI: lon -= 2 * PI
        lat = asin(-1 + 2 * p / float(n_points))
        new_points = WB_Point(radius * cos(lat) * cos(lon), radius * cos(lat) * sin(lon), radius * sin(lat))
        liste.append(new_points)
 
    triangulation = WB_Triangulate.alphaTriangulate3D(liste)
    triangles = triangulation.getAlphaTriangles(radius+1)
 
    noFill()
    beginShape(TRIANGLES)
 
def draw():
    global t
    background(255)
 
    translate(width/2, height/2)
    rotateY(t/2)   
 
    for i in range(0, len(triangles), 3):
        p1 = PVector(liste[triangles[i]].xd(), liste[triangles[i]].yd(), liste[triangles[i]].zd()).normalize()
        p2 = PVector(liste[triangles[i+1]].xd(), liste[triangles[i+1]].yd(), liste[triangles[i+1]].zd()).normalize()
        p3 = PVector(liste[triangles[i+2]].xd(), liste[triangles[i+2]].yd(), liste[triangles[i+2]].zd()).normalize()
 
        for p in [p1, p2, p3]:
            n = map(noise(p.x/2 + t , p.y/2 + t , p.z/2 + t), 0, 1, 40, 100)
            p.mult(n*2)
            vertex(p.x, p.y, p.z)
    endShape()
 
    t += .02