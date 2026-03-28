**A pythonic 2D rig animator**
A python built 2d rig animator. Design rigs programmatically, then animate them in the editor, save and export them as needed! By default, the program starts up by loading the demo rig, but you can change that in the configs. See below for more details.

**Controls**
Most controls are button based, but there are a few keyboard/mouse controls:
- left click to move around an element with no parent
- right click to rotate an element
- arrow keys to scroll
- tab to cycle through the elements.

**What is a rig?**
A rig consists of a series of elements loaded in from a json file. Each element needs to have a name, length and parent. All other fields are optional.

```js
"element_name": {
  "length":int,
  "parent":element_name|null,
  "direction":int (degrees) - defaults to 0 - relative to parent,
  "bind_to_end"bool - defaults to true - see below for clarification,
  "layer":int - defaults to 0,
  "sprite":str (path), defaults to null.
}
```

If an element has no parent, it can be freely moved around the editor. However, if an element does have a parent, it's starting point will either bind to the start or end of it's parent element, as determined by the bind_to_end argument. Similarly, if an element doesn't have a parent, it's direction behaves as expected, but if it does have a parent, the direction you give is relative to the direction of it's parent (so, if you wanted it to point in the same direction as the parent, you'd give a direction of 0!)

When rotating elements, elements with parents will rotate around their origin. Elements without parents will rotate around their center.

**Configurations**
These configuration options handle what rig is loaded, where it is saved to, how it is exported, and also include some QOL features to make your life easier! Note that, unlike in rig elements, you cannot delete any config field, as otherwise, the editor will crash!

```js
{
  "background_color":[0, 0, 0],

  "rig_path":str (path) - the path to the rig you want to load,
  "rig_name":str - the name of the rig (for exporting),
  "save_path":str (path) | null - the path where you want the rig to be saved to. If left as null, saving is disabled,
  "load_save_on_boot":bool - whether you want to load in the save when the editor starts up,

  "bone_thickness":2,
  "bone_highlight_color":[255, 255, 255],
  "bone_highlight":1,
  "bone_colors":[[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [0, 255, 255], [255, 0, 255]],

  "text_color":[1, 1, 1],
  "ui_background_color":[255, 255, 255],

  "grid_size":[64, 64],
  "grid_color":[25, 25, 25],

  "export_padding":[10, 10] - for exporting,
  "export_tag":str|null - also for exporting
}
```
**Exporting**
When you click the export button, the program will automatically determine the best size to export the images at. The images will be saved to `user_data/exports`, and will have the file name of `rig_name-frame-frame_no.png` or `rig_name-export_tag-frame-frame_no.png`, if you specify an export tag. Padding controls how much padding is added to the sides of the images, to avoid clipping out sprites you've made.
