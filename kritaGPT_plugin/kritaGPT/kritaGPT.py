"""
Main KritaGPT Plugin Module
Natural language commands for Krita using GPT-4 and Claude
"""

from krita import DockWidget, DockWidgetFactory, DockWidgetFactoryBase, Krita
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QTextEdit, QLabel, QComboBox, QCheckBox, QLineEdit,
    QTabWidget, QListWidget, QMessageBox, QGroupBox,
    QSpinBox, QDoubleSpinBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QFont, QTextCursor

from .config import Config, MODELS
from .gpt_handler import GPTHandler
from .command_processor import CommandProcessor

class KritaGPTDocker(DockWidget):
    """Main docker widget for KritaGPT"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KritaGPT")
        
        # Initialize components
        self.config = Config()
        self.gpt_handler = None
        self.processor = CommandProcessor()
        self.command_history = []
        self.history_index = -1
        
        # Create main widget
        main_widget = QWidget()
        self.setWidget(main_widget)
        
        # Setup UI
        self.setup_ui(main_widget)
        
        # Initialize GPT handler if API key exists
        self.initialize_gpt()
        
        # Connect processor signals
        self.processor.execution_started.connect(self.on_execution_started)
        self.processor.execution_completed.connect(self.on_execution_completed)
        self.processor.execution_error.connect(self.on_execution_error)
    
    def canvasChanged(self, canvas):
        """Required override for DockWidget - called when canvas changes"""
        pass
    
    def setup_ui(self, parent):
        """Setup the user interface"""
        layout = QVBoxLayout(parent)
        
        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Main tab
        main_tab = QWidget()
        self.setup_main_tab(main_tab)
        self.tabs.addTab(main_tab, "Commands")
        
        # Settings tab
        settings_tab = QWidget()
        self.setup_settings_tab(settings_tab)
        self.tabs.addTab(settings_tab, "Settings")
        
        # History tab
        history_tab = QWidget()
        self.setup_history_tab(history_tab)
        self.tabs.addTab(history_tab, "History")
    
    def setup_main_tab(self, parent):
        """Setup the main command interface"""
        layout = QVBoxLayout(parent)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("QLabel { color: green; }")
        layout.addWidget(self.status_label)
        
        # Command input
        input_group = QGroupBox("Command")
        input_layout = QVBoxLayout()
        
        self.command_input = QTextEdit()
        self.command_input.setPlaceholderText("Type your command here...\nE.g., 'Create a new layer called Background'")
        self.command_input.setMaximumHeight(100)
        input_layout.addWidget(self.command_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.execute_btn = QPushButton("Execute")
        self.execute_btn.clicked.connect(self.execute_command)
        self.execute_btn.setStyleSheet("QPushButton { font-weight: bold; }")
        button_layout.addWidget(self.execute_btn)
        
        self.show_code_checkbox = QCheckBox("Show Code")
        self.show_code_checkbox.setChecked(self.config.get("show_code", False))
        button_layout.addWidget(self.show_code_checkbox)
        
        self.auto_execute_checkbox = QCheckBox("Auto Execute")
        self.auto_execute_checkbox.setChecked(self.config.get("auto_execute", True))
        button_layout.addWidget(self.auto_execute_checkbox)
        
        button_layout.addStretch()
        
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_output)
        button_layout.addWidget(self.clear_btn)
        
        input_layout.addLayout(button_layout)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Output area
        output_group = QGroupBox("Output")
        output_layout = QVBoxLayout()
        
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Consolas", 9))
        output_layout.addWidget(self.output_text)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # Setup keyboard shortcuts
        self.setup_shortcuts()
    
    def setup_settings_tab(self, parent):
        """Setup the settings interface"""
        layout = QVBoxLayout(parent)
        
        # API Provider Selection
        provider_group = QGroupBox("API Provider")
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("Provider:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItem("OpenAI (GPT-4/GPT-3.5)", "openai")
        self.provider_combo.addItem("Anthropic (Claude)", "anthropic")
        current_provider = self.config.get("api_provider", "openai")
        index = self.provider_combo.findData(current_provider)
        if index >= 0:
            self.provider_combo.setCurrentIndex(index)
        self.provider_combo.currentIndexChanged.connect(self.on_provider_changed)
        provider_layout.addWidget(self.provider_combo)
        provider_layout.addStretch()
        provider_group.setLayout(provider_layout)
        layout.addWidget(provider_group)
        
        # API Keys
        api_group = QGroupBox("API Configuration")
        api_layout = QVBoxLayout()
        
        # OpenAI API Key
        openai_key_layout = QHBoxLayout()
        openai_key_layout.addWidget(QLabel("OpenAI Key:"))
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setEchoMode(QLineEdit.Password)
        self.openai_key_input.setText(self.config.get("openai_api_key", self.config.get("api_key", "")))
        self.openai_key_input.setPlaceholderText("sk-...")
        openai_key_layout.addWidget(self.openai_key_input)
        api_layout.addLayout(openai_key_layout)
        
        # Anthropic API Key
        anthropic_key_layout = QHBoxLayout()
        anthropic_key_layout.addWidget(QLabel("Anthropic Key:"))
        self.anthropic_key_input = QLineEdit()
        self.anthropic_key_input.setEchoMode(QLineEdit.Password)
        self.anthropic_key_input.setText(self.config.get("anthropic_api_key", ""))
        self.anthropic_key_input.setPlaceholderText("sk-ant-...")
        anthropic_key_layout.addWidget(self.anthropic_key_input)
        api_layout.addLayout(anthropic_key_layout)
        
        # Save button
        self.save_api_keys_btn = QPushButton("Save API Keys")
        self.save_api_keys_btn.clicked.connect(self.save_api_keys)
        api_layout.addWidget(self.save_api_keys_btn)
        
        # Model selection
        model_layout = QHBoxLayout()
        model_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.update_model_combo()
        self.model_combo.currentIndexChanged.connect(self.save_model)
        model_layout.addWidget(self.model_combo)
        model_layout.addStretch()
        
        api_layout.addLayout(model_layout)
        
        # Temperature
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(QLabel("Temperature:"))
        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setRange(0.0, 1.0)
        self.temperature_spin.setSingleStep(0.1)
        self.temperature_spin.setValue(self.config.get("temperature", 0.1))
        self.temperature_spin.valueChanged.connect(self.save_temperature)
        temp_layout.addWidget(self.temperature_spin)
        temp_layout.addWidget(QLabel("(0=precise, 1=creative)"))
        temp_layout.addStretch()
        
        api_layout.addLayout(temp_layout)
        
        api_group.setLayout(api_layout)
        layout.addWidget(api_group)
        
        # Behavior settings
        behavior_group = QGroupBox("Behavior")
        behavior_layout = QVBoxLayout()
        
        history_layout = QHBoxLayout()
        history_layout.addWidget(QLabel("History Size:"))
        self.history_spin = QSpinBox()
        self.history_spin.setRange(5, 50)
        self.history_spin.setValue(self.config.get("history_size", 10))
        self.history_spin.valueChanged.connect(self.save_history_size)
        history_layout.addWidget(self.history_spin)
        history_layout.addStretch()
        
        behavior_layout.addLayout(history_layout)
        
        behavior_group.setLayout(behavior_layout)
        layout.addWidget(behavior_group)
        
        # Info
        info_label = QLabel(
            "<b>Getting API Keys:</b><br>"
            "<b>OpenAI:</b> Visit <a href='https://platform.openai.com'>platform.openai.com</a><br>"
            "<b>Anthropic:</b> Visit <a href='https://console.anthropic.com'>console.anthropic.com</a><br><br>"
            "<b>Costs:</b><br>"
            "GPT-4: ~$0.03 per command<br>"
            "GPT-3.5: ~$0.001 per command<br>"
            "Claude 3.5: ~$0.003 per command<br>"
            "Claude Haiku: ~$0.00025 per command"
        )
        info_label.setOpenExternalLinks(True)
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        layout.addStretch()
    
    def setup_history_tab(self, parent):
        """Setup the history interface"""
        layout = QVBoxLayout(parent)
        
        layout.addWidget(QLabel("Command History:"))
        
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.use_history_command)
        layout.addWidget(self.history_list)
        
        history_buttons = QHBoxLayout()
        
        self.clear_history_btn = QPushButton("Clear History")
        self.clear_history_btn.clicked.connect(self.clear_history)
        history_buttons.addWidget(self.clear_history_btn)
        
        history_buttons.addStretch()
        
        layout.addLayout(history_buttons)
    
    def setup_shortcuts(self):
        """Setup keyboard shortcuts for command input"""
        # This would be implemented with proper Qt key event handling
        pass
    
    def update_model_combo(self):
        """Update model combo based on selected provider"""
        self.model_combo.clear()
        provider = self.provider_combo.currentData() if hasattr(self, 'provider_combo') else self.config.get("api_provider", "openai")
        
        if provider == "anthropic":
            models = MODELS.get("anthropic", {})
        else:
            models = MODELS.get("openai", {})
        
        for model_id, model_info in models.items():
            self.model_combo.addItem(model_info["description"], model_id)
        
        # Set current model
        current_model = self.config.get("model", "gpt-4" if provider == "openai" else "claude-3-5-sonnet-20241022")
        index = self.model_combo.findData(current_model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
    
    @pyqtSlot(int)
    def on_provider_changed(self, index):
        """Handle provider change"""
        provider = self.provider_combo.currentData()
        self.config.set("api_provider", provider)
        self.update_model_combo()
        self.reinitialize_gpt()
    
    @pyqtSlot()
    def save_api_keys(self):
        """Save API keys to config"""
        openai_key = self.openai_key_input.text().strip()
        anthropic_key = self.anthropic_key_input.text().strip()
        
        self.config.set("openai_api_key", openai_key)
        self.config.set("anthropic_api_key", anthropic_key)
        
        # Reinitialize GPT handler
        self.reinitialize_gpt()
        QMessageBox.information(self, "Success", "API keys saved successfully!")
    
    def reinitialize_gpt(self):
        """Reinitialize GPT handler with current settings"""
        provider = self.config.get("api_provider", "openai")
        
        if provider == "anthropic":
            api_key = self.config.get("anthropic_api_key", "")
        else:
            api_key = self.config.get("openai_api_key", self.config.get("api_key", ""))
        
        if api_key:
            model = self.model_combo.currentData() if hasattr(self, 'model_combo') and self.model_combo.count() > 0 else self.config.get("model", "gpt-4")
            temperature = self.config.get("temperature", 0.1)
            self.gpt_handler = GPTHandler(provider, api_key, model, temperature)
            self.status_label.setText(f"Ready ({provider.title()} configured)")
            self.status_label.setStyleSheet("QLabel { color: green; }")
        else:
            self.status_label.setText(f"Please configure {provider.title()} API key in Settings")
            self.status_label.setStyleSheet("QLabel { color: orange; }")
            self.gpt_handler = None
    
    def initialize_gpt(self):
        """Initialize GPT handler with saved API key"""
        self.reinitialize_gpt()
    
    @pyqtSlot()
    def execute_command(self):
        """Execute the command from input"""
        command = self.command_input.toPlainText().strip()
        
        if not command:
            self.show_error("Please enter a command")
            return
        
        if not self.gpt_handler:
            self.show_error("Please configure your API key in Settings tab")
            return
        
        # Add to history
        self.add_to_history(command)
        
        # Clear output if needed
        if not self.show_code_checkbox.isChecked():
            self.output_text.clear()
        
        # Show processing
        self.status_label.setText("Processing...")
        self.status_label.setStyleSheet("QLabel { color: blue; }")
        self.execute_btn.setEnabled(False)
        
        # Process with GPT
        QTimer.singleShot(100, lambda: self.process_command(command))
    
    def process_command(self, command):
        """Process command with GPT and execute"""
        try:
            # Get code from GPT
            result = self.gpt_handler.get_code(command)
            
            if not result["success"]:
                self.show_error(f"API Error: {result['error']}")
                return
            
            code = result["code"]
            
            # Show code if requested
            if self.show_code_checkbox.isChecked():
                self.output_text.append(f"<b>Generated Code:</b>")
                self.output_text.append(f"<pre>{code}</pre>")
                self.output_text.append("")
            
            # Execute code
            auto_execute = self.auto_execute_checkbox.isChecked()
            exec_result = self.processor.execute(code, auto_execute)
            
            if exec_result["success"]:
                self.output_text.append(f"<span style='color: green;'>✓ {exec_result['message']}</span>")
            else:
                self.show_error(f"Execution Error: {exec_result['error']}")
                if self.show_code_checkbox.isChecked() and 'traceback' in exec_result:
                    self.output_text.append(f"<pre>{exec_result['traceback']}</pre>")
            
        except Exception as e:
            self.show_error(f"Unexpected error: {str(e)}")
        
        finally:
            self.status_label.setText("Ready")
            self.status_label.setStyleSheet("QLabel { color: green; }")
            self.execute_btn.setEnabled(True)
    
    def add_to_history(self, command):
        """Add command to history"""
        self.command_history.append(command)
        self.history_list.addItem(command)
        
        # Limit history size
        max_history = self.config.get("history_size", 10)
        if len(self.command_history) > max_history:
            self.command_history = self.command_history[-max_history:]
            self.history_list.clear()
            for cmd in self.command_history:
                self.history_list.addItem(cmd)
    
    def use_history_command(self, item):
        """Use command from history"""
        self.command_input.setText(item.text())
        self.tabs.setCurrentIndex(0)  # Switch to main tab
    
    def clear_history(self):
        """Clear command history"""
        self.command_history.clear()
        self.history_list.clear()
        if self.gpt_handler:
            self.gpt_handler.clear_history()
    
    def clear_output(self):
        """Clear output text"""
        self.output_text.clear()
    
    def show_error(self, message):
        """Show error in output"""
        self.output_text.append(f"<span style='color: red;'>✗ {message}</span>")
        self.status_label.setText("Error")
        self.status_label.setStyleSheet("QLabel { color: red; }")
    
    @pyqtSlot(int)
    def save_model(self, index):
        """Save selected model"""
        model = self.model_combo.itemData(index)
        self.config.set("model", model)
        if self.gpt_handler:
            self.gpt_handler.set_model(model)
    
    @pyqtSlot(float)
    def save_temperature(self, value):
        """Save temperature setting"""
        self.config.set("temperature", value)
        if self.gpt_handler:
            self.gpt_handler.set_temperature(value)
    
    @pyqtSlot(int)
    def save_history_size(self, value):
        """Save history size setting"""
        self.config.set("history_size", value)
    
    @pyqtSlot()
    def on_execution_started(self):
        """Handle execution started signal"""
        self.status_label.setText("Executing...")
        self.status_label.setStyleSheet("QLabel { color: blue; }")
    
    @pyqtSlot(dict)
    def on_execution_completed(self, result):
        """Handle execution completed signal"""
        self.status_label.setText("Ready")
        self.status_label.setStyleSheet("QLabel { color: green; }")
    
    @pyqtSlot(str)
    def on_execution_error(self, error):
        """Handle execution error signal"""
        self.status_label.setText("Execution Error")
        self.status_label.setStyleSheet("QLabel { color: red; }")

# Factory for creating the docker
class KritaGPTDockerFactory(DockWidgetFactory):
    def __init__(self):
        super().__init__("kritaGPT", DockWidgetFactoryBase.DockRight)
    
    def createWidget(self):
        return KritaGPTDocker()