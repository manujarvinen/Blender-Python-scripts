# Usage: 
# - Select objects you want to hide/show in BGE, set delay below, run script. 
# - Visibility Toggle happens when the delay frame below is hit.
# - You only need to apply this for the parent object, all the children will be hidden/shown at the same time.
# - In the Logic Editor (Shift+F2) open the side panel (N) to toggle on or off the HIDE property.
# - If it's ON, the objects are visible and will hide when the delay frame is hit.
# - If it's OFF, the objects are hidden and will show when the delay frame is hit.
# - You can create another point of show/hide toggle by adding a new Delay sensor and dragging the connection to the HIDE property toggle like so: https://i.imgur.com/0mYflPy.png

import bpy
sensor_delay=145 #frames

ops=bpy.ops
context=bpy.context

# Cache shortcuts.
ops_mesh = ops.mesh
ops_object = ops.object
ops_logic = ops.logic
scene = context.scene

selected = bpy.context.selected_objects

#First row of logic bricks

for obj in selected:
    bpy.context.scene.objects.active = obj

    current_object = context.active_object

    # Cache shortcut to cube's game engine.
    game_engine = current_object.game

    # Add property 'HIDE'.
    bpy.ops.object.game_property_new(type='BOOL', name="HIDE")
    game_engine.properties[-1].value=True

    # Add sensor.
    ops_logic.sensor_add(type='DELAY')
                         #name='Always')
                         #object=cube_name)
    sensor = game_engine.sensors[-1]
    sensor.delay=sensor_delay


    # Add controller.
    ops_logic.controller_add(type='LOGIC_AND')
                             #name='And')
                             #object=cube_name)
    controller = game_engine.controllers[-1]
    
    # Add actuator.
    ops_logic.actuator_add(type='PROPERTY')
                           #name='Action',
                           #object=cube_name)
    actuator = game_engine.actuators[-1]
    actuator.mode='TOGGLE'
    actuator.property=game_engine.properties.items()[-1][0]

    # Link logic together.
    sensor.link(controller)
    actuator.link(controller)
    
#Second row of logic bricks
    
for obj in selected:
    bpy.context.scene.objects.active = obj

    current_object = context.active_object

    # Cache shortcut to cube's game engine.
    game_engine = current_object.game

    # Add sensor.
    ops_logic.sensor_add(type='PROPERTY')
                         #name='Always')
                         #object=cube_name)
    sensor = game_engine.sensors[-1]
    sensor.use_pulse_true_level=True
    sensor.property=game_engine.properties.items()[-1][0]
    sensor.value='True'

    # Add controller.
    ops_logic.controller_add(type='LOGIC_AND')
                             #name='And')
                             #object=cube_name)
    controller = game_engine.controllers[-1]
    
    # Add actuator.
    ops_logic.actuator_add(type='VISIBILITY')
                           #name='Action',
                           #object=cube_name)
    actuator = game_engine.actuators[-1]
    #actuator.use_visible=True
    actuator.apply_to_children=True

    # Link logic together.
    sensor.link(controller)
    actuator.link(controller)
    
#Third row of logic bricks
    
for obj in selected:
    bpy.context.scene.objects.active = obj

    current_object = context.active_object

    # Cache shortcut to cube's game engine.
    game_engine = current_object.game

    # Add sensor.
    ops_logic.sensor_add(type='PROPERTY')
                         #name='Always')
                         #object=cube_name)
    sensor = game_engine.sensors[-1]
    sensor.use_pulse_true_level=True
    sensor.property=game_engine.properties.items()[-1][0]
    sensor.value='False'


    # Add controller.
    ops_logic.controller_add(type='LOGIC_AND')
                             #name='And')
                             #object=cube_name)
    controller = game_engine.controllers[-1]
    
    # Add actuator.
    ops_logic.actuator_add(type='VISIBILITY')
                           #name='Action',
                           #object=cube_name)
    actuator = game_engine.actuators[-1]
    actuator.use_visible=False
    actuator.use_occlusion=True
    actuator.apply_to_children=True

    # Link logic together.
    sensor.link(controller)
    actuator.link(controller)
