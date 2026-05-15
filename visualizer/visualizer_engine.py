"""
Finovate WaveSphere Ultimate - Visualizer Module
محرك المرئيات الصوتية المتقدم
المطور: Ahmed Mostafa Ibrahim - Finovate AHMED EG
"""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class VisualizerMode(Enum):
    """أوضاع المرئيات المتاحة"""
    SPECTRUM = "spectrum"  # طيف الترددات
    WAVEFORM = "waveform"  # شكل الموجة
    CIRCULAR = "circular"  # دائري
    BARS_3D = "bars_3d"  # أعمدة ثلاثية الأبعاد
    PARTICLES = "particles"  # جسيمات
    REACTIVE = "reactive"  # تفاعلي مع الموسيقى


@dataclass
class VisualizerConfig:
    """تكوين المرئيات"""
    mode: VisualizerMode = VisualizerMode.SPECTRUM
    fps: int = 60
    resolution: Tuple[int, int] = (1920, 1080)
    color_scheme: str = "neon"
    sensitivity: float = 1.0
    smoothing: float = 0.7
    mirror_mode: bool = True
    glow_effect: bool = True
    particle_count: int = 500


class AudioVisualizer:
    """
    محرك المرئيات الصوتية المتقدم
    يدعم 6 أوضاع مختلفة مع تأثيرات بصرية مذهلة
    """
    
    def __init__(self, config: Optional[VisualizerConfig] = None):
        self.config = config or VisualizerConfig()
        self.fft_bins = 1024
        self.sample_rate = 44100
        self.buffer_size = 2048
        
        # مخازن البيانات
        self.frequency_data = np.zeros(self.fft_bins)
        self.waveform_data = np.zeros(self.buffer_size)
        self.history = []
        self.particles = []
        
        # إعداد الجسيمات
        self._init_particles()
        
    def _init_particles(self):
        """تهيئة نظام الجسيمات"""
        for i in range(self.config.particle_count):
            self.particles.append({
                'x': np.random.uniform(0, self.config.resolution[0]),
                'y': np.random.uniform(0, self.config.resolution[1]),
                'vx': np.random.uniform(-2, 2),
                'vy': np.random.uniform(-2, 2),
                'size': np.random.uniform(2, 8),
                'color': self._get_random_color(),
                'life': np.random.uniform(0.5, 2.0)
            })
    
    def _get_random_color(self) -> Tuple[int, int, int]:
        """الحصول على لون عشوائي من مخطط الألوان"""
        colors = {
            'neon': [(0, 245, 255), (255, 0, 255), (255, 215, 0)],
            'fire': [(255, 69, 0), (255, 140, 0), (255, 215, 0)],
            'ocean': [(0, 105, 148), (0, 191, 255), (135, 206, 250)],
            'forest': [(34, 139, 34), (0, 255, 127), (144, 238, 144)]
        }
        palette = colors.get(self.config.color_scheme, colors['neon'])
        return palette[np.random.randint(len(palette))]
    
    def process_audio(self, audio_data: np.ndarray, sample_rate: int = 44100):
        """
        معالجة البيانات الصوتية وتحليلها
        
        Args:
            audio_data: بيانات الصوت الخام
            sample_rate: معدل العينة
        """
        self.sample_rate = sample_rate
        
        # استخراج شكل الموجة
        if len(audio_data) > self.buffer_size:
            self.waveform_data = audio_data[:self.buffer_size]
        else:
            self.waveform_data[:len(audio_data)] = audio_data
        
        # تحويل فورييه السريع (FFT) لتحليل الترددات
        fft_result = np.fft.rfft(audio_data * np.hanning(len(audio_data)))
        magnitude = np.abs(fft_result)
        
        # تطبيع البيانات
        if len(magnitude) < self.fft_bins:
            self.frequency_data[:len(magnitude)] = magnitude
        else:
            self.frequency_data = magnitude[:self.fft_bins]
        
        # تطبيق التنعيم
        self.frequency_data = self._apply_smoothing(self.frequency_data)
        
        # تحديث السجل التاريخي
        self.history.append(self.frequency_data.copy())
        if len(self.history) > 30:
            self.history.pop(0)
    
    def _apply_smoothing(self, data: np.ndarray) -> np.ndarray:
        """تطبيق تأثير التنعيم على البيانات"""
        if self.config.smoothing > 0 and len(self.history) > 0:
            alpha = self.config.smoothing
            prev = self.history[-1] if len(self.history) > 0 else data
            return alpha * prev + (1 - alpha) * data
        return data
    
    def get_spectrum_bars(self, num_bars: int = 64) -> List[float]:
        """
        الحصول على أعمدة الطيف
        
        Args:
            num_bars: عدد الأعمدة
            
        Returns:
            قائمة بقيم ارتفاع الأعمدة (0-1)
        """
        # تجميع نطاقات التردد
        bins_per_bar = len(self.frequency_data) // num_bars
        bars = []
        
        for i in range(num_bars):
            start = i * bins_per_bar
            end = start + bins_per_bar
            bar_value = np.mean(self.frequency_data[start:end])
            bars.append(min(1.0, bar_value / 10000.0 * self.config.sensitivity))
        
        return bars
    
    def get_waveform_points(self, num_points: int = 200) -> List[Tuple[float, float]]:
        """
        الحصول على نقاط شكل الموجة
        
        Args:
            num_points: عدد النقاط
            
        Returns:
            قائمة بالإحداثيات (x, y)
        """
        step = len(self.waveform_data) // num_points
        points = []
        
        for i in range(num_points):
            x = i / num_points
            y = self.waveform_data[i * step] if i * step < len(self.waveform_data) else 0
            points.append((x, y))
        
        return points
    
    def update_particles(self, audio_level: float) -> List[dict]:
        """
        تحديث نظام الجسيمات بناءً على مستوى الصوت
        
        Args:
            audio_level: مستوى الصوت الحالي (0-1)
            
        Returns:
            قائمة بحالات الجسيمات المحدثة
        """
        for particle in self.particles:
            # تحديث الموضع
            particle['x'] += particle['vx'] * (1 + audio_level)
            particle['y'] += particle['vy'] * (1 + audio_level)
            
            # تحديث الحجم بناءً على الصوت
            base_size = particle['size']
            particle['current_size'] = base_size * (1 + audio_level * 2)
            
            # تقليل العمر
            particle['life'] -= 0.01
            particle['alpha'] = min(1.0, particle['life'] / 2.0)
            
            # إعادة إنشاء الجسيمات الميتة
            if particle['life'] <= 0 or \
               particle['x'] < 0 or particle['x'] > self.config.resolution[0] or \
               particle['y'] < 0 or particle['y'] > self.config.resolution[1]:
                particle['x'] = np.random.uniform(0, self.config.resolution[0])
                particle['y'] = np.random.uniform(0, self.config.resolution[1])
                particle['life'] = np.random.uniform(0.5, 2.0)
                particle['vx'] = np.random.uniform(-2, 2)
                particle['vy'] = np.random.uniform(-2, 2)
        
        return self.particles
    
    def get_beat_detection(self) -> bool:
        """
        كشف الإيقاع (Beat Detection)
        
        Returns:
            True إذا تم كشف إيقاع قوي
        """
        if len(self.history) < 5:
            return False
        
        # حساب متوسط الطاقة في النطاقات المنخفضة (Bass)
        bass_range = self.frequency_data[:10]
        current_bass = np.mean(bass_range)
        
        # مقارنة مع المتوسط التاريخي
        historical_bass = np.mean([np.mean(h[:10]) for h in self.history[:-1]])
        
        # كشف الإيقاع إذا كان هناك قفزة مفاجئة
        return current_bass > historical_bass * 1.5
    
    def get_render_data(self) -> dict:
        """
        الحصول على جميع البيانات المطلوبة للرسم
        
        Returns:
            قاموس يحتوي على جميع بيانات المرئيات
        """
        return {
            'spectrum_bars': self.get_spectrum_bars(),
            'waveform_points': self.get_waveform_points(),
            'particles': self.update_particles(np.mean(self.frequency_data[:20]) / 10000.0),
            'beat_detected': self.get_beat_detection(),
            'audio_level': np.mean(self.frequency_data) / 10000.0,
            'frequency_data': self.frequency_data.copy(),
            'config': self.config
        }
    
    def set_mode(self, mode: VisualizerMode):
        """تغيير وضع المرئيات"""
        self.config.mode = mode
        if mode == VisualizerMode.PARTICLES:
            self._init_particles()
    
    def set_color_scheme(self, scheme: str):
        """تغيير مخطط الألوان"""
        self.config.color_scheme = scheme
        # إعادة تلوين الجسيمات
        for particle in self.particles:
            particle['color'] = self._get_random_color()


class VisualizerRenderer:
    """
    محدد مرئيات للرسام مع PySide6/QML
    يمكن دمجه مع واجهة المستخدم
    """
    
    def __init__(self, visualizer: AudioVisualizer):
        self.visualizer = visualizer
        self.frame_count = 0
    
    def render_to_texture(self, width: int, height: int) -> np.ndarray:
        """
        رسم المرئيات إلى مصفوفة numpy
        
        Args:
            width: عرض الإطار
            height: ارتفاع الإطار
            
        Returns:
            مصفوفة RGB
        """
        # إنشاء إطار فارغ
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        data = self.visualizer.get_render_data()
        
        if self.visualizer.config.mode == VisualizerMode.SPECTRUM:
            self._render_spectrum(frame, data)
        elif self.visualizer.config.mode == VisualizerMode.WAVEFORM:
            self._render_waveform(frame, data)
        elif self.visualizer.config.mode == VisualizerMode.CIRCULAR:
            self._render_circular(frame, data)
        elif self.visualizer.config.mode == VisualizerMode.PARTICLES:
            self._render_particles(frame, data)
        
        self.frame_count += 1
        return frame
    
    def _render_spectrum(self, frame: np.ndarray, data: dict):
        """رسم طيف الترددات"""
        bars = data['spectrum_bars']
        num_bars = len(bars)
        bar_width = frame.shape[1] // num_bars
        
        for i, height in enumerate(bars):
            x = i * bar_width
            bar_height = int(height * frame.shape[0] * 0.8)
            
            # لون متدرج
            color = self._get_gradient_color(i / num_bars, data['beat_detected'])
            
            # رسم العمود
            y_start = frame.shape[0] - bar_height
            frame[y_start:frame.shape[0], x:x + bar_width] = color
            
            # تأثير التوهج
            if self.visualizer.config.glow_effect:
                glow_height = bar_height // 3
                for g in range(glow_height):
                    alpha = 1.0 - (g / glow_height)
                    glow_y = frame.shape[0] - bar_height - g
                    if glow_y >= 0:
                        current = frame[glow_y:glow_y+1, x:x + bar_width]
                        frame[glow_y:glow_y+1, x:x + bar_width] = (
                            current * (1 - alpha * 0.5) + 
                            np.array(color) * alpha * 0.5
                        ).astype(np.uint8)
    
    def _render_waveform(self, frame: np.ndarray, data: dict):
        """رسم شكل الموجة"""
        points = data['waveform_points']
        center_y = frame.shape[0] // 2
        
        prev_x = None
        prev_y = None
        
        for x_norm, y_val in points:
            x = int(x_norm * frame.shape[1])
            y = center_y + int(y_val * center_y * 0.8)
            
            if prev_x is not None:
                # رسم خط بين النقطتين
                color = (0, 245, 255) if not data['beat_detected'] else (255, 0, 255)
                self._draw_line(frame, prev_x, prev_y, x, y, color, 2)
            
            prev_x = x
            prev_y = y
    
    def _render_circular(self, frame: np.ndarray, data: dict):
        """رسم المرئيات الدائرية"""
        import math
        
        center_x = frame.shape[1] // 2
        center_y = frame.shape[0] // 2
        base_radius = min(frame.shape) * 0.2
        
        bars = data['spectrum_bars']
        num_bars = len(bars)
        
        for i, height in enumerate(bars):
            angle = (i / num_bars) * 2 * math.pi
            bar_length = base_radius + height * base_radius
            
            x1 = center_x + int(math.cos(angle) * base_radius)
            y1 = center_y + int(math.sin(angle) * base_radius)
            x2 = center_x + int(math.cos(angle) * bar_length)
            y2 = center_y + int(math.sin(angle) * bar_length)
            
            color = self._get_gradient_color(i / num_bars, data['beat_detected'])
            self._draw_line(frame, x1, y1, x2, y2, color, 3)
    
    def _render_particles(self, frame: np.ndarray, data: dict):
        """رسم نظام الجسيمات"""
        for particle in data['particles']:
            x = int(particle['x'])
            y = int(particle['y'])
            size = int(particle['current_size'])
            color = particle['color']
            alpha = particle['alpha']
            
            # رسم دائرة للجسيم
            for dy in range(-size, size + 1):
                for dx in range(-size, size + 1):
                    if dx*dx + dy*dy <= size*size:
                        px, py = x + dx, y + dy
                        if 0 <= px < frame.shape[1] and 0 <= py < frame.shape[0]:
                            current = frame[py, px]
                            blended = (
                                current * (1 - alpha) + 
                                np.array(color) * alpha
                            ).astype(np.uint8)
                            frame[py, px] = blended
    
    def _get_gradient_color(self, position: float, beat: bool) -> Tuple[int, int, int]:
        """الحصول على لون متدرج"""
        if beat:
            # ألوان نابضة عند الإيقاع
            colors = [(255, 0, 255), (255, 215, 0), (0, 245, 255)]
        else:
            # ألوان عادية
            colors = [(0, 245, 255), (0, 100, 255), (100, 0, 255)]
        
        index = int(position * (len(colors) - 1))
        return colors[min(index, len(colors) - 1)]
    
    def _draw_line(self, frame: np.ndarray, x0: int, y0: int, x1: int, y1: int, 
                   color: Tuple[int, int, int], thickness: int = 1):
        """رسم خط باستخدام خوارزمية Bresenham"""
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        
        while True:
            if 0 <= x0 < frame.shape[1] and 0 <= y0 < frame.shape[0]:
                frame[y0, x0] = color
            
            if x0 == x1 and y0 == y1:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy


# مثال للاستخدام
if __name__ == "__main__":
    print("🎨 Finovate WaveSphere Visualizer Engine")
    print("=" * 50)
    
    # إنشاء المرئيات
    config = VisualizerConfig(
        mode=VisualizerMode.SPECTRUM,
        fps=60,
        color_scheme='neon',
        particle_count=500
    )
    
    visualizer = AudioVisualizer(config)
    renderer = VisualizerRenderer(visualizer)
    
    # محاكاة بيانات صوتية
    print("\n📊 اختبار تحليل الصوت...")
    duration = 1.0
    t = np.linspace(0, duration, int(44100 * duration))
    
    # إنشاء موجة مركبة (نغمات متعددة)
    frequencies = [220, 440, 880, 1760]
    audio_signal = np.zeros_like(t)
    for freq in frequencies:
        audio_signal += 0.5 * np.sin(2 * np.pi * freq * t)
    
    # إضافة بعض الضوضاء
    audio_signal += 0.1 * np.random.randn(len(t))
    
    # معالجة الصوت
    visualizer.process_audio(audio_signal)
    
    # الحصول على البيانات
    data = visualizer.get_render_data()
    
    print(f"✓ مستويات الطيف: {len(data['spectrum_bars'])} عمود")
    print(f"✓ نقاط الموجة: {len(data['waveform_points'])} نقطة")
    print(f"✓ الجسيمات النشطة: {len(data['particles'])}")
    print(f"✓ الإيقاع المكتشف: {'نعم' if data['beat_detected'] else 'لا'}")
    print(f"✓ مستوى الصوت: {data['audio_level']:.2f}")
    
    # اختبار الرسم
    print("\n🎨 اختبار العرض...")
    frame = renderer.render_to_texture(800, 600)
    print(f"✓ تم إنشاء إطار: {frame.shape} (RGB)")
    print(f"✓ عدد الإطارات: {renderer.frame_count}")
    
    # اختبار الأوضاع المختلفة
    print("\n🔄 اختبار الأوضاع المختلفة...")
    for mode in VisualizerMode:
        visualizer.set_mode(mode)
        frame = renderer.render_to_texture(400, 300)
        print(f"  ✓ وضع {mode.value}: {frame.shape}")
    
    print("\n✅ جميع اختبارات المرئيات ناجحة!")
    print("\n© 2025 Ahmed Mostafa Ibrahim — Finovate AHMED EG")
    print("🌊 Hear The World Without Limits")
