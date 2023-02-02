# Import javascript modules
from js import THREE, window, document, Object, console
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js
# Import python module
import math
# Import NumPy as np
import numpy as np
import random

#-----------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    #-----------------------------------------------------------------------
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
    back_color = THREE.Color.new(0.1,0.1,0.1)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 1000)
    camera.position.z = 150
    scene.add(camera)

    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    global geom1_params

    geom1_params = {
        "test": 1,
        "test1": 1
    }

    geom1_params = Object.fromEntries(to_js(geom1_params))
    
    #Generating Base Shape
    global BaseShapeLines
    
    BSp1 = np.array([0,0])
    BSp2 = np.array([0,100])
    BSp3 = np.array([100,100])
    BSp4 = np.array([100,0])

    BaseShapePoints = [BSp1,BSp2,BSp3,BSp4]

    BaseShapeLines = []
    for i in range(len(BaseShapePoints)):
        if i < len(BaseShapePoints)-1:
            CurrentLine = [BaseShapePoints[i], BaseShapePoints[i+1]]
            BaseShapeLines.append(CurrentLine)
        else:
            CurrentLine = [BaseShapePoints[i], BaseShapePoints[i-(len(BaseShapePoints)-1)]]
            BaseShapeLines.append(CurrentLine)

    #Generating Input Lines

    ILp1_1 = np.array([-5,20])
    ILp1_2 = np.array([7,25])
    ILp2_1 = np.array([71,108])
    ILp2_2 = np.array([70,92])
    ILp3_1 = np.array([35,70])
    ILp3_2 = np.array([40,69])
    ILp4_1 = np.array([106,35])
    ILp4_2 = np.array([111,49])
    ILp5_1 = np.array([41,0])
    ILp5_2 = np.array([41,11])


    InputLinePoints = [ILp1_1,ILp1_2,ILp2_1,ILp2_2,ILp3_1,ILp3_2,ILp4_1,ILp4_2,ILp5_1,ILp5_2]

    InputLineLines = []
    count = 0
    for i in range(len(InputLinePoints)):
        count += 1
        if count % 2 or count == 0:
            CurrentLine = [InputLinePoints[i], InputLinePoints[i+1]]
            InputLineLines.append(CurrentLine)
        else:
            continue
    randomInputLines = InputLineLines.copy()
    random.shuffle(randomInputLines)
    
    #-------------Hiermit wird weitergearbeitet!:-----------------------------------------------------------------------------------------------------------------
    #-------------mainStreetNetwork beinhaltet alle generierten Straßen(ungesplittet),BaseShapeLines enthält alle äußeren Begrenzungslinien(ungesplittet)---------
    mainStreetNetwork = mainStreetGenerator(BaseShapeLines,randomInputLines)

    #Aus Straßen und Baseshape gehardcodete Plots und dazugehörige Nachbarn
    Plot1 = [np.array([0,0]),np.array([0,22.08333333]),np.array([67.38502674,50.16042781]),np.array([100,63.75]),np.array([100,0])]
    Plot2 = [np.array([0,22.08333333]),np.array([0,77]),np.array([68.20987654, 63.35802469]),np.array([67.38502674,50.16042781])]
    Plot3 = [np.array([0,77]),np.array([100,0]),np.array([70.5, 100]),np.array([68.20987654, 63.35802469])]
    Plot4 = [np.array([70.5, 100]),np.array([100,100]),np.array([100,63.75]),np.array([67.38502674,50.16042781]),np.array([68.20987654, 63.35802469])]
    Plot1Nachbarn = ["Plot2","Plot4"]
    Plot2Nachbarn = ["Plot1","Plot3","Plot4"]
    Plot3Nachbarn = ["Plot2","Plot4"]
    Plot4Nachbarn = ["Plot1","Plot2","Plot3"]


    #Transferring NumPy-Lines into Three.js for visualization
    ThreeCurrentLine = []
    ThreeLinesStreet = []
    ThreeLinesBaseShape = []
    ThreeLinesInput = []

    #BaseShape
    for i in BaseShapeLines:
        for j in i:
            TempArrayToList = j.tolist()
            ThreeVec1 = THREE.Vector2.new(TempArrayToList[0],TempArrayToList[1])
            ThreeCurrentLine.append(ThreeVec1)
        ThreeLinesBaseShape.append (ThreeCurrentLine)
        ThreeCurrentLine = []

    #InputLines
    for i in InputLineLines:
        for j in i:
            TempArrayToList = j.tolist()
            ThreeVec1 = THREE.Vector2.new(TempArrayToList[0],TempArrayToList[1])
            ThreeCurrentLine.append(ThreeVec1)
        ThreeLinesInput.append (ThreeCurrentLine)
        ThreeCurrentLine = []

    #GeneratedStreets
    for i in mainStreetNetwork:
        for j in i:
            TempArrayToList = j.tolist()
            ThreeVec1 = THREE.Vector2.new(TempArrayToList[0],TempArrayToList[1])
            ThreeCurrentLine.append(ThreeVec1)
        ThreeLinesStreet.append (ThreeCurrentLine)
        ThreeCurrentLine = []
    
    

    
    draw_system_streets(ThreeLinesStreet)
    draw_system_baseshape(ThreeLinesBaseShape)
    draw_system_input(ThreeLinesInput)


    """system(0, geom1_params.i)"""


    
    #-----------------------------------------------------------------------
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS
# Main street network generator


def pointInPoly(pointAsNP,polyAsNPLines):
    pointList = pointAsNP.tolist()
    polyNP = []
    poly = []

    for i in polyAsNPLines:
        polyNP.append(i[0])
    for i in polyNP:
        poly.append(i.tolist())

    if len(poly) < 3:  # not a polygon - no area
        return False
    
    total = 0
    i = 0
    x = pointList[0]
    y = pointList[1]
    next = 0
    for i in range(len(poly)):
        next = (i + 1) % len(poly)
        if poly[i][1] <= y < poly[next][1]:
            if x < poly[i][0] + (y - poly[i][1]) * (poly[next][0] - poly[i][0]) / (poly[next][1] - poly[i][1]):
                total += 1
        elif poly[next][1] <= y < poly[i][1]:
            if x < poly[i][0] + (y - poly[i][1]) * (poly[next][0] - poly[i][0]) / (poly[next][1] - poly[i][1]):
                total += 1
    if total % 2 == 0:
        return False
    else:
        return True

def pointOnLine(pointAsNP,lineAsNP):
    # NP to List
    lineList = []
    tempPoint = []
    for i in lineAsNP:
        tempPoint = i.tolist()
        lineList.append (tempPoint)
    pointList = pointAsNP.tolist()
    
    endpoint1 = lineList[0]
    endpoint2 = lineList[1]
    #Exeption for Vertical lines with undefined slope
    if (endpoint2[0] - endpoint1[0]) == 0:
        if pointList[0] == endpoint1[0]:
            #Point Is On Line
            return True
        else:
            #Point is not on line
            return False
    #Calculate Slope
    else:
        slope = (endpoint2[1] - endpoint1[1]) / (endpoint2[0] - endpoint1[0])

    # Calculate the y-intercept of the line segment
    y_intercept = endpoint1[1] - (slope * endpoint1[0])
    # Calculate the y-coordinate of the point on the line segment
    y_on_line = (slope * pointList[0]) + y_intercept

    # Check if the y-coordinate of the point is equal to the y-coordinate of the point passed to the function
    if y_on_line == pointList[1]:
        #Point is on line
        return True
    else:
        #Point is not on line
        return False

def pointOnLineSegment(pointAsNP, lineAsNP):
    if onSegment(lineAsNP[0], pointAsNP, lineAsNP[1]) and np.cross(lineAsNP[1] - lineAsNP[0], pointAsNP - lineAsNP[0]) == 0:
        return True
    return False

def onSegment(p, q, r):
    if (q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and
        q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1])):
        return True
    return False

def isIntersecting(intersectLinesAsNPList):
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y


    # Given three collinear points p, q, r, the function checks if
    # point q lies on line segment 'pr'
    def onSegment(p, q, r):
        if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
            return True
        return False

    def orientation(p, q, r):
    #Find point orientation
        val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
        if (val > 0):
            
            # Clockwise orientation
            return 1
        elif (val < 0):
            
            # Counterclockwise orientation
            return 2
        else:
            
            # Collinear orientation
            return 0

    # The main function that returns true if
    # the line segment 'p1q1' and 'p2q2' intersect.
    def doIntersect(p1,q1,p2,q2):
        
        # Find the 4 orientations required for
        # the general and special cases
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        # General case
        if ((o1 != o2) and (o3 != o4)):
            return True

        # Special Cases

        # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        if ((o1 == 0) and onSegment(p1, p2, q1)):
            return True

        # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        if ((o2 == 0) and onSegment(p1, q2, q1)):
            return True

        # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        if ((o3 == 0) and onSegment(p2, p1, q2)):
            return True

        # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        if ((o4 == 0) and onSegment(p2, q1, q2)):
            return True

        # If none of the cases
        return False

    TempArrayToList = []
    tempArray1 = []
    for i in intersectLinesAsNPList:
        for j in i:
            tempArray1.append(j.tolist())
        TempArrayToList.append(tempArray1)
        tempArray1 = []

    p1 = Point(TempArrayToList[0][0][0],TempArrayToList[0][0][1])
    q1 = Point(TempArrayToList[0][1][0],TempArrayToList[0][1][1])
    p2 = Point(TempArrayToList[1][0][0],TempArrayToList[1][0][1])
    q2 = Point(TempArrayToList[1][1][0],TempArrayToList[1][1][1])
    
    if doIntersect(p1, q1, p2, q2):
        return True
    else:
        return False

def getIntersectPoint(intersectLinesAsNPList):

    a1 = intersectLinesAsNPList[0][0]
    a2 = intersectLinesAsNPList[0][1]
    b1 = intersectLinesAsNPList[1][0]
    b2 = intersectLinesAsNPList[1][1]
    
    s = np.vstack([a1,a2,b1,b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return "False"
    return np.array([x/z, y/z])         # returns intersection point as NP-Array

def pointOnPolygon(pointAsNP,polygonAsNPLines):
    for i in polygonAsNPLines:
        if pointOnLineSegment(pointAsNP,i) == True:
            return True
    return False

def scaleVec(vecAsNP,newLength):
    distance = np.linalg.norm(vecAsNP)
    scale_factor = newLength / distance
    return vecAsNP * scale_factor

def mainStreetGenerator(BaseShape,InputLines):
    #Find valid generation starting points
    startPointAndVec = [] 
    generatedStreets = []
    for i in InputLines:
        pc = []
        #Testing both points of the current Inputline for their position
        for j in i:
            if pointOnPolygon(j,BaseShape) == True:
                pc.append("onOutline")
                continue
            elif pointInPoly(j,BaseShape) == True:
                pc.append("inside")
                continue
            else:
                pc.append("outside")
       
        #Generating start-points and vectors for the street generation out of the inputlines and their points' conditions

        if pc[0] == "outside" and pc[1] == "outside": #Both points are outside of baseshape
            intersectPoints = []
            for j in BaseShape: #test if inputline runs through base shape (for every boundary line of base shape) despite endpoints beeing outside
                testLines = [i]
                testLines.append(j)
                if isIntersecting(testLines) == True:
                    tempIntersectPoint = getIntersectPoint(testLines)
                    if type(tempIntersectPoint) is not np.ndarray:   # Exeption if line runs through baseshape but is colinear with boundary line
                        intersectPoints = []               # - of baseshape which could lead to problems
                        break                                  
                    else:
                        intersectPoints.append(tempIntersectPoint)
                        tempIntersectPoint = []
            
            if len(intersectPoints) == 2:                 # if the endpoints of the inputline are outside the baseshape, but it intersects the baseshape twice, 
                generatedStreets.append(intersectPoints)  # - the resulting line inside the baseshape is effectivly a valid street
            else:
                continue
            
        if pc[0] == "inside" and pc[1] == "inside": #Both points are contained in baseshape
            intersectPoints = []
            for j in BaseShape: #test if inputline runs through base shape (for every boundary line of base shape) despite endpoints beeing inside
                testLines = [i]
                testLines.append(j)
                if isIntersecting(testLines) == True:
                    tempIntersectPoint = getIntersectPoint(testLines)
                    if type(tempIntersectPoint) is not np.ndarray:        # Exeption if line runs through baseshape but is colinear with boundary line
                        intersectPoints = []               # - of baseshape which could lead to problems
                        break                                  
                    else:
                        intersectPoints.append(tempIntersectPoint)
                        tempIntersectPoint = []
            if len(intersectPoints) == 0:  #When there are no intersections with the outter lines, midpoint of inputline = start, and vectors in both directions as dir_vecs
                tP = []
                for p in i:
                    tP.append(p.tolist())
                midpoint = np.array([(tP[0][0] + tP[1][0])/2, (tP[0][1] + tP[1][1])/2])
                for p in i:
                    dirVec = p - midpoint
                    dirVecScaled = scaleVec(dirVec,1)
                    startPointAndVec.append([midpoint,dirVecScaled])
                continue
            elif len(intersectPoints) == 1: #When there is one intersectionpoint with the edges, just take the intersectionpoint as start
                for p in i:
                    dirVec = p - intersectPoints[0]
                    dirVecScaled = scaleVec(dirVec,1)
                    startPointAndVec.append([intersectPoints[0],dirVecScaled])
                continue
            elif len(intersectPoints) == 2:  #When there are two intersectionpoints with the boundary, take the closest to the point as start and calculate dir_vec
                for p in i:
                    pointDistance = []
                    for k in intersectPoints:
                        pointDistance.append(np.linalg.norm(k-p))
                    if pointDistance[0] < pointDistance[1]:
                        dirVec = p - intersectPoints[0]
                        dirVecScaled = scaleVec(dirVec,1)
                        startPointAndVec.append([intersectPoints[0],dirVecScaled])
                    elif pointDistance[0] > pointDistance[1]:
                        dirVec = p - intersectPoints[1]
                        dirVecScaled = scaleVec(dirVec,1)
                        startPointAndVec.append([intersectPoints[1],dirVecScaled])
                    else:
                        continue
            else:
                continue
        
        if pc[0] == "onOutline" and pc[1] == "onOutline": #Both points are on the baseshapes outline DEACTIVATED, MAYBE FIX LATER
            continue #Both points on outline have a high chance to be no ciable street. Could also mean street outside of polygon. MAYBE FIX LATER!
        
        if pc[0] == "inside" and pc[1] == "outside" or pc[0] == "outside" and pc[1] == "inside": #One point inside of baseshape, other outside
            intersectPoints = []
            for j in BaseShape: #test on every boundary line of base shape for intersection and find out intersection point
                testLines = [i]
                testLines.append(j)
                if isIntersecting(testLines) == True:
                    tempIntersectPoint = getIntersectPoint(testLines)
                    if type(tempIntersectPoint) is not np.ndarray:   # Exeption if line runs through baseshape but is colinear with boundary line
                        intersectPoints = []          # - of baseshape which could lead to problems
                        break                                  
                    else:
                        intersectPoints.append(tempIntersectPoint)
                        tempIntersectPoint = []
            if len(intersectPoints) == 1: #If the line has one intersection with baseshape, this is starting point for generation, dir_vec towards point in baseshape
                if pc[0] == "inside":
                    dirVec = i[0] - intersectPoints[0]
                    dirVecScaled = scaleVec(dirVec,1)
                    startPointAndVec.append([intersectPoints[0],dirVecScaled])
                    continue
                elif pc[1] == "inside":
                    dirVec = i[1] - intersectPoints[0]
                    dirVecScaled = scaleVec(dirVec,1)
                    startPointAndVec.append([intersectPoints[0],dirVecScaled])
                    continue
                else:
                    continue
            
            elif len(intersectPoints) > 1:   #If the line has multiple intersections,closest intersection to the inside-point is takes as start, inside-point for dir_vec
                if pc[0] == "inside":
                    pointDistance = []
                    for k in intersectPoints:
                        pointDistance.append(np.linalg.norm(k - i[0]))
                    minpos = pointDistance.index(min(pointDistance))
                    dirVec = i[0] - intersectPoints[minpos]
                    dirVecScaled = scaleVec(dirVec,1)
                    startPointAndVec.append([intersectPoints[minpos],dirVecScaled])
                    continue
                elif pc[1] == "inside":
                    pointDistance = []
                    for k in intersectPoints:
                        pointDistance.append(np.linalg.norm(k - i[1]))
                    minpos = pointDistance.index(min(pointDistance))
                    dirVec = i[1] - intersectPoints[minpos]
                    dirVecScaled = scaleVec(dirVec,1)
                    startPointAndVec.append([intersectPoints[minpos],dirVecScaled])
                    continue
            else:
                continue

        if pc[0] == "inside" and pc[1] == "onOutline" or pc[0] == "onOutline" and pc[1] == "inside": #One point inside baseshape, other on it's outline
            intersectPoints = []
            for j in BaseShape: #test on every boundary line of base shape for intersection and find out intersection point
                testLines = [i]
                testLines.append(j)
                if isIntersecting(testLines) == True:
                    tempIntersectPoint = getIntersectPoint(testLines)
                    if type(tempIntersectPoint) is not np.ndarray:   # Exeption if line runs through baseshape but is colinear with boundary line
                        intersectPoints = []          # - of baseshape which could lead to problems
                        break                                  
                    else:
                        intersectPoints.append(tempIntersectPoint)
                        tempIntersectPoint = []
            if len(intersectPoints) == 1:  #If the line has one intersection (should be the point which is on the line) take this as start, iside point as dir_vec
                if pc[0] == "inside":
                    dirVec = i[0] - intersectPoints[0]
                    dirVecScaled = scaleVec(dirVec,1)
                    startPointAndVec.append([intersectPoints[0],dirVecScaled])
                    continue
                elif pc[1] == "inside":
                    dirVec = i[1] - intersectPoints[0]
                    dirVecScaled = scaleVec(dirVec,1)
                    startPointAndVec.append([intersectPoints[0],dirVecScaled])
                    continue
                else:
                    continue
            elif len(intersectPoints) > 1:   #If the line has multiple intersections,closest intersection to the inside-point is takes as start, inside-point for dir_vec
                if pc[0] == "inside":
                    pointDistance = []
                    for k in intersectPoints:
                        pointDistance.append(np.linalg.norm(k - i[0]))
                    minpos = pointDistance.index(min(pointDistance))
                    dirVec = i[0] - intersectPoints[minpos]
                    dirVecScaled = scaleVec(dirVec,1)
                    startPointAndVec.append([intersectPoints[minpos],dirVecScaled])
                    continue
                elif pc[1] == "inside":
                    pointDistance = []
                    for k in intersectPoints:
                        pointDistance.append(np.linalg.norm(k - i[1]))
                    minpos = pointDistance.index(min(pointDistance))
                    dirVec = i[1] - intersectPoints[minpos]
                    dirVecScaled = scaleVec(dirVec,1)
                    startPointAndVec.append([intersectPoints[minpos],dirVecScaled])
                    continue
            else:
                continue

        if pc[0] == "onOutline" and pc[1] == "outside" or pc[0] == "outside" and pc[1] == "onOutline": #One point on Outline, other outside DEACTIVATED, MAYBE FIX LATER
            continue

        else:
            continue
        
    for i in startPointAndVec:

        def generateStreetSegment(startPoint,dirVec,BaseShape,existingStreets,segmentLength):
            
            newDirVec = scaleVec(dirVec,segmentLength)
            currentSegment = [startPoint, startPoint + newDirVec]
            intersectPoints = []
            allLinesToTest = BaseShape + existingStreets
            
            for j in allLinesToTest: #test on every boundary line of base shape for intersection and find out intersection points

                testLines = [currentSegment]
                testLines.append(j)
                #print ("lines testet",testLines)
                if isIntersecting(testLines) == True:
                    tempIntersectPoint = getIntersectPoint(testLines)
                    #print ("intersectpointFound",tempIntersectPoint)
                    if type(tempIntersectPoint) is not np.ndarray:   # Exeption if line runs through baseshape but is colinear with boundary line
                        intersectPoints = []          # - of baseshape which could lead to problems
                        break                                  
                    else:
                        intersectPoints.append(tempIntersectPoint)
                        tempIntersectPoint = []



            #print ("INTERSECT POINTS",intersectPoints)
            spList = startPoint.tolist()
            spListRounded = []
            for i in spList:
                spListRounded.append(round(i,3))
            ipList = []
            for b in intersectPoints:
                ipList.append(b.tolist())
            
            ipListRounded = []
            tempIpList = []
            for o in ipList:
                for k in o:
                    tempIpList.append(round(k,3))
                ipListRounded.append(tempIpList)
                tempIpList = []
  
            if spListRounded in ipListRounded:
                ind = ipListRounded.index(spListRounded)
                del intersectPoints[ind]

            if len(intersectPoints) == 0:
                return "noIntersect"
            elif len(intersectPoints) == 1:
                return [startPoint,intersectPoints[0]]
            elif len(intersectPoints) > 1:
                pointDistance = []
                for k in intersectPoints:
                    pointDistance.append(np.linalg.norm(k - startPoint))
                minpos = pointDistance.index(min(pointDistance))
                return [startPoint,intersectPoints[minpos]]
            


        def system(startPoint,dirVec,BaseShape,existingStreets,segmentLength):
            
            segmentLength += 500
            currentStreetSegment = generateStreetSegment(startPoint,dirVec,BaseShape,existingStreets,segmentLength)
            #print ("result system",currentStreetSegment)
            if currentStreetSegment == "noIntersect" and segmentLength <= 500:
                return system(startPoint,dirVec,BaseShape,existingStreets,segmentLength)
            elif currentStreetSegment == "noIntersect" and segmentLength > 500:
                return "false"
            else:
                #print("RETURNSTREETSEGMENT",currentStreetSegment)
                return currentStreetSegment

        segmentLength = 0
        
        currentGeneratedStreet = system(i[0],i[1],BaseShape,generatedStreets,segmentLength)
        #print("THISARRIVESOUTSIDEFUNCTION",currentGeneratedStreet)
        if currentGeneratedStreet == "false":
            continue
        else:
            generatedStreets.append(currentGeneratedStreet)

    return generatedStreets

def splitLine(lineToSplitAsNP,splittingLineOrPointAsNP):
    if len(splittingLineOrPointAsNP) == 1:
        if splittingLineOrPointAsNP == lineToSplitAsNP[0] or splittingLineOrPointAsNP == lineToSplitAsNP[1]:
            return "Intersecting only in Endpoint of Line"
        isOnLine = pointOnLineSegment(splittingLineOrPointAsNP,lineToSplitAsNP)
        if isOnLine == False:
            return "notIntersecting"
        else:
            return [[lineToSplitAsNP[0],splittingLineOrPointAsNP],[splittingLineOrPointAsNP,lineToSplitAsNP[1]]]

    elif len(splittingLineOrPointAsNP) == 2:
        for i in lineToSplitAsNP:
            if pointOnLineSegment(i,splittingLineOrPointAsNP) == True:
                return "Intersecting only in Endpoint of Line"
        if isIntersecting(lineToSplitAsNP,splittingLineOrPointAsNP) == True:
            intersectPoint = getIntersectPoint[lineToSplitAsNP,splittingLineOrPointAsNP]
            if type(intersectPoint) is not np.ndarray:
                return "no single splittingpoint"
            else:
                return [[lineToSplitAsNP[0],intersectPoint],[intersectPoint,lineToSplitAsNP[1]]]
        else:
            return "notIntersecting"
    else:
        return "please only pass a single point or line as splittingLineOrPointAsNP"

"""def splitAllLines(listOfLinesToSplitAsNP): #Splitting a list of line is difficult, what to do when a line is hit by multiple splittinglines?
    splitLines = []
    tempLinesToSplit = [listOfLinesToSplitAsNP]
    
    def recursiveLineSplitting(tempLinesToSplit):
        newTempLinesToSplit = []
        splitCount = 0
        for i in tempLinesToSplit:
            for j in tempLinesToSplit:
                if i == j:
                    continue
                currentSplit = splitLine(i,j)
                if type(currentSplit) is str:
                    newTempLinesToSplit.append(i)
                else:
                    splitCount += 1
                    newTempLinesToSplit.append[currentSplit]
    
        if splitCount >= 1:
            return recursiveLineSplitting(newTempLinesToSplit)
        if splitCount == 0:
            return newTempLinesToSplit"""

    



    
#Turning the generated point-list into a drawn line
def draw_system_streets(lines):
    #print (lines)
    for points in lines:
        line_geom = THREE.BufferGeometry.new()
        points = to_js(points)
        
        line_geom.setFromPoints( points )

        material = THREE.LineBasicMaterial.new()
        material.color = THREE.Color.new("#FDFEFE")
        
        vis_line = THREE.Line.new( line_geom, material )
        global scene
        scene.add(vis_line)

def draw_system_baseshape(lines):
    #print (lines)
    for points in lines:
        line_geom = THREE.BufferGeometry.new()
        points = to_js(points)
        
        line_geom.setFromPoints( points )

        material = THREE.LineBasicMaterial.new()
        material.color = THREE.Color.new("#58D68D")
        
        vis_line = THREE.Line.new( line_geom, material )
        global scene
        scene.add(vis_line)

def draw_system_input(lines):
    #print (lines)
    for points in lines:
        line_geom = THREE.BufferGeometry.new()
        points = to_js(points)
        
        line_geom.setFromPoints( points )

        material = THREE.LineBasicMaterial.new()
        material.color = THREE.Color.new("#FA8072")
                
        vis_line = THREE.Line.new( line_geom, material )
        global scene
        scene.add(vis_line)


#Space for potential GUI- might be added later (still WIP)!


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
