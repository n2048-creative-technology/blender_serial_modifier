
##
#$ socat -d -d pty,raw,echo=0 pty,raw,echo=0
# 2025/02/14 11:43:31 socat[208745] N PTY is /dev/pts/2
# 2025/02/14 11:43:31 socat[208745] N PTY is /dev/pts/4
# 2025/02/14 11:43:31 socat[208745] N starting data transfer loop with FDs [5,5] and [7,7]
#
# Then: use /dev/pts/2 in the serial stream panel
# open a new terminal and monitor using 
#
#$ cat /dev/pts/4
#
##

bl_info = {
    "name": "Serial Stream Modifier Panel",
    "blender": (3, 0, 0),
    "category": "Object",
}

import bpy
import serial
import serial.tools.list_ports

# Define available transform properties
TRANSFORM_ITEMS = [
    ("location.x", "Location X", ""),
    ("location.y", "Location Y", ""),
    ("location.z", "Location Z", ""),
    ("rotation_euler.x", "Rotation X", ""),
    ("rotation_euler.y", "Rotation Y", ""),
    ("rotation_euler.z", "Rotation Z", ""),
    ("scale.x", "Scale X", ""),
    ("scale.y", "Scale Y", ""),
    ("scale.z", "Scale Z", ""),
]

# Safe getters and setters to avoid ID writing errors
def get_serial_port(self):
    return self.get("serial_port", "")

def set_serial_port(self, value):
    self["serial_port"] = value

def get_transform_property(self):
    return self.get("transform_property", "location.x")

def set_transform_property(self, value):
    self["transform_property"] = value

# Attach properties per object
bpy.types.Object.serial_port = bpy.props.StringProperty(
    name="Serial Port",
    description="Serial port for this object",
    get=get_serial_port,
    set=set_serial_port,
)

bpy.types.Object.transform_property = bpy.props.EnumProperty(
    name="Property",
    description="Object transform property to send",
    items=TRANSFORM_ITEMS,
    get=get_transform_property,
    set=set_transform_property,
)

class SERIAL_OT_SelectPort(bpy.types.Operator):
    """Operator to select the first available serial port"""
    bl_idname = "serial.select_port"
    bl_label = "Select First Serial Port"
    bl_description = "Select a serial port for this object"

    def execute(self, context):
        obj = context.object
        if not obj:
            self.report({'WARNING'}, "No object selected!")
            return {'CANCELLED'}
        
        ports = list(serial.tools.list_ports.comports())
        if ports:
            obj.serial_port = ports[0].device  # Assign to object
            self.report({'INFO'}, f"Set serial port to {ports[0].device}")
        else:
            self.report({'WARNING'}, "No serial ports found!")

        return {'FINISHED'}

class SERIAL_PT_ModifierPanel(bpy.types.Panel):
    """UI Panel to configure per-object serial settings inside the Modifiers tab"""
    bl_label = "Serial Stream"
    bl_idname = "OBJECT_PT_serial_stream"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "modifier"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if not obj:
            layout.label(text="Select an object to configure")
            return

        layout.prop(obj, "serial_port")
        layout.operator("serial.select_port")
        layout.prop(obj, "transform_property")

def frame_change_handler(scene):
    """Handler to send data on frame change"""
    for obj in scene.objects:
        if not obj:
            continue

        serial_port = obj.serial_port
        transform_property = obj.transform_property

        if serial_port and transform_property:
            try:
                value = eval(f"obj.{transform_property}")  # Get selected transform property
                with serial.Serial(serial_port, 115200, timeout=1) as ser:
                    ser.write(f"{obj.name}, {transform_property}, {value}\n".encode())
            except serial.SerialException:
                print(f"Error: Unable to open serial port {serial_port} for {obj.name}")

def register():
    bpy.utils.register_class(SERIAL_OT_SelectPort)
    bpy.utils.register_class(SERIAL_PT_ModifierPanel)

    bpy.app.handlers.frame_change_post.append(frame_change_handler)

def unregister():
    bpy.utils.unregister_class(SERIAL_OT_SelectPort)
    bpy.utils.unregister_class(SERIAL_PT_ModifierPanel)

    bpy.app.handlers.frame_change_post.remove(frame_change_handler)

if __name__ == "__main__":
    register()
