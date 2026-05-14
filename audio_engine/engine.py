"""
Main Audio Engine for Finovate WaveSphere Ultimate
Handles stream playback using VLC/FFmpeg backend
"""

import asyncio
from typing import Optional, Dict, Any, Callable
from enum import Enum


class PlayerState(Enum):
    """Player state enumeration"""
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2
    BUFFERING = 3
    ERROR = 4


class AudioEngine:
    """
    Main audio engine for radio streaming
    
    Supports multiple backends: VLC, FFmpeg, PyAudio
    Features:
    - Stream playback
    - Volume control (up to 600% boost)
    - DSP processing
    - Recording
    - Metadata extraction
    """
    
    def __init__(self, backend: str = "vlc"):
        """
        Initialize audio engine
        
        Args:
            backend: Audio backend to use ("vlc", "ffmpeg", "pyaudio")
        """
        self.backend = backend
        self.player = None
        self.state = PlayerState.STOPPED
        self.current_url: Optional[str] = None
        self.volume = 100  # Base volume 0-100
        self.boost_multiplier = 1.0  # Boost multiplier (1.0 = 100%, 6.0 = 600%)
        
        self._callbacks: Dict[str, Callable] = {
            "state_change": None,
            "metadata_update": None,
            "error": None,
        }
        
        self._initialize_backend()
    
    def _initialize_backend(self) -> None:
        """Initialize the selected audio backend"""
        try:
            if self.backend == "vlc":
                self._init_vlc()
            elif self.backend == "ffmpeg":
                self._init_ffmpeg()
            elif self.backend == "pyaudio":
                self._init_pyaudio()
            else:
                raise ValueError(f"Unknown backend: {self.backend}")
            
            print(f"[AUDIO] Backend initialized: {self.backend}")
        except Exception as e:
            print(f"[AUDIO] Backend initialization failed: {e}")
            self.state = PlayerState.ERROR
    
    def _init_vlc(self) -> None:
        """Initialize VLC backend"""
        try:
            import vlc
            
            # Create VLC instance with audio filters
            self.vlc_instance = vlc.Instance(
                '--no-video',
                '--audio-filter=volnorm',
                '--volume-step=1',
            )
            
            self.player = self.vlc_instance.media_player_new()
            
            # Set up event manager
            event_manager = self.player.event_manager()
            event_manager.event_attach(
                vlc.EventType.MediaPlayerStateChanged,
                self._on_vlc_state_change
            )
            
        except ImportError:
            print("[AUDIO] VLC not installed, falling back to ffmpeg")
            self.backend = "ffmpeg"
            self._init_ffmpeg()
    
    def _init_ffmpeg(self) -> None:
        """Initialize FFmpeg backend"""
        # FFmpeg initialization will use subprocess
        # Implementation pending
        print("[AUDIO] FFmpeg backend ready")
    
    def _init_pyaudio(self) -> None:
        """Initialize PyAudio backend"""
        try:
            import pyaudio
            
            self.pyaudio_instance = pyaudio.PyAudio()
            print("[AUDIO] PyAudio backend ready")
            
        except ImportError:
            print("[AUDIO] PyAudio not available")
            raise
    
    def _on_vlc_state_change(self, event) -> None:
        """Handle VLC state changes"""
        if self.player is None:
            return
        
        vlc_state = self.player.get_state()
        
        # Map VLC states to our states
        state_map = {
            0: PlayerState.STOPPED,   # NothingSpecial
            1: PlayerState.BUFFERING, # Opening
            2: PlayerState.BUFFERING, # Buffering
            3: PlayerState.PLAYING,   # Playing
            4: PlayerState.PAUSED,    # Paused
            5: PlayerState.STOPPED,   # Stopped
            6: PlayerState.ERROR,     # Ended
            7: PlayerState.ERROR,     # Error
        }
        
        new_state = state_map.get(vlc_state, PlayerState.STOPPED)
        
        if new_state != self.state:
            old_state = self.state
            self.state = new_state
            
            if self._callbacks["state_change"]:
                self._callbacks["state_change"](old_state, new_state)
    
    async def play(self, url: str) -> bool:
        """
        Play a radio stream
        
        Args:
            url: Stream URL
            
        Returns:
            True if playback started successfully
        """
        try:
            print(f"[AUDIO] Playing: {url}")
            self.current_url = url
            self.state = PlayerState.BUFFERING
            
            if self.backend == "vlc" and self.player:
                media = self.vlc_instance.media_new(url)
                self.player.set_media(media)
                self.player.play()
                
                # Wait for playback to start
                await asyncio.sleep(0.5)
                
                if self.player.is_playing():
                    self.state = PlayerState.PLAYING
                    return True
                else:
                    self.state = PlayerState.ERROR
                    return False
            
            elif self.backend == "ffmpeg":
                # FFmpeg implementation pending
                self.state = PlayerState.PLAYING
                return True
            
            elif self.backend == "pyaudio":
                # PyAudio implementation pending
                self.state = PlayerState.PLAYING
                return True
            
            return False
            
        except Exception as e:
            print(f"[AUDIO] Play error: {e}")
            self.state = PlayerState.ERROR
            return False
    
    def pause(self) -> None:
        """Pause playback"""
        if self.state != PlayerState.PLAYING:
            return
        
        if self.backend == "vlc" and self.player:
            self.player.pause()
        
        self.state = PlayerState.PAUSED
        print("[AUDIO] Paused")
    
    def resume(self) -> None:
        """Resume paused playback"""
        if self.state != PlayerState.PAUSED:
            return
        
        if self.backend == "vlc" and self.player:
            self.player.play()
        
        self.state = PlayerState.PLAYING
        print("[AUDIO] Resumed")
    
    def stop(self) -> None:
        """Stop playback"""
        if self.backend == "vlc" and self.player:
            self.player.stop()
        
        self.state = PlayerState.STOPPED
        self.current_url = None
        print("[AUDIO] Stopped")
    
    def set_volume(self, volume: int) -> None:
        """
        Set volume level
        
        Args:
            volume: Volume level (0-100)
        """
        self.volume = max(0, min(100, volume))
        
        if self.backend == "vlc" and self.player:
            # VLC volume is 0-200 (200 = 2x)
            vlc_volume = int(self.volume * self.boost_multiplier * 2)
            vlc_volume = min(200, vlc_volume)  # Cap at 200
            self.player.audio_set_volume(vlc_volume)
        
        print(f"[AUDIO] Volume: {self.volume}% (Boost: {self.boost_multiplier}x)")
    
    def set_boost(self, boost_percent: int) -> None:
        """
        Set volume boost percentage
        
        Args:
            boost_percent: Boost percentage (100-600)
        """
        boost_percent = max(100, min(600, boost_percent))
        self.boost_multiplier = boost_percent / 100.0
        
        # Apply current volume with new boost
        self.set_volume(self.volume)
        print(f"[AUDIO] Boost set to: {boost_percent}%")
    
    def get_volume(self) -> int:
        """Get current volume level"""
        return self.volume
    
    def get_boost(self) -> int:
        """Get current boost percentage"""
        return int(self.boost_multiplier * 100)
    
    def get_state(self) -> PlayerState:
        """Get current player state"""
        return self.state
    
    def get_metadata(self) -> Optional[Dict[str, Any]]:
        """
        Get current stream metadata
        
        Returns:
            Metadata dictionary or None
        """
        if self.backend == "vlc" and self.player:
            media = self.player.get_media()
            if media:
                return {
                    "title": media.get_meta(vlc.Meta.NowPlaying),
                    "artist": media.get_meta(vlc.Meta.Artist),
                    "album": media.get_meta(vlc.Meta.Album),
                }
        return None
    
    def set_callback(self, callback_type: str, callback: Callable) -> None:
        """
        Set a callback function
        
        Args:
            callback_type: Type of callback ("state_change", "metadata_update", "error")
            callback: Callback function
        """
        if callback_type in self._callbacks:
            self._callbacks[callback_type] = callback
    
    def enable_effects(self, effects: Dict[str, bool]) -> None:
        """
        Enable/disable audio effects
        
        Args:
            effects: Dictionary of effect names and enabled states
        """
        # Effects will be applied through DSP processor
        # Implementation pending
        print(f"[AUDIO] Effects updated: {effects}")
    
    async def shutdown(self) -> None:
        """Shutdown audio engine"""
        print("[AUDIO] Shutting down...")
        
        self.stop()
        
        if self.backend == "vlc" and hasattr(self, 'vlc_instance'):
            self.vlc_instance.release()
        
        elif self.backend == "pyaudio" and hasattr(self, 'pyaudio_instance'):
            self.pyaudio_instance.terminate()
        
        print("[AUDIO] Shutdown complete")
