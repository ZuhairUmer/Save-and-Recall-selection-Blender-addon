bl_info = {
    "name": "Save and Recall Selection",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import bmesh

def save_selection(context, slot):
    obj = context.object
    bm = bmesh.from_edit_mesh(obj.data)
    
    mode = context.tool_settings.mesh_select_mode[:]
    
    if mode[0]:  # Vertex mode
        selection = [v.index for v in bm.verts if v.select]
        obj[f'saved_selection_{slot}'] = {'mode': 'VERT', 'indices': selection}
    elif mode[1]:  # Edge mode
        selection = [e.index for e in bm.edges if e.select]
        obj[f'saved_selection_{slot}'] = {'mode': 'EDGE', 'indices': selection}
    elif mode[2]:  # Face mode
        selection = [f.index for f in bm.faces if f.select]
        obj[f'saved_selection_{slot}'] = {'mode': 'FACE', 'indices': selection}
    
    print(f"Selection saved in slot {slot}")

def recall_selection(context, slot):
    obj = context.object
    bm = bmesh.from_edit_mesh(obj.data)
    
    saved_selection = obj.get(f'saved_selection_{slot}', None)
    if saved_selection is None:
        print(f"No selection saved in slot {slot}")
        return
    
    mode = saved_selection['mode']
    indices = saved_selection['indices']
    
    if mode == 'VERT':
        for v in bm.verts:
            if v.index in indices:
                v.select = True
    elif mode == 'EDGE':
        for e in bm.edges:
            if e.index in indices:
                e.select = True
    elif mode == 'FACE':
        for f in bm.faces:
            if f.index in indices:
                f.select = True
    
    bmesh.update_edit_mesh(obj.data)
    print(f"Selection recalled from slot {slot}")

class OBJECT_OT_SaveSelection(bpy.types.Operator):
    """Save Selection"""
    bl_idname = "object.save_selection"
    bl_label = "Save Selection"
    slot: bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'MESH' and
                context.object.mode == 'EDIT')
    
    def execute(self, context):
        save_selection(context, self.slot)
        return {'FINISHED'}

class OBJECT_OT_RecallSelection(bpy.types.Operator):
    """Recall Selection"""
    bl_idname = "object.recall_selection"
    bl_label = "Recall Selection"
    slot: bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        return (context.object is not None and
                context.object.type == 'MESH' and
                context.object.mode == 'EDIT')
    
    def execute(self, context):
        recall_selection(context, self.slot)
        return {'FINISHED'}

class VIEW3D_PT_SaveRecallSelectionPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Save and Recall Selection"
    bl_idname = "VIEW3D_PT_save_recall_selection"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Selection History'

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text="Save Selection to Slot")
        row = layout.row()
        row.operator("object.save_selection", text="Save Slot 1").slot = 1
        row.operator("object.save_selection", text="Save Slot 2").slot = 2
        row.operator("object.save_selection", text="Save Slot 3").slot = 3
        
        row = layout.row()
        row.label(text="Recall Selection from Slot")
        row = layout.row()
        row.operator("object.recall_selection", text="Recall Slot 1").slot = 1
        row.operator("object.recall_selection", text="Recall Slot 2").slot = 2
        row.operator("object.recall_selection", text="Recall Slot 3").slot = 3

def register():
    bpy.utils.register_class(OBJECT_OT_SaveSelection)
    bpy.utils.register_class(OBJECT_OT_RecallSelection)
    bpy.utils.register_class(VIEW3D_PT_SaveRecallSelectionPanel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_SaveSelection)
    bpy.utils.unregister_class(OBJECT_OT_RecallSelection)
    bpy.utils.unregister_class(VIEW3D_PT_SaveRecallSelectionPanel)

if __name__ == "__main__":
    register()
