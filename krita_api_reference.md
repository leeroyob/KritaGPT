# Krita Python API Reference

## CRITICAL RULES
1. `rotateNode()` takes RADIANS not degrees - use `math.radians(degrees)` to convert
2. `setOpacity()` takes 0-255 not 0-100
3. Always call `doc.refreshProjection()` after any changes
4. Always check if `doc` and `node` exist before using them
5. Import `from PyQt5.QtCore import QPointF, QRectF` if needed
6. Import `from krita import *` at the start

## Application Instance
```python
app = Krita.instance()  # Get Krita application instance
```

## Document Class Methods

### Getting the Document
```python
doc = app.activeDocument()  # Returns Document or None
```

### Document Methods
- `doc.activeNode()` → Node or None - Get currently selected layer
- `doc.nodeByName(name: str)` → Node or None - Find layer by exact name
- `doc.createNode(name: str, nodeType: str)` → Node - Create new node
  - Valid nodeTypes: "paintlayer", "grouplayer", "filelayer", "filterlayer", "filllayer", "clonelayer", "vectorlayer", "transparencymask", "filtermask", "transformmask", "selectionmask"
- `doc.rootNode()` → Node - Get root node of document
- `doc.selection()` → Selection or None - Get current selection
- `doc.setSelection(selection: Selection)` - Set document selection
- `doc.width()` → int - Document width in pixels
- `doc.height()` → int - Document height in pixels
- `doc.name()` → str - Document name
- `doc.resolution()` → float - Document resolution in DPI
- `doc.colorDepth()` → str - Color depth (e.g., "U8", "U16")
- `doc.colorModel()` → str - Color model (e.g., "RGBA", "CMYK")
- `doc.refreshProjection()` - **MUST CALL after any changes**
- `doc.save()` → bool - Save document
- `doc.saveAs(filename: str)` → bool - Save with new name
- `doc.exportImage(filename: str, exportConfiguration: InfoObject)` → bool

## Node Class Methods (Layers)

### Node Properties
- `node.name()` → str - Get layer name
- `node.setName(name: str)` - Set layer name
- `node.type()` → str - Get node type (e.g., "paintlayer")
- `node.visible()` → bool - Check if visible
- `node.setVisible(visible: bool)` - Show/hide layer
- `node.opacity()` → int - Get opacity (0-255)
- `node.setOpacity(value: int)` - Set opacity (0-255, NOT percentage!)

### Node Transformation
- `node.rotateNode(radians: float)` - Rotate by RADIANS (not degrees!)
  - Example: `node.rotateNode(math.radians(90))` for 90 degrees
- `node.move(x: int, y: int)` - Move by x,y pixels relative to current position
- `node.scaleNode(origin: QPointF, width: int, height: int, strategy: str)` - Scale node
  - strategy can be: "bicubic", "bilinear", "nearestneighbor"

### Node Hierarchy
- `node.parentNode()` → Node or None - Get parent node
- `node.childNodes()` → list[Node] - Get list of child nodes
- `node.addChildNode(child: Node, above: Node)` - Add child node
- `node.duplicate()` → Node - Duplicate node (returns new node)
- `node.remove()` - Delete this node
- `node.mergeDown()` → Node - Merge with layer below

### Node Bounds and Position
- `node.bounds()` → QRect - Get bounding rectangle
- `node.position()` → QPoint - Get position
- `node.setPosition(point: QPoint)` - Set position

### Pixel Data (Advanced)
- `node.pixelData(x: int, y: int, w: int, h: int)` → bytes - Get pixel data
- `node.setPixelData(data: bytes, x: int, y: int, w: int, h: int)` - Set pixel data
- `node.colorForCanvas()` → ManagedColor - Get color at position

## Selection Class

### Creating Selection
```python
from krita import Selection
selection = Selection()
selection.select(x: int, y: int, width: int, height: int, value: int)
# value is 0-255 for selection strength
```

### Selection Methods
- `selection.x()` → int - Left position
- `selection.y()` → int - Top position  
- `selection.width()` → int - Width
- `selection.height()` → int - Height
- `selection.clear()` - Clear selection
- `selection.invert()` - Invert selection

## Common Patterns

### Create New Layer
```python
app = Krita.instance()
doc = app.activeDocument()
if doc:
    layer = doc.createNode("Layer Name", "paintlayer")
    root = doc.rootNode()
    root.addChildNode(layer, None)
    doc.refreshProjection()
```

### Rotate Current Layer
```python
import math
app = Krita.instance()
doc = app.activeDocument()
if doc:
    node = doc.activeNode()
    if node:
        node.rotateNode(math.radians(90))  # Convert degrees to radians!
        doc.refreshProjection()
```

### Set Layer Opacity
```python
app = Krita.instance()
doc = app.activeDocument()
if doc:
    node = doc.activeNode()
    if node:
        node.setOpacity(128)  # 50% = 128 (not 50!)
        doc.refreshProjection()
```

### Move Layer
```python
app = Krita.instance()
doc = app.activeDocument()
if doc:
    node = doc.activeNode()
    if node:
        node.move(100, 50)  # Move 100px right, 50px down
        doc.refreshProjection()
```

### Duplicate Layer
```python
app = Krita.instance()
doc = app.activeDocument()
if doc:
    node = doc.activeNode()
    if node:
        new_node = node.duplicate()
        parent = node.parentNode()
        parent.addChildNode(new_node, node)
        doc.refreshProjection()
```

### Select All
```python
from krita import Selection
app = Krita.instance()
doc = app.activeDocument()
if doc:
    selection = Selection()
    selection.select(0, 0, doc.width(), doc.height(), 255)
    doc.setSelection(selection)
    doc.refreshProjection()
```

## IMPORTANT GOTCHAS

1. **Radians vs Degrees**: `rotateNode()` uses RADIANS. Always use `math.radians(degrees)`
2. **Opacity Range**: 0-255, not 0-100 or 0.0-1.0
3. **RefreshProjection**: MUST call `doc.refreshProjection()` after changes or nothing appears
4. **Node Hierarchy**: After creating a node, you must add it to parent with `addChildNode()`
5. **Null Checks**: Always check if `doc` and `node` are not None before using
6. **Coordinate System**: (0,0) is top-left corner
7. **Move is Relative**: `move(x,y)` moves relative to current position, not absolute

## DO NOT USE THESE (Common Mistakes)
- `node.clear()` - Does not exist
- `node.fillPixelSelection()` - Does not exist  
- `node.rotateNode(degrees, center)` - Takes only 1 argument (radians)
- `node.setTransparency()` - Use setOpacity() instead