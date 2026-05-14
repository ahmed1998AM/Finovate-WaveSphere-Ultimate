"""
Metadata Translator AI - مترجم البيانات الوصفية بالذكاء الاصطناعي
ترجمة أسماء المحطات والأغاني والمعلومات إلى لغات متعددة
المطور: Ahmed Mostafa Ibrahim - Finovate – AHMED EG
"""

from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class MetadataTranslatorAI:
    """
    نظام ترجمة البيانات الوصفية
    يدعم 9 لغات مع دعم RTL للعربية
    """
    
    SUPPORTED_LANGUAGES = [
        'ar',  # العربية
        'en',  # English
        'fr',  # Français
        'de',  # Deutsch
        'es',  # Español
        'ru',  # Русский
        'tr',  # Türkçe
        'it',  # Italiano
        'zh',  # 中文
    ]
    
    RTL_LANGUAGES = ['ar']
    
    def __init__(self):
        self.target_language = 'ar'
        self.cache: Dict[str, str] = {}
        self.model_loaded = False
    
    def set_target_language(self, lang_code: str):
        """تعيين اللغة المستهدفة"""
        if lang_code in self.SUPPORTED_LANGUAGES:
            self.target_language = lang_code
            logger.info(f"تم تعيين اللغة إلى {lang_code}")
        else:
            logger.warning(f"اللغة {lang_code} غير مدعومة")
    
    def is_rtl(self) -> bool:
        """التحقق إذا كانت اللغة من اليمين لليسار"""
        return self.target_language in self.RTL_LANGUAGES
    
    def translate(
        self,
        text: str,
        source_lang: Optional[str] = None,
        target_lang: Optional[str] = None
    ) -> str:
        """
        ترجمة نص
        
        Args:
            text: النص المراد ترجمته
            source_lang: اللغة المصدر (اختياري للكشف التلقائي)
            target_lang: اللغة المستهدفة (اختياري)
        
        Returns:
            النص المترجم
        """
        target = target_lang or self.target_language
        
        # التحقق من الكاش
        cache_key = f"{text}:{target}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # إذا لم يكن النموذج محملاً، نستخدم قاموس بسيط
        if not self.model_loaded:
            translated = self._simple_translate(text, target)
        else:
            translated = self._ai_translate(text, source_lang, target)
        
        # حفظ في الكاش
        self.cache[cache_key] = translated
        return translated
    
    def _simple_translate(self, text: str, target: str) -> str:
        """ترجمة بسيطة باستخدام قاموس محدود"""
        # قاموس بسيط للأمثلة الشائعة
        dictionary = {
            'ar': {
                'News': 'أخبار',
                'Music': 'موسيقى',
                'Sports': 'رياضة',
                'Talk': 'حوار',
                'Live': 'مباشر',
                'Classic': 'كلاسيكي',
                'Pop': 'بوب',
                'Rock': 'روك',
                'Jazz': 'جاز',
                'Islamic': 'إسلامي',
                'Quran': 'قرآن',
            },
            'en': {
                'أخبار': 'News',
                'موسيقى': 'Music',
                'رياضة': 'Sports',
            }
        }
        
        if target in dictionary:
            for key, value in dictionary[target].items():
                if key.lower() in text.lower():
                    text = text.replace(key, value)
        
        return text
    
    def _ai_translate(
        self,
        text: str,
        source_lang: Optional[str],
        target: str
    ) -> str:
        """ترجمة باستخدام الذكاء الاصطناعي"""
        try:
            # يمكن استخدام:
            # - Google Translate API
            # - DeepL API
            # - نموذج Transformers (mBART, M2M100)
            
            # مثال باستخدام transformers (إذا كان متاحاً)
            try:
                from transformers import pipeline
                
                if not hasattr(self, '_translator'):
                    self._translator = pipeline(
                        "translation",
                        model="facebook/mbart-large-50-many-to-many-mmt"
                    )
                
                result = self._translator(
                    text,
                    src_lang=source_lang or "en_XX",
                    tgt_lang=f"{target}_XX"
                )
                return result[0]['translation_text']
            except ImportError:
                logger.warning("transformers غير مثبت، استخدام الترجمة البسيطة")
                return self._simple_translate(text, target)
        
        except Exception as e:
            logger.error(f"خطأ في الترجمة: {e}")
            return text
    
    def translate_metadata(self, metadata: Dict) -> Dict:
        """
        ترجمة بيانات وصفية كاملة
        
        Args:
            metadata: قاموس يحتوي على بيانات المحطة/الأغنية
        
        Returns:
            بيانات مترجمة
        """
        translated = metadata.copy()
        
        # حقول قابلة للترجمة
        translatable_fields = [
            'name',
            'title',
            'artist',
            'album',
            'description',
            'genre',
            'tags'
        ]
        
        for field in translatable_fields:
            if field in translated:
                if isinstance(translated[field], str):
                    translated[field] = self.translate(translated[field])
                elif isinstance(translated[field], list):
                    translated[field] = [
                        self.translate(item) 
                        for item in translated[field]
                    ]
        
        # إضافة معلومات اللغة
        translated['language'] = self.target_language
        translated['is_rtl'] = self.is_rtl()
        
        return translated
    
    def detect_language(self, text: str) -> str:
        """
        كشف لغة النص تلقائياً
        
        Args:
            text: النص للكشف
        
        Returns:
            كود اللغة
        """
        # كشف بسيط بناءً على الأحرف
        arabic_chars = any('\u0600' <= c <= '\u06FF' for c in text)
        cyrillic_chars = any('\u0400' <= c <= '\u04FF' for c in text)
        chinese_chars = any('\u4E00' <= c <= '\u9FFF' for c in text)
        
        if arabic_chars:
            return 'ar'
        elif cyrillic_chars:
            return 'ru'
        elif chinese_chars:
            return 'zh'
        else:
            return 'en'  # افتراضي
    
    def clear_cache(self):
        """مسح ذاكرة التخزين المؤقت"""
        self.cache.clear()
        logger.info("تم مسح كاش الترجمة")


# مثال للاستخدام
if __name__ == "__main__":
    translator = MetadataTranslatorAI()
    
    # اختبار الترجمة
    text = "News Radio - Live Music"
    translated = translator.translate(text, target_lang='ar')
    print(f"الأصلي: {text}")
    print(f"مترجم: {translated}")
    
    # اختبار RTL
    translator.set_target_language('ar')
    print(f"RTL: {translator.is_rtl()}")
