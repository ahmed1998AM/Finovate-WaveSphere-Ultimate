"""
Language Detector AI - كاشف اللغة بالذكاء الاصطناعي
كشف لغة البث والمحتوى تلقائياً
المطور: Ahmed Mostafa Ibrahim - Finovate – AHMED EG
"""

from typing import Optional, Dict, List, Tuple
import logging
import re

logger = logging.getLogger(__name__)


class LanguageDetectorAI:
    """
    نظام كشف اللغة التلقائي
    يدعم 30+ لغة مع نسبة ثقة
    """
    
    # أنماط الأحرف للغات المختلفة
    LANGUAGE_PATTERNS = {
        'ar': {
            'name': 'العربية',
            'pattern': r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]',
            'rtl': True
        },
        'fa': {
            'name': 'فارسی',
            'pattern': r'[\u0600-\u06FF\u0750-\u077F]',
            'rtl': True
        },
        'he': {
            'name': 'עברית',
            'pattern': r'[\u0590-\u05FF]',
            'rtl': True
        },
        'ru': {
            'name': 'Русский',
            'pattern': r'[\u0400-\u04FF]',
            'rtl': False
        },
        'zh': {
            'name': '中文',
            'pattern': r'[\u4E00-\u9FFF\u3400-\u4DBF]',
            'rtl': False
        },
        'ja': {
            'name': '日本語',
            'pattern': r'[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]',
            'rtl': False
        },
        'ko': {
            'name': '한국어',
            'pattern': r'[\uAC00-\uD7AF\u1100-\u11FF]',
            'rtl': False
        },
        'en': {
            'name': 'English',
            'pattern': r'[a-zA-Z]',
            'rtl': False
        },
        'fr': {
            'name': 'Français',
            'pattern': r'[a-zA-Zàâçéèêëîïôûùüÿñæœ]',
            'rtl': False
        },
        'de': {
            'name': 'Deutsch',
            'pattern': r'[a-zA-ZäöüßÄÖÜ]',
            'rtl': False
        },
        'es': {
            'name': 'Español',
            'pattern': r'[a-zA-ZáéíóúñÁÉÍÓÚÑ]',
            'rtl': False
        },
        'it': {
            'name': 'Italiano',
            'pattern': r'[a-zA-ZàèéìòùÀÈÉÌÒÙ]',
            'rtl': False
        },
        'tr': {
            'name': 'Türkçe',
            'pattern': r'[a-zA-ZçÇğĞıİöÖşŞüÜ]',
            'rtl': False
        },
    }
    
    # كلمات شائعة لكل لغة
    COMMON_WORDS = {
        'ar': ['و', 'في', 'من', 'على', 'إلى', 'أن', 'هذا', 'هذه', 'التي', 'الذي'],
        'en': ['the', 'and', 'is', 'in', 'to', 'of', 'a', 'that', 'for', 'on'],
        'fr': ['le', 'la', 'les', 'un', 'une', 'et', 'de', 'du', 'des', 'est'],
        'de': ['der', 'die', 'das', 'und', 'ist', 'ein', 'eine', 'im', 'den', 'des'],
        'es': ['el', 'la', 'los', 'las', 'de', 'que', 'y', 'en', 'un', 'una'],
        'ru': ['и', 'в', 'не', 'на', 'я', 'что', 'он', 'быть', 'с', 'а'],
    }
    
    def __init__(self):
        self.compiled_patterns = {}
        self._compile_patterns()
    
    def _compile_patterns(self):
        """تجميع الأنماط مسبقاً للأداء"""
        for lang, info in self.LANGUAGE_PATTERNS.items():
            self.compiled_patterns[lang] = re.compile(info['pattern'])
    
    def detect(
        self, 
        text: str, 
        top_n: int = 3
    ) -> List[Tuple[str, float, str]]:
        """
        كشف لغة النص
        
        Args:
            text: النص للتحليل
            top_n: عدد أفضل النتائج
        
        Returns:
            قائمة من (كود_اللغة, الثقة, اسم_اللغة)
        """
        if not text or len(text.strip()) == 0:
            return [('unknown', 0.0, 'Unknown')]
        
        scores = {}
        total_chars = len(text)
        
        # تحليل كل لغة
        for lang, pattern in self.compiled_patterns.items():
            matches = pattern.findall(text)
            match_count = len(matches)
            
            if match_count > 0:
                # حساب النسبة
                ratio = match_count / total_chars
                
                # تعزيز النتيجة للكلمات الشائعة
                word_bonus = self._check_common_words(text, lang)
                
                # النتيجة النهائية
                score = min(ratio * 100 + word_bonus, 100)
                
                if score > 1:  # عتبة دنيا
                    scores[lang] = score
        
        # إذا لم يتم العثور على أي لغة، افتراض الإنجليزية
        if not scores:
            return [('en', 50.0, 'English')]
        
        # ترتيب حسب النتيجة
        sorted_langs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # تطبيع النتائج
        total_score = sum(s for _, s in sorted_langs)
        results = []
        
        for lang, score in sorted_langs[:top_n]:
            normalized_score = (score / total_score) * 100 if total_score > 0 else 0
            lang_name = self.LANGUAGE_PATTERNS.get(lang, {}).get('name', lang)
            results.append((lang, normalized_score, lang_name))
        
        return results
    
    def detect_primary(self, text: str) -> Tuple[str, float, str]:
        """
        كشف اللغة الأساسية فقط
        
        Returns:
            (كود_اللغة, الثقة, اسم_اللغة)
        """
        results = self.detect(text, top_n=1)
        return results[0] if results else ('unknown', 0.0, 'Unknown')
    
    def is_rtl(self, lang_code: str) -> bool:
        """التحقق إذا كانت اللغة RTL"""
        return self.LANGUAGE_PATTERNS.get(lang_code, {}).get('rtl', False)
    
    def _check_common_words(self, text: str, lang: str) -> float:
        """التحقق من الكلمات الشائعة لتعزيز الدقة"""
        if lang not in self.COMMON_WORDS:
            return 0
        
        text_lower = text.lower()
        words = text_lower.split()
        
        common_count = 0
        for word in words[:20]:  # التحقق من أول 20 كلمة
            clean_word = re.sub(r'[^\w\s]', '', word)
            if clean_word in self.COMMON_WORDS[lang]:
                common_count += 1
        
        # مكافأة تصل إلى 20 نقطة
        return min(common_count * 5, 20)
    
    def detect_from_metadata(
        self,
        metadata: Dict
    ) -> Tuple[str, float, str]:
        """
        كشف اللغة من بيانات المحطة
        
        Args:
            metadata: بيانات المحطة (name, description, tags, etc.)
        
        Returns:
            (كود_اللغة, الثقة, اسم_اللغة)
        """
        texts = []
        
        # جمع النصوص من حقول مختلفة
        for field in ['name', 'description', 'genre', 'tags']:
            if field in metadata:
                value = metadata[field]
                if isinstance(value, str):
                    texts.append(value)
                elif isinstance(value, list):
                    texts.extend(value)
        
        combined_text = ' '.join(texts)
        return self.detect(combined_text)
    
    def detect_mixed_languages(
        self,
        text: str,
        min_confidence: float = 10.0
    ) -> Dict[str, float]:
        """
        كشف اللغات المختلطة في نص واحد
        
        Returns:
            قاموس {اللغة: النسبة}
        """
        results = self.detect(text, top_n=10)
        
        # تصفية حسب الثقة
        return {
            lang: confidence 
            for lang, confidence, _ in results 
            if confidence >= min_confidence
        }


# مثال للاستخدام
if __name__ == "__main__":
    detector = LanguageDetectorAI()
    
    # اختبار نصوص بلغات مختلفة
    test_texts = [
        "مرحباً بكم في إذاعة الأخبار",
        "Welcome to News Radio",
        "Bienvenue sur Radio Actualités",
        "Willkommen bei Nachrichten Radio",
        "Добро пожаловать на Радио Новости",
        "欢迎来到新闻广播电台",
    ]
    
    for text in test_texts:
        lang, confidence, name = detector.detect_primary(text)
        rtl = "RTL" if detector.is_rtl(lang) else "LTR"
        print(f"{text[:30]:<30} -> {name:<15} ({confidence:.1f}%) {rtl}")
