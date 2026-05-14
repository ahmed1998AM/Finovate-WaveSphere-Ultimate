"""
Constants for Finovate WaveSphere Ultimate
"""

from enum import Enum
from typing import Dict, List


class Constants:
    """Application constants and configuration values"""
    
    # Application Info
    APP_NAME = "Finovate WaveSphere Ultimate"
    APP_SHORT_NAME = "WaveSphere"
    VERSION = "1.0.0"
    SLOGAN = "Hear The World Without Limits"
    
    # Developer Info
    DEVELOPER_NAME = "Ahmed Mostafa Ibrahim"
    DEVELOPER_BRAND = "Finovate – AHMED EG"
    DEVELOPER_EMAIL = "gogom8870@gmail.com"
    DEVELOPER_PHONE = "01225155329"
    DEVELOPER_GITHUB = "https://github.com/ahmed1998AM"
    DEVELOPER_FACEBOOK = "https://www.facebook.com/profile.php?id=100049475271023&sk=followers"
    COPYRIGHT = "© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved"
    
    # Branding Colors
    MAIN_COLOR = "#00F5FF"      # Cyan
    SECONDARY_COLOR = "#FFD700"  # Gold
    ACCENT_COLOR = "#FF00FF"     # Magenta
    
    # Supported Platforms
    PLATFORMS = ["Windows", "Linux", "macOS"]
    
    # Supported Languages
    LANGUAGES = [
        "Arabic",
        "English",
        "French",
        "German",
        "Spanish",
        "Russian",
        "Turkish",
        "Italian",
        "Chinese"
    ]
    
    RTL_LANGUAGES = ["Arabic"]
    
    # Radio Station Categories
    CATEGORIES = [
        "News", "Music", "Islamic", "Quran", "Sports", "Talk Shows",
        "Podcasts", "Educational", "Technology", "Classical", "Jazz",
        "Rock", "Pop", "Hip Hop", "Electronic", "Dance", "Arabic",
        "Oriental", "Chill", "Gaming", "Anime", "Kids", "Documentary",
        "Weather", "Traffic", "Local Radio", "Live DJ", "Festival", "Cultural"
    ]
    
    # Supported Countries
    COUNTRIES = [
        "Egypt", "Saudi Arabia", "UAE", "Kuwait", "Qatar", "Jordan",
        "Lebanon", "Morocco", "Algeria", "Tunisia", "USA", "Canada",
        "UK", "France", "Germany", "Italy", "Spain", "Turkey", "Russia",
        "India", "Japan", "China", "Brazil", "Argentina", "Australia",
        "South Africa", "Nigeria", "Mexico", "Indonesia", "Malaysia"
    ]
    
    # Audio Formats
    AUDIO_FORMATS = ["MP3", "AAC", "AAC+", "OGG", "FLAC", "WAV", "Opus", "M3U8"]
    
    # Volume Boost Settings
    MAX_VOLUME_BOOST = 600  # 600%
    DEFAULT_VOLUME_BOOST = 100  # 100%
    
    # Equalizer Bands
    EQUALIZER_BANDS = 31
    
    # Equalizer Presets
    EQ_PRESETS = [
        "Flat", "Bass Boost", "Treble Boost", "Arabic", "Cinema",
        "Gaming", "Podcast", "Jazz", "Rock", "Pop", "Electronic",
        "Night Mode", "Voice Clear"
    ]
    
    # Audio Effects
    AUDIO_EFFECTS = [
        "3D Surround", "Reverb", "Echo", "Stereo Widening",
        "AI Noise Reduction", "Dynamic Compressor", "Smart Volume",
        "Virtual Bass", "Spatial Audio"
    ]
    
    # UI Themes
    THEMES = [
        "Neon Cyberpunk",
        "Glass Morphism",
        "Dark Professional",
        "Minimal White",
        "RGB Reactive",
        "Finovate Gold"
    ]
    
    # Desktop Modes
    DESKTOP_MODES = [
        "Normal Mode",
        "Compact Mode",
        "Mini Player",
        "Always On Top",
        "Transparent Overlay",
        "Fullscreen Visualizer"
    ]
    
    # Network Settings
    AUTO_UPDATE_INTERVAL_HOURS = 6
    STREAM_TIMEOUT_SECONDS = 30
    RECONNECT_ATTEMPTS = 5
    BUFFER_SIZE_SECONDS = 5
    
    # Database Settings
    DATABASE_TYPE = "SQLite"  # Can be SQLite, PostgreSQL
    REDIS_ENABLED = True
    
    # Security Settings
    SANDBOX_PLAYBACK = True
    URL_FILTERING = True
    ENCRYPT_SETTINGS = True
    
    # Recording Settings
    RECORDING_ENABLED = True
    RECORDING_FORMATS = ["MP3", "WAV", "FLAC"]
    
    # Cloud Sync
    CLOUD_SYNC_ENABLED = True
    
    # Plugin System
    PLUGIN_SYSTEM_ENABLED = True
    
    # Radio Source APIs
    RADIO_SOURCES = {
        "Radio Browser": "https://www.radio-browser.info/",
        "Shoutcast Directory": "https://directory.shoutcast.com/",
        "Icecast Directory": "https://dir.xiph.org/",
        "Online Radio Box": "https://onlineradiobox.com/",
        "MyTuner": "https://mytuner-radio.com/"
    }
    
    # AI Features
    AI_FEATURES = [
        "AI station recommendations",
        "AI audio repair",
        "AI metadata translation",
        "AI language detection",
        "AI smart categorization",
        "AI favorite prediction",
        "AI stream quality optimization"
    ]
    
    # Future Features (Roadmap)
    FUTURE_FEATURES = [
        "AI DJ",
        "Live chat rooms",
        "Personal broadcasting",
        "Voice assistant",
        "VR visualizer",
        "Podcast marketplace",
        "Music recognition",
        "Lyrics synchronization",
        "Real-time subtitles",
        "Multi-room streaming"
    ]


class PlaybackState(Enum):
    """Playback state enumeration"""
    STOPPED = "stopped"
    PLAYING = "playing"
    PAUSED = "paused"
    BUFFERING = "buffering"
    ERROR = "error"


class UpdateChannel(Enum):
    """Update channel types"""
    STABLE = "stable"
    BETA = "beta"
    DEV = "dev"
