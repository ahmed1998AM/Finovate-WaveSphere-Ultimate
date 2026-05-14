"""
Quality Optimizer AI - محسن جودة البث الذكي
تحسين جودة البث تلقائياً بناءً على ظروف الشبكة
المطور: Ahmed Mostafa Ibrahim - Finovate – AHMED EG
"""

import asyncio
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
import logging
import time

logger = logging.getLogger(__name__)


@dataclass
class StreamQuality:
    """جودة البث الحالية"""
    bitrate: int
    buffer_health: float  # 0-1
    latency_ms: float
    packet_loss: float  # 0-1
    jitter_ms: float
    bandwidth_available: int  # kbps


@dataclass
class QualityRecommendation:
    """توصية الجودة المثلى"""
    recommended_bitrate: int
    buffer_size: int
    reason: str
    confidence: float


class QualityOptimizerAI:
    """
    نظام تحسين جودة البث بالذكاء الاصطناعي
    يضبط الجودة تلقائياً بناءً على الشبكة والأداء
    """
    
    # مستويات الجودة المتاحة
    QUALITY_LEVELS = [
        {'bitrate': 320, 'label': 'Ultra High'},
        {'bitrate': 256, 'label': 'Very High'},
        {'bitrate': 192, 'label': 'High'},
        {'bitrate': 128, 'label': 'Medium'},
        {'bitrate': 96, 'label': 'Low'},
        {'bitrate': 64, 'label': 'Very Low'},
        {'bitrate': 48, 'label': 'Minimum'},
    ]
    
    def __init__(self):
        self.current_quality: Optional[StreamQuality] = None
        self.history: List[StreamQuality] = []
        self.max_history = 100
        
        # عتبات الأداء
        self.thresholds = {
            'excellent_buffer': 0.9,
            'good_buffer': 0.7,
            'poor_buffer': 0.3,
            'excellent_latency': 50,
            'good_latency': 150,
            'poor_latency': 500,
            'acceptable_packet_loss': 0.02,
            'poor_packet_loss': 0.05,
        }
        
        # نموذج التنبؤ (بسيط)
        self.trend_weights = {
            'recent': 0.5,
            'medium': 0.3,
            'old': 0.2,
        }
    
    def update_quality_metrics(
        self,
        bitrate: int,
        buffer_health: float,
        latency_ms: float,
        packet_loss: float = 0.0,
        jitter_ms: float = 0.0,
        bandwidth_available: int = 0
    ):
        """تحديث مقاييس الجودة"""
        quality = StreamQuality(
            bitrate=bitrate,
            buffer_health=buffer_health,
            latency_ms=latency_ms,
            packet_loss=packet_loss,
            jitter_ms=jitter_ms,
            bandwidth_available=bandwidth_available or bitrate * 2
        )
        
        self.current_quality = quality
        self.history.append(quality)
        
        # الاحتفاظ بآخر N سجلات فقط
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def analyze_connection(self) -> Dict[str, any]:
        """تحليل حالة الاتصال"""
        if not self.current_quality:
            return {'status': 'unknown', 'score': 0}
        
        q = self.current_quality
        score = 100
        
        # خصم نقاط للمشاكل
        if q.buffer_health < self.thresholds['poor_buffer']:
            score -= 40
        elif q.buffer_health < self.thresholds['good_buffer']:
            score -= 20
        
        if q.latency_ms > self.thresholds['poor_latency']:
            score -= 30
        elif q.latency_ms > self.thresholds['good_latency']:
            score -= 15
        
        if q.packet_loss > self.thresholds['poor_packet_loss']:
            score -= 25
        elif q.packet_loss > self.thresholds['acceptable_packet_loss']:
            score -= 10
        
        # تحديد الحالة
        if score >= 90:
            status = 'excellent'
        elif score >= 70:
            status = 'good'
        elif score >= 50:
            status = 'fair'
        else:
            status = 'poor'
        
        return {
            'status': status,
            'score': score,
            'buffer': q.buffer_health,
            'latency': q.latency_ms,
            'packet_loss': q.packet_loss,
        }
    
    def recommend_quality(self) -> QualityRecommendation:
        """
        التوصية بالجودة المثلى
        
        Returns:
            توصية بالجودة المناسبة
        """
        if not self.current_quality:
            return QualityRecommendation(
                recommended_bitrate=128,
                buffer_size=5,
                reason="No data available, using default",
                confidence=0.5
            )
        
        analysis = self.analyze_connection()
        q = self.current_quality
        
        # التنبؤ بالاتجاه
        trend = self._predict_trend()
        
        # حساب الجودة الموصى بها
        if analysis['status'] == 'excellent':
            # يمكن استخدام أعلى جودة
            recommended = max(
                min(q.bandwidth_available // 2, 320),
                192
            )
            reason = "Excellent connection, high quality recommended"
            confidence = 0.9
        
        elif analysis['status'] == 'good':
            # جودة عالية مع هامش أمان
            recommended = max(
                min(q.bandwidth_available // 3, 256),
                128
            )
            reason = "Good connection, balanced quality"
            confidence = 0.8
        
        elif analysis['status'] == 'fair':
            # جودة متوسطة للاستقرار
            recommended = max(
                min(q.bandwidth_available // 4, 192),
                96
            )
            reason = "Fair connection, prioritizing stability"
            confidence = 0.7
        
        else:  # poor
            # جودة منخفضة لتجنب التقطع
            recommended = max(
                min(q.bandwidth_available // 5, 128),
                48
            )
            reason = "Poor connection, low quality for continuity"
            confidence = 0.6
        
        # تعديل حسب الاتجاه
        if trend == 'degrading':
            recommended = max(recommended - 32, 48)
            reason += " (adjusting for degrading trend)"
        elif trend == 'improving':
            recommended = min(recommended + 32, 320)
            reason += " (adjusting for improving trend)"
        
        # حساب حجم المخزن المؤقت الموصى به
        buffer_size = self._recommend_buffer_size(analysis)
        
        return QualityRecommendation(
            recommended_bitrate=recommended,
            buffer_size=buffer_size,
            reason=reason,
            confidence=confidence
        )
    
    def _predict_trend(self) -> str:
        """التنبؤ باتجاه الجودة"""
        if len(self.history) < 5:
            return 'stable'
        
        recent = self.history[-5:]
        older = self.history[-10:-5] if len(self.history) >= 10 else self.history[:5]
        
        avg_recent = sum(q.buffer_health for q in recent) / len(recent)
        avg_older = sum(q.buffer_health for q in older) / len(older)
        
        diff = avg_recent - avg_older
        
        if diff < -0.1:
            return 'degrading'
        elif diff > 0.1:
            return 'improving'
        else:
            return 'stable'
    
    def _recommend_buffer_size(self, analysis: Dict) -> int:
        """التوصية بحجم المخزن المؤقت (بالثواني)"""
        if analysis['status'] == 'excellent':
            return 3  # مخزن صغير للكشف السريع
        elif analysis['status'] == 'good':
            return 5
        elif analysis['status'] == 'fair':
            return 8
        else:
            return 15  # مخزن كبير للاستقرار
    
    async def auto_optimize(
        self,
        callback=None,
        check_interval: float = 5.0
    ):
        """
        التحسين التلقائي المستمر
        
        Args:
            callback: دالة لاستدعاء عند تغيير الجودة
            check_interval: الفاصل بين الفحوصات (ثواني)
        """
        logger.info("بدء التحسين التلقائي للجودة")
        
        while True:
            try:
                recommendation = self.recommend_quality()
                
                if callback:
                    await callback(recommendation)
                
                await asyncio.sleep(check_interval)
            
            except Exception as e:
                logger.error(f"خطأ في التحسين التلقائي: {e}")
                await asyncio.sleep(check_interval * 2)
    
    def get_optimal_url(
        self,
        base_url: str,
        available_bitrates: List[int]
    ) -> str:
        """
        الحصول على رابط البث الأمثل
        
        Args:
            base_url: الرابط الأساسي
            available_bitrates: السرعات المتاحة
        
        Returns:
            الرابط الأمثل
        """
        recommendation = self.recommend_quality()
        target = recommendation.recommended_bitrate
        
        # العثور على أقرب سرعة متاحة
        closest = min(available_bitrates, key=lambda x: abs(x - target))
        
        # تعديل الرابط
        if '{bitrate}' in base_url:
            return base_url.format(bitrate=closest)
        elif '?' in base_url:
            return f"{base_url}&bitrate={closest}"
        else:
            return f"{base_url}?bitrate={closest}"
    
    def export_stats(self) -> Dict:
        """تصدير إحصائيات الجودة"""
        if not self.history:
            return {}
        
        bitrates = [q.bitrate for q in self.history]
        buffers = [q.buffer_health for q in self.history]
        latencies = [q.latency_ms for q in self.history]
        
        return {
            'samples': len(self.history),
            'avg_bitrate': sum(bitrates) / len(bitrates),
            'avg_buffer': sum(buffers) / len(buffers),
            'avg_latency': sum(latencies) / len(latencies),
            'min_bitrate': min(bitrates),
            'max_bitrate': max(bitrates),
            'current_status': self.analyze_connection(),
        }


# مثال للاستخدام
if __name__ == "__main__":
    optimizer = QualityOptimizerAI()
    
    # محاكاة بيانات جودة
    optimizer.update_quality_metrics(
        bitrate=192,
        buffer_health=0.85,
        latency_ms=120,
        packet_loss=0.01,
        bandwidth_available=500
    )
    
    # تحليل الاتصال
    analysis = optimizer.analyze_connection()
    print(f"حالة الاتصال: {analysis['status']} (نتيجة: {analysis['score']})")
    
    # الحصول على توصية
    rec = optimizer.recommend_quality()
    print(f"\nالتوصية:")
    print(f"  السرعة: {rec.recommended_bitrate} kbps")
    print(f"  المخزن: {rec.buffer_size} ثواني")
    print(f"  السبب: {rec.reason}")
    print(f"  الثقة: {rec.confidence:.0%}")
