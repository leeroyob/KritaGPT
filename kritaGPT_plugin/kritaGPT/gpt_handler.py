"""
GPT Handler Module for KritaGPT
Manages communication with OpenAI API
"""

import re
import json
from typing import Optional, Dict, List
from krita import Krita

try:
    import sys
    import os
    # Add Krita's site-packages to path if not already there
    site_packages = r"C:\Program Files\Krita (x64)\lib\site-packages"
    if os.path.exists(site_packages) and site_packages not in sys.path:
        sys.path.insert(0, site_packages)
    import openai
except ImportError as e:
    print(f"OpenAI import error: {e}")
    openai = None

from .config import SYSTEM_PROMPT

class GPTHandler:
    def __init__(self, api_key: str, model: str = "gpt-4", temperature: float = 0.1):
        """Initialize GPT handler with API credentials"""
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.chat_history = []
        
        # Note: In OpenAI v1.0+, api_key is passed to the client, not set globally
    
    def get_context(self) -> Dict:
        """Get current Krita context information"""
        app = Krita.instance()
        doc = app.activeDocument()
        
        context = {
            "has_document": doc is not None,
            "document_info": {},
            "active_layer": None,
            "selection": False
        }
        
        if doc:
            context["document_info"] = {
                "width": doc.width(),
                "height": doc.height(),
                "name": doc.name(),
                "colorDepth": doc.colorDepth(),
                "colorModel": doc.colorModel(),
                "resolution": doc.resolution()
            }
            
            active_node = doc.activeNode()
            if active_node:
                context["active_layer"] = {
                    "name": active_node.name(),
                    "type": active_node.type(),
                    "visible": active_node.visible(),
                    "opacity": active_node.opacity()
                }
            
            selection = doc.selection()
            if selection:
                context["selection"] = {
                    "x": selection.x(),
                    "y": selection.y(),
                    "width": selection.width(),
                    "height": selection.height()
                }
        
        return context
    
    def build_prompt(self, command: str, context: Optional[Dict] = None) -> str:
        """Build the full prompt with context"""
        if context is None:
            context = self.get_context()
        
        prompt = f"User command: {command}\n\n"
        
        if context["has_document"]:
            prompt += f"Document context:\n"
            prompt += f"- Document: {context['document_info']['name']}\n"
            prompt += f"- Size: {context['document_info']['width']}x{context['document_info']['height']}\n"
            
            if context["active_layer"]:
                prompt += f"- Active layer: '{context['active_layer']['name']}' (type: {context['active_layer']['type']})\n"
            
            if context["selection"]:
                sel = context["selection"]
                prompt += f"- Selection: {sel['width']}x{sel['height']} at ({sel['x']}, {sel['y']})\n"
        else:
            prompt += "Note: No document is currently open.\n"
        
        prompt += "\nGenerate Python code to execute this command:"
        
        return prompt
    
    def extract_code(self, response: str) -> str:
        """Extract Python code from GPT response"""
        # Try to find code blocks with ```python or ```
        code_pattern = r'```(?:python)?\n?(.*?)```'
        matches = re.findall(code_pattern, response, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # If no code blocks, assume entire response is code
        # Remove any lines that look like explanations (starting with #, //, or natural language)
        lines = response.strip().split('\n')
        code_lines = []
        
        for line in lines:
            # Skip obvious non-code lines
            stripped = line.strip()
            if stripped and not stripped.startswith(('Note:', 'Error:', 'Warning:', 'INFO:')):
                code_lines.append(line)
        
        return '\n'.join(code_lines)
    
    def get_code(self, command: str, context: Optional[Dict] = None) -> Dict:
        """Get Python code from GPT for the given command"""
        if not openai:
            return {
                "success": False,
                "error": "OpenAI library not installed. Please install with: pip install openai",
                "code": None
            }
        
        if not self.api_key:
            return {
                "success": False,
                "error": "No API key configured. Please set your OpenAI API key in settings.",
                "code": None
            }
        
        try:
            # Build the prompt with context
            prompt = self.build_prompt(command, context)
            
            # Create messages for chat completion
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
            
            # Add recent history for context (last 5 exchanges)
            for msg in self.chat_history[-10:]:
                messages.append(msg)
            
            # Add current command
            messages.append({"role": "user", "content": prompt})
            
            # Call OpenAI API (v1.0+ syntax)
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=1500
            )
            
            # Extract the response
            gpt_response = response.choices[0].message.content
            
            # Extract code from response
            code = self.extract_code(gpt_response)
            
            # Add to history
            self.chat_history.append({"role": "user", "content": prompt})
            self.chat_history.append({"role": "assistant", "content": code})
            
            # Keep history size manageable
            if len(self.chat_history) > 20:
                self.chat_history = self.chat_history[-20:]
            
            return {
                "success": True,
                "code": code,
                "raw_response": gpt_response,
                "error": None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "code": None
            }
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []
    
    def set_api_key(self, api_key: str):
        """Update API key"""
        self.api_key = api_key
        # Note: In OpenAI v1.0+, api_key is passed to the client, not set globally
    
    def set_model(self, model: str):
        """Update model"""
        self.model = model
    
    def set_temperature(self, temperature: float):
        """Update temperature"""
        self.temperature = max(0.0, min(1.0, temperature))