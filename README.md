# KritaGPT - Natural Language Commands for Krita

Transform your Krita workflow with AI-powered natural language commands. Simply type what you want to do, and KritaGPT translates your words into actions.

## What is KritaGPT?

KritaGPT is a plugin that adds a natural language interface to Krita. Instead of navigating menus or remembering shortcuts, just describe what you want in plain English:

- "Create a 3x3 grid of the current layer"
- "Make all text layers 50% transparent"
- "Arrange selected layers in a circle"
- "Resize canvas to 1920x1080 and center everything"
- "Add 10px margins to all sides"
- "Duplicate this layer 5 times with 20px spacing"

## Features

### 🎯 Natural Language Processing
- Understands commands in plain English
- No need to learn scripting or complex interfaces
- Powered by GPT-4 for intelligent interpretation

### 🛠️ Workflow Automation
- Batch operations on multiple layers
- Complex layouts and arrangements
- Repetitive task automation
- Print preparation tools

### 🎨 Artist-Friendly
- Non-destructive operations
- Full undo support
- Preview generated code before execution
- Command history for repeated use

### 🔒 Safe & Reliable
- Validates all operations before execution
- No file system access outside your document
- Clear error messages
- Cannot crash Krita

## Installation

1. **Download** the KritaGPT.zip file
2. **Open Krita** and go to `Tools → Scripts → Import Python Plugin`
3. **Select** the downloaded KritaGPT.zip file
4. **Restart Krita**
5. **Enable** the plugin in `Settings → Configure Krita → Python Plugins`
6. **Access** KritaGPT from `Settings → Dockers → KritaGPT`

## Setup

1. **Get an OpenAI API Key**:
   - Visit [platform.openai.com](https://platform.openai.com)
   - Create an account or sign in
   - Go to API Keys section
   - Create a new API key

2. **Configure KritaGPT**:
   - Click the settings icon in KritaGPT docker
   - Enter your OpenAI API key
   - Choose GPT-4 (recommended) or GPT-3.5 (cheaper)
   - Save settings

## Usage

### Basic Commands

Type natural language commands in the input box:

```
"Create a new layer called Background"
"Fill current layer with red"
"Duplicate layer and move right 100 pixels"
"Rotate selection by 45 degrees"
```

### Layout Operations

```
"Arrange layers in a 4x4 grid"
"Space layers evenly horizontally"
"Align all text to center"
"Create margins of 20px around content"
```

### Batch Operations

```
"Make all layers except background 70% opacity"
"Add drop shadow to all text layers"
"Resize all layers to 500px width maintaining ratio"
"Hide layers with 'sketch' in the name"
```

### Print Preparation

```
"Add crop marks to corners"
"Create bleed area of 3mm"
"Set up for double-sided printing"
"Add registration marks"
```

## Tips & Tricks

### Be Specific
- ❌ "Make it bigger" 
- ✅ "Scale current layer to 200%"

### Use Layer Names
- "Move layer named 'Logo' to top-right"
- "Group all layers starting with 'text_'"

### Combine Operations
- "Duplicate current layer 3 times and arrange vertically with 10px gaps"

### Reference Selections
- "Fill selection with gradient from blue to white"
- "Crop canvas to selection bounds"

## Command Examples

### Creating Grids
```
"Create a 3x3 grid of current layer with 10px spacing"
"Make a contact sheet with 4 columns"
"Arrange all layers in grid formation"
```

### Text Operations
```
"Center all text layers horizontally"
"Make text layers bold" (if using text tool)
"Space text layers evenly from top to bottom"
```

### Color & Effects
```
"Desaturate all layers except current"
"Add blue tint to background layer"
"Apply gaussian blur of 5px to selection"
```

### Canvas Operations
```
"Extend canvas by 100px on all sides"
"Crop to content with 20px padding"
"Resize canvas to A4 at 300 DPI"
```

## Troubleshooting

### "Command not understood"
- Try rephrasing more specifically
- Break complex commands into steps
- Check if you have an active document

### "No document open"
- Create or open a document first
- Some commands require an active selection or layer

### "API Error"
- Check your internet connection
- Verify API key is correct
- Check OpenAI API status

### Performance Issues
- GPT-4 is slower but more accurate
- Consider GPT-3.5 for simple commands
- Commands typically take 1-3 seconds

## Cost

- **GPT-4**: ~$0.03 per command
- **GPT-3.5**: ~$0.001 per command
- Average user: $1-5 per month
- OpenAI provides $5 free credits for new accounts

## Privacy & Security

- Commands are sent to OpenAI for processing
- No document data is stored or logged
- API key is stored locally only
- Open source - audit the code yourself

## Advanced Usage

### Show Generated Code
Click "Show Code" to see the Python code that will be executed. useful for:
- Learning Krita's Python API
- Debugging complex commands
- Creating your own scripts

### Command History
- Access previous commands with up/down arrows
- Re-run successful commands
- Build a library of useful operations

### Context Awareness
KritaGPT understands:
- Current selection
- Active layer
- Document dimensions
- Layer names and types

## Supported Operations

### ✅ Can Do
- Layer manipulation (move, resize, rotate, duplicate)
- Canvas operations (resize, crop, extend)
- Selections (create, modify, fill)
- Basic filters and adjustments
- Text and shape creation
- Group and organize layers
- Export and save operations

### ❌ Cannot Do
- Create new brush engines
- Modify tool settings
- Complex painting operations
- Real-time drawing
- UI customization

## Examples Gallery

### Example 1: Product Sheet
```
"Create 2x4 grid of product layer with labels"
"Add product codes below each image"
"Export as print-ready PDF"
```

### Example 2: Social Media Kit
```
"Resize canvas to 1080x1080"
"Center all content"
"Create 5 color variations"
```

### Example 3: Batch Processing
```
"Load all PNG files from folder"
"Resize to 512px width"
"Add watermark to bottom-right"
"Export with suffix '_web'"
```

## Contributing

KritaGPT is open source! Contribute at:
- Report issues: GitHub Issues
- Submit features: Pull Requests
- Share commands: Community Forum

## Support

- **Documentation**: [Link to docs]
- **Community**: [Discord/Forum link]
- **Email**: support@example.com
- **Video Tutorials**: [YouTube link]

## Credits

Developed with NASA Systems Engineering principles for reliability.
Inspired by BlenderGPT's success in 3D workflows.
Built for artists, by artists.

## License

MIT License - Free to use, modify, and distribute.

## Changelog

### Version 1.0.0 (2025)
- Initial release
- Basic command execution
- GPT-4 and GPT-3.5 support
- Command history
- Error handling

### Roadmap
- Local AI model support (Ollama)
- Command templates library
- Macro recording
- Batch file processing
- Multi-language support

---

**Transform your Krita workflow today. Type less, create more.**