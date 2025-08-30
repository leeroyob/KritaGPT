"""
Command Processor Module for KritaGPT
Validates and executes generated Python code safely
"""

import sys
import traceback
from typing import Dict, Any, Optional
from krita import Krita
from PyQt5.QtCore import QObject, pyqtSignal

class CommandProcessor(QObject):
    # Signals for UI updates
    execution_started = pyqtSignal()
    execution_completed = pyqtSignal(dict)
    execution_error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.last_state = None
        self.execution_namespace = {}
    
    def validate_code(self, code: str) -> Dict[str, Any]:
        """Validate code for safety before execution"""
        if not code or not code.strip():
            return {"valid": False, "error": "Empty code"}
        
        # List of potentially dangerous operations
        dangerous_patterns = [
            "import os",
            "import subprocess",
            "import sys",
            "__import__",
            "eval(",
            "exec(",
            "compile(",
            "open(",
            "file(",
            "input(",
            "raw_input(",
            "execfile(",
            "reload(",
            "globals(",
            "locals(",
            "__builtins__",
            "setattr(",
            "delattr(",
            "__dict__",
            "__class__",
            "__bases__",
            "__subclasses__",
        ]
        
        code_lower = code.lower()
        for pattern in dangerous_patterns:
            if pattern.lower() in code_lower:
                # Allow some safe imports
                if pattern == "import sys" and "sys.path" not in code_lower:
                    continue
                return {
                    "valid": False,
                    "error": f"Potentially unsafe operation detected: {pattern}"
                }
        
        # Check for basic syntax
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            return {
                "valid": False,
                "error": f"Syntax error: {str(e)}"
            }
        
        return {"valid": True, "error": None}
    
    def save_state(self):
        """Save current document state for potential undo"""
        try:
            app = Krita.instance()
            doc = app.activeDocument()
            
            if doc:
                # In a real implementation, we might save more complex state
                # For now, we'll rely on Krita's built-in undo system
                self.last_state = {
                    "document": doc.name(),
                    "active_node": doc.activeNode().name() if doc.activeNode() else None
                }
        except:
            self.last_state = None
    
    def execute(self, code: str, auto_execute: bool = True) -> Dict[str, Any]:
        """Execute validated Python code in Krita context"""
        if not auto_execute:
            return {
                "success": True,
                "message": "Code ready for execution (auto-execute disabled)",
                "code": code,
                "executed": False
            }
        
        # Validate first
        validation = self.validate_code(code)
        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["error"],
                "code": code,
                "executed": False
            }
        
        # Save state before execution
        self.save_state()
        
        # Emit start signal
        self.execution_started.emit()
        
        # Prepare execution namespace with Krita context
        namespace = {
            'Krita': Krita,
            'app': Krita.instance(),
            'doc': Krita.instance().activeDocument() if Krita.instance() else None,
            '__builtins__': __builtins__,
            'QPointF': None,  # Will be imported if needed
            'QRectF': None,   # Will be imported if needed
            'Selection': None  # Will be imported if needed
        }
        
        # Add PyQt imports if needed
        if 'QPointF' in code or 'QRectF' in code or 'Selection' in code:
            from PyQt5.QtCore import QPointF, QRectF
            from krita import Selection
            namespace['QPointF'] = QPointF
            namespace['QRectF'] = QRectF
            namespace['Selection'] = Selection
        
        try:
            # Execute the code
            exec(code, namespace)
            
            # Refresh the canvas if document exists
            if namespace.get('doc'):
                namespace['doc'].refreshProjection()
            
            result = {
                "success": True,
                "message": "Command executed successfully",
                "code": code,
                "executed": True
            }
            
            self.execution_completed.emit(result)
            return result
            
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            traceback_str = traceback.format_exc()
            
            result = {
                "success": False,
                "error": error_msg,
                "traceback": traceback_str,
                "code": code,
                "executed": True
            }
            
            self.execution_error.emit(error_msg)
            return result
    
    def execute_safe(self, code: str) -> Dict[str, Any]:
        """Execute code with additional safety checks"""
        # First validate
        validation = self.validate_code(code)
        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["error"],
                "code": code
            }
        
        # Check if we have an active document for operations that need it
        doc_required_operations = [
            'activeNode', 'createNode', 'selection', 'rootNode',
            'setSelection', 'refreshProjection'
        ]
        
        needs_document = any(op in code for op in doc_required_operations)
        
        if needs_document and not Krita.instance().activeDocument():
            return {
                "success": False,
                "error": "No active document. Please open or create a document first.",
                "code": code
            }
        
        # Execute
        return self.execute(code)
    
    def get_available_functions(self) -> list:
        """Return list of available Krita functions for reference"""
        return [
            "Krita.instance()",
            "app.activeDocument()",
            "app.activeWindow()",
            "doc.activeNode()",
            "doc.createNode(name, type)",
            "doc.rootNode()",
            "doc.selection()",
            "doc.setSelection(selection)",
            "doc.refreshProjection()",
            "node.name()",
            "node.setName(name)",
            "node.move(x, y)",
            "node.setOpacity(value)",
            "node.duplicate()",
            "node.remove()",
            "node.setVisible(bool)",
            "node.parentNode()",
            "node.childNodes()",
        ]