"""
Finovate WaveSphere Ultimate - Widgets
مكونات واجهة المستخدم المخصصة

المطور: Ahmed Mostafa Ibrahim
العلامة التجارية: Finovate – AHMED EG
"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import math


class WaveVisualizer(QWidget):
    """مرئي الموجة الصوتية"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(100)
        self.bars = [0.0] * 64
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_bars)
        self.animation_timer.start(50)
        
    def update_bars(self):
        """تحديث أشرطة الموجة"""
        for i in range(len(self.bars)):
            target = math.sin(QTime.currentTime().msecsSinceStartOfDay() / 100 + i * 0.3) * 0.5 + 0.5
            self.bars[i] += (target - self.bars[i]) * 0.2
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        colors = [QColor('#00F5FF'), QColor('#FF00FF'), QColor('#FFD700')]
        bar_width = self.width() // len(self.bars)
        
        for i, amplitude in enumerate(self.bars):
            x = i * bar_width
            height = amplitude * self.height() * 0.8
            y = (self.height() - height) / 2
            
            gradient = QLinearGradient(x, y, x, y + height)
            gradient.setColorAt(0, colors[0])
            gradient.setColorAt(0.5, colors[1])
            gradient.setColorAt(1, colors[2])
            
            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(x + 1, y, bar_width - 2, height, 3, 3)


class SpectrumAnalyzer(QWidget):
    """محلل الطيف الترددي"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.frequencies = [0.0] * 32
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_frequencies)
        self.animation_timer.start(30)
        
    def update_frequencies(self):
        """تحديث الترددات"""
        time_factor = QTime.currentTime().msecsSinceStartOfDay() / 500
        for i in range(len(self.frequencies)):
            freq = i / len(self.frequencies)
            self.frequencies[i] = abs(math.sin(time_factor + freq * math.pi)) * (0.3 + freq * 0.7)
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        bar_width = self.width() // len(self.frequencies)
        
        for i, amplitude in enumerate(self.frequencies):
            x = i * bar_width
            height = amplitude * self.height()
            
            hue = (i / len(self.frequencies)) * 360
            color = QColor.fromHsl(hue, 255, 128, 200)
            
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(x + 1, self.height() - height, bar_width - 2, height, 4, 4)


class GlowButton(QPushButton):
    """زر مع تأثير توهج"""
    
    def __init__(self, text, parent=None, color='#00F5FF'):
        super().__init__(text, parent)
        self.glow_color = QColor(color)
        self.glow_intensity = 0
        self.hovered = False
        
        self.animation = QPropertyAnimation(self, b"glowIntensity")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        
    @Property(float)
    def glowIntensity(self):
        return self.glow_intensity
    
    @glowIntensity.setter
    def glowIntensity(self, value):
        self.glow_intensity = value
        self.update()
        
    def enterEvent(self, event):
        self.hovered = True
        self.animation.setEndValue(1.0)
        self.animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.hovered = False
        self.animation.setEndValue(0.0)
        self.animation.start()
        super().leaveEvent(event)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if self.glow_intensity > 0:
            glow_radius = self.width() * (0.5 + self.glow_intensity * 0.5)
            glow = QRadialGradient(self.rect().center(), glow_radius)
            glow_color = QColor(self.glow_color)
            glow_color.setAlpha(int(100 * self.glow_intensity))
            glow.setColorAt(0, glow_color)
            glow.setColorAt(1, Qt.transparent)
            
            painter.setBrush(glow)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(self.rect())
        
        super().paintEvent(event)


class VolumeSlider(QSlider):
    """شريط صوت مخصص مع تعزيز حتى 600%"""
    
    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self.setRange(0, 600)
        self.setValue(100)
        self.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #1A1A2E;
                height: 10px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #00F5FF, stop:1 #FF00FF);
                width: 20px;
                margin: -5px 0;
                border-radius: 10px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00F5FF, stop:0.5 #FF00FF, stop:1 #FFD700);
                border-radius: 5px;
            }
        """)


class StationCard(QWidget):
    """بطاقة محطة راديو"""
    
    clicked = Signal(object)
    
    def __init__(self, station_data, parent=None):
        super().__init__(parent)
        self.station = station_data
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # اسم المحطة
        name_label = QLabel(self.station.get('name', 'Unknown'))
        name_label.setObjectName('title')
        name_label.setWordWrap(True)
        layout.addWidget(name_label)
        
        # معلومات إضافية
        info_layout = QHBoxLayout()
        
        if 'country' in self.station:
            country_label = QLabel(f"🌍 {self.station['country']}")
            country_label.setObjectName('subtitle')
            info_layout.addWidget(country_label)
        
        if 'genre' in self.station:
            genre_label = QLabel(f"🎵 {self.station['genre']}")
            genre_label.setObjectName('subtitle')
            info_layout.addWidget(genre_label)
        
        info_layout.addStretch()
        layout.addLayout(info_layout)
        
        # حالة البث
        self.status_label = QLabel("● متوقف")
        self.status_label.setObjectName('subtitle')
        layout.addWidget(self.status_label)
        
        self.setStyleSheet("""
            QWidget {
                background: rgba(30, 30, 50, 0.8);
                border: 1px solid rgba(0, 245, 255, 0.3);
                border-radius: 12px;
            }
            QWidget:hover {
                background: rgba(40, 40, 70, 0.9);
                border: 1px solid rgba(0, 245, 255, 0.6);
            }
        """)
        
    def mousePressEvent(self, event):
        self.clicked.emit(self.station)
        super().mousePressEvent(event)
        
    def set_playing(self, playing: bool):
        """تحديث حالة التشغيل"""
        if playing:
            self.status_label.setText("● يعمل الآن")
            self.status_label.setStyleSheet("color: #00FF88;")
        else:
            self.status_label.setText("● متوقف")
            self.status_label.setStyleSheet("color: #B0B0B0;")


class MiniPlayer(QWidget):
    """مشغل مصغر عائم"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # زر تشغيل/إيقاف مؤقت
        self.play_btn = GlowButton("▶", color='#00F5FF')
        self.play_btn.setFixedSize(40, 40)
        layout.addWidget(self.play_btn)
        
        # معلومات المحطة
        info_layout = QVBoxLayout()
        self.station_name = QLabel("لا توجد محطة")
        self.station_name.setStyleSheet("color: white; font-weight: bold;")
        info_layout.addWidget(self.station_name)
        
        self.status_label = QLabel("متوقف")
        self.status_label.setStyleSheet("color: #AAAAAA; font-size: 12px;")
        info_layout.addWidget(self.status_label)
        
        layout.addLayout(info_layout)
        
        # شريط الصوت
        self.volume_slider = VolumeSlider()
        self.volume_slider.setFixedWidth(100)
        layout.addWidget(self.volume_slider)
        
        self.setStyleSheet("""
            QWidget {
                background: rgba(10, 10, 15, 0.9);
                border: 1px solid rgba(0, 245, 255, 0.4);
                border-radius: 30px;
            }
        """)


class SearchBox(QLineEdit):
    """صندوق بحث مع أيقونة"""
    
    search_triggered = Signal(str)
    
    def __init__(self, placeholder="ابحث عن محطة...", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(40)
        self.setup_style()
        
    def setup_style(self):
        self.setStyleSheet("""
            QLineEdit {
                background: rgba(30, 30, 50, 0.8);
                color: white;
                border: 2px solid rgba(0, 245, 255, 0.3);
                border-radius: 20px;
                padding: 10px 15px 10px 40px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid rgba(0, 245, 255, 0.8);
                background: rgba(40, 40, 70, 0.9);
            }
        """)
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.search_triggered.emit(self.text())
        super().keyPressEvent(event)


__all__ = [
    'WaveVisualizer',
    'SpectrumAnalyzer', 
    'GlowButton',
    'VolumeSlider',
    'StationCard',
    'MiniPlayer',
    'SearchBox'
]
