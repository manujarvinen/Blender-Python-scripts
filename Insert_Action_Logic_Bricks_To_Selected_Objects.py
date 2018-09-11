import bpy

#########################################################
# INSERT ACTION LOGIC BRICKS TO SELECTED OBJECTS SCRIPT #
#########################################################

#########################################################
# Note:
#
# Each of the selected objects must have a transform 
# (Location/Rotation/Scale) action (animation/keyframes) 
# before running this script. The action can be empty.
# Otherwise nothing will be inserted to the objects.
#########################################################

############
# Settings #
############

action_brick_start_frame = 0

action_brick_end_frame = 9999 

# action_brick_end_frame = bpy.context.scene.frame_end
# Uncomment to set the Action Logic Brick end frame to be 
# the end frame of the Timeline.

#############################################################
# Make sure that each of the selected objects has an action #
#############################################################

all_objs_have_action = True

for obj in bpy.context.selected_objects:
    ad = obj.animation_data
    if ad == None:
        obj.animation_data_create()
        all_objs_have_action = False
        #print(obj.name,"has no object.animation_data, creating...")
    if ad:
        if not ad.action:
            all_objs_have_action = False
            #print(obj.name,"does NOT have an action")
        #else:
            #print(obj.name,"has an action")

if all_objs_have_action == True:
    print("Inserting some Logic Bricks to the selected objects")

if all_objs_have_action == False:
    def oops(self, context):
        self.layout.label("All of the selected objects must have an action. Cancelling... ")

    bpy.context.window_manager.popup_menu(oops, title="Error", icon='ERROR')
    print("All of the selected objects must have an action. Cancelling... ")

####################################################################
# The following adds the Logic Bricks to objects that allow them to 
# be playable in Blender Game Engine, but only to the selected 
# objects that have an action. Actionless objects are ignored.
# Credit goes mostly to Jeremy Behreandt
####################################################################

if all_objs_have_action == True:
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

                # Set frame start to scene end.
                actuator.frame_start = action_brick_start_frame

                # Set frame end to scene end.
                actuator.frame_end = action_brick_end_frame

                # Link logic together.
                sensor.link(controller)
                actuator.link(controller)
