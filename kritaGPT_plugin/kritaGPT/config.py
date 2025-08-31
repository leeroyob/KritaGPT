"""
Configuration module for KritaGPT
Handles API keys, settings, and constants
"""

import json
import os
from pathlib import Path

class Config:
    def __init__(self):
        self.config_dir = Path.home() / ".kritaGPT"
        self.config_file = self.config_dir / "config.json"
        self.ensure_config_dir()
        self.load_config()
    
    def ensure_config_dir(self):
        """Create config directory if it doesn't exist"""
        self.config_dir.mkdir(exist_ok=True)
    
    def load_config(self):
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = self.get_default_config()
            self.save_config()
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_default_config(self):
        """Return default configuration"""
        return {
            "api_provider": "openai",  # "openai" or "anthropic"
            "openai_api_key": "",
            "anthropic_api_key": "",
            "model": "gpt-4",
            "temperature": 0.1,
            "max_tokens": 1500,
            "show_code": False,
            "history_size": 10,
            "timeout": 30,
            "auto_execute": True
        }
    
    def get(self, key, default=None):
        """Get configuration value"""
        # Handle legacy configs
        if key == "api_key" and "api_key" in self.data:
            # Migrate old api_key to openai_api_key
            self.data["openai_api_key"] = self.data.pop("api_key")
            self.save_config()
            return self.data.get("openai_api_key", default)
        return self.data.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.data[key] = value
        self.save_config()

# Import the comprehensive API documentation
from .krita_api_docs import KRITA_API_REFERENCE

# System prompt for GPT/Claude with full API documentation
SYSTEM_PROMPT = f"""You are a Krita automation assistant. Convert user commands to Krita Python code.

{KRITA_API_REFERENCE}

STRICT INSTRUCTIONS:
1. ONLY use methods that are documented above
2. NEVER invent or guess method names
3. Follow the exact signatures shown
4. Use the working examples as templates
5. Return ONLY executable Python code - no explanations
6. Always use math.radians() for rotations
7. Always check if doc and nodes exist
8. Always end with doc.refreshProjection()

If a requested operation cannot be done with the documented API, respond with:
# Cannot perform this operation - method not available in Krita API
"""

# Model configurations
MODELS = {
    "openai": {
        "gpt-4": {
            "name": "gpt-4",
            "description": "OpenAI GPT-4 - Most capable",
            "cost_per_1k": 0.03
        },
        "gpt-4-turbo-preview": {
            "name": "gpt-4-turbo-preview",
            "description": "OpenAI GPT-4 Turbo - Faster",
            "cost_per_1k": 0.01
        },
        "gpt-3.5-turbo": {
            "name": "gpt-3.5-turbo",
            "description": "OpenAI GPT-3.5 - Fast & cheap",
            "cost_per_1k": 0.001
        }
    },
    "anthropic": {
        "claude-3-5-sonnet-20241022": {
            "name": "claude-3-5-sonnet-20241022",
            "description": "Claude 3.5 Sonnet - Most capable",
            "cost_per_1k": 0.003
        },
        "claude-3-haiku-20240307": {
            "name": "claude-3-haiku-20240307",
            "description": "Claude 3 Haiku - Fast & cheap",
            "cost_per_1k": 0.00025
        }
    }
}