# blender_serial_modifier

STATUS: SUPERSEDED. This is a first-generation prototype in a lineage of
serial/hardware-control add-ons for Blender:

  blender-addons-serial-runner
    -> blender_serial_modifier (this repo)
    -> blender-addon-multi-serial-control  <-- current/recommended version

Use [blender-addon-multi-serial-control](https://github.com/n2048-creative-technology/blender-addon-multi-serial-control)
for new work — it supports multiple objects on multiple independent serial
ports at once, ships udev rules for stable Arduino device naming, a sample
.blend scene, and a proper GPLv3 license file, none of which this repo has.

This repo is kept for history/reference. It also has a known bug (see
"Known issues" below) that was fixed in the successor add-on's design.

## What it does

Adds a "Serial Stream" panel to the Modifier tab for the active object. Lets
you pick one transform property (location/rotation/scale, X/Y/Z) and stream
its live value out over a serial port as the object moves in the viewport —
useful for driving a single physical actuator or LED/servo rig from Blender
animation in real time.

## Hardware / protocol dependency

Sends the numeric value over a plain serial (UART) connection — there is no
defined byte protocol beyond "the current value as text/bytes over the wire."
You need your own receiver (Arduino, ESP32, etc.) parsing whatever this add-on
sends; check `serial_modifier.py` for the exact write format before wiring up
hardware. It does not work standalone.

For local testing without real hardware, the code comments show how to use
`socat` to create a virtual serial pair on Linux.

## Blender version compatibility

`bl_info` declares `"blender": (3, 0, 0)`. Uses basic `bpy.props` and
`bpy.types.Panel`/`Operator` patterns that are still valid in Blender 4.x, so
it likely still loads, but this has not been re-verified against a current
Blender build — use blender-addon-multi-serial-control instead for anything
that needs to be reliable on 4.x.

## Known issues

On closing and reopening Blender, the add-on sometimes fails to register
serial output correctly. Workaround: Edit > Preferences > Add-ons, find
"Serial Stream Modifier Panel", and toggle it off/on to reactivate.

## Install (for reference only)

1. Download `serial_modifier.py`.
2. In Blender: Edit > Preferences > Add-ons > Install..., select the file,
   and enable "Serial Stream Modifier Panel".
3. Select an object, open the Modifier Properties tab, find the "Serial
   Stream" panel, pick a serial port and a transform property to stream.

## License

MIT (no license was declared in the original repo; added as the account's
default choice — see `LICENSE`).
