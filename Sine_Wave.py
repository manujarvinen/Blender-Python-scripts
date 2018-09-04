# Written by:
# Jeremy Behreandt (https://medium.com/@behreajj/creative-coding-in-blender-a-primer-53e79ff71e)
# This script differs from the one in the article. It adds logic bricks to the cube objects in order to make them animate in BGE.
# and:
# Daniel Shiffman (https://youtu.be/H81Tdrmz2LA)

import bpy
from math import pi, sin, sqrt
from random import TWOPI


def gen_cube_grid_2d(ops=bpy.ops,
                     context=bpy.context,
                     dimensions=16,
                     step=1,
                     center=[0.0, 0.0, 0.0],
                     extent=[8.0, 8.0, 8.0],
                     padding=0.0,
                     calc_uvs=True,
                     min_to_max_percent=0.2,
                     key_frames=10,
                     frames_per_key=10,
                     play_mode='LOOPEND'):

    # Cache shortcuts.
    ops_mesh = ops.mesh
    ops_object = ops.object
    ops_logic = ops.logic
    scene = context.scene

    # Calculate variables for scale of grid and of each cube within it.
    dim_range = range(0, dimensions, step)
    dim_to_percent = 1.0 / (dimensions - 1)
    extent_2 = [extent[0] * 2.0,
                extent[1] * 2.0,
                extent[2] * 2.0]
    default_cube_scale = min(extent) * dim_to_percent - padding
    inv_max_dist = 1.0 / sqrt((extent[0] ** 2.0) + (extent[1] ** 2.0))

    # Create an empty grid object to contain cubes so as to not clutter the outliner.
    ops_object.empty_add(type='PLAIN_AXES',
                         location=center)
    grid = context.active_object
    grid.name = 'Cube Grid'

    # Create list to store cube objects and return from function.
    cubes = []

    # Calculate variables for keyframes.
    frame_start = scene.frame_start
    key_frame_range = range(0, key_frames + 1, 1)
    inv_key_frames = 1.0 / (key_frames)

    # Set last frame of scene.
    scene.frame_end = frames_per_key * key_frames

    # Since height of each cube is property to be animated,
    # calculate minimum and maximum edge to oscillate between.
    min_cube_scale_z = default_cube_scale * min_to_max_percent
    max_cube_scale_z = default_cube_scale / min_to_max_percent
    cube_scale_diff = max_cube_scale_z - min_cube_scale_z

    # Loop through columns.
    for i in dim_range:

        # Calculate progress through loop as a percent.
        i_percent = i * dim_to_percent

        # Calculate vertical location.
        y = -extent[1] + i_percent * extent_2[1]

        # Calculate rise.
        rise = y ** 2

        # Loop through rows.
        for j in dim_range:

            # Calculate progress through loop as a percent.
            j_percent = j * dim_to_percent

            # Calculate horizontal location.
            x = -extent[0] + j_percent * extent_2[0]

            # Calculate run.
            run = x ** 2

            # Calculate distance.
            dist = sqrt(rise + run)

            # Convert distance to a percent by dividing by a maximum distance.
            dist_percent = dist * inv_max_dist

            # Convert the distance percent to an offset.
            # (This offset will be supplied to a sine wave).
            offset = -TWOPI * dist_percent + pi

            # Create cube.
            ops_mesh.primitive_cube_add(
                location=[x, y, 0.0],
                radius=1.0,
                calc_uvs=calc_uvs)

            # Cache reference to cube and data.
            current_cube = context.active_object
            current_data = current_cube.data

            # Name cube and cube data.
            cube_name = 'Cube ({0:0>3d}, {1:0>3d})'.format(j, i)
            current_cube.name = cube_name
            current_data.name = 'Mesh ({0:0>3d}, {1:0>3d})'.format(j, i)

            # Add cube to cubes array and to parent object.
            cubes.append(current_cube)

            # Parent cube to grid object.
            current_cube.parent = grid

            # Scale cube.
            current_cube.scale = [default_cube_scale, default_cube_scale, default_cube_scale]

            # Reset to starting frame of scene.
            current_frame = frame_start

            # Loop through keyframes.
            for key_frame in key_frame_range:

                # Calculate progress through loop as a percent.
                kf_percent = key_frame * inv_key_frames

                # Convert percent to an angle.
                angle = TWOPI * kf_percent

                # Set scene to current frame.
                scene.frame_set(current_frame)

                # Change the height of the cube with a sine wave.
                current_cube.scale[2] = min_cube_scale_z + abs(sin(offset + angle)) * cube_scale_diff

                # Set the keyframe.
                current_cube.keyframe_insert(
                    data_path='scale',
                    index=2)

                # Add to current frame.
                current_frame += frames_per_key

            # Cache shortcut to cube's game engine.
            game_engine = current_cube.game

            # Add sensor.
            ops_logic.sensor_add(type='ALWAYS',
                                 name='Always',
                                 object=cube_name)
            sensor = game_engine.sensors[-1]

            # Add controller.
            ops_logic.controller_add(type='LOGIC_AND',
                                     name='And',
                                     object=cube_name)
            controller = game_engine.controllers[-1]

            # Add actuator.
            ops_logic.actuator_add(type='ACTION',
                                   name='Action',
                                   object=cube_name)
            actuator = game_engine.actuators[-1]

            # Set actuator action to cube's animation data action.
            actuator.action = current_cube.animation_data.action

            # Play mode options are:
            # ['PLAY', 'PINGPONG', 'FLIPPER', 'LOOPSTOP', 'LOOPEND', 'PROPERTY']
            # 'PLAY' is the default.
            actuator.play_mode = play_mode

            # Set frame end to scene end.
            actuator.frame_end = scene.frame_end

            # Link logic together.
            sensor.link(controller)
            actuator.link(controller)

    return cubes


gen_cube_grid_2d(padding=0.02)
