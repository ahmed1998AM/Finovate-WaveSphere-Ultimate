"""
Equalizer for Finovate WaveSphere Ultimate
31-band graphic equalizer with presets
"""

from typing import Dict, List, Optional


class Equalizer:
    """
    31-band graphic equalizer
    
    Features:
    - 31 frequency bands (20Hz - 20kHz)
    - Multiple presets
    - Custom user settings
    - Real-time adjustment
    """
    
    # Center frequencies for 31 bands (ISO standard)
    FREQUENCIES = [
        20, 25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500,
        630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000,
        10000, 12500, 16000, 20000
    ]
    
    # Preset configurations (gain values for each band in dB)
    PRESETS: Dict[str, List[float]] = {
        "Flat": [0.0] * 31,
        "Bass Boost": [6, 5, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Treble Boost": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 6, 6],
        "Arabic": [3, 3, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2,
                   3, 3, 2, 1, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 0, 0],
        "Cinema": [4, 4, 3, 2, 1, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0,
                   1, 2, 3, 4, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 4, 3],
        "Gaming": [3, 3, 3, 2, 1, 0, 0, 0, 1, 2, 2, 1, 0, 0, 1,
                   2, 3, 3, 2, 1, 0, 0, 1, 2, 3, 4, 4, 3, 2, 1, 0],
        "Podcast": [2, 2, 1, 0, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 3,
                    3, 2, 1, 0, 0, 0, 1, 2, 2, 1, 0, 0, 0, 0, 0, 0],
        "Jazz": [3, 3, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2,
                 3, 3, 2, 1, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 0, 0],
        "Rock": [4, 4, 3, 2, 1, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0,
                 1, 2, 3, 4, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 4, 3],
        "Pop": [3, 3, 2, 1, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 1,
                2, 3, 3, 2, 1, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 0],
        "Electronic": [5, 4, 3, 2, 1, 0, 0, 1, 2, 3, 4, 4, 3, 2, 1,
                       0, 0, 1, 2, 3, 4, 5, 5, 4, 3, 2, 1, 0, 0, 0, 0],
        "Night Mode": [-3, -2, -1, 0, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2,
                       1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Voice Clear": [1, 1, 0, 0, 0, 0, 1, 2, 3, 3, 2, 1, 0, 0, 1,
                        2, 3, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }
    
    def __init__(self):
        """Initialize equalizer"""
        self.current_preset = "Flat"
        self.bands = self.PRESETS["Flat"].copy()
        self.enabled = True
        
        print(f"[EQ] Equalizer initialized ({len(self.FREQUENCIES)} bands)")
    
    def set_preset(self, preset_name: str) -> bool:
        """
        Set equalizer preset
        
        Args:
            preset_name: Name of preset to apply
            
        Returns:
            True if preset found and applied
        """
        if preset_name in self.PRESETS:
            self.current_preset = preset_name
            self.bands = self.PRESETS[preset_name].copy()
            print(f"[EQ] Preset applied: {preset_name}")
            return True
        
        print(f"[EQ] Preset not found: {preset_name}")
        return False
    
    def set_band(self, band_index: int, gain_db: float) -> bool:
        """
        Set gain for a specific band
        
        Args:
            band_index: Band index (0-30)
            gain_db: Gain in dB (-12 to +12)
            
        Returns:
            True if successful
        """
        if 0 <= band_index < len(self.bands):
            gain_db = max(-12, min(12, gain_db))  # Clamp to valid range
            self.bands[band_index] = gain_db
            self.current_preset = "Custom"
            return True
        
        return False
    
    def set_all_bands(self, gains: List[float]) -> None:
        """
        Set all band gains at once
        
        Args:
            gains: List of 31 gain values in dB
        """
        if len(gains) == len(self.bands):
            self.bands = [max(-12, min(12, g)) for g in gains]
            self.current_preset = "Custom"
    
    def get_band(self, band_index: int) -> Optional[float]:
        """Get gain for a specific band"""
        if 0 <= band_index < len(self.bands):
            return self.bands[band_index]
        return None
    
    def get_bands(self) -> List[float]:
        """Get all band gains"""
        return self.bands.copy()
    
    def get_frequencies(self) -> List[float]:
        """Get all center frequencies"""
        return self.FREQUENCIES.copy()
    
    def get_available_presets(self) -> List[str]:
        """Get list of available presets"""
        return list(self.PRESETS.keys())
    
    def reset(self) -> None:
        """Reset to flat response"""
        self.set_preset("Flat")
    
    def toggle(self, enabled: bool) -> None:
        """Enable or disable equalizer"""
        self.enabled = enabled
        print(f"[EQ] {'Enabled' if enabled else 'Disabled'}")
    
    def get_status(self) -> Dict:
        """Get equalizer status"""
        return {
            "enabled": self.enabled,
            "preset": self.current_preset,
            "bands": self.bands,
        }