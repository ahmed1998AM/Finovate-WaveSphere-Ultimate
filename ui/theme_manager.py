"""
Finovate WaveSphere Ultimate - Theme Manager
مدير السمات والثيمات للتطبيق

يدعم 6 سمات رئيسية:
- Neon Cyberpunk
- Glass Morphism
- Dark Professional
- Minimal White
- RGB Reactive
- Finovate Gold
"""

from PySide6.QtCore import QObject, Signal, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QPalette, QFont
from PySide6.QtWidgets import QApplication
import json


class ThemeManager(QObject):
    """مدير سمات التطبيق"""
    
    theme_changed = Signal(str)
    
    # ألوان العلامة التجارية
    BRAND_COLORS = {
        'main': '#00F5FF',      # سيان نيون
        'secondary': '#FFD700', # ذهبي
        'accent': '#FF00FF',    # وردي نيون
        'background': '#0A0A0F',
        'surface': '#12121A',
        'text': '#FFFFFF',
        'text_secondary': '#B0B0B0'
    }
    
    THEMES = {
        'neon_cyberpunk': {
            'name': 'Neon Cyberpunk',
            'name_ar': 'سايبربانك نيون',
            'colors': {
                'primary': '#00F5FF',
                'secondary': '#FF00FF',
                'accent': '#FFD700',
                'background': '#0A0A0F',
                'surface': '#12121A',
                'surface_hover': '#1A1A2E',
                'text': '#FFFFFF',
                'text_secondary': '#00F5FF',
                'success': '#00FF88',
                'warning': '#FFAA00',
                'error': '#FF4444',
                'border': '#00F5FF40'
            },
            'gradient': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0A0A0F, stop:1 #1A0A2E)',
            'font': 'Segoe UI',
            'glow_effect': True
        },
        'glass_morphism': {
            'name': 'Glass Morphism',
            'name_ar': 'تأثير الزجاج',
            'colors': {
                'primary': '#4A90D9',
                'secondary': '#6DD5FA',
                'accent': '#FFFFFF',
                'background': '#1A1A2E',
                'surface': '#25254080',
                'surface_hover': '#30305080',
                'text': '#FFFFFF',
                'text_secondary': '#CCCCCC',
                'success': '#4ADE80',
                'warning': '#FBBF24',
                'error': '#F87171',
                'border': '#FFFFFF20'
            },
            'gradient': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1A1A2E, stop:1 #2D2D44)',
            'font': 'Segoe UI',
            'blur_effect': True
        },
        'dark_professional': {
            'name': 'Dark Professional',
            'name_ar': 'داكن احترافي',
            'colors': {
                'primary': '#3B82F6',
                'secondary': '#10B981',
                'accent': '#8B5CF6',
                'background': '#18181B',
                'surface': '#27272A',
                'surface_hover': '#3F3F46',
                'text': '#FAFAFA',
                'text_secondary': '#A1A1AA',
                'success': '#22C55E',
                'warning': '#EAB308',
                'error': '#EF4444',
                'border': '#3F3F46'
            },
            'gradient': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #18181B, stop:1 #27272A)',
            'font': 'Segoe UI',
            'minimal': True
        },
        'minimal_white': {
            'name': 'Minimal White',
            'name_ar': 'أبيض بسيط',
            'colors': {
                'primary': '#00F5FF',
                'secondary': '#FFD700',
                'accent': '#FF00FF',
                'background': '#FAFAFA',
                'surface': '#FFFFFF',
                'surface_hover': '#F5F5F5',
                'text': '#18181B',
                'text_secondary': '#71717A',
                'success': '#22C55E',
                'warning': '#EAB308',
                'error': '#EF4444',
                'border': '#E4E4E7'
            },
            'gradient': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FAFAFA, stop:1 #FFFFFF)',
            'font': 'Segoe UI',
            'light_mode': True
        },
        'rgb_reactive': {
            'name': 'RGB Reactive',
            'name_ar': 'RGB تفاعلي',
            'colors': {
                'primary': '#FF0000',
                'secondary': '#00FF00',
                'accent': '#0000FF',
                'background': '#050505',
                'surface': '#101010',
                'surface_hover': '#1A1A1A',
                'text': '#FFFFFF',
                'text_secondary': '#AAAAAA',
                'success': '#00FF88',
                'warning': '#FFFF00',
                'error': '#FF0044',
                'border': '#FF000040'
            },
            'gradient': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #050505, stop:0.5 #100000, stop:1 #001000)',
            'font': 'Consolas',
            'rgb_animation': True
        },
        'finovate_gold': {
            'name': 'Finovate Gold',
            'name_ar': 'فينوفيت ذهبي',
            'colors': {
                'primary': '#FFD700',
                'secondary': '#FFA500',
                'accent': '#00F5FF',
                'background': '#0D0D0D',
                'surface': '#1A1A1A',
                'surface_hover': '#252525',
                'text': '#FFFFFF',
                'text_secondary': '#FFD700',
                'success': '#FFD700',
                'warning': '#FFA500',
                'error': '#FF4444',
                'border': '#FFD70040'
            },
            'gradient': 'qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0D0D0D, stop:1 #1A1500)',
            'font': 'Times New Roman',
            'premium': True
        }
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_theme = 'neon_cyberpark'
        self._rtl = False
        self._animations_enabled = True
        
    def get_theme(self, theme_name: str) -> dict:
        """الحصول على بيانات السمة"""
        return self.THEMES.get(theme_name, self.THEMES['neon_cyberpunk'])
    
    def set_theme(self, theme_name: str):
        """تطبيق سمة جديدة"""
        if theme_name in self.THEMES:
            self._current_theme = theme_name
            self.apply_theme()
            self.theme_changed.emit(theme_name)
            
    def apply_theme(self):
        """تطبيق السمة الحالية على التطبيق"""
        theme = self.get_theme(self._current_theme)
        app = QApplication.instance()
        
        if app:
            palette = self._create_palette(theme['colors'])
            app.setPalette(palette)
            app.setStyleSheet(self._get_stylesheet(theme))
            
    def _create_palette(self, colors: dict) -> QPalette:
        """إنشاء لوحة الألوان"""
        palette = QPalette()
        
        palette.setColor(QPalette.Window, QColor(colors['background']))
        palette.setColor(QPalette.WindowText, QColor(colors['text']))
        palette.setColor(QPalette.Base, QColor(colors['surface']))
        palette.setColor(QPalette.AlternateBase, QColor(colors['surface_hover']))
        palette.setColor(QPalette.Text, QColor(colors['text']))
        palette.setColor(QPalette.Button, QColor(colors['surface']))
        palette.setColor(QPalette.ButtonText, QColor(colors['text']))
        palette.setColor(QPalette.BrightText, QColor(colors['primary']))
        palette.setColor(QPalette.Highlight, QColor(colors['primary']))
        palette.setColor(QPalette.HighlightedText, QColor(colors['background']))
        
        return palette
    
    def _get_stylesheet(self, theme: dict) -> str:
        """الحصول على ورقة الأنماط للسمة"""
        colors = theme['colors']
        
        return f"""
            QMainWindow, QDialog {{
                background: {theme['gradient']};
                color: {colors['text']};
                font-family: {theme['font']};
            }}
            
            QPushButton {{
                background-color: {colors['primary']};
                color: {colors['background']};
                border: 2px solid {colors['border']};
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }}
            
            QPushButton:hover {{
                background-color: {colors['secondary']};
            }}
            
            QPushButton:pressed {{
                background-color: {colors['accent']};
            }}
            
            QSlider::groove:horizontal {{
                background: {colors['surface']};
                height: 8px;
                border-radius: 4px;
            }}
            
            QSlider::handle:horizontal {{
                background: {colors['primary']};
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }}
            
            QProgressBar {{
                background: {colors['surface']};
                border: none;
                border-radius: 4px;
                height: 8px;
            }}
            
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 {colors['primary']}, stop:1 {colors['secondary']});
                border-radius: 4px;
            }}
            
            QListWidget, QTableWidget {{
                background: {colors['surface']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}
            
            QListWidget::item:selected, QTableWidget::item:selected {{
                background: {colors['primary']};
                color: {colors['background']};
            }}
            
            QScrollBar:vertical {{
                background: {colors['surface']};
                width: 10px;
                border-radius: 5px;
            }}
            
            QScrollBar::handle:vertical {{
                background: {colors['primary']};
                border-radius: 5px;
            }}
            
            QLineEdit, QTextEdit {{
                background: {colors['surface']};
                color: {colors['text']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                padding: 8px;
            }}
            
            QLabel#title {{
                font-size: 24px;
                font-weight: bold;
                color: {colors['primary']};
            }}
            
            QLabel#subtitle {{
                font-size: 14px;
                color: {colors['text_secondary']};
            }}
        """
    
    def toggle_rtl(self, rtl: bool):
        """تبديل اتجاه النص (يمين/يسار)"""
        self._rtl = rtl
        app = QApplication.instance()
        if app:
            app.setLayoutDirection(1 if rtl else 0)  # Qt.RightToLeft = 1
            
    def get_available_themes(self) -> list:
        """الحصول على قائمة السمات المتاحة"""
        return list(self.THEMES.keys())
    
    def get_theme_names(self, language: str = 'en') -> dict:
        """الحصول على أسماء السمات بلغة محددة"""
        result = {}
        for key, theme in self.THEMES.items():
            if language == 'ar':
                result[key] = theme.get('name_ar', theme['name'])
            else:
                result[key] = theme['name']
        return result
    
    @property
    def current_theme(self) -> str:
        """السمة الحالية"""
        return self._current_theme
    
    @property
    def is_rtl(self) -> bool:
        """هل الاتجاه من اليمين لليسار؟"""
        return self._rtl
    
    @property
    def brand_colors(self) -> dict:
        """ألوان العلامة التجارية"""
        return self.BRAND_COLORS.copy()


# Singleton instance
_theme_manager_instance = None

def get_theme_manager() -> ThemeManager:
    """الحصول على مثيل مدير السمات"""
    global _theme_manager_instance
    if _theme_manager_instance is None:
        _theme_manager_instance = ThemeManager()
    return _theme_manager_instance
