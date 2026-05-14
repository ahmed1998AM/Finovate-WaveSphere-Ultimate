"""
Finovate WaveSphere Ultimate - Installer Module
وحدة التثبيت والحزم

المطور: Ahmed Mostafa Ibrahim
العلامة التجارية: Finovate – AHMED EG
"""

__version__ = "1.0.0"
__author__ = "Ahmed Mostafa Ibrahim"

# منصات التثبيت المدعومة
SUPPORTED_PLATFORMS = {
    'windows': {
        'installer': 'Inno Setup',
        'builder': 'PyInstaller',
        'output': '.exe'
    },
    'linux': {
        'installer': 'AppImage',
        'builder': 'Flatpak',
        'output': '.AppImage'
    },
    'macos': {
        'installer': 'DMG Builder',
        'builder': 'PyInstaller',
        'output': '.dmg'
    }
}

def get_platform_info():
    """الحصول على معلومات المنصة الحالية"""
    import sys
    
    if sys.platform.startswith('win'):
        return SUPPORTED_PLATFORMS['windows']
    elif sys.platform.startswith('linux'):
        return SUPPORTED_PLATFORMS['linux']
    elif sys.platform.startswith('darwin'):
        return SUPPORTED_PLATFORMS['macos']
    else:
        return None
