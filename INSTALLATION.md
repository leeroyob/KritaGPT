# KritaGPT Installation Guide

## Quick Installation

1. **Download** the KritaGPT plugin
2. **Install OpenAI library** (required dependency):
   - Option A: Run `install.py` from this folder
   - Option B: Manual install - Open terminal and run:
     ```bash
     pip install openai
     ```

3. **Install Plugin in Krita**:
   - Open Krita
   - Go to `Tools → Scripts → Import Python Plugin from File...`
   - Select the KritaGPT folder or zip file
   - Restart Krita

4. **Enable Plugin**:
   - Go to `Settings → Configure Krita → Python Plugins`
   - Check the box next to "KritaGPT"
   - Click OK

5. **Access KritaGPT**:
   - Go to `Settings → Dockers → KritaGPT`
   - The KritaGPT panel will appear

## Configure API Key

1. In the KritaGPT docker, go to the **Settings** tab
2. Enter your OpenAI API key
3. Click **Save**

### Getting an OpenAI API Key:
1. Visit [platform.openai.com](https://platform.openai.com)
2. Sign in or create an account
3. Go to API Keys section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)

## Troubleshooting

### "ImportError: No module named openai"
- The OpenAI library is not installed
- Run `install.py` or manually install with `pip install openai`

### "No API key configured"
- You need to add your OpenAI API key in the Settings tab
- Make sure to click Save after entering the key

### Plugin doesn't appear in Krita
1. Make sure you restarted Krita after installation
2. Check that the plugin is enabled in Python Plugins settings
3. Verify all files are in the correct location

### Commands not working
1. Check you have an active document open
2. Verify your API key is valid
3. Check your internet connection
4. Try a simple command like "create a new layer"

## File Structure

Your Krita resources folder should contain:
```
pykrita/
└── kritaGPT/
    ├── __init__.py
    ├── kritaGPT.py
    ├── kritaGPT.desktop
    ├── config.py
    ├── gpt_handler.py
    └── command_processor.py
```

## Manual Installation

If automatic installation doesn't work:

1. Locate your Krita resources folder:
   - Windows: `%APPDATA%\krita\pykrita\`
   - Linux: `~/.local/share/krita/pykrita/`
   - macOS: `~/Library/Application Support/Krita/pykrita/`

2. Create a folder called `kritaGPT` in the pykrita directory

3. Copy all Python files into this folder

4. Copy `kritaGPT.desktop` to the pykrita folder (not inside kritaGPT)

5. Restart Krita and enable the plugin

## System Requirements

- Krita 5.0 or later
- Python 3.6 or later
- Internet connection for API calls
- OpenAI API key (free tier available)

## Cost Information

- GPT-4: Approximately $0.03 per command
- GPT-3.5-turbo: Approximately $0.001 per command
- New OpenAI accounts get $5 free credits
- Average usage: $1-5 per month

## Support

For issues or questions:
- Check the README for usage examples
- Visit the GitHub repository
- Review the Technical Design Document for details

## Uninstallation

To remove KritaGPT:
1. Disable the plugin in Krita's Python Plugins settings
2. Delete the `kritaGPT` folder from your pykrita directory
3. Delete the `kritaGPT.desktop` file
4. Delete the config folder at `~/.kritaGPT` (if you want to remove settings)