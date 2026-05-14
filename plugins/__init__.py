"""
Finovate WaveSphere Ultimate - Plugins Module
نظام الإضافات والتكاملات

المطور: Ahmed Mostafa Ibrahim
العلامة التجارية: Finovate – AHMED EG
"""

from .plugin_manager import PluginManager
from .plugins.spotify import SpotifyPlugin
from .plugins.discord import DiscordPlugin
from .plugins.obs import OBSPlugin

__version__ = "1.0.0"
__author__ = "Ahmed Mostafa Ibrahim"
