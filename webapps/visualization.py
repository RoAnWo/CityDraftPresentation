# Import javascript modules
from js import THREE, window, document, Object, console

# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js

#Import python module
import math

# Import NumPy as np
import numpy as np


#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM

def main():
    # VISUAL SETUP
    # Declare the variables

    global renderer, scene, camera, controls,composer

    #Set up the renderer

    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

 # Set up the scene

    scene = THREE.Scene.new()
    back_color = THREE.Color.new(0,0,0)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(80, window.innerWidth/window.innerHeight, 0.1, 10000)
    camera.position.z = 200
    scene.add(camera)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window

    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 



    #-----------------------------------------------------------------------



    #YOUR DESIGN / GEOMETRY GENERATION

    global geom1_params
    geom1_params = {

        "test": 1,
        "test1": 1,

    }

    geom1_params = Object.fromEntries(to_js(geom1_params))

    #Generating blockperimeterdevelopment
    global BaseShapeLines
    
    # valid solution 1:
    BaseShape1 = [np.array([0, 0]), np.array([40, 40]), np.array([40, 0])] 
    #R
    G(BaseShape1)
    
    BaseShape2 = [np.array([120, 0]), np.array([40, 0]), np.array([40, 40]), np.array([120, 40])] 
    #g
    B(BaseShape2)
    BaseShape21 = [np.array([120, 0]), np.array([100, 0]), np.array([100, 20]), np.array([120, 20])]
    R(BaseShape21)
    BaseShape22 = [np.array([100, 0]), np.array([80, 0]), np.array([80, 20]), np.array([100, 20])]
    R(BaseShape22)
    BaseShape23 = [np.array([80, 0]), np.array([60, 0]), np.array([60, 20]), np.array([80, 20])]
    R(BaseShape23)
    BaseShape24 = [np.array([60, 0]), np.array([40, 0]), np.array([40, 20]), np.array([60, 20])]
    R(BaseShape24)
    BaseShape25 = [np.array([120, 20]), np.array([100, 20]), np.array([100, 40]), np.array([120, 40])]
    R(BaseShape25)
    BaseShape26 = [np.array([100, 20]), np.array([80, 20]), np.array([80, 40]), np.array([100, 40])]
    R(BaseShape26)
    BaseShape27 = [np.array([80, 20]), np.array([60, 20]), np.array([60, 40]), np.array([80, 40])]
    R(BaseShape27)
    BaseShape28 = [np.array([60, 20]), np.array([40, 20]), np.array([40, 40]), np.array([60, 40])]
    R(BaseShape28)   
    
    BaseShape3 = [np.array([120, 0]), np.array([120, 40]), np.array([160, 60]), np.array([180, 10]), np.array([160, 0])]
    #p
    P(BaseShape3)
    BaseShape4 = [np.array([120, 80]), np.array([120, 100]), np.array([160, 100]), np.array([160, 60]), np.array([120, 40])] 
    #g
    G(BaseShape4)
    BaseShape5 = [np.array([120, 80]), np.array([60, 80]), np.array([40, 40]), np.array([120, 40])]
    #c 
    C3(BaseShape5)
    BaseShape6 = [np.array([0, 0]), np.array([0, 60]), np.array([40, 40])] 
    #g
    G(BaseShape6)
    BaseShape7 = [np.array([0, 60]), np.array([40, 40]), np.array([60, 80]), np.array([60, 100]), np.array([0, 100])] 
    #g
    G(BaseShape7)
    BaseShape8 = [np.array([120, 80]), np.array([120, 100]), np.array([60, 100]), np.array([60, 80])] 
    #c
    C2(BaseShape8)
    BaseShape9 = [np.array([120, 100]), np.array([60, 100]), np.array([60, 140])]
    #c
    C(BaseShape9)
    BaseShape10 = [np.array([0, 140]), np.array([0, 100]), np.array([60, 100]), np.array([60, 140])]
    #i
    I(BaseShape10)
    
    

    
        #-----------------------------------------------------------------------

    # Set up Mouse orbit control

    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    #-----------------------------------------------------------------------

    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    #Space for potential GUI- might be added later (still WIP)!


    render()
    
def G(arraypoints):
    arraylines = generateLinesNum(arraypoints)
    Plotboundary = transferNumLines(arraylines)
    draw_system(Plotboundary)
 

    #generate list of x and y coordinates

    global Xcoordinates, Ycoordinates

    Xcoordinates = []
 
    xCoordAr = []
    yCoordAr = []
    Ycoordinates = []

    for m in range(len(arraypoints)):
        Xcoordinates.append(arraypoints[m][0])
        #xCoordAr.append(float(BaseShapePoints[m][0]))
        Ycoordinates.append(arraypoints[m][1])
        #yCoordAr.append(float(BaseShapePoints[m][1]))


    #greenery(Xcoordinates,Ycoordinates)
    #offsetting Shape returns newX, newY
  
    makeOffsetPoly(Xcoordinates,Ycoordinates, 2)
 
    xCoordAr, yCoordAr = makeFloatfromPoint(Xcoordinates,Ycoordinates)
    greenery(xCoordAr,yCoordAr,THREE.Color.new("rgb(112,128,47)"))

def P(arraypoints):
    arraylines = generateLinesNum(arraypoints)
    
    Plotboundary = transferNumLines(arraylines)

    draw_system(Plotboundary)
 

    #generate list of x and y coordinates

    global Xcoordinates, Ycoordinates

    Xcoordinates = []
 
    xCoordAr = []
    yCoordAr = []
    Ycoordinates = []

    for m in range(len(arraypoints)):
        Xcoordinates.append(arraypoints[m][0])
        #xCoordAr.append(float(BaseShapePoints[m][0]))
        Ycoordinates.append(arraypoints[m][1])
        #yCoordAr.append(float(BaseShapePoints[m][1]))


    #greenery(Xcoordinates,Ycoordinates)
    #offsetting Shape returns newX, newY
  
    makeOffsetPoly(Xcoordinates,Ycoordinates, 2)
 
    xCoordAr, yCoordAr = makeFloatfromPoint(Xcoordinates,Ycoordinates)
    greenery(xCoordAr,yCoordAr,THREE.Color.new("rgb(100,100,100)"))

def B(arraypoints):
    arraylines = generateLinesNum(arraypoints)
    Plotboundary = transferNumLines(arraylines)
    draw_system(Plotboundary)
    
def R(arraypoints):
    arraylines = generateLinesNum(arraypoints)
    # Plotboundary = transferNumLines(arraylines)
    # draw_system(Plotboundary)

    #generate Baseshape of x and y coordinates
    global Xcoordinates, Ycoordinates
    Xcoordinates = []
    Ycoordinates = []

    for m in range(len(arraypoints)):
        Xcoordinates.append(arraypoints[m][0])
        Ycoordinates.append(arraypoints[m][1])
       
 
    #greenery(Xcoordinates,Ycoordinates)
    #offsetting Shape returns newX, newY
  
    makeOffsetPoly(Xcoordinates,Ycoordinates, 3)

    #generate greenery for value G


    #convert x and y lists 
    xCoordAr, yCoordAr = makeFloatfromPoint(newX,newY)
   
    
    #generate list of lines
    IntersectionLines = ListPoint2Lines(newX,newY)
     #Transferring NumPy-Lines into Three.js for visualization    
    IntersectionLines = transferNumLines(IntersectionLines)
    draw_system(IntersectionLines)

    #check distance of intersectes points and offsets plot if possible
    # if offset_valid_plots(newX, newY) == True:
    #     makeOffsetPoly(newX,newY, 10)
    
    
    # BlockPermiterLines = ListPoint2Lines(newX,newY)
    #  #Transferring NumPy-Lines into Three.js for visualization    
    # BlockPermiterLines = transferNumLines(BlockPermiterLines)
    # draw_system(BlockPermiterLines)
    generateShaperesidential(xCoordAr,yCoordAr,THREE.Color.new(255, 255, 255))

def I(arraypoints):
    arraylines = generateLinesNum(arraypoints)
    Plotboundary = transferNumLines(arraylines)
    draw_system(Plotboundary)

    #generate Baseshape of x and y coordinates
    global Xcoordinates, Ycoordinates
    Xcoordinates = []
    Ycoordinates = []

    for m in range(len(arraypoints)):
        Xcoordinates.append(arraypoints[m][0])
        Ycoordinates.append(arraypoints[m][1])
       
 
    #greenery(Xcoordinates,Ycoordinates)
    #offsetting Shape returns newX, newY
  
    makeOffsetPoly(Xcoordinates,Ycoordinates, -4)

    #convert x and y lists 
    xCoordAr, yCoordAr = makeFloatfromPoint(newX,newY)
   
    
    #generate list of lines
    IntersectionLines = ListPoint2Lines(newX,newY)
     #Transferring NumPy-Lines into Three.js for visualization    
    IntersectionLines = transferNumLines(IntersectionLines)
    draw_system(IntersectionLines)

    #check distance of intersectes points and offsets plot if possible
    # if offset_valid_plots(newX, newY) == True:
    #     makeOffsetPoly(newX,newY, 10)
    
    
    # BlockPermiterLines = ListPoint2Lines(newX,newY)
    #  #Transferring NumPy-Lines into Three.js for visualization    
    # BlockPermiterLines = transferNumLines(BlockPermiterLines)
    # draw_system(BlockPermiterLines)
    generateShape(xCoordAr,yCoordAr,THREE.Color.new(200, 200, 200))

def C(arraypoints):
    
    arraylines = generateLinesNum(arraypoints)
    Plotboundary = transferNumLines(arraylines)
    draw_system(Plotboundary)
 

    #generate Baseshape of x and y coordinates
    global Xcoordinates, Ycoordinates
    Xcoordinates = []
    Ycoordinates = []

    for m in range(len(arraypoints)):
        Xcoordinates.append(arraypoints[m][0])
        Ycoordinates.append(arraypoints[m][1])
       
 
    #greenery(Xcoordinates,Ycoordinates)
    #offsetting Shape returns newX, newY
  
    makeOffsetPoly(Xcoordinates,Ycoordinates, 2)
    #generate greenery for value G


    #convert x and y lists 
    xCoordAr, yCoordAr = makeFloatfromPoint(newX,newY)
   
    
    #generate list of lines
    IntersectionLines = ListPoint2Lines(newX,newY)
     #Transferring NumPy-Lines into Three.js for visualization    
    IntersectionLines = transferNumLines(IntersectionLines)
    draw_system(IntersectionLines)

    #check distance of intersectes points and offsets plot if possible
    if offset_valid_plots(newX, newY) == True:
        makeOffsetPoly(newX,newY, 7)
    
    
    BlockPermiterLines = ListPoint2Lines(newX,newY)
     #Transferring NumPy-Lines into Three.js for visualization    
    BlockPermiterLines = transferNumLines(BlockPermiterLines)
    draw_system(BlockPermiterLines)
    generateShapeblock(xCoordAr,yCoordAr,THREE.Color.new(255, 255, 255),newX, newY, BlockPermiterLines)

def C2(arraypoints):
    
    arraylines = generateLinesNum(arraypoints)
    Plotboundary = transferNumLines(arraylines)
    draw_system(Plotboundary)
 

    #generate Baseshape of x and y coordinates
    global Xcoordinates, Ycoordinates
    Xcoordinates = []
    Ycoordinates = []

    for m in range(len(arraypoints)):
        Xcoordinates.append(arraypoints[m][0])
        Ycoordinates.append(arraypoints[m][1])
       
 
    #greenery(Xcoordinates,Ycoordinates)
    #offsetting Shape returns newX, newY
  
    makeOffsetPoly(Xcoordinates,Ycoordinates, -2)
    #generate greenery for value G


    #convert x and y lists 
    xCoordAr, yCoordAr = makeFloatfromPoint(newX,newY)
   
    
    #generate list of lines
    IntersectionLines = ListPoint2Lines(newX,newY)
     #Transferring NumPy-Lines into Three.js for visualization    
    IntersectionLines = transferNumLines(IntersectionLines)
    draw_system(IntersectionLines)

    #check distance of intersectes points and offsets plot if possible
    if offset_valid_plots(newX, newY) == True:
        makeOffsetPoly(newX,newY, -6)
        
        BlockPermiterLines = ListPoint2Lines(newX,newY)
        #Transferring NumPy-Lines into Three.js for visualization    
        BlockPermiterLines = transferNumLines(BlockPermiterLines)
        draw_system(BlockPermiterLines)
        generateShapeblock(xCoordAr,yCoordAr,THREE.Color.new(255, 255, 255),newX, newY, BlockPermiterLines)
    
    else:
        generateShape(xCoordAr,yCoordAr,THREE.Color.new(255, 255, 255))
    
def C3(arraypoints):
    
    arraylines = generateLinesNum(arraypoints)
    Plotboundary = transferNumLines(arraylines)
    draw_system(Plotboundary)
 

    #generate Baseshape of x and y coordinates
    global Xcoordinates, Ycoordinates
    Xcoordinates = []
    Ycoordinates = []

    for m in range(len(arraypoints)):
        Xcoordinates.append(arraypoints[m][0])
        Ycoordinates.append(arraypoints[m][1])
       
 
    #greenery(Xcoordinates,Ycoordinates)
    #offsetting Shape returns newX, newY
  
    makeOffsetPoly(Xcoordinates,Ycoordinates, -2)
    #generate greenery for value G


    #convert x and y lists 
    xCoordAr, yCoordAr = makeFloatfromPoint(newX,newY)
   
    
    #generate list of lines
    IntersectionLines = ListPoint2Lines(newX,newY)
     #Transferring NumPy-Lines into Three.js for visualization    
    IntersectionLines = transferNumLines(IntersectionLines)
    draw_system(IntersectionLines)

    #check distance of intersectes points and offsets plot if possible
    if offset_valid_plots(newX, newY) == True:
        makeOffsetPoly(newX,newY, -10)
    
    
    BlockPermiterLines = ListPoint2Lines(newX,newY)
     #Transferring NumPy-Lines into Three.js for visualization    
    BlockPermiterLines = transferNumLines(BlockPermiterLines)
    draw_system(BlockPermiterLines)
    generateShapeblock(xCoordAr,yCoordAr,THREE.Color.new(255, 255, 255),newX, newY, BlockPermiterLines)

#HELPER FUNCTIONS 
def generateLinesNum(listpoints):
        listLines = []
        
        for i in range(len(listpoints)):
            if i < len(listpoints)-1:
                CurrentLine = [listpoints[i], listpoints[i+1]]
                listLines.append(CurrentLine)

            else:
                CurrentLine = [listpoints[i], listpoints[i-(len(listpoints)-1)]]
                listLines.append(CurrentLine)
        return listLines
     
def makeFloatfromPoint(xlist,ylist):
    fXlist = []
    fyList = []
    for fx in xlist:
        fXlist.append(float(fx))
    for fy in ylist:
        fyList.append(float(fy))
    return fXlist,fyList

def ListPoint2Lines(x,y):

    BlockPermiter = []
    for k in range(len(x)): 
        BlockPermiter.append(np.array([x[k], y[k]]))
    lines = []
    for h in range(len(BlockPermiter)):
        if h < len(BlockPermiter)-1:
            CurrentLine = [BlockPermiter[h], BlockPermiter[h+1]]
            lines.append(CurrentLine)

        else:
            CurrentLine = [BlockPermiter[h], BlockPermiter[h-(len(BlockPermiter)-1)]]
            lines.append(CurrentLine)
    return lines

def transferNumLines(ListStartEndpoint): 

        Currentoffset = []
        ListStartEndVec = []

    #offset Shape

        for i in ListStartEndpoint:
            for j in i:
                TempArrayToList = j.tolist()
                ThreeVec1 = THREE.Vector2.new(TempArrayToList[0],TempArrayToList[1])
                Currentoffset.append(ThreeVec1)
            ListStartEndVec.append (Currentoffset)
            Currentoffset = []
        return ListStartEndVec
        

def normalizeVec(x,y):

    distance = np.sqrt(x*x+y*y)
    return x/distance, y/distance

def makeOffsetPoly(oldX, oldY, offset, outer_ccw = 1):
    

    num_points = len(oldX)
    global newX,newY

    newX = []
    newY = []

    for indexpoint in range(num_points):
        prev = (indexpoint + num_points -1 ) % num_points
        next = (indexpoint + 1) % num_points
        vnX =  oldX[next] - oldX[indexpoint]
        vnY =  oldY[next] - oldY[indexpoint]
        vnnX, vnnY = normalizeVec(vnX,vnY)
        nnnX = vnnY
        nnnY = -vnnX
        vpX =  oldX[indexpoint] - oldX[prev]
        vpY =  oldY[indexpoint] - oldY[prev]
        vpnX, vpnY = normalizeVec(vpX,vpY)
        npnX = vpnY * outer_ccw
        npnY = -vpnX * outer_ccw
        bisX = (nnnX + npnX) * outer_ccw
        bisY = (nnnY + npnY) * outer_ccw
        bisnX, bisnY = normalizeVec(bisX,  bisY)
        bislen = offset /  np.sqrt((1 + nnnX*npnX + nnnY*npnY)/2)

        newX.append(oldX[indexpoint] + bislen * bisnX)
        newY.append(oldY[indexpoint] + bislen * bisnY)
        
        
def offset_valid_plots(xcoord, ycoord):



        global LengthList
        LengthList = []

        for i in range(len(xcoord)-1):
            length = np.sqrt((xcoord[i]-xcoord[i+1])**2 + ((ycoord[i]-ycoord[i+1])**2))
            LengthList.append(length)

        if min(LengthList) >= 7:
            return True



#calculate area
def Area(corners):

    n = len(corners) # of corners
    area = 0

    for i in range(n):
        j = (i + 1) % n
        area += (corners[i][0] * corners[j][1])
        area -= (corners[j][0] * corners[i][1])
    area = abs(area)/2.0

    return area

#Turning the generated point-list into a drawn line
def draw_system(lines):

    for points in lines:
        line_geom = THREE.BufferGeometry.new()

        points = to_js(points)
        line_geom.setFromPoints( points )
        material = THREE.LineBasicMaterial.new( THREE.Color.new(0x0000ff))
        vis_line = THREE.Line.new( line_geom, material )

        global scene
        scene.add(vis_line)



#generate shape to extrude
def generateShape(xCordsArray,yCordsArray, color):


    extrudeSettings = {"steps" : 20,"depth" : 5,"bevelEnabled": False, "bevelSize": 0 }
    extrudeSettings = Object.fromEntries(to_js(extrudeSettings ))
    
    shape_Green = THREE.Shape.new()
  
    for i in range(len(xCordsArray)):
        if i == 0 :
            shape_Green.moveTo (xCordsArray[i], yCordsArray[i])
        else: 
            shape_Green.lineTo(xCordsArray[i], yCordsArray[i])  

    geometry = THREE.ExtrudeGeometry.new(shape_Green,extrudeSettings)
    mesh_material = THREE.MeshBasicMaterial.new(color)
    mesh_material.transparent = True
    mesh_material.opacity = 0.1
    mesh_material.color = color
    mesh = THREE.Mesh.new(geometry, mesh_material)
    edgesout = THREE.EdgesGeometry.new( geometry )
    line = THREE.LineSegments.new( edgesout, THREE.LineBasicMaterial.new( color ) )
    
    global scene
    scene.add( line )
    scene.add(mesh)

def generateShaperesidential(xCordsArray,yCordsArray, color):


    extrudeSettings = {"steps" : 20,"depth" : 7,"bevelEnabled": False, "bevelSize": 0 }
    extrudeSettings = Object.fromEntries(to_js(extrudeSettings ))
    
    shape_Green = THREE.Shape.new()
  
    for i in range(len(xCordsArray)):
        if i == 0 :
            shape_Green.moveTo (xCordsArray[i], yCordsArray[i])
        else: 
            shape_Green.lineTo(xCordsArray[i], yCordsArray[i])  

    geometry = THREE.ExtrudeGeometry.new(shape_Green,extrudeSettings)
    mesh_material = THREE.MeshBasicMaterial.new(color)
    mesh_material.transparent = True
    mesh_material.opacity = 0.3
    mesh_material.color = color
    mesh = THREE.Mesh.new(geometry, mesh_material)
    edgesout = THREE.EdgesGeometry.new( geometry )
    line = THREE.LineSegments.new( edgesout, THREE.LineBasicMaterial.new( color ) )
    
    global scene
    scene.add( line )
    scene.add(mesh)
    
def generateShapeblock(xCordsArray,yCordsArray, color, xCordsHoles, yCordsHoles, array):


    extrudeSettings = {"steps" : 20,"depth" : 12,"bevelEnabled": False, "bevelSize": 0 }
    extrudeSettings = Object.fromEntries(to_js(extrudeSettings ))
    
    shape_Green = THREE.Shape.new()
  
    for i in range(len(xCordsArray)):
        if i == 0 :
            shape_Green.moveTo (xCordsArray[i], yCordsArray[i])
        else: 
            shape_Green.lineTo(xCordsArray[i], yCordsArray[i])  
    
    shape_hole = THREE.Shape.new()
    for i in range(len(xCordsHoles)):
        if i == 0 :
            shape_hole.moveTo (xCordsHoles[i], yCordsHoles[i])
        else: 
            shape_hole.lineTo(xCordsHoles[i], yCordsHoles[i])  
    
    shape_Green.holes.push(shape_hole)
    geometry = THREE.ExtrudeGeometry.new(shape_Green,extrudeSettings)
    mesh_material = THREE.MeshBasicMaterial.new(color)
    mesh_material.transparent = True
    mesh_material.opacity = 0.5
    mesh_material.color = color
    mesh = THREE.Mesh.new(geometry, mesh_material)
    edgesout = THREE.EdgesGeometry.new( geometry )
    line = THREE.LineSegments.new( edgesout, THREE.LineBasicMaterial.new( color ) )
    
    
    global scene
    scene.add( line )
    scene.add(mesh)
    
    for points in array:

        points = to_js(points)
    
        shape = THREE.Shape.new(points) 
    
        geometry2 = THREE.ExtrudeGeometry.new(shape,extrudeSettings)
        mesh_material = THREE.MeshBasicMaterial.new(color)
        mesh_material.transparent = True
        mesh_material.opacity = 0.2
        mesh_material.color = color
        mesh2 = THREE.Mesh.new(geometry2, mesh_material)
    
        edges = THREE.EdgesGeometry.new( geometry2 )
        line = THREE.LineSegments.new( edges, THREE.LineBasicMaterial.new( color ) )
        scene.add( line )
        scene.add(mesh2)

def greenery(xCordsArray,yCordsArray,colorgreen):

    shape_Green = THREE.Shape.new()

    for i in range(len(xCordsArray)):
        if i == 0 :
            #("moveTo",xCordsArray[i], yCordsArray[i])
            shape_Green.moveTo (xCordsArray[i], yCordsArray[i])
        else: 
            shape_Green.lineTo(xCordsArray[i], yCordsArray[i])     
    geometrygreenery = THREE.ShapeGeometry.new(shape_Green)
    
    #colorgreen = 
    meshgreen_material = THREE.MeshBasicMaterial.new(colorgreen)
    meshgreen_material.color = colorgreen

    meshgreen = THREE.Mesh.new(geometrygreenery, meshgreen_material)
    scene.add(meshgreen)



# Simple render and animate

def render(*args):

    window.requestAnimationFrame(create_proxy(render))
    controls.update()
    composer.render()

# Graphical post-processing



def post_process():

    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)
    pixelRatio = window.devicePixelRatio
    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )

    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)



# Adjust display when window size changes



def on_window_resize(event):
    event.preventDefault()
    global renderer
    global camera
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()
    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing after resize
    post_process()

#-----------------------------------------------------------------------

#RUN THE MAIN PROGRAM

if __name__=='__main__':
    main()
