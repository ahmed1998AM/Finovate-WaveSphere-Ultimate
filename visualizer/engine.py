"""
Finovate WaveSphere Ultimate - Visualizer Module
محرك المرئيات الصوتية المتقدم
© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved
"""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass
import colorsys


@dataclass
class VisualizerConfig:
    """إعدادات المرئيات"""
    fps: int = 60
    bar_count: int = 64
    sensitivity: float = 1.5
    smoothing: float = 0.8
    theme: str = "neon"
    mirror_mode: bool = True
    peak_hold: bool = True
    peak_decay: float = 0.02


class AudioVisualizer:
    """
    محرك المرئيات الصوتية المتقدم
    يدعم: Spectrum Analyzer, Waveform, Circular, Particles
    """
    
    def __init__(self, config: Optional[VisualizerConfig] = None):
        self.config = config or VisualizerConfig()
        self.audio_data = np.zeros(1024)
        self.frequency_data = np.zeros(self.config.bar_count)
        self.waveform_data = np.zeros(512)
        self.peak_values = np.zeros(self.config.bar_count)
        self.phase = 0.0
        
    def update_audio_data(self, audio_buffer: np.ndarray):
        """تحديث بيانات الصوت"""
        if len(audio_buffer) > 0:
            self.audio_data = audio_buffer[:1024] if len(audio_buffer) >= 1024 else \
                            np.pad(audio_buffer, (0, 1024 - len(audio_buffer)))
        
    def compute_frequency_spectrum(self, sample_rate: int = 44100) -> np.ndarray:
        """حساب طيف الترددات باستخدام FFT"""
        if len(self.audio_data) == 0:
            return np.zeros(self.config.bar_count)
        
        # تطبيق نافذة Hanning
        window = np.hanning(len(self.audio_data))
        windowed_data = self.audio_data * window
        
        # FFT
        fft_data = np.fft.rfft(windowed_data)
        magnitude = np.abs(fft_data)
        
        # تجميع الترددات في نطاقات
        bins_per_bar = len(magnitude) // self.config.bar_count
        spectrum = np.zeros(self.config.bar_count)
        
        for i in range(self.config.bar_count):
            start = i * bins_per_bar
            end = start + bins_per_bar
            spectrum[i] = np.mean(magnitude[start:end])
        
        # تطبيع وتطبيق الحساسية
        spectrum = spectrum / (np.max(spectrum) + 1e-10) * self.config.sensitivity
        spectrum = np.clip(spectrum, 0, 1)
        
        # تنعيم
        if self.config.smoothing > 0:
            spectrum = self._smooth_data(spectrum, self.config.smoothing)
        
        self.frequency_data = spectrum
        return spectrum
    
    def compute_waveform(self) -> np.ndarray:
        """حساب شكل الموجة"""
        if len(self.audio_data) == 0:
            return np.zeros(512)
        
        # أخذ عينات من البيانات
        step = len(self.audio_data) // 512
        waveform = np.array([
            np.max(self.audio_data[i:i+step]) if i+step <= len(self.audio_data) else 0
            for i in range(0, len(self.audio_data), step)
        ])
        
        waveform = waveform[:512]
        waveform = np.pad(waveform, (0, 512 - len(waveform))) if len(waveform) < 512 else waveform
        
        self.waveform_data = waveform
        return waveform
    
    def _smooth_data(self, data: np.ndarray, factor: float) -> np.ndarray:
        """تنعيم البيانات"""
        if factor <= 0:
            return data
        
        smoothed = np.copy(data)
        for i in range(1, len(data) - 1):
            smoothed[i] = (1 - factor) * data[i] + factor * 0.5 * (data[i-1] + data[i+1])
        
        return smoothed
    
    def update_peaks(self):
        """تحديث قيم الذروة مع التلاشي"""
        for i in range(len(self.peak_values)):
            if self.frequency_data[i] > self.peak_values[i]:
                self.peak_values[i] = self.frequency_data[i]
            else:
                self.peak_values[i] = max(0, self.peak_values[i] - self.config.peak_decay)
    
    def get_bar_colors(self, base_color: Tuple[int, int, int] = (0, 245, 255)) -> List[Tuple[int, int, int]]:
        """الحصول على ألوان الأعمدة مع تدرج"""
        colors = []
        r, g, b = base_color
        
        # تحويل إلى HSV للتعديل على Hue
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        
        for i, value in enumerate(self.frequency_data):
            # تعديل Hue بناءً على الارتفاع
            hue_shift = i / len(self.frequency_data) * 0.3
            new_h = (h + hue_shift * value) % 1.0
            new_v = min(1.0, v * (0.5 + value * 0.5))
            
            nr, ng, nb = colorsys.hsv_to_rgb(new_h, s, new_v)
            colors.append((int(nr * 255), int(ng * 255), int(nb * 255)))
        
        return colors
    
    def get_circle_visualizer_data(self, radius: int = 200) -> List[Tuple[int, int, int, int]]:
        """بيانات للمرئي الدائري"""
        points = []
        n_bars = len(self.frequency_data)
        
        for i, value in enumerate(self.frequency_data):
            angle = (i / n_bars) * 2 * np.pi
            bar_length = value * radius * 0.8
            
            x = int(radius + bar_length * np.cos(angle))
            y = int(radius + bar_length * np.sin(angle))
            thickness = max(2, int(value * 8))
            
            points.append((x, y, thickness, i))
        
        return points
    
    def reset(self):
        """إعادة تعيين المرئي"""
        self.audio_data = np.zeros(1024)
        self.frequency_data = np.zeros(self.config.bar_count)
        self.waveform_data = np.zeros(512)
        self.peak_values = np.zeros(self.config.bar_count)
        self.phase = 0.0


class ParticleSystem:
    """نظام الجسيمات للمؤثرات البصرية"""
    
    def __init__(self, count: int = 200):
        self.count = count
        self.particles = np.zeros((count, 4))  # x, y, vx, vy
        self.lifetimes = np.zeros(count)
        self.max_lifetime = 2.0
        self.initialize_particles()
    
    def initialize_particles(self):
        """تهيئة الجسيمات"""
        for i in range(self.count):
            self.reset_particle(i)
    
    def reset_particle(self, index: int):
        """إعادة تعيين جسيمة"""
        self.particles[index] = [
            np.random.uniform(-1, 1),
            np.random.uniform(-1, 1),
            np.random.uniform(-0.5, 0.5),
            np.random.uniform(-0.5, 0.5)
        ]
        self.lifetimes[index] = np.random.uniform(0.5, self.max_lifetime)
    
    def update(self, dt: float, audio_intensity: float = 0.5):
        """تحديث نظام الجسيمات"""
        for i in range(self.count):
            self.lifetimes[i] -= dt
            
            if self.lifetimes[i] <= 0:
                self.reset_particle(i)
                continue
            
            # تحديث الموقع
            self.particles[i, 0] += self.particles[i, 2] * dt * (1 + audio_intensity)
            self.particles[i, 1] += self.particles[i, 3] * dt * (1 + audio_intensity)
            
            # حدود الشاشة
            if abs(self.particles[i, 0]) > 1.5:
                self.particles[i, 2] *= -1
            if abs(self.particles[i, 1]) > 1.5:
                self.particles[i, 3] *= -1
    
    def get_active_particles(self) -> np.ndarray:
        """الحصول على الجسيمات النشطة"""
        active_mask = self.lifetimes > 0
        return self.particles[active_mask], self.lifetimes[active_mask]


class VisualizerTheme:
    """سمات المرئيات"""
    
    THEMES = {
        "neon": {
            "primary": (0, 245, 255),
            "secondary": (255, 215, 0),
            "accent": (255, 0, 255),
            "background": (10, 10, 30),
            "glow_intensity": 1.5
        },
        "glass": {
            "primary": (100, 200, 255),
            "secondary": (200, 255, 255),
            "accent": (150, 100, 255),
            "background": (20, 20, 40),
            "glow_intensity": 0.8
        },
        "fire": {
            "primary": (255, 100, 0),
            "secondary": (255, 200, 0),
            "accent": (255, 50, 50),
            "background": (30, 10, 5),
            "glow_intensity": 1.8
        },
        "ocean": {
            "primary": (0, 150, 255),
            "secondary": (0, 255, 200),
            "accent": (100, 255, 255),
            "background": (5, 20, 40),
            "glow_intensity": 1.2
        },
        "matrix": {
            "primary": (0, 255, 0),
            "secondary": (0, 200, 100),
            "accent": (100, 255, 100),
            "background": (0, 10, 0),
            "glow_intensity": 1.3
        }
    }
    
    @classmethod
    def get_theme(cls, name: str) -> dict:
        """الحصول على سمة بالاسم"""
        return cls.THEMES.get(name.lower(), cls.THEMES["neon"])
    
    @classmethod
    def get_theme_names(cls) -> List[str]:
        """الحصول على أسماء السمات المتاحة"""
        return list(cls.THEMES.keys())


# اختبار الوحدة
if __name__ == "__main__":
    print("🎨 Finovate WaveSphere Visualizer Engine")
    print("=" * 40)
    
    config = VisualizerConfig(fps=60, bar_count=64, theme="neon")
    visualizer = AudioVisualizer(config)
    
    # محاكاة بيانات صوتية
    test_audio = np.random.randn(1024) * 0.5
    visualizer.update_audio_data(test_audio)
    
    spectrum = visualizer.compute_frequency_spectrum()
    waveform = visualizer.compute_waveform()
    
    print(f"✓ طيف الترددات: {len(spectrum)} نطاق")
    print(f"✓ شكل الموجة: {len(waveform)} نقطة")
    print(f"✓ السمات المتاحة: {VisualizerTheme.get_theme_names()}")
    
    # اختبار الجسيمات
    particles = ParticleSystem(count=100)
    particles.update(0.016, audio_intensity=0.7)
    active = particles.get_active_particles()
    print(f"✓ الجسيمات النشطة: {len(active[0])}")
    
    print("\n✅ محرك المرئيات جاهز!")
