"""
Finovate WaveSphere Ultimate - Plugin Manager
مدير نظام الإضافات

المطور: Ahmed Mostafa Ibrahim
العلامة التجارية: Finovate – AHMED EG
"""

import os
import json
import importlib
from typing import Dict, List, Optional, Any
from PySide6.QtCore import QObject, Signal


class BasePlugin(QObject):
    """الفئة الأساسية للإضافات"""
    
    name = "Base Plugin"
    version = "1.0.0"
    description = "وصف الإضافة"
    author = "Ahmed Mostafa Ibrahim"
    enabled = False
    
    def __init__(self):
        super().__init__()
        
    def activate(self):
        """تفعيل الإضافة"""
        self.enabled = True
        
    def deactivate(self):
        """تعطيل الإضافة"""
        self.enabled = False
        
    def get_settings(self) -> dict:
        """الحصول على إعدادات الإضافة"""
        return {}
        
    def set_settings(self, settings: dict):
        """تعيين إعدادات الإضافة"""
        pass


class PluginManager(QObject):
    """مدير الإضافات"""
    
    plugin_loaded = Signal(str)
    plugin_unloaded = Signal(str)
    plugin_error = Signal(str, str)
    
    def __init__(self):
        super().__init__()
        self.plugins: Dict[str, BasePlugin] = {}
        self.plugin_dir = os.path.join(os.path.dirname(__file__), 'plugins')
        self.config_file = os.path.join(os.path.dirname(__file__), 'plugins_config.json')
        self.load_config()
        
    def load_config(self):
        """تحميل تكوين الإضافات"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {}
            
    def save_config(self):
        """حفظ تكوين الإضافات"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
            
    def discover_plugins(self) -> List[str]:
        """اكتشاف الإضافات المتاحة"""
        available = []
        
        if os.path.exists(self.plugin_dir):
            for item in os.listdir(self.plugin_dir):
                if item.endswith('.py') and not item.startswith('_'):
                    plugin_name = item[:-3]
                    available.append(plugin_name)
                    
        return available
        
    def load_plugin(self, plugin_name: str) -> bool:
        """تحميل إضافة معينة"""
        try:
            module_path = f'plugins.plugins.{plugin_name}'
            module = importlib.import_module(module_path)
            
            # البحث عن فئة الإضافة
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and issubclass(attr, BasePlugin) and attr != BasePlugin:
                    plugin_instance = attr()
                    self.plugins[plugin_name] = plugin_instance
                    
                    # تحميل الإعدادات المحفوظة
                    if plugin_name in self.config:
                        plugin_instance.set_settings(self.config[plugin_name])
                        
                    self.plugin_loaded.emit(plugin_name)
                    return True
                    
        except Exception as e:
            self.plugin_error.emit(plugin_name, str(e))
            return False
            
        return False
        
    def unload_plugin(self, plugin_name: str):
        """إلغاء تحميل إضافة"""
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            plugin.deactivate()
            del self.plugins[plugin_name]
            self.plugin_unloaded.emit(plugin_name)
            
    def enable_plugin(self, plugin_name: str):
        """تفعيل إضافة"""
        if plugin_name in self.plugins:
            self.plugins[plugin_name].activate()
            self.config[plugin_name] = self.plugins[plugin_name].get_settings()
            self.save_config()
            
    def disable_plugin(self, plugin_name: str):
        """تعطيل إضافة"""
        if plugin_name in self.plugins:
            self.plugins[plugin_name].deactivate()
            if plugin_name in self.config:
                del self.config[plugin_name]
                self.save_config()
                
    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        """الحصول على إضافة"""
        return self.plugins.get(plugin_name)
        
    def get_all_plugins(self) -> Dict[str, BasePlugin]:
        """الحصول على جميع الإضافات"""
        return self.plugins.copy()
        
    def get_enabled_plugins(self) -> List[str]:
        """الحصول على الإضافات المفعلة"""
        return [name for name, plugin in self.plugins.items() if plugin.enabled]
        
    def load_all_plugins(self):
        """تحميل جميع الإضافات المكتشفة"""
        discovered = self.discover_plugins()
        for plugin_name in discovered:
            self.load_plugin(plugin_name)
            
    def scan_and_load(self):
        """مسح وتحميل جميع الإضافات"""
        self.load_all_plugins()
        
        # تفعيل الإضافات التي كانت مفعلة سابقاً
        for plugin_name in list(self.config.keys()):
            if plugin_name in self.plugins:
                self.enable_plugin(plugin_name)


# Singleton instance
_plugin_manager_instance = None

def get_plugin_manager() -> PluginManager:
    """الحصول على مثيل مدير الإضافات"""
    global _plugin_manager_instance
    if _plugin_manager_instance is None:
        _plugin_manager_instance = PluginManager()
    return _plugin_manager_instance
