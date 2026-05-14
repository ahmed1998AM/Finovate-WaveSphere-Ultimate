"""
Finovate WaveSphere Ultimate - Main Window
النافذة الرئيسية للتطبيق

المطور: Ahmed Mostafa Ibrahim
العلامة التجارية: Finovate – AHMED EG
"""

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from .theme_manager import ThemeManager, get_theme_manager
from .widgets import *


class MainWindow(QMainWindow):
    """النافذة الرئيسية لتطبيق WaveSphere"""
    
    def __init__(self):
        super().__init__()
        self.theme_manager = get_theme_manager()
        self.current_station = None
        self.is_playing = False
        self.favorites = []
        
        self.setup_ui()
        self.setup_connections()
        self.apply_theme()
        
    def setup_ui(self):
        """إعداد واجهة المستخدم"""
        self.setWindowTitle("Finovate WaveSphere Ultimate 📻")
        self.setMinimumSize(1200, 800)
        self.setStyleSheet("background: #0A0A0F;")
        
        #_widget المركزي
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # الشريط العلوي
        header = self.create_header()
        main_layout.addWidget(header)
        
        # المحتوى الرئيسي
        content = self.create_content()
        main_layout.addWidget(content, 1)
        
        # شريط التحكم السفلي
        player_bar = self.create_player_bar()
        main_layout.addWidget(player_bar)
        
    def create_header(self) -> QWidget:
        """إنشاء الشريط العلوي"""
        header = QWidget()
        header.setFixedHeight(80)
        header.setStyleSheet("background: rgba(20, 20, 35, 0.9); border-bottom: 1px solid rgba(0, 245, 255, 0.3);")
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # الشعار والعنوان
        logo_layout = QVBoxLayout()
        logo_label = QLabel("🌊 WaveSphere")
        logo_label.setStyleSheet("color: #00F5FF; font-size: 28px; font-weight: bold;")
        logo_layout.addWidget(logo_label)
        
        slogan = QLabel("اسمع العالم بلا حدود")
        slogan.setStyleSheet("color: #B0B0B0; font-size: 12px;")
        logo_layout.addWidget(slogan)
        
        layout.addLayout(logo_layout)
        layout.addStretch()
        
        # صندوق البحث
        self.search_box = SearchBox("ابحث عن محطة، دولة، أو نوع...")
        self.search_box.setFixedWidth(400)
        layout.addWidget(self.search_box)
        
        layout.addStretch()
        
        # أزرار الإعدادات
        settings_btn = GlowButton("⚙️", color='#FFD700')
        settings_btn.setFixedSize(45, 45)
        layout.addWidget(settings_btn)
        
        return header
    
    def create_content(self) -> QWidget:
        """إنشاء المحتوى الرئيسي"""
        content = QWidget()
        layout = QHBoxLayout(content)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # القائمة الجانبية
        sidebar = self.create_sidebar()
        layout.addWidget(sidebar, 0)
        
        # منطقة المحطات
        stations_area = self.create_stations_area()
        layout.addWidget(stations_area, 1)
        
        # اللوحة الجانبية اليمنى
        info_panel = self.create_info_panel()
        layout.addWidget(info_panel, 0)
        
        return content
    
    def create_sidebar(self) -> QWidget:
        """إنشاء القائمة الجانبية"""
        sidebar = QWidget()
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("background: rgba(15, 15, 25, 0.8); border-right: 1px solid rgba(0, 245, 255, 0.2);")
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # العنوان
        title = QLabel("القائمة")
        title.setStyleSheet("color: #00F5FF; font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # عناصر القائمة
        menu_items = [
            ("🏠", "الرئيسية"),
            ("❤️", "المفضلة"),
            ("📜", "سجل الاستماع"),
            ("🌍", "الدول"),
            ("🎵", "الأنواع"),
            ("🎙️", "البودكاست"),
            ("📻", "محطاتي"),
            ("⚙️", "الإعدادات"),
        ]
        
        for icon, text in menu_items:
            btn = QPushButton(f"{icon} {text}")
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #FFFFFF;
                    text-align: right;
                    padding: 12px 15px;
                    border-radius: 8px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: rgba(0, 245, 255, 0.1);
                }
                QPushButton:checked {
                    background: rgba(0, 245, 255, 0.2);
                    border-left: 3px solid #00F5FF;
                }
            """)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # معلومات المطور
        dev_info = QLabel("© 2025 Ahmed Mostafa Ibrahim\nFinovate – AHMED EG")
        dev_info.setStyleSheet("color: #666; font-size: 10px; padding: 10px;")
        dev_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(dev_info)
        
        return sidebar
    
    def create_stations_area(self) -> QWidget:
        """إنشاء منطقة عرض المحطات"""
        area = QWidget()
        layout = QVBoxLayout(area)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # شريط الفلترة
        filter_bar = self.create_filter_bar()
        layout.addWidget(filter_bar)
        
        # مرئي الموجة
        self.wave_visualizer = WaveVisualizer()
        self.wave_visualizer.setFixedHeight(120)
        layout.addWidget(self.wave_visualizer)
        
        # شبكة المحطات
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("border: none; background: transparent;")
        
        stations_widget = QWidget()
        self.stations_layout = QGridLayout(stations_widget)
        self.stations_layout.setSpacing(15)
        
        # إضافة بطاقات تجريبية
        self.populate_stations()
        
        scroll.setWidget(stations_widget)
        layout.addWidget(scroll, 1)
        
        return area
    
    def create_filter_bar(self) -> QWidget:
        """إنشاء شريط الفلترة"""
        bar = QWidget()
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(0, 0, 0, 10)
        
        # فلتر الدولة
        country_combo = QComboBox()
        country_combo.addItem("🌍 كل الدول")
        countries = ["مصر", "السعودية", "الإمارات", "الكويت", "قطر", "الأردن", "لبنان", "المغرب", "الجزائر", "تونس", "USA", "UK", "France", "Germany"]
        for country in countries:
            country_combo.addItem(country)
        country_combo.setFixedWidth(150)
        layout.addWidget(country_combo)
        
        # فلتر النوع
        genre_combo = QComboBox()
        genre_combo.addItem("🎵 كل الأنواع")
        genres = ["أخبار", "موسيقى", "إسلامي", "قرآن", "رياضة", "حوارات", "بودكاست", "تعليمي", "تقنية", "كلاسيكي", "جاز", "روك", "بوب", "هيب هوب", "إلكتروني"]
        for genre in genres:
            genre_combo.addItem(genre)
        genre_combo.setFixedWidth(150)
        layout.addWidget(genre_combo)
        
        layout.addStretch()
        
        # زر تحديث
        refresh_btn = GlowButton("🔄 تحديث", color='#00FF88')
        layout.addWidget(refresh_btn)
        
        return bar
    
    def populate_stations(self):
        """ملء بطاقات المحطات التجريبية"""
        sample_stations = [
            {"name": "Nile FM", "country": "Egypt", "genre": "Music"},
            {"name": "Nogoum FM", "country": "Egypt", "genre": "Arabic"},
            {"name": "Quran Radio", "country": "Saudi Arabia", "genre": "Islamic"},
            {"name": "BBC Arabic", "country": "UK", "genre": "News"},
            {"name": "Rotana FM", "country": "Saudi Arabia", "genre": "Arabic"},
            {"name": "Radio Monte Carlo", "country": "Lebanon", "genre": "Music"},
            {"name": "Medi 1", "country": "Morocco", "genre": "News"},
            {"name": "Jazz Radio", "country": "France", "genre": "Jazz"},
            {"name": "Classic FM", "country": "UK", "genre": "Classical"},
            {"name": "Kiss FM", "country": "USA", "genre": "Pop"},
            {"name": "Energy FM", "country": "Germany", "genre": "Electronic"},
            {"name": "Virgin Radio", "country": "UAE", "genre": "Rock"},
        ]
        
        row, col = 0, 0
        for i, station in enumerate(sample_stations):
            card = StationCard(station)
            card.clicked.connect(self.on_station_clicked)
            self.stations_layout.addWidget(card, row, col)
            
            col += 1
            if col >= 3:
                col = 0
                row += 1
    
    def create_info_panel(self) -> QWidget:
        """إنشاء لوحة المعلومات الجانبية"""
        panel = QWidget()
        panel.setFixedWidth(300)
        panel.setStyleSheet("background: rgba(15, 15, 25, 0.8); border-left: 1px solid rgba(0, 245, 255, 0.2);")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # العنوان
        title = QLabel("معلومات المحطة")
        title.setStyleSheet("color: #00F5FF; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # معلومات المحطة الحالية
        self.station_info_card = QWidget()
        self.station_info_card.setStyleSheet("background: rgba(30, 30, 50, 0.5); border-radius: 10px; padding: 10px;")
        info_layout = QVBoxLayout(self.station_info_card)
        
        self.info_name = QLabel("لا توجد محطة محددة")
        self.info_name.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        info_layout.addWidget(self.info_name)
        
        self.info_status = QLabel("الحالة: متوقف")
        self.info_status.setStyleSheet("color: #AAAAAA;")
        info_layout.addWidget(self.info_status)
        
        self.info_quality = QLabel("الجودة: --")
        self.info_quality.setStyleSheet("color: #AAAAAA;")
        info_layout.addWidget(self.info_quality)
        
        layout.addWidget(self.station_info_card)
        
        # محلل الطيف
        spectrum_label = QLabel("محلل الطيف")
        spectrum_label.setStyleSheet("color: #00F5FF; font-size: 14px;")
        layout.addWidget(spectrum_label)
        
        self.spectrum_analyzer = SpectrumAnalyzer()
        self.spectrum_analyzer.setFixedHeight(150)
        layout.addWidget(self.spectrum_analyzer)
        
        # قائمة التشغيل
        playlist_label = QLabel("قائمة التشغيل")
        playlist_label.setStyleSheet("color: #00F5FF; font-size: 14px;")
        layout.addWidget(playlist_label)
        
        self.playlist_widget = QListWidget()
        self.playlist_widget.setStyleSheet("""
            QListWidget {
                background: rgba(30, 30, 50, 0.3);
                border: none;
                border-radius: 8px;
                color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background: rgba(0, 245, 255, 0.3);
            }
        """)
        layout.addWidget(self.playlist_widget)
        
        layout.addStretch()
        
        return panel
    
    def create_player_bar(self) -> QWidget:
        """إنشاء شريط مشغل الصوت"""
        bar = QWidget()
        bar.setFixedHeight(100)
        bar.setStyleSheet("background: rgba(20, 20, 35, 0.95); border-top: 2px solid rgba(0, 245, 255, 0.4);")
        
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 10, 20, 10)
        
        # معلومات المحطة
        info_layout = QVBoxLayout()
        self.current_station_label = QLabel("اختر محطة للبدء")
        self.current_station_label.setStyleSheet("color: #00F5FF; font-size: 18px; font-weight: bold;")
        info_layout.addWidget(self.current_station_label)
        
        self.current_status_label = QLabel("جاهز للتشغيل")
        self.current_status_label.setStyleSheet("color: #AAAAAA; font-size: 12px;")
        info_layout.addWidget(self.current_status_label)
        
        layout.addLayout(info_layout, 1)
        
        # أدوات التحكم
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        # الأزرار
        btn_style = """
            QPushButton {
                background: rgba(0, 245, 255, 0.1);
                color: #00F5FF;
                border: 2px solid rgba(0, 245, 255, 0.3);
                border-radius: 25px;
                padding: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background: rgba(0, 245, 255, 0.2);
                border: 2px solid rgba(0, 245, 255, 0.6);
            }
        """
        
        prev_btn = QPushButton("⏮")
        prev_btn.setStyleSheet(btn_style)
        prev_btn.setFixedSize(50, 50)
        controls_layout.addWidget(prev_btn)
        
        self.play_pause_btn = GlowButton("▶", color='#00F5FF')
        self.play_pause_btn.setFixedSize(60, 60)
        controls_layout.addWidget(self.play_pause_btn)
        
        next_btn = QPushButton("⏭")
        next_btn.setStyleSheet(btn_style)
        next_btn.setFixedSize(50, 50)
        controls_layout.addWidget(next_btn)
        
        layout.addLayout(controls_layout, 1)
        
        # شريط الصوت
        volume_layout = QVBoxLayout()
        volume_label = QLabel("الصوت: 100%")
        volume_label.setStyleSheet("color: #AAAAAA; font-size: 12px;")
        volume_layout.addWidget(volume_label)
        
        self.volume_slider = VolumeSlider()
        self.volume_slider.setFixedWidth(200)
        volume_layout.addWidget(self.volume_slider)
        
        layout.addLayout(volume_layout, 1)
        
        # أزرار إضافية
        extra_layout = QHBoxLayout()
        extra_layout.setSpacing(8)
        
        record_btn = QPushButton("🔴 تسجيل")
        record_btn.setStyleSheet("background: rgba(255, 68, 68, 0.2); color: #FF4444; border: 2px solid #FF4444; border-radius: 8px; padding: 8px 15px;")
        extra_layout.addWidget(record_btn)
        
        fav_btn = QPushButton("❤️ مفضلة")
        fav_btn.setStyleSheet("background: rgba(255, 170, 0, 0.2); color: #FFAA00; border: 2px solid #FFAA00; border-radius: 8px; padding: 8px 15px;")
        extra_layout.addWidget(fav_btn)
        
        layout.addLayout(extra_layout)
        
        return bar
    
    def setup_connections(self):
        """إعداد الاتصالات"""
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        self.search_box.search_triggered.connect(self.on_search)
        
    def apply_theme(self):
        """تطبيق السمة الحالية"""
        self.theme_manager.apply_theme()
        
    def on_station_clicked(self, station):
        """عند النقر على محطة"""
        self.current_station = station
        self.current_station_label.setText(station.get('name', 'Unknown'))
        self.info_name.setText(station.get('name', 'Unknown'))
        
        country = station.get('country', 'Unknown')
        genre = station.get('genre', 'Unknown')
        self.info_status.setText(f"الحالة: {country} - {genre}")
        
    def toggle_play_pause(self):
        """تبديل التشغيل/الإيقاف المؤقت"""
        self.is_playing = not self.is_playing
        
        if self.is_playing:
            self.play_pause_btn.setText("⏸")
            self.current_status_label.setText("جاري التشغيل 🔊")
            self.current_status_label.setStyleSheet("color: #00FF88;")
            self.info_status.setText("الحالة: يعمل الآن")
            self.info_status.setStyleSheet("color: #00FF88;")
        else:
            self.play_pause_btn.setText("▶")
            self.current_status_label.setText("متوقف ⏸")
            self.current_status_label.setStyleSheet("color: #AAAAAA;")
            self.info_status.setText("الحالة: متوقف")
            self.info_status.setStyleSheet("color: #AAAAAA;")
            
    def on_search(self, query):
        """عند البحث"""
        print(f"Searching for: {query}")
        # سيتم تنفيذ البحث هنا


def run_app():
    """تشغيل التطبيق"""
    import sys
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()
