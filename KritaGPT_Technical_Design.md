# KritaGPT Technical Design Document

## Project Overview
KritaGPT is a natural language command interface plugin for Krita that translates plain English instructions into executed Python operations, focusing on formatting, layout, and workflow automation.

## Requirements Summary

### Primary Objective
Create a natural language command interface for Krita that translates text descriptions into executed Python operations, focusing on formatting, layout, and workflow automation (not image generation).

### Functional Requirements

**Core Capability:**
- Text input box where users type commands in plain English
- Translates commands to Krita Python API calls
- Executes the operations in real-time
- Shows generated code (optional toggle)

**Command Scope:**
- Layout operations: "Create 2x4 grid", "space evenly", "align to center"
- Batch operations: "Apply to all text layers", "duplicate 5 times"
- Formatting: "Add 10px margins", "resize to 500px"
- Print prep: "Add cut marks", "setup for double-sided"
- Object manipulation: "Rotate by 45°", "make 50% transparent"
- Organization: "Group by color", "arrange in circle"

### Performance Requirements
- Response time: <3 seconds for standard commands
- Success rate: 85%+ for basic commands, 70%+ for complex
- No crashes or data loss on failure
- Undo-able operations

### Technical Constraints
- Uses standard GPT-4 API (not custom model)
- Works within Krita's Python plugin system
- Respects Krita's existing UI/UX patterns
- Cross-platform (Windows/Mac/Linux)

## Architecture Overview

```
KritaGPT/
├── __init__.py           # Plugin registration
├── kritaGPT.py          # Main plugin class
├── gpt_handler.py       # GPT-4 API interface
├── command_processor.py # Code validation & execution
├── ui_components.py     # Docker widget UI
├── config.py           # API keys, settings
└── kritaGPT.desktop    # Plugin metadata
```

## Component Design

### 1. Main Plugin Class (`kritaGPT.py`)

```python
class KritaGPT(DockWidget):
    def __init__(self):
        # Initialize UI
        # Load API key from config
        # Set up signal/slot connections
        
    def process_command(self, text):
        # Get GPT response
        # Validate code
        # Execute in Krita
        # Update UI with result
```

### 2. GPT Handler (`gpt_handler.py`)

```python
class GPTHandler:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        self.system_prompt = """
        You are a Krita automation assistant.
        Convert user commands to Krita Python code.
        
        Available APIs:
        - Krita.instance()
        - activeDocument()
        - activeNode() 
        - createNode(name, type)
        - selection()
        - layers()
        
        Return ONLY executable Python code, no explanations.
        """
    
    def get_code(self, command, context=None):
        # Add context about current document/selection
        # Send to GPT-4
        # Extract code from response
        # Return validated Python string
```

### 3. Command Processor (`command_processor.py`)

```python
class CommandProcessor:
    def validate_code(self, code):
        # Check for dangerous operations
        # Verify Krita API calls exist
        # Return safe/unsafe status
    
    def execute(self, code):
        # Store current state (for undo)
        # Execute in controlled scope
        # Catch exceptions
        # Return success/error
```

## Data Flow

```
User Input → GPT Handler → Command Processor → Krita API
     ↓            ↓               ↓               ↓
  Text Box    GPT-4 API     Validation      Execution
     ↑            ↑               ↑               ↑
  Feedback    Response        Safety          Result
```

## API Integration Details

```python
# Simplified flow
def handle_user_command(text):
    # 1. Enhance with context
    context = {
        'has_document': bool(Krita.activeDocument()),
        'selected_layers': get_selected_layers(),
        'document_size': get_canvas_dimensions()
    }
    
    # 2. Build GPT prompt
    prompt = f"""
    Context: {context}
    Command: {text}
    Generate Krita Python code:
    """
    
    # 3. Get response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1  # Low for consistency
    )
    
    # 4. Execute
    code = extract_code(response)
    exec(code, {'Krita': Krita})
```

## UI Design

```
┌─────────────────────────┐
│ KritaGPT                │
├─────────────────────────┤
│ Command:                │
│ ┌─────────────────────┐ │
│ │(text input area)    │ │
│ └─────────────────────┘ │
│ [Execute] [Show Code]   │
├─────────────────────────┤
│ History:                │
│ • Create grid           │
│ • Resize to 500px       │
│ • Add shadow            │
└─────────────────────────┘
```

## Key Implementation Decisions

1. **Direct execution** - No sandbox needed (Krita's Python is already limited)
2. **Stateless by default** - Each command independent 
3. **Context injection** - Add document state to every request
4. **Simple validation** - Just check for `import`, `exec`, `eval`
5. **History tracking** - Store last 10 commands for context
6. **Model choice** - GPT-4 for maximum accuracy
7. **Temperature** - Set to 0.1 for consistent outputs

## Error Handling Strategy

- **Invalid code**: Display error message, don't execute
- **API failure**: Fallback message, retry option
- **Execution error**: Catch exception, show user-friendly error
- **Rate limiting**: Queue commands, show waiting indicator

## Security Considerations

- No file system access outside Krita documents
- No network calls except to OpenAI API
- No execution of imported modules
- Validation of all generated code before execution

## Testing Strategy

### Unit Tests
- GPT response parsing
- Code validation logic
- Context extraction

### Integration Tests
- End-to-end command execution
- UI responsiveness
- Error recovery

### User Acceptance Tests
- Common artist workflows
- Edge cases
- Performance under load

## Future Enhancements

1. **Local model support** - Ollama integration for offline use
2. **Command templates** - Pre-built complex operations
3. **Batch processing** - Multiple commands in sequence
4. **Smart context** - Remember objects between commands
5. **Custom training** - Learn from user corrections

## Development Phases

1. **Phase 1**: Core functionality (Week 1)
   - Basic UI
   - GPT integration
   - Simple command execution

2. **Phase 2**: Robustness (Week 2)
   - Error handling
   - Validation
   - Context awareness

3. **Phase 3**: Polish (Week 3)
   - UI improvements
   - Command history
   - Documentation

## Success Metrics

- 85% command success rate
- <3 second average response time
- Zero data loss incidents
- 90% user satisfaction score

## Dependencies

- Krita 5.0+
- Python 3.8+
- openai Python package
- PyQt5 (included with Krita)

## File Structure Detail

### `__init__.py`
Registers the plugin with Krita

### `kritaGPT.py`
Main plugin class, UI creation, event handling

### `gpt_handler.py`
OpenAI API communication, prompt engineering

### `command_processor.py`
Code validation, safe execution, error handling

### `ui_components.py`
Custom widgets, styling, layout management

### `config.py`
API key storage, user preferences, constants

### `kritaGPT.desktop`
Plugin metadata for Krita's plugin manager

## Deployment

1. Package as .zip file
2. User installs via Krita's plugin manager
3. Enter OpenAI API key in settings
4. Enable docker in Window menu

## License

MIT License - Open source, free to use and modify

## Author

Developed using NASA Systems Engineering principles for reliability and robustness.