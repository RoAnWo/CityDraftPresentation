# Import javascript modules
from js import THREE, window, document, Object
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js






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
    camera = THREE.PerspectiveCamera.new(75, window.innerWidth/window.innerHeight, 0.1, 9999)
    camera.position.z = 100
    scene.add(camera)
    
    # Graphic Post Processing
    global composer
    post_process()

    # Set up responsive window
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy) 
    #-----------------------------------------------------------------------
    # YOUR DESIGN / GEOMETRY GENERATION
    # Geometry Creation
   









    def find_overlapping_plots(plots):
        # Create a dictionary to store the mapping from plot number to overlapping plots
        plot_overlaps = {}
        # Iterate over each plot
        for i, plot in enumerate(plots):
            # Initialize an empty list to store the overlapping plots for this plot
            overlaps = []
            # Iterate over the other plots
            for j, other_plot in enumerate(plots):
                # Skip the current plot
                if i == j:
                    continue
                # Check if the current plot has 2 or more coordinates in common with the other plot
                common_coords = set(plot).intersection(set(other_plot))
                if len(common_coords) >= 2:
                    overlaps.append(j)
            # Add the mapping from plot number to overlapping plots to the dictionary
            plot_overlaps[i] = overlaps
        # Create a list of tuples (plot number, overlapping plots) from the dictionary
        result = [(plot, overlaps) for plot, overlaps in plot_overlaps.items()]
        return result

    # Test the function with the given input
    plots = [
    [(0,0),(2,2),(2,0),(0,0)],#1
    [(6,0),(2,0),(2,2),(6,2),(6,0)],#2
    [(6,0),(6,2),(8,3),(9,1),(8,0),(6,0)],#3
    [(6,4),(6,5),(8,5),(8,3),(6,2),(6,4)],#4
    [(6,4),(3,4),(2,2),(6,2),(6,4)],#5
    [(0,0),(0,3),(2,2),(0,0)],#6
    [(0,3),(2,2),(3,4),(3,5),(0,5),(0,3)],#7
    [(6,4),(6,5),(3,5),(3,4),(6,4)],#8
    [(6,5),(3,5),(3,7),(6,5)],#9
    [(0,7),(0,5),(3,5),(3,7),(0,7)]]#10
    result = find_overlapping_plots(plots)
    print(result)



    PLOT_POINT_LIST = [
    [[0,0],[2,2],[2,0],[0,0]],#1
    [[6,0],[2,0],[2,2],[6,2],[6,0]],#2
    [[6,0],[6,2],[8,3],[9,1],[8,0],[6,0]],#3
    [[6,4],[6,5],[8,5],[8,3],[6,2],[6,4]],#4
    [[6,4],[3,4],[2,2],[6,2],[6,4]],#5
    [[0,0],[0,3],[2,2],[0,0]],#6
    [[0,3],[2,2],[3,4],[3,5],[0,5],[0,3]],#7
    [[6,4],[6,5],[3,5],[3,4],[6,4]],#8
    [[6,5],[3,5],[3,7],[6,5]],#9
    [[0,7],[0,5],[3,5],[3,7],[0,7]]]#10

    #print(PLOT_POINT_LIST)
    


    #Turning the generated point-list into a drawn line
    def draw_system(lines):
        #print (lines)
        for points in lines:
            line_geom = THREE.BufferGeometry.new()
            points = to_js(points)
            
            line_geom.setFromPoints( points )

            material = THREE.LineBasicMaterial.new( THREE.Color.new(0x0000ff))
            
            vis_line = THREE.Line.new( line_geom, material )
            
            global scene
            scene.add(vis_line)  
            
    
    
    
    ThreeCurrentLine = []
    
    ThreeLines = []
    
    for i in PLOT_POINT_LIST:
        for TempArrayToList in i:
            # to array
            #print(TempArrayToList)
            #TempArrayToList =Array.tolist() 
            
            #print (TempArrayToList)
            ThreeVec1 = THREE.Vector2.new(TempArrayToList[0],TempArrayToList[1])
            ThreeCurrentLine.append(ThreeVec1)
        ThreeLines.append (ThreeCurrentLine)
        ThreeCurrentLine = []
    draw_system(ThreeLines)
    
        
   
            






#-----------------------------------------------------------------------
    # USER INTERFACE
    # Set up Mouse orbit control
    controls = THREE.OrbitControls.new(camera, renderer.domElement)

    # # Set up GUI
    # gui = window.dat.GUI.new()
    # param_folder = gui.addFolder('Parameters')
    # param_folder.add(geom1_params, 'size', 1,6,1)
    
    # param_folder.open()
    
    
    
    #-----------------------------------------------------------------------
    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    render()
    
    
#-----------------------------------------------------------------------
# HELPER FUNCTIONS


#print(Maximum,geom1_params.size)

#### update   


# Simple render and animate
def render(*args):
    window.requestAnimationFrame(create_proxy(render))
    #update()
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