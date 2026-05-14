"""
Station Recommender AI - نظام توصية المحطات الذكي
يستخدم التعلم الآلي لتوصية المحطات المناسبة للمستخدم
المطور: Ahmed Mostafa Ibrahim - Finovate – AHMED EG
"""

import numpy as np
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from collections import defaultdict
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


@dataclass
class UserPreference:
    """تفضيلات المستخدم"""
    favorite_genres: Set[str]
    favorite_countries: Set[str]
    favorite_languages: Set[str]
    listening_history: List[str]  # station IDs
    skip_rate: Dict[str, float]  # genre -> skip rate
    avg_listening_duration: float  # بالدقائق
    preferred_bitrate_min: int
    listening_time_pattern: Dict[int, float]  # hour -> activity level


@dataclass
class StationScore:
    """نتيجة تقييم المحطة"""
    station_id: str
    score: float
    reasons: List[str]


class StationRecommenderAI:
    """
    نظام توصية المحطات بالذكاء الاصطناعي
    يستخدم خوارزميات تصفية تعاونية ومحتوية
    """
    
    def __init__(self):
        self.user_preferences: Optional[UserPreference] = None
        self.station_features: Dict[str, Dict] = {}
        self.listening_history: List[Dict] = []
        self.genre_popularity: Dict[str, int] = defaultdict(int)
        self.country_popularity: Dict[str, int] = defaultdict(int)
        
        # أوزان عوامل التقييم
        self.weights = {
            'genre_match': 0.30,
            'country_match': 0.15,
            'language_match': 0.10,
            'popularity': 0.15,
            'quality': 0.10,
            'diversity': 0.10,
            'recency': 0.10
        }
    
    def set_user_preferences(
        self,
        favorite_genres: Set[str] = None,
        favorite_countries: Set[str] = None,
        favorite_languages: Set[str] = None,
        preferred_bitrate_min: int = 64
    ):
        """إعداد تفضيلات المستخدم"""
        self.user_preferences = UserPreference(
            favorite_genres=favorite_genres or set(),
            favorite_countries=favorite_countries or set(),
            favorite_languages=favorite_languages or set(),
            listening_history=[],
            skip_rate={},
            avg_listening_duration=0,
            preferred_bitrate_min=preferred_bitrate_min,
            listening_time_pattern={}
        )
    
    def add_station_feature(self, station_id: str, features: Dict):
        """إضافة خصائص محطة للتقييم"""
        self.station_features[station_id] = {
            'genre': features.get('genre', ''),
            'country': features.get('country', ''),
            'language': features.get('language', ''),
            'bitrate': features.get('bitrate', 0),
            'listeners': features.get('listeners', 0),
            'tags': features.get('tags', []),
            'added_date': features.get('added_date', datetime.now())
        }
    
    def record_listening(
        self,
        station_id: str,
        duration_seconds: int,
        completed: bool = False
    ):
        """تسجيل جلسة استماع"""
        session = {
            'station_id': station_id,
            'duration': duration_seconds,
            'completed': completed,
            'timestamp': datetime.now()
        }
        self.listening_history.append(session)
        
        if self.user_preferences:
            self.user_preferences.listening_history.append(station_id)
            
            # تحديث نمط الاستماع
            hour = session['timestamp'].hour
            if hour not in self.user_preferences.listening_time_pattern:
                self.user_preferences.listening_time_pattern[hour] = 0
            self.user_preferences.listening_time_pattern[hour] += 1
        
        # تحديث شعبية النوع والدولة
        if station_id in self.station_features:
            features = self.station_features[station_id]
            if features['genre']:
                self.genre_popularity[features['genre']] += 1
            if features['country']:
                self.country_popularity[features['country']] += 1
    
    def record_skip(self, station_id: str, genre: str):
        """تسجيل تخطي محطة"""
        if self.user_preferences:
            if genre not in self.user_preferences.skip_rate:
                self.user_preferences.skip_rate[genre] = 0
            self.user_preferences.skip_rate[genre] += 1
    
    def recommend_stations(
        self,
        all_stations: List[Dict],
        limit: int = 20,
        exclude_recent: bool = True
    ) -> List[StationScore]:
        """
        توصية محطات للمستخدم
        
        Args:
            all_stations: قائمة جميع المحطات المتاحة
            limit: عدد التوصيات
            exclude_recent: استبعاد المحطات التي سُمعت مؤخراً
        
        Returns:
            قائمة المحطات الموصى بها مع النتائج
        """
        if not self.user_preferences:
            # إذا لم تكن هناك تفضيلات، نعود للأكثر شعبية
            return self._recommend_by_popularity(all_stations, limit)
        
        # حساب النتيجة لكل محطة
        scored_stations = []
        recent_ids = self._get_recent_stations(hours=24) if exclude_recent else set()
        
        for station in all_stations:
            station_id = station.get('id', '')
            
            # استبعاد المحطات الحديثة
            if exclude_recent and station_id in recent_ids:
                continue
            
            score = self._calculate_station_score(station)
            scored_stations.append(score)
        
        # ترتيب حسب النتيجة
        scored_stations.sort(key=lambda s: s.score, reverse=True)
        
        # إضافة تنوع في النتائج
        return self._add_diversity(scored_stations[:limit * 2])[:limit]
    
    def _calculate_station_score(self, station: Dict) -> StationScore:
        """حساب نتيجة محطة واحدة"""
        station_id = station.get('id', '')
        reasons = []
        total_score = 0.0
        
        prefs = self.user_preferences
        
        # تطابق النوع (30%)
        genre = station.get('genre', '')
        tags = station.get('tags', [])
        genre_score = 0
        
        if genre in prefs.favorite_genres:
            genre_score = 1.0
            reasons.append(f"نوع مفضل: {genre}")
        elif any(tag in prefs.favorite_genres for tag in tags):
            genre_score = 0.7
            reasons.append("يتضمن أنواعاً مفضلة")
        
        # التحقق من معدل التخطي
        if genre in prefs.skip_rate:
            skip_penalty = min(prefs.skip_rate[genre] * 0.1, 0.5)
            genre_score *= (1 - skip_penalty)
        
        total_score += genre_score * self.weights['genre_match']
        
        # تطابق الدولة (15%)
        country = station.get('country', '')
        country_score = 0
        
        if country in prefs.favorite_countries:
            country_score = 1.0
            reasons.append(f"دولة مفضلة: {country}")
        elif country in self.country_popularity:
            country_score = 0.5
        
        total_score += country_score * self.weights['country_match']
        
        # تطابق اللغة (10%)
        language = station.get('language', '')
        lang_score = 1.0 if language in prefs.favorite_languages else 0.5
        total_score += lang_score * self.weights['language_match']
        
        # الشعبية (15%)
        listeners = station.get('listeners', 0)
        popularity_score = min(listeners / 10000, 1.0)
        total_score += popularity_score * self.weights['popularity']
        
        # الجودة (10%)
        bitrate = station.get('bitrate', 0)
        quality_score = 0
        if bitrate >= prefs.preferred_bitrate_min:
            quality_score = min(bitrate / 320, 1.0)
        total_score += quality_score * self.weights['quality']
        
        # التنوع (10%)
        diversity_score = self._calculate_diversity_score(station)
        total_score += diversity_score * self.weights['diversity']
        
        # الحداثة (10%)
        recency_score = self._calculate_recency_score(station)
        total_score += recency_score * self.weights['recency']
        
        return StationScore(
            station_id=station_id,
            score=total_score * 100,
            reasons=reasons
        )
    
    def _calculate_diversity_score(self, station: Dict) -> float:
        """حساب درجة التنوع لتشجيع اكتشاف محطات جديدة"""
        genre = station.get('genre', '')
        
        # مكافأة الأنواع غير المستكشفة
        if genre not in self.genre_popularity:
            return 1.0
        
        # معاقبة الأنواع الشائعة جداً
        total = sum(self.genre_popularity.values()) or 1
        frequency = self.genre_popularity[genre] / total
        
        return 1.0 - min(frequency * 2, 0.8)
    
    def _calculate_recency_score(self, station: Dict) -> float:
        """حساب درجة الحداثة"""
        station_id = station.get('id', '')
        
        # البحث في سجل الاستماع
        for session in reversed(self.listening_history[-50:]):
            if session['station_id'] == station_id:
                hours_ago = (datetime.now() - session['timestamp']).total_seconds() / 3600
                # تقليل النتيجة إذا سُمعت مؤخراً
                return max(0, 1.0 - (hours_ago / 24))
        
        return 1.0  # لم تُسمع من قبل
    
    def _get_recent_stations(self, hours: int = 24) -> Set[str]:
        """الحصول على المحطات التي سُمعت مؤخراً"""
        cutoff = datetime.now() - timedelta(hours=hours)
        recent = set()
        
        for session in self.listening_history:
            if session['timestamp'] >= cutoff:
                recent.add(session['station_id'])
        
        return recent
    
    def _recommend_by_popularity(
        self,
        stations: List[Dict],
        limit: int
    ) -> List[StationScore]:
        """التوصية بناءً على الشعبية فقط"""
        scored = []
        
        for station in stations:
            listeners = station.get('listeners', 0)
            score = StationScore(
                station_id=station.get('id', ''),
                score=min(listeners / 100, 100),
                reasons=["شعبية عالية"]
            )
            scored.append(score)
        
        scored.sort(key=lambda s: s.score, reverse=True)
        return scored[:limit]
    
    def _add_diversity(
        self,
        scored_stations: List[StationScore],
        diversity_factor: float = 0.3
    ) -> List[StationScore]:
        """إضافة تنوع في التوصيات"""
        if len(scored_stations) <= 3:
            return scored_stations
        
        result = []
        used_genres = set()
        used_countries = set()
        
        # أخذ أفضل المحطات مع ضمان التنوع
        for station in scored_stations:
            station_data = self.station_features.get(station.station_id, {})
            genre = station_data.get('genre', '')
            country = station_data.get('country', '')
            
            # قبول المحطة إذا كانت متنوعة أو ذات نتيجة عالية
            is_diverse = genre not in used_genres or country not in used_countries
            
            if is_diverse or len(result) < 3:
                result.append(station)
                
                if len(used_genres) < 5:
                    used_genres.add(genre)
                if len(used_countries) < 5:
                    used_countries.add(country)
            
            if len(result) >= len(scored_stations) * diversity_factor:
                break
        
        # إكمال القائمة بأفضل النتائج المتبقية
        remaining = [s for s in scored_stations if s not in result]
        result.extend(remaining[:len(scored_stations) - len(result)])
        
        return result
    
    def get_similar_stations(
        self,
        station_id: str,
        all_stations: List[Dict],
        limit: int = 10
    ) -> List[Dict]:
        """العثور على محطات مشابهة لمحطة معينة"""
        if station_id not in self.station_features:
            return []
        
        target = self.station_features[station_id]
        scored = []
        
        for station in all_stations:
            if station.get('id') == station_id:
                continue
            
            similarity = 0
            
            # تشابه النوع
            if station.get('genre') == target['genre']:
                similarity += 0.5
            
            # تشابه الدولة
            if station.get('country') == target['country']:
                similarity += 0.2
            
            # تشابه اللغة
            if station.get('language') == target['language']:
                similarity += 0.2
            
            # تشابه العلامات
            common_tags = set(station.get('tags', [])) & set(target.get('tags', []))
            similarity += len(common_tags) * 0.05
            
            if similarity > 0:
                scored.append((similarity, station))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s[1] for s in scored[:limit]]


# مثال للاستخدام
if __name__ == "__main__":
    recommender = StationRecommenderAI()
    
    # إعداد التفضيلات
    recommender.set_user_preferences(
        favorite_genres={"News", "Islamic", "Arabic"},
        favorite_countries={"Egypt", "Saudi Arabia"},
        favorite_languages={"Arabic", "English"}
    )
    
    print("نظام التوصية جاهز!")
