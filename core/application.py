"""
Main Application Class for Finovate WaveSphere Ultimate
Orchestrates all components and manages application lifecycle
"""

import sys
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime

from .config import Config
from .constants import Constants, PlaybackState


class Application:
    """Main application controller"""
    
    _instance: Optional['Application'] = None
    
    def __new__(cls) -> 'Application':
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize application"""
        if self._initialized:
            return
        
        self.config: Optional[Config] = None
        self.playback_state: PlaybackState = PlaybackState.STOPPED
        self.current_station: Optional[Dict[str, Any]] = None
        self.components: Dict[str, Any] = {}
        self._initialized = True
        
        # Print startup banner
        self._print_banner()
    
    def _print_banner(self) -> None:
        """Print application startup banner"""
        banner = f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🌊  Finovate WaveSphere Ultimate v{Constants.VERSION}          ║
║                                                          ║
║   {Constants.SLOGAN}                          ║
║                                                          ║
║   Developer: {Constants.DEVELOPER_NAME:<42} ║
║   Brand: {Constants.DEVELOPER_BRAND:<50} ║
║                                                          ║
║   {Constants.COPYRIGHT:<56} ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def initialize(self) -> bool:
        """
        Initialize all application components
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            print("[INIT] Starting application initialization...")
            
            # Load configuration
            self.config = Config()
            print(f"[INIT] Configuration loaded from: {self.config.config_file}")
            
            # Initialize core components
            self._init_components()
            
            print("[INIT] Application initialized successfully!")
            return True
            
        except Exception as e:
            print(f"[ERROR] Initialization failed: {e}")
            return False
    
    def _init_components(self) -> None:
        """Initialize application components"""
        print("[INIT] Initializing components...")
        
        # Component initialization will be implemented as modules are created
        # Placeholder for future component initialization
        
        self.components = {
            "audio_engine": None,
            "radio_sources": None,
            "ui_manager": None,
            "network_manager": None,
            "database": None,
            "ai_system": None,
            "cloud_sync": None,
            "recording": None,
            "visualizer": None,
            "plugins": None,
            "security": None,
        }
    
    async def start(self) -> None:
        """Start the application main loop"""
        if not self._initialized:
            self.initialize()
        
        print("[APP] Starting application...")
        
        # TODO: Initialize UI and start event loop
        # This will be implemented with PySide6
        
        try:
            # Main application loop
            await self._main_loop()
        except KeyboardInterrupt:
            print("\n[APP] Shutting down...")
        finally:
            await self.shutdown()
    
    async def _main_loop(self) -> None:
        """Main application event loop"""
        # This will be replaced with Qt event loop
        running = True
        
        while running:
            await asyncio.sleep(0.1)
            
            # Check for auto-update
            await self._check_auto_update()
    
    async def _check_auto_update(self) -> None:
        """Check if station update is needed"""
        if not self.config:
            return
        
        if not self.config.get("radio.auto_update_stations", True):
            return
        
        last_update = self.config.get("radio.last_update")
        if not last_update:
            await self._update_stations()
            return
        
        try:
            last_update_dt = datetime.fromisoformat(last_update)
            interval_hours = self.config.get("radio.update_interval_hours", 6)
            
            if (datetime.now() - last_update_dt).total_seconds() > interval_hours * 3600:
                await self._update_stations()
        except Exception as e:
            print(f"[UPDATE] Error checking update: {e}")
    
    async def _update_stations(self) -> None:
        """Update radio station list from sources"""
        print("[UPDATE] Updating radio stations...")
        
        # TODO: Implement station update from radio_sources module
        if self.config:
            self.config.update_last_update()
    
    def play_station(self, station: Dict[str, Any]) -> bool:
        """
        Play a radio station
        
        Args:
            station: Station information dictionary
            
        Returns:
            True if playback started successfully
        """
        try:
            print(f"[PLAY] Playing station: {station.get('name', 'Unknown')}")
            
            self.current_station = station
            self.playback_state = PlaybackState.PLAYING
            
            # TODO: Delegate to audio engine
            # self.components["audio_engine"].play(station['url'])
            
            return True
        except Exception as e:
            print(f"[ERROR] Failed to play station: {e}")
            self.playback_state = PlaybackState.ERROR
            return False
    
    def pause(self) -> None:
        """Pause current playback"""
        if self.playback_state == PlaybackState.PLAYING:
            print("[PLAYBACK] Paused")
            self.playback_state = PlaybackState.PAUSED
            # TODO: self.components["audio_engine"].pause()
    
    def resume(self) -> None:
        """Resume paused playback"""
        if self.playback_state == PlaybackState.PAUSED:
            print("[PLAYBACK] Resumed")
            self.playback_state = PlaybackState.PLAYING
            # TODO: self.components["audio_engine"].resume()
    
    def stop(self) -> None:
        """Stop current playback"""
        print("[PLAYBACK] Stopped")
        self.playback_state = PlaybackState.STOPPED
        self.current_station = None
        # TODO: self.components["audio_engine"].stop()
    
    def set_volume(self, volume: int) -> None:
        """
        Set playback volume
        
        Args:
            volume: Volume level (0-100)
        """
        volume = max(0, min(100, volume))
        print(f"[AUDIO] Volume set to: {volume}%")
        
        if self.config:
            self.config.set("audio.volume", volume)
        
        # TODO: self.components["audio_engine"].set_volume(volume)
    
    def toggle_favorite(self, station: Dict[str, Any]) -> None:
        """
        Toggle station as favorite
        
        Args:
            station: Station information dictionary
        """
        if not self.config:
            return
        
        favorites = self.config.get("radio.favorite_stations", [])
        station_id = station.get('id')
        
        if any(s.get('id') == station_id for s in favorites):
            self.config.remove_favorite_station(station_id)
            print(f"[FAVORITE] Removed: {station.get('name')}")
        else:
            self.config.add_favorite_station(station)
            print(f"[FAVORITE] Added: {station.get('name')}")
    
    def get_playback_state(self) -> PlaybackState:
        """Get current playback state"""
        return self.playback_state
    
    def get_current_station(self) -> Optional[Dict[str, Any]]:
        """Get currently playing station"""
        return self.current_station
    
    async def shutdown(self) -> None:
        """Gracefully shutdown application"""
        print("[SHUTDOWN] Closing application...")
        
        # Stop playback
        self.stop()
        
        # Shutdown components
        for name, component in self.components.items():
            if component and hasattr(component, 'shutdown'):
                print(f"[SHUTDOWN] Closing {name}...")
                await component.shutdown()
        
        # Save configuration
        if self.config:
            self.config.save()
        
        print("[SHUTDOWN] Application closed")
    
    def get_version(self) -> str:
        """Get application version"""
        return Constants.VERSION
    
    def get_info(self) -> Dict[str, Any]:
        """Get application information"""
        return {
            "name": Constants.APP_NAME,
            "version": Constants.VERSION,
            "developer": Constants.DEVELOPER_NAME,
            "brand": Constants.DEVELOPER_BRAND,
            "copyright": Constants.COPYRIGHT,
            "slogan": Constants.SLOGAN
        }
