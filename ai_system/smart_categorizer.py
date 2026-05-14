"""
Smart Categorizer AI - المصنف الذكي للمحطات
تصنيف المحطات تلقائياً باستخدام الذكاء الاصطناعي
المطور: Ahmed Mostafa Ibrahim - Finovate – AHMED EG
"""

from typing import List, Dict, Optional, Set, Tuple
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class SmartCategorizerAI:
    """
    نظام التصنيف الذكي للمحطات
    يصنف المحطات بناءً على المحتوى والبيانات الوصفية
    """
    
    # تصنيفات رئيسية
    MAIN_CATEGORIES = {
        'News': ['news', 'أخبار', 'actualités', 'nachrichten', 'noticias'],
        'Music': ['music', 'موسيقى', 'musique', 'musik', 'música'],
        'Sports': ['sports', 'رياضة', 'sport', 'deportes'],
        'Talk': ['talk', 'حوار', 'discussion', 'talkshow'],
        'Islamic': ['islamic', 'إسلامي', 'islam', 'muslim'],
        'Quran': ['quran', 'قرآن', 'coran', 'koran'],
        'Educational': ['educational', 'تعليمي', 'éducation', 'bildung'],
        'Entertainment': ['entertainment', 'ترفيه', 'divertissement'],
        'Technology': ['technology', 'تكنولوجيا', 'tech', 'technologie'],
        'Culture': ['culture', 'ثقافة', 'kultur', 'cultura'],
        'Kids': ['kids', 'أطفال', 'enfants', 'kinder'],
        'Religious': ['religious', 'ديني', 'religion', 'religieux'],
        'Classical': ['classical', 'كلاسيكي', 'classique', 'klassik'],
        'Pop': ['pop', 'بوب', 'populaire'],
        'Rock': ['rock', 'روك'],
        'Jazz': ['jazz', 'جاز'],
        'Electronic': ['electronic', 'إلكتروني', 'elektronik', 'edm'],
        'Country': ['country', 'كانتري'],
        'HipHop': ['hip hop', 'هيب هوب', 'rap'],
        'Oldies': ['oldies', 'قديم', 'vintage', 'retro'],
        'Chill': ['chill', 'هادئ', 'relax', 'lounge'],
        'Gaming': ['gaming', 'ألعاب', 'jeux', 'spiele'],
        'Podcast': ['podcast', 'بودكاست'],
        'Community': ['community', 'مجتمع', 'communauté'],
        'Public': ['public', 'عام', 'public radio'],
        'College': ['college', 'جامعة', 'university', 'campus'],
    }
    
    # كلمات دلالية لكل تصنيف
    KEYWORDS = {
        'News': ['breaking', 'عاجل', 'headline', 'bulletin', 'report'],
        'Music': ['song', 'أغنية', 'hit', 'track', 'album'],
        'Sports': ['match', 'مباراة', 'game', 'score', 'goal'],
        'Islamic': ['prayer', 'صلاة', 'allah', 'islam', 'مسجد'],
        'Quran': ['recitation', 'تلاوة', 'surah', 'ayah', 'قارئ'],
        'Technology': ['tech', 'digital', 'software', 'hardware', 'برمجة'],
        'Education': ['learn', 'تعلم', 'study', 'course', 'درس'],
    }
    
    def __init__(self):
        self.category_cache: Dict[str, str] = {}
        self.confidence_threshold = 0.5
    
    def categorize(
        self,
        station_data: Dict
    ) -> Tuple[str, float, List[str]]:
        """
        تصنيف محطة راديو
        
        Args:
            station_data: بيانات المحطة
        
        Returns:
            (التصنيف الرئيسي, الثقة, قائمة التصنيفات الفرعية)
        """
        station_id = station_data.get('id', 'unknown')
        
        # التحقق من الكاش
        if station_id in self.category_cache:
            cached = self.category_cache[station_id]
            return (cached, 1.0, [cached])
        
        # جمع النصوص للتحليل
        texts = self._extract_texts(station_data)
        
        # حساب درجات التصنيفات
        scores = self._calculate_category_scores(texts)
        
        if not scores:
            return ('Uncategorized', 0.0, [])
        
        # الحصول على أفضل تصنيف
        best_category = max(scores.items(), key=lambda x: x[1])
        category_name = best_category[0]
        confidence = min(best_category[1] / 100, 1.0)
        
        # الحصول على تصنيفات أخرى ذات صلة
        sub_categories = [
            cat for cat, score in scores.items()
            if score > confidence * 50 and cat != category_name
        ][:3]
        
        # حفظ في الكاش
        self.category_cache[station_id] = category_name
        
        return (category_name, confidence, sub_categories)
    
    def _extract_texts(self, data: Dict) -> List[str]:
        """استخراج النصوص من بيانات المحطة"""
        texts = []
        
        for field in ['name', 'description', 'genre', 'tags', 'country', 'language']:
            if field in data:
                value = data[field]
                if isinstance(value, str):
                    texts.append(value.lower())
                elif isinstance(value, list):
                    texts.extend([t.lower() for t in value])
        
        return texts
    
    def _calculate_category_scores(
        self,
        texts: List[str]
    ) -> Dict[str, float]:
        """حساب درجات جميع التصنيفات"""
        scores = defaultdict(float)
        combined_text = ' '.join(texts)
        
        for category, keywords in self.MAIN_CATEGORIES.items():
            score = 0
            
            for keyword in keywords:
                keyword_lower = keyword.lower()
                
                # البحث عن الكلمة في النصوص
                count = combined_text.count(keyword_lower)
                if count > 0:
                    # زيادة الدرجة حسب عدد الظهور
                    score += count * 10
                
                # بحث جزئي للكلمات الطويلة
                if len(keyword) > 4:
                    for text in texts:
                        if keyword_lower in text:
                            score += 5
            
            # تعزيز من الكلمات الدلالية
            if category in self.KEYWORDS:
                for keyword in self.KEYWORDS[category]:
                    if keyword.lower() in combined_text:
                        score += 15
            
            if score > 0:
                scores[category] = score
        
        return dict(scores)
    
    def categorize_batch(
        self,
        stations: List[Dict],
        progress_callback=None
    ) -> Dict[str, Tuple[str, float, List[str]]]:
        """
        تصنيف مجموعة من المحطات
        
        Args:
            stations: قائمة المحطات
            progress_callback: دالة لاستدعاء التقدم
        
        Returns:
            قاموس {station_id: (category, confidence, sub_categories)}
        """
        results = {}
        total = len(stations)
        
        for i, station in enumerate(stations):
            result = self.categorize(station)
            station_id = station.get('id', f'station_{i}')
            results[station_id] = result
            
            if progress_callback and i % 100 == 0:
                progress_callback(i, total)
        
        return results
    
    def get_station_categories(
        self,
        stations: List[Dict],
        category: str
    ) -> List[Dict]:
        """الحصول على جميع المحطات في تصنيف معين"""
        matching = []
        
        for station in stations:
            cat, _, _ = self.categorize(station)
            if cat.lower() == category.lower():
                matching.append(station)
        
        return matching
    
    def get_all_categories(self) -> List[str]:
        """الحصول على قائمة جميع التصنيفات المتاحة"""
        return list(self.MAIN_CATEGORIES.keys())
    
    def add_custom_category(
        self,
        name: str,
        keywords: List[str]
    ):
        """إضافة تصنيف مخصص"""
        self.MAIN_CATEGORIES[name] = keywords
        logger.info(f"تم إضافة تصنيف مخصص: {name}")
    
    def remove_category(self, name: str):
        """إزالة تصنيف"""
        if name in self.MAIN_CATEGORIES:
            del self.MAIN_CATEGORIES[name]
            logger.info(f"تم إزالة التصنيف: {name}")
    
    def clear_cache(self):
        """مسح ذاكرة التخزين المؤقت"""
        self.category_cache.clear()
        logger.info("تم مسح كاش التصنيفات")
    
    def get_category_stats(
        self,
        stations: List[Dict]
    ) -> Dict[str, int]:
        """
        إحصائيات التصنيفات
        
        Returns:
            قاموس {category: count}
        """
        stats = defaultdict(int)
        
        for station in stations:
            category, _, _ = self.categorize(station)
            stats[category] += 1
        
        return dict(stats)


# مثال للاستخدام
if __name__ == "__main__":
    categorizer = SmartCategorizerAI()
    
    # اختبار تصنيف محطات
    test_stations = [
        {'id': '1', 'name': 'Nile FM News', 'genre': 'News', 'tags': ['egypt', 'breaking']},
        {'id': '2', 'name': 'Quran Radio Makkah', 'genre': 'Religious', 'tags': ['quran', 'islam']},
        {'id': '3', 'name': 'Radio Hits FM', 'genre': 'Music', 'tags': ['pop', 'hits']},
        {'id': '4', 'name': 'Sports Talk Radio', 'genre': 'Sports', 'tags': ['football', 'match']},
        {'id': '5', 'name': 'Tech Today', 'genre': 'Technology', 'tags': ['tech', 'digital']},
    ]
    
    print("نتائج التصنيف:")
    for station in test_stations:
        category, confidence, sub_cats = categorizer.categorize(station)
        print(f"  {station['name']}: {category} ({confidence:.0%})")
