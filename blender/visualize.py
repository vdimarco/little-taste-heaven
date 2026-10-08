"""
Blender driver for the first Little Taste of Heaven visual experiment.

Run:
    blender --background --python blender/visualize.py

This creates a procedural scene for the 2:26-2:41 prototype.
The 2:32 harmony bloom separates six pitch layers in space.
"""

import json
import math
from pathlib import Path

import bpy

FEATURES = Path("analysis/features.json")
FPS = 30
START_SEC = 146.0
END_SEC = 161.0
PIVOT_SEC = 152.0

PITCHES = [
    ("F#", (0.0, 0.0, 0.0), 1.00),
    ("C#", (0.0, 0.0, 1.4), 0.88),
    ("A#", (-1.3, 0.4, 0.5), 0.82),
    ("E#", (0.35, 0.0, 0.15), 0.74),
    ("G#", (1.8, -0.2, 0.8), 0.68),
    ("D#", (0.0, 0.0, 2.7), 0.62),
]


def frame_at(sec):
    return int((sec - START_SEC) * FPS) + 1


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def make_emissive_material(name, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (0.08, 0.10, 0.14, 1)
    bsdf.inputs["Emission Color"].default_value = (0.65, 0.78, 1.0, 1)
    bsdf.inputs["Emission Strength"].default_value = strength
    bsdf.inputs["Roughness"].default_value = 0.35
    return mat


def make_pitch_orb(note, location, strength):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=4, radius=0.22, location=location)
    obj = bpy.context.object
    obj.name = f"Pitch_{note}"
    obj.data.materials.append(make_emissive_material(f"Mat_{note}", 2.0 + strength * 3.0))
    return obj


def animate_bloom(obj, final_location, delay_frames):
    pivot = frame_at(PIVOT_SEC)
    obj.scale = (0.12, 0.12, 0.12)
    obj.location = (0.0, 0.0, 0.0)
    obj.keyframe_insert("scale", frame=pivot - 10)
    obj.keyframe_insert("location", frame=pivot - 10)

    obj.scale = (1.0, 1.0, 1.0)
    obj.location = final_location
    obj.keyframe_insert("scale", frame=pivot + delay_frames)
    obj.keyframe_insert("location", frame=pivot + delay_frames)


def setup_camera():
    bpy.ops.object.camera_add(location=(0, -9, 2.2), rotation=(math.radians(78), 0, 0))
    camera = bpy.context.object
    bpy.context.scene.camera = camera

    pivot = frame_at(PIVOT_SEC)
    camera.location = (0, -9, 2.2)
    camera.keyframe_insert("location", frame=1)
    camera.location = (0, -7.2, 2.4)
    camera.keyframe_insert("location", frame=pivot)
    camera.location = (0, -6.6, 2.8)
    camera.keyframe_insert("location", frame=frame_at(END_SEC))


def main():
    clear_scene()

    features = {}
    if FEATURES.exists():
        features = json.loads(FEATURES.read_text())

    for i, (note, location, strength) in enumerate(PITCHES):
        orb = make_pitch_orb(note, (0, 0, 0), strength)
        animate_bloom(orb, location, i * 3)

    setup_camera()

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = frame_at(END_SEC)
    scene.render.fps = FPS
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = "renders/frame_"

    world = scene.world
    world.color = (0.004, 0.006, 0.012)

    print("Scene ready.")
    print("Loaded feature keys:", list(features.keys()))


if __name__ == "__main__":
    main()
