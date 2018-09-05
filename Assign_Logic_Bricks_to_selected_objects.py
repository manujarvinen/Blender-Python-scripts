# This adds the logic bricks to objects that allow them to be playable in BGE, but only to the selected objects that have an action. Actionless objects are ignored.
# Credit goes mostly to Jeremy Behreandt

import bpy

frames_to_be_played = 9999

ops=bpy.ops
context=bpy.context

# Cache shortcuts.
ops_mesh = ops.mesh
ops_object = ops.object
ops_logic = ops.logic
scene = context.scene

selected = bpy.context.selected_objects

for obj in selected:
    ad = obj.animation_data
    if ad:
        if ad.action:
            bpy.context.scene.objects.active = obj

            current_object = context.active_object

            # Cache shortcut to cube's game engine.
            game_engine = current_object.game

            # Add sensor.
            ops_logic.sensor_add(type='ALWAYS')
                                 #name='Always')
                                 #object=cube_name)
            sensor = game_engine.sensors[-1]

            # Add controller.
            ops_logic.controller_add(type='LOGIC_AND')
                                     #name='And')
                                     #object=cube_name)
            controller = game_engine.controllers[-1]
            
            # Add actuator.
            ops_logic.actuator_add(type='ACTION')
                                   #name='Action',
                                   #object=cube_name)
            actuator = game_engine.actuators[-1]

            # Set actuator action to cube's animation data action.
            actuator.action = current_object.animation_data.action

            # Play mode options are:
            # ['PLAY', 'PINGPONG', 'FLIPPER', 'LOOPSTOP', 'LOOPEND', 'PROPERTY']
            # 'PLAY' is the default.
            #actuator.play_mode = play_mode

            # Set frame end to scene end.
            #actuator.frame_end = scene.frame_end
            actuator.frame_end = frames_to_be_played

            # Link logic together.
            sensor.link(controller)
            actuator.link(controller)
