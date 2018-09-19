# WARNING: This is quite a heavy script. It takes like 30-60 seconds to handle 512 faces alone.

## SETTINGS ##
PolygonName = "PolygonObject.000"
GroupName = "PolygonGroup"


## CODE ##
import bpy
bpy.ops.group.create(name=GroupName)
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_all(action = 'SELECT')
bpy.ops.mesh.mark_sharp()
bpy.ops.object.modifier_add(type = 'EDGE_SPLIT')
bpy.ops.object.mode_set(mode = 'OBJECT') 
bpy.ops.object.modifier_apply(apply_as = 'DATA', modifier="EdgeSplit")
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.separate(type = 'LOOSE')
bpy.ops.object.mode_set(mode = 'OBJECT') 

for obj in bpy.context.selected_objects:
    bpy.ops.mesh.primitive_cube_add(layers=(True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True,True))
    #bpy.context.active_object.show_axis = True
    bpy.context.active_object.name = "NormalAxisObject"
    bpy.ops.object.mode_set(mode = 'EDIT')
    bpy.ops.mesh.delete(type ='FACE')
    bpy.ops.object.mode_set(mode = 'OBJECT') 
    bpy.context.active_object.rotation_mode = 'YXZ'    

    bpy.context.scene.objects.active = obj
    bpy.ops.object.particle_system_add()
    obj.particle_systems['ParticleSystem'].settings.type = 'HAIR'
    obj.particle_systems['ParticleSystem'].settings.use_advanced_hair = True
    #obj.particle_systems['ParticleSystem'].settings.hair_length = 1
    obj.particle_systems['ParticleSystem'].settings.count = 1
    obj.particle_systems['ParticleSystem'].settings.userjit = 1
    obj.particle_systems['ParticleSystem'].settings.render_type = 'OBJECT'
    obj.particle_systems['ParticleSystem'].settings.dupli_object = bpy.data.objects['NormalAxisObject']
    obj.select = True
    bpy.ops.object.duplicates_make_real()
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['NormalAxisObject'].select = True
    bpy.ops.object.delete()

    bpy.data.objects['NormalAxisObject.001'].select = True
    bpy.context.scene.objects.active = bpy.data.objects['NormalAxisObject.001']
    #bpy.context.object.rotation_euler[0] = bpy.context.object.rotation_euler[0] - 1.57079633 # put Z as the up axis
    bpy.ops.object.select_all(action='DESELECT')

    obj.select = True
    bpy.data.objects['NormalAxisObject.001'].select = True
    bpy.context.scene.objects.active = bpy.data.objects['NormalAxisObject.001']
    bpy.ops.object.join()
    bpy.ops.object.transform_apply(scale=True)
    bpy.data.objects['NormalAxisObject.001'].name = PolygonName
    bpy.ops.object.group_link(group=GroupName)

bpy.ops.object.select_same_group(group=GroupName)
