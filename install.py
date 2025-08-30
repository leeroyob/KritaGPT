#!/usr/bin/env python3
"""
Installation helper for KritaGPT
Installs the OpenAI dependency into Krita's Python environment
"""

import subprocess
import sys
import os
from pathlib import Path

def install_openai():
    """Install OpenAI package for Krita's Python"""
    print("KritaGPT Installer")
    print("=" * 50)
    print()
    
    # Check if openai is already installed
    try:
        import openai
        print("✓ OpenAI library is already installed")
        print(f"  Version: {openai.__version__}")
        return True
    except ImportError:
        print("OpenAI library not found. Installing...")
    
    # Try to install using pip
    try:
        print("Installing openai package...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openai>=0.27.0"])
        print("✓ OpenAI library installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing OpenAI library: {e}")
        print()
        print("Manual installation instructions:")
        print("1. Open a terminal/command prompt")
        print("2. Navigate to Krita's Python directory")
        print("3. Run: pip install openai")
        return False

def main():
    """Main installation process"""
    print("This script will install the OpenAI library required for KritaGPT.")
    print()
    
    # Install OpenAI
    success = install_openai()
    
    print()
    print("=" * 50)
    
    if success:
        print("Installation complete!")
        print()
        print("Next steps:")
        print("1. Restart Krita")
        print("2. Enable KritaGPT in Settings → Configure Krita → Python Plugins")
        print("3. Access KritaGPT from Settings → Dockers → KritaGPT")
        print("4. Configure your OpenAI API key in the Settings tab")
    else:
        print("Installation failed. Please install manually.")
    
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()