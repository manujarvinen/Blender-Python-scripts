# This adds the logic bricks only to the selected objects that have an action. Actionless objects are ignored.

import bpy

selected = bpy.context.selected_objects

for obj in selected:
    ad = obj.animation_data
    if ad:
        if ad.action:
            bpy.context.scene.objects.active = obj
            
            bpy.ops.logic.sensor_add(type="ALWAYS")
            bpy.ops.logic.controller_add(type="LOGIC_AND")
            bpy.ops.logic.actuator_add(type="ACTION")
            bpy.context.object.game.actuators['Action'].action=obj.animation_data.action
            bpy.context.object.game.actuators['Action'].frame_end=9999
            obj.game.sensors['Always'].link(obj.game.controllers['And']) 
            obj.game.actuators['Action'].link(obj.game.controllers['And'])
