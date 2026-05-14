"""
Audio Engine Module for Finovate WaveSphere Ultimate
Handles audio playback, DSP processing, and volume enhancement
"""

__version__ = "1.0.0"
__author__ = "Ahmed Mostafa Ibrahim"

from .engine import AudioEngine
from .dsp import DSPProcessor
from .equalizer import Equalizer
from .volume_boost import VolumeBooster

__all__ = [
    "AudioEngine",
    "DSPProcessor",
    "Equalizer",
    "VolumeBooster",
]
