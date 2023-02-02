from js import window, document, console
from js import THREE, Math
from pyodide import create_proxy, to_js


def main():
    
    global objects, control_points, transform_control, spheres, Boundary_status, Mouse1Bool, controls,Close_Bool, preview_Sphere, spheres_road,all_spheres,all_curve_object_road,Saved,Hover_over_Save,object_clicked, output_lists,clicked_sphere
    clicked_sphere = None
    object_clicked=False
    Hover_over_Save = False
    Saved = False
    Close_Bool = False
    Mouse1Bool = False
    Boundary_status = "open"
    all_spheres = []
    spheres = []
    spheres_road = []
    objects = []
    control_points = []
    all_curve_object_road =[]
    #Curve Material
    global curve_material
    curve_material = THREE.LineBasicMaterial.new()
    curve_material.color = THREE.Color.new("rgb(255,255,255)")
    global camera
    camera = THREE.PerspectiveCamera.new( 45, window.innerWidth / window.innerHeight, 1, 10000 )
    camera.position.set( 500, 800, 1300 )
    camera.lookAt( 0, 0, 0 )

    global scene
    scene = THREE.Scene.new()
    scene.background = THREE.Color.new( "rgb(40,40,40)" )
  
    #spheres
    global sphere_geom, sphere_material,preview_Sphere,prev_sphere_geom
   
    sphere_geom = THREE.SphereGeometry.new( 10, 20, 20 )
    sphere_material = THREE.MeshPhongMaterial.new()
    sphere_material.color = THREE.Color.new( "rgb(255,255,255)" )


    prev_sphere_geom = THREE.SphereGeometry.new( 15, 20, 20 )
    prev_sphere_material = THREE.MeshPhongMaterial.new()
    prev_sphere_material.color = THREE.Color.new( "rgb(180,212,244)" )
    prev_sphere_material.transparent = True
    prev_sphere_material.opacity = 0.5
    preview_Sphere = THREE.Mesh.new( prev_sphere_geom, prev_sphere_material )
    preview_Sphere.visible= False
    scene.add( preview_Sphere )

    #Box
    Geo = THREE.BoxGeometry.new( 50, 50, 50 )
    Geo_mat = THREE.MeshPhongMaterial.new() 
    global Geo_Mesh
    Geo_Mesh = THREE.Mesh.new( Geo, Geo_mat )
    #scene.add( Geo_Mesh )
    #Box2(ResetButton)
    Reset_Mesh_Mat = THREE.MeshPhongMaterial.new()
    texture_Reset = THREE.TextureLoader.new().load("./maps\ResetBoundary.png")
    Reset_Mesh_Mat.map = texture_Reset

    Save_Mesh_Mat = THREE.MeshPhongMaterial.new()
    texture_Save = THREE.TextureLoader.new().load("./maps\SaveBoundary.png")
    Save_Mesh_Mat.map = texture_Save

    Geo2 = THREE.BoxGeometry.new( 78, 1, 34 )
    global Reset_Mesh, Save_Mesh
    

    Reset_Mesh = THREE.Mesh.new( Geo2, Reset_Mesh_Mat )
    Reset_Mesh.translateX(461)
    Reset_Mesh.translateZ(483)
    scene.add( Reset_Mesh )
    
    
    Save_Mesh = THREE.Mesh.new( Geo2, Save_Mesh_Mat )
    Save_Mesh.translateX(461)
    Save_Mesh.translateZ(449)
    scene.add( Save_Mesh )
	

  
    

	
    #grid
    global grid_helper
    grid_helper = THREE.GridHelper.new( 1000, 20 )
    grid_helper.position.y = -1
    scene.add( grid_helper )

    #raycaster
    global raycaster
    raycaster = THREE.Raycaster.new()
    global mouse
    mouse = THREE.Vector2.new()

    geometry = THREE.PlaneGeometry.new( 1000, 1000 )
    geometry.rotateX( - Math.PI / 2 )

    global plane
    plane = THREE.Mesh.new( geometry, THREE.MeshPhongMaterial.new())
    plane.visible = False
    scene.add( plane )
    objects.append(plane)

    #lights
    global ambientLight
    ambientLight = THREE.AmbientLight.new( 0x606060 )
    scene.add( ambientLight )
    
    global directionalLight
    directionalLight = THREE.DirectionalLight.new( 0xffffff )
    directionalLight.position.set( 1, 0.75, 0.5 ).normalize()
    scene.add( directionalLight )

    #renderer
    global renderer
    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize( window.innerWidth, window.innerHeight )
    document.body.appendChild(renderer.domElement )

    #transform_control
    transform_control = THREE.TransformControls.new(camera, renderer.domElement)
    transform_drag_proxy = create_proxy(transform_drag)
    transform_control.addEventListener('dragging-changed', transform_drag_proxy)
    
    #post processing
    global render_pass, fxaa_pass
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
    

    #orbit controls

    controls = THREE.OrbitControls.new(camera, renderer.domElement)
    controls.update()
    
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy)

    mouse_move_proxy = create_proxy(on_mouse_move)
    document.addEventListener('mousemove', mouse_move_proxy)

    mouse_down_proxy = create_proxy(on_mouse_down)
    document.addEventListener('mousedown', mouse_down_proxy)

    mouse_up_proxy = create_proxy(on_mouse_up)
    document.addEventListener('mouseup', mouse_up_proxy)

    dbl_click_proxy = create_proxy(on_dbl_click)
    document.addEventListener('dblclick', dbl_click_proxy)
    
    #initiate empty curve
    global curve_object
    curve_object = None

     #initiate empty curve2
    global curve_object_road
    curve_object_road = None

    
    render()


def transform_drag(event):
    event.preventDefault()

    if not event.value:
        update_Boundary()
        

def update_Boundary(): 
    global len_coords, curve_object, Close_Bool,curve_material
    coords=[]
    for i in spheres:
        coords.append(i.position)
    len_coords = len(coords)
    #console.log("CHECK_IF WORKING:", coords)

    if Close_Bool == False:
        js_coords = to_js(coords)
        geometry = THREE.BufferGeometry.new()
        geometry.setFromPoints( js_coords )

        curve_object = THREE.Line.new( geometry, curve_material )

        scene.remove(curve_object)
        scene.add(curve_object)
        
    if Close_Bool == True:
        if len_coords == 2:
            js_coords = to_js(coords)
            geometry = THREE.BufferGeometry.new()
            geometry.setFromPoints( js_coords )
            curve_object = THREE.Line.new( geometry, curve_material )
            scene.remove(curve_object)
            scene.add(curve_object)
            Close_Bool = False
            


        elif len_coords>2:
            scene.remove(curve_object)

            js_coords = to_js(coords)
            geometry = THREE.BufferGeometry.new()
            geometry.setFromPoints( js_coords )

            curve_object = THREE.LineLoop.new( geometry, curve_material )
            
            scene.add(curve_object)
            global Boundary_status
            Boundary_status = "closed"

def update_road():
    global len_coords_road, curve_object_road,all_curve_object_road,curve_material, output_lists
    coords_road=[]
    output_lists= []
    for i in spheres_road:
        coords_road.append(i.position)
    len_coords_road = len(coords_road)

    if len_coords_road >= 2:
    
        output_lists = [coords_road[i:i+2] for i in range(0, len(coords_road), 2)]
        scene.remove(curve_object_road)
        for i in output_lists:
            js_coords = to_js(i)
            geometry = THREE.BufferGeometry.new()
            geometry.setFromPoints( js_coords )

            curve_object_road = THREE.Line.new( geometry, curve_material )
            all_curve_object_road.append(curve_object_road)
            scene.add(curve_object_road)


def render(*args):
    window.requestAnimationFrame(create_proxy(render))

    global composer
    composer.render()

def on_window_resize(event):

    event.preventDefault()

    global renderer
    global camera
    
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()

    renderer.setSize( window.innerWidth, window.innerHeight )

    #post processing
    global render_pass, fxaa_pass
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
    
def toggle_Boundary_status():
    global Boundary_status, Close_Bool
    Boundary_status = "open"
    Close_Bool = False
def on_mouse_move(event):

    event.preventDefault()

    global raycaster, mouse, objects, preview_Sphere,clicked_sphere,object_clicked,Hover_over_Save


    mouse.set( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 )

    raycaster.setFromCamera( mouse, camera )

    js_objects = to_js(objects)
    intersects = raycaster.intersectObjects( js_objects, True )

    if intersects.length > 0 :
        if object_clicked == True:
            
            preview_Sphere.visible= True
            intersect = intersects[ 0 ]
            preview_Sphere.position.copy( intersect.point ).add( intersect.face.normal )
            
    mouse.set( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 )
    raycaster.setFromCamera( mouse, camera ) 
    js_objects = to_js(all_spheres)
    intersects = raycaster.intersectObjects( js_objects, True )
    if Saved== False:
        if intersects.length > 0 :
            intersect = intersects[ 0 ]
            Object = intersect.object
            
            
            Object_material = THREE.MeshPhongMaterial.new()
            Object_material.color = THREE.Color.new( "rgb(180,212,244)" )
            Object_material.transparent = True
            Object_material.opacity = 1
            Object.geometry = prev_sphere_geom
            Object.material = Object_material

            
            global Hover_over_Sphere
            Hover_over_Sphere=True
        

        else:
            for ball in all_spheres:
                ball.material = sphere_material
                ball.geometry = sphere_geom
            Hover_over_Sphere=False
        
    raycaster.setFromCamera( mouse, camera )
    intersects = raycaster.intersectObject(Save_Mesh , True )
    
    if intersects.length > 0 :
        intersect = intersects[ 0 ]
        Hover_over_Save=True
    else:
        Hover_over_Save=False
    

def on_mouse_down(event):

    event.preventDefault()

    global raycaster, mouse, objects,clicked_sphere,object_clicked
    
   
    mouse.set((event.clientX / window.innerWidth) * 2 - 1, -(event.clientY / window.innerHeight) * 2 + 1)
    raycaster.setFromCamera(mouse, camera)
    js_objects = to_js(all_spheres)
    intersects = raycaster.intersectObjects(js_objects, True)
    if intersects.length > 0:
        if Saved== False:
            intersect = intersects[0]
            clicked_sphere = intersect.object
            object_clicked = True
            controls.enabled = False
    
def on_mouse_up(event):

    event.preventDefault()
    global raycaster, mouse, objects, clicked_sphere,object_clicked
    object_clicked = False
    mouse.set((event.clientX / window.innerWidth) * 2 - 1, -(event.clientY / window.innerHeight) * 2 + 1)
    raycaster.setFromCamera(mouse, camera)
    intersects = raycaster.intersectObject(plane, True)
    if intersects.length > 0 and clicked_sphere is not None:
        intersect = intersects[0]
        clicked_sphere.position.copy(intersect.point).add(intersect.face.normal)
        clicked_sphere = None
        controls.enabled = True
        preview_Sphere.visible= False
    scene.remove(curve_object)
    for x in all_curve_object_road:
        scene.remove(x)

    update_Boundary()
    update_road()
      


def on_dbl_click(event):
    event.preventDefault()
    global raycaster, mouse, objects, sphere_geom, sphere_material,Close_Bool, spheres,spheres_road,all_spheres, Saved, Hover_over_Save, output_lists
    

    mouse.set( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 )

    raycaster.setFromCamera( mouse, camera )

    intersects = raycaster.intersectObject( plane, True )
    
    if intersects.length > 0 :
        intersect = intersects[ 0 ]
        ball = THREE.Mesh.new( sphere_geom, sphere_material )
        ball.rotation.x = Math.PI * -0.5
        ball.position.copy( intersect.point ).add( intersect.face.normal )
        ball2 = THREE.Mesh.new( sphere_geom, sphere_material )
        ball2.rotation.x = Math.PI * -0.5
        ball2.position.copy( intersect.point ).add( intersect.face.normal )
        if Hover_over_Save == False:
            if Hover_over_Sphere==False and Boundary_status == "open" and Saved == False:
                spheres.append(ball)
                scene.add(ball)
            
                objects.append(ball)
            if Hover_over_Sphere==True:
                Close_Bool = True
            if Hover_over_Sphere==False and Close_Bool == True and Saved == False:
                scene.add(ball2)
                spheres_road.append(ball2)
                update_road()

    all_spheres = spheres + spheres_road
    raycaster.setFromCamera( mouse, camera )

    intersects = raycaster.intersectObject(Reset_Mesh , True )
    
    if intersects.length > 0 :
        sphere_material.color = THREE.Color.new( "rgb(255,255,255)" )
        curve_material.color = THREE.Color.new("rgb(255,255,255)")
        Saved=False
        scene.clear()
        spheres = []
        spheres_road =[]
        objects =[]
        objects.append(plane)
        scene.add(grid_helper)
        scene.add(Reset_Mesh)
        scene.add(Save_Mesh)
        scene.add(ambientLight)
        scene.add(directionalLight)
        scene.add(preview_Sphere)
        toggle_Boundary_status()
        Boundary_Coords = []
        Boundary_Coords_py = []

        Input_Road_Coords = []
        Input_Road_Coords_py = []
    #save the current state and lock "editor"
    raycaster.setFromCamera( mouse, camera )
    intersects = raycaster.intersectObject(Save_Mesh , True )
    
    if intersects.length > 0 :
        Saved=True
        Boundary_Coords = []
        Boundary_Coords_py = []
        Input_Road_Coords = []
        Input_Road_Coords_py = []
        Input_Road_Coords_js = []


        #Transform Js Vectors to coords for Boundary
        for i in spheres:
            Js_prox = to_js(i.position)
            Boundary_Coords.append(Js_prox)
        for k in Boundary_Coords:
            temp_list=[]
            X_val =k.getComponent(0)
            temp_list.append(X_val)
            Y_val =k.getComponent(1)
            temp_list.append(Y_val)
            Z_val = k.getComponent(2)
            temp_list.append(Z_val)
            Boundary_Coords_py.append(temp_list)
            
        #Transform Js Vectors to coords for Input Roads
        # for i in output_lists:
        #     temp_list=[]
        #     for j in i:
        #         Js_prox = to_js(j)
        #         Input_Road_Coords.append(Js_prox)
        #     Input_Road_Coords_js.append(Input_Road_Coords)
        
        console.log("BounfdfdgfdgDS", output_lists)
        print("BoundarfdgdfgfgddfgDS", output_lists)
        for l in output_lists: 
            Input_Road_Coords_temp =[]
 
            for m in l:
                temp_list=[]
                X_val =m.getComponent(0)
                temp_list.append(X_val)
                Y_val =m.getComponent(1)
                temp_list.append(Y_val)
                Z_val = m.getComponent(2)
                temp_list.append(Z_val)
                Input_Road_Coords_temp.append(temp_list)
            Input_Road_Coords_py.append(Input_Road_Coords_temp)

        
        # for i in output_lists:
        #     temp_list_for_line=[]
        #     for j in i:
        #         Js_prox = to_js(j.position)
        #         temp_list_for_line.append(Js_prox)
        #     Input_Road_Coords.append(temp_list_for_line)
        # for k in Input_Road_Coords:
        #     temp_list_for_line2=[]
        #     for l in k:
        #         temp_list=[]
        #         X_val =l.getComponent(0)
        #         temp_list.append(X_val)
        #         Y_val =l.getComponent(1)
        #         temp_list.append(Y_val)
        #         Z_val = l.getComponent(2)
        #         temp_list.append(Z_val)
        #         temp_list_for_line2.append(temp_list)
        #     Input_Road_Coords_py.append(temp_list_for_line2)



        
        # for j in output_lists:
        #     Boundary_Coords_py.append(i)

        sphere_material.color = THREE.Color.new( "rgb(80,80,80)" )
        curve_material.color = THREE.Color.new("rgb(100,100,100)")

        console.log("Boundary_COORDS", Boundary_Coords_py)
        print("Boundary_COORDS", Boundary_Coords_py)
        console.log("Road_COORDS", Input_Road_Coords_py)
        print("Road_COORDS", Input_Road_Coords_py)
    scene.remove(curve_object)
    scene.remove(curve_object_road)
    update_Boundary()
    update_road()
    





if __name__ == '__main__':
        main()

       