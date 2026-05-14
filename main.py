#!/usr/bin/env python3
"""
Finovate WaveSphere Ultimate - Main Entry Point
نقطة الدخول الرئيسية للتطبيق
المطور: Ahmed Mostafa Ibrahim - Finovate – AHMED EG
"""

import sys
import asyncio
import logging
from pathlib import Path

# إعداد السجلات
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('wavesphere.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


def check_dependencies():
    """التحقق من المكتبات المطلوبة"""
    required = [
        'pyside6',
        'numpy',
        'scipy',
        'aiohttp',
        'requests'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        logger.warning(f"بعض المكتبات غير مثبتة: {missing}")
        logger.info("قم بتثبيتها باستخدام: pip install " + " ".join(missing))
        return False
    
    return True


async def run_demo():
    """تشغيل عرض توضيحي"""
    from radio_sources import RadioAggregator
    from ai_system import (
        AudioEnhancerAI,
        StationRecommenderAI,
        MetadataTranslatorAI,
        LanguageDetectorAI,
        SmartCategorizerAI,
        QualityOptimizerAI
    )
    
    print("\n" + "="*60)
    print("🌊 Finovate WaveSphere Ultimate - عرض توضيحي")
    print("="*60 + "\n")
    
    # 1. تجميع المحطات
    print("📻 جاري تجميع مصادر الراديو...")
    async with RadioAggregator() as aggregator:
        stations = await aggregator.get_top_stations(limit=5)
        print(f"   تم الحصول على {len(stations)} محطة علوية\n")
        
        for i, station in enumerate(stations, 1):
            print(f"   {i}. {station.name} - {station.country}")
    
    print("\n" + "-"*60 + "\n")
    
    # 2. نظام التوصية
    print("🤖 نظام التوصية الذكي...")
    recommender = StationRecommenderAI()
    recommender.set_user_preferences(
        favorite_genres={"News", "Islamic", "Arabic"},
        favorite_countries={"Egypt", "Saudi Arabia"},
        favorite_languages={"Arabic", "English"}
    )
    print("   تم إعداد التفضيلات بنجاح ✓\n")
    
    # 3. تحسين الصوت
    print("🎵 تحسين الصوت بالذكاء الاصطناعي...")
    enhancer = AudioEnhancerAI()
    enhancer.load_model()
    print("   تم تحميل نموذج تحسين الصوت ✓\n")
    
    # 4. الترجمة
    print("🌐 نظام الترجمة...")
    translator = MetadataTranslatorAI()
    translator.set_target_language('ar')
    translated = translator.translate("News Radio")
    print(f"   'News Radio' → '{translated}' ✓\n")
    
    # 5. كشف اللغة
    print("🔍 كاشف اللغة...")
    detector = LanguageDetectorAI()
    lang, conf, name = detector.detect_primary("مرحباً بكم في إذاعة الأخبار")
    print(f"   اللغة: {name} ({conf:.1f}%) ✓\n")
    
    # 6. التصنيف الذكي
    print("📂 المصنف الذكي...")
    categorizer = SmartCategorizerAI()
    test_station = {
        'id': 'test_1',
        'name': 'Nile FM News',
        'genre': 'News',
        'tags': ['egypt', 'breaking', 'arabic']
    }
    category, confidence, subcats = categorizer.categorize(test_station)
    print(f"   التصنيف: {category} ({confidence:.0%}) ✓\n")
    
    # 7. تحسين الجودة
    print("⚡ محسن الجودة...")
    optimizer = QualityOptimizerAI()
    optimizer.update_quality_metrics(
        bitrate=192,
        buffer_health=0.85,
        latency_ms=120,
        bandwidth_available=500
    )
    rec = optimizer.recommend_quality()
    print(f"   السرعة الموصى بها: {rec.recommended_bitrate} kbps ✓\n")
    
    print("="*60)
    print("✅ اكتمل العرض التوضيحي بنجاح!")
    print("="*60 + "\n")


def main():
    """الدالة الرئيسية"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     🌊 Finovate WaveSphere Ultimate v1.0.0              ║")
    print("║     اسمع العالم بلا حدود                                ║")
    print("║     المطور: Ahmed Mostafa Ibrahim                       ║")
    print("║     Finovate – AHMED EG                                 ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print("\n")
    
    # التحقق من المتطلبات
    if not check_dependencies():
        logger.info("جاري المتابعة مع المكتبات المتاحة...")
    
    # تشغيل العرض التوضيحي
    try:
        asyncio.run(run_demo())
    except KeyboardInterrupt:
        print("\n\nتم إيقاف البرنامج بواسطة المستخدم")
        sys.exit(0)
    except Exception as e:
        logger.error(f"حدث خطأ: {e}")
        sys.exit(1)
    
    print("🎉 شكراً لاستخدامكم WaveSphere!")
    print("© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved\n")


if __name__ == "__main__":
    main()
