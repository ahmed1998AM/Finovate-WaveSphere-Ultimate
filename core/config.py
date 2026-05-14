"""
Configuration Manager for Finovate WaveSphere Ultimate
Handles application settings, preferences, and persistence
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime


class Config:
    """Application configuration manager"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            config_file: Path to configuration file
        """
        self.config_file = config_file or self._get_default_config_path()
        self.config: Dict[str, Any] = {}
        self.load()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path based on platform"""
        home = Path.home()
        
        if os.name == 'nt':  # Windows
            config_dir = home / "AppData" / "Roaming" / "WaveSphere"
        elif os.name == 'posix':  # Linux/macOS
            config_dir = home / ".config" / "wavesphere"
        else:
            config_dir = Path.cwd() / "config"
        
        config_dir.mkdir(parents=True, exist_ok=True)
        return str(config_dir / "config.json")
    
    def load(self) -> None:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = self._get_default_config()
                self.save()
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = self._get_default_config()
    
    def save(self) -> bool:
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration values"""
        return {
            "general": {
                "language": "English",
                "theme": "Neon Cyberpunk",
                "desktop_mode": "Normal Mode",
                "auto_start": False,
                "minimize_to_tray": True,
                "always_on_top": False,
                "check_updates": True,
                "update_channel": "stable"
            },
            "audio": {
                "volume": 100,
                "volume_boost": 100,
                "equalizer_preset": "Flat",
                "equalizer_bands": [0.0] * 31,
                "effects": {
                    "3d_surround": False,
                    "reverb": False,
                    "echo": False,
                    "stereo_widening": False,
                    "ai_noise_reduction": False,
                    "dynamic_compressor": True,
                    "smart_volume": True,
                    "virtual_bass": False,
                    "spatial_audio": False
                },
                "output_device": "default",
                "buffer_size": 5,
                "low_latency_mode": False
            },
            "streaming": {
                "auto_reconnect": True,
                "reconnect_attempts": 5,
                "stream_timeout": 30,
                "adaptive_buffering": True,
                "bandwidth_limit": 0,  # 0 = unlimited
                "preferred_quality": "high"
            },
            "radio": {
                "favorite_stations": [],
                "recent_stations": [],
                "auto_update_stations": True,
                "update_interval_hours": 6,
                "last_update": None,
                "hidden_stations": []
            },
            "recording": {
                "enabled": True,
                "output_directory": "~/Music/WaveSphere/Recordings",
                "format": "MP3",
                "bitrate": 320,
                "auto_split_songs": True,
                "add_metadata": True
            },
            "cloud_sync": {
                "enabled": True,
                "sync_favorites": True,
                "sync_settings": True,
                "sync_history": True,
                "sync_playlists": True,
                "last_sync": None
            },
            "plugins": {
                "enabled": True,
                "installed_plugins": [],
                "plugin_settings": {}
            },
            "ai": {
                "recommendations_enabled": True,
                "audio_repair_enabled": False,
                "metadata_translation": False,
                "language_detection": True,
                "smart_categorization": True,
                "favorite_prediction": True,
                "quality_optimization": True
            },
            "security": {
                "sandbox_playback": True,
                "url_filtering": True,
                "encrypt_settings": True,
                "safe_plugin_execution": True
            },
            "ui": {
                "show_visualizer": True,
                "show_spectrum": True,
                "animated_backgrounds": True,
                "blur_effects": True,
                "gpu_acceleration": True,
                "touch_support": False,
                "mini_player_position": "bottom-right",
                "show_notifications": True
            },
            "shortcuts": {
                "play_pause": "Space",
                "stop": "Ctrl+S",
                "next_station": "Ctrl+Right",
                "previous_station": "Ctrl+Left",
                "volume_up": "Ctrl+Up",
                "volume_down": "Ctrl+Down",
                "mute": "Ctrl+M",
                "favorite": "Ctrl+F",
                "record": "Ctrl+R"
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Dot-separated key path (e.g., "audio.volume")
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set configuration value
        
        Args:
            key: Dot-separated key path (e.g., "audio.volume")
            value: Value to set
            
        Returns:
            True if successful, False otherwise
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        return self.save()
    
    def reset(self, section: Optional[str] = None) -> bool:
        """
        Reset configuration to defaults
        
        Args:
            section: Specific section to reset, or None for full reset
            
        Returns:
            True if successful, False otherwise
        """
        if section:
            default_config = self._get_default_config()
            if section in default_config:
                self.config[section] = default_config[section]
                return self.save()
            return False
        else:
            self.config = self._get_default_config()
            return self.save()
    
    def update_last_update(self) -> None:
        """Update the last station update timestamp"""
        self.set("radio.last_update", datetime.now().isoformat())
    
    def update_last_sync(self) -> None:
        """Update the last cloud sync timestamp"""
        self.set("cloud_sync.last_sync", datetime.now().isoformat())
    
    def add_favorite_station(self, station: Dict[str, Any]) -> None:
        """Add a station to favorites"""
        favorites = self.get("radio.favorite_stations", [])
        if station not in favorites:
            favorites.append(station)
            self.set("radio.favorite_stations", favorites)
    
    def remove_favorite_station(self, station_id: str) -> None:
        """Remove a station from favorites"""
        favorites = self.get("radio.favorite_stations", [])
        favorites = [s for s in favorites if s.get('id') != station_id]
        self.set("radio.favorite_stations", favorites)
    
    def is_rtl_language(self) -> bool:
        """Check if current language is RTL"""
        current_language = self.get("general.language", "English")
        return current_language in ["Arabic"]
