# Note that all of the selected objects need to have at least one transform keyframe in them so that they have an action that can be assigned to the actuator logic brick, otherwise you have an error by running this.

import bpy

selected = bpy.context.selected_objects

for obj in selected:
    bpy.context.scene.objects.active = obj
    
    bpy.ops.logic.sensor_add(type="ALWAYS")
    bpy.ops.logic.controller_add(type="LOGIC_AND")
    bpy.ops.logic.actuator_add(type="ACTION")
    bpy.context.object.game.actuators['Action'].action=obj.animation_data.action
    bpy.context.object.game.actuators['Action'].frame_end=9999
    obj.game.sensors['Always'].link(obj.game.controllers['And']) 
    obj.game.actuators['Action'].link(obj.game.controllers['And']) 