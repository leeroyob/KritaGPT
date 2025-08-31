"""
Comprehensive Krita Python API Documentation
This module contains the complete API reference for accurate code generation
"""

KRITA_API_REFERENCE = """
## KRITA PYTHON API - USE ONLY THESE METHODS

### CRITICAL RULES:
1. rotateNode() takes RADIANS not degrees - use math.radians(degrees) to convert
2. setOpacity() takes 0-255 not 0-100
3. Always call doc.refreshProjection() after any changes
4. Always check if doc and node exist before using them

### Getting Started:
```python
app = Krita.instance()
doc = app.activeDocument()  # Returns Document or None
```

### Document Methods:
- doc.activeNode() → Node or None - Get currently selected layer
- doc.nodeByName(name: str) → Node or None - Find layer by exact name
- doc.createNode(name: str, nodeType: str) → Node - Create new node
  Valid nodeTypes: "paintlayer", "grouplayer", "filelayer", "filterlayer", "filllayer", "clonelayer", "vectorlayer"
- doc.rootNode() → Node - Get root node of document
- doc.width() → int - Document width in pixels
- doc.height() → int - Document height in pixels
- doc.refreshProjection() - MUST CALL after any changes
- doc.selection() → Selection or None - Get current selection
- doc.setSelection(selection: Selection) - Set selection

### Node (Layer) Methods:
- node.name() → str - Get layer name
- node.setName(name: str) - Set layer name
- node.visible() → bool - Check if visible
- node.setVisible(visible: bool) - Show/hide layer
- node.opacity() → int - Get opacity (0-255)
- node.setOpacity(value: int) - Set opacity (0-255, NOT percentage!)
- node.rotateNode(radians: float) - Rotate by RADIANS only! Use math.radians(degrees)
- node.move(x: int, y: int) - Move by x,y pixels relative to current position
- node.duplicate() → Node - Duplicate node (returns new node)
- node.remove() - Delete this node
- node.parentNode() → Node - Get parent
- node.childNodes() → list[Node] - Get children
- node.addChildNode(child: Node, above: Node) - Add child

### Selection:
```python
from krita import Selection
selection = Selection()
selection.select(x, y, width, height, 255)  # 255 = fully selected
doc.setSelection(selection)
```

### COMMON WORKING EXAMPLES:

Create new layer:
```python
app = Krita.instance()
doc = app.activeDocument()
if doc:
    layer = doc.createNode("New Layer", "paintlayer")
    doc.rootNode().addChildNode(layer, None)
    doc.refreshProjection()
```

Rotate 90 degrees:
```python
import math
app = Krita.instance()
doc = app.activeDocument()
if doc and doc.activeNode():
    doc.activeNode().rotateNode(math.radians(90))
    doc.refreshProjection()
```

Set 50% opacity:
```python
app = Krita.instance()
doc = app.activeDocument()
if doc and doc.activeNode():
    doc.activeNode().setOpacity(128)  # 50% = 128
    doc.refreshProjection()
```

Move layer:
```python
app = Krita.instance()
doc = app.activeDocument()
if doc and doc.activeNode():
    doc.activeNode().move(100, 50)  # Right 100px, down 50px
    doc.refreshProjection()
```

### DO NOT USE (Common AI Mistakes):
- node.clear() - DOES NOT EXIST
- node.fillPixelSelection() - DOES NOT EXIST
- node.rotateNode(degrees, center) - WRONG! Only takes radians, no center
- node.setTransparency() - WRONG! Use setOpacity()
- node.rotate() - WRONG! Use rotateNode()

### REMEMBER:
- ONLY use methods listed above
- rotateNode needs RADIANS: math.radians(degrees)
- opacity is 0-255, not 0-100
- ALWAYS call doc.refreshProjection() at the end
"""