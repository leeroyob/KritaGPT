# KritaGPT Plugin Initialization
from .kritaGPT import *

# Register the plugin with Krita
Krita.instance().addDockWidgetFactory(DockWidgetFactory("kritaGPT", DockWidgetFactoryBase.DockRight, KritaGPTDocker))