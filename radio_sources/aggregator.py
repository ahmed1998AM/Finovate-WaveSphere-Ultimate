"""
Radio Aggregator - مجمع مصادر الراديو
دمج جميع مصادر الراديو في واجهة موحدة
المطور: Ahmed Mostafa Ibrahim - Finovate – AHMED EG
"""

import asyncio
from typing import List, Dict, Optional, Any, Union
from dataclasses import dataclass, field
import logging
from datetime import datetime

from .radio_browser import RadioBrowserAPI, RadioStation as RBStation
from .shoutcast import ShoutcastAPI, ShoutcastStation
from .icecast import IcecastAPI, IcecastStation
from .onlineradiobox import OnlineRadioBoxAPI, OnlineRadioBoxStation
from .mytuner import MyTunerAPI, MyTunerStation

logger = logging.getLogger(__name__)


@dataclass
class UnifiedStation:
    """محطة راديو موحدة من جميع المصادر"""
    id: str
    name: str
    url: str
    stream_url: str
    source: str  # radio_browser, shoutcast, icecast, onlineradiobox, mytuner
    country: str
    genre: str
    language: str
    bitrate: int
    logo: str
    website: str
    description: str
    tags: List[str] = field(default_factory=list)
    listeners: int = 0
    popularity: int = 0
    is_active: bool = True
    last_checked: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class RadioAggregator:
    """
    مجمع مصادر الراديو
    يجمع المحطات من جميع المصادر ويوفر واجهة موحدة
    """
    
    def __init__(self):
        self.radio_browser = RadioBrowserAPI()
        self.shoutcast = ShoutcastAPI()
        self.icecast = IcecastAPI()
        self.onlineradiobox = OnlineRadioBoxAPI()
        self.mytuner = MyTunerAPI()
        
        self._station_cache: Dict[str, UnifiedStation] = {}
        self._favorites: set = set()
        self._history: List[str] = []
    
    async def search_all_sources(
        self,
        query: str,
        country: Optional[str] = None,
        genre: Optional[str] = None,
        language: Optional[str] = None,
        limit: int = 100
    ) -> List[UnifiedStation]:
        """البحث في جميع المصادر одновременно"""
        tasks = []
        
        # Radio Browser
        if country or genre or language:
            tasks.append(self._search_radio_browser(query, country, genre, language, limit))
        else:
            tasks.append(self._search_radio_browser(query, None, None, None, limit))
        
        # Shoutcast
        tasks.append(self._search_shoutcast(query, limit // 4))
        
        # Icecast
        tasks.append(self._search_icecast(query, limit // 4))
        
        # MyTuner
        tasks.append(self._search_mytuner(query, country, genre, limit // 4))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # دمج النتائج وإزالة التكرارات
        all_stations = []
        seen_urls = set()
        
        for result in results:
            if isinstance(result, list):
                for station in result:
                    if station.stream_url not in seen_urls:
                        seen_urls.add(station.stream_url)
                        all_stations.append(station)
        
        # ترتيب حسب الشعبية
        all_stations.sort(key=lambda s: s.popularity, reverse=True)
        
        return all_stations[:limit]
    
    async def _search_radio_browser(
        self,
        query: str,
        country: Optional[str],
        genre: Optional[str],
        language: Optional[str],
        limit: int
    ) -> List[UnifiedStation]:
        """البحث في Radio Browser"""
        try:
            stations = await self.radio_browser.search_stations(
                name=query if query else None,
                country=country,
                tag=genre,
                language=language,
                limit=limit
            )
            
            return [self._convert_rb_station(s) for s in stations]
        except Exception as e:
            logger.error(f"Radio Browser search error: {e}")
            return []
    
    async def _search_shoutcast(
        self,
        query: str,
        limit: int
    ) -> List[UnifiedStation]:
        """البحث في Shoutcast"""
        try:
            stations = await self.shoutcast.search_stations(query, limit=limit)
            
            unified = []
            for s in stations:
                station = UnifiedStation(
                    id=f"sc_{s.id}",
                    name=s.name,
                    url=s.homepage or s.url,
                    stream_url=s.url,
                    source="shoutcast",
                    country=s.country,
                    genre=s.genre,
                    language=s.language,
                    bitrate=s.bitrate,
                    logo="",
                    website=s.homepage,
                    description=s.description,
                    tags=[s.genre] if s.genre else [],
                    listeners=s.listeners,
                    popularity=s.listeners
                )
                unified.append(station)
            
            return unified
        except Exception as e:
            logger.error(f"Shoutcast search error: {e}")
            return []
    
    async def _search_icecast(
        self,
        query: str,
        limit: int
    ) -> List[UnifiedStation]:
        """البحث في Icecast"""
        try:
            stations = await self.icecast.search_stations(query, limit=limit)
            
            unified = []
            for s in stations:
                station = UnifiedStation(
                    id=f"ic_{hash(s.server_name)}",
                    name=s.server_name,
                    url=s.server_url,
                    stream_url=s.listen_url,
                    source="icecast",
                    country=s.country,
                    genre=s.genre,
                    language=s.language,
                    bitrate=s.bitrate,
                    logo=s.server_icon,
                    website=s.server_url,
                    description=s.server_description,
                    tags=[s.genre] if s.genre else [],
                    listeners=s.listeners_current,
                    popularity=s.listeners_current
                )
                unified.append(station)
            
            return unified
        except Exception as e:
            logger.error(f"Icecast search error: {e}")
            return []
    
    async def _search_mytuner(
        self,
        query: str,
        country: Optional[str],
        genre: Optional[str],
        limit: int
    ) -> List[UnifiedStation]:
        """البحث في MyTuner"""
        try:
            stations = await self.mytuner.search_stations(
                query=query,
                country=country,
                genre=genre,
                limit=limit
            )
            
            unified = []
            for s in stations:
                station = UnifiedStation(
                    id=f"mt_{s.id}",
                    name=s.name,
                    url=s.website or s.url,
                    stream_url=s.stream_url,
                    source="mytuner",
                    country=s.country,
                    genre=s.genres[0] if s.genres else "",
                    language=s.language,
                    bitrate=s.bitrate,
                    logo=s.logo,
                    website=s.website,
                    description=s.description,
                    tags=s.tags + s.genres,
                    popularity=s.popularity
                )
                unified.append(station)
            
            return unified
        except Exception as e:
            logger.error(f"MyTuner search error: {e}")
            return []
    
    def _convert_rb_station(self, station: RBStation) -> UnifiedStation:
        """تحويل محطة Radio Browser إلى الصيغة الموحدة"""
        return UnifiedStation(
            id=f"rb_{station.station_uuid}",
            name=station.name,
            url=station.homepage or station.url,
            stream_url=station.url_resolved or station.url,
            source="radio_browser",
            country=station.country,
            genre=station.tags[0] if station.tags else "",
            language=station.language,
            bitrate=station.bitrate,
            logo=station.favicon,
            website=station.homepage,
            description="",
            tags=station.tags,
            listeners=station.clickcount,
            popularity=station.clickcount,
            metadata={
                'state': station.state,
                'codec': station.codec,
                'hls': bool(station.hls),
                'geo_lat': station.geo_lat,
                'geo_long': station.geo_long
            }
        )
    
    async def get_top_stations(self, limit: int = 50) -> List[UnifiedStation]:
        """الحصول على أفضل المحطات من جميع المصادر"""
        tasks = [
            self.radio_browser.get_top_stations(limit),
            self.shoutcast.get_top_stations(limit),
            self.icecast.get_top_stations(limit),
            self.mytuner.get_top_stations(limit=limit)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        all_stations = []
        seen_urls = set()
        
        for i, result in enumerate(results):
            if isinstance(result, list):
                for station in result:
                    if isinstance(station, RBStation):
                        unified = self._convert_rb_station(station)
                    else:
                        continue
                    
                    if unified.stream_url not in seen_urls:
                        seen_urls.add(unified.stream_url)
                        all_stations.append(unified)
        
        all_stations.sort(key=lambda s: s.popularity, reverse=True)
        return all_stations[:limit]
    
    async def get_stations_by_country(
        self,
        country: str,
        limit: int = 50
    ) -> List[UnifiedStation]:
        """الحصول على المحطات حسب الدولة"""
        return await self.search_all_sources(
            query="",
            country=country,
            limit=limit
        )
    
    async def get_stations_by_genre(
        self,
        genre: str,
        limit: int = 50
    ) -> List[UnifiedStation]:
        """الحصول على المحطات حسب النوع"""
        return await self.search_all_sources(
            query="",
            genre=genre,
            limit=limit
        )
    
    async def refresh_station_status(self, station: UnifiedStation) -> bool:
        """تحديث حالة المحطة والتحقق من فعاليتها"""
        # يمكن إضافة فحص فعلي للرابط هنا
        station.last_checked = datetime.now()
        return station.is_active
    
    def add_favorite(self, station_id: str):
        """إضافة محطة للمفضلة"""
        self._favorites.add(station_id)
    
    def remove_favorite(self, station_id: str):
        """إزالة محطة من المفضلة"""
        self._favorites.discard(station_id)
    
    def is_favorite(self, station_id: str) -> bool:
        """التحقق إذا كانت المحطة في المفضلة"""
        return station_id in self._favorites
    
    def get_favorites(self) -> set:
        """الحصول على قائمة المفضلة"""
        return self._favorites.copy()
    
    def add_to_history(self, station_id: str):
        """إضافة محطة لسجل الاستماع"""
        self._history.insert(0, station_id)
        # الاحتفاظ بآخر 100 محطة فقط
        self._history = self._history[:100]
    
    def get_history(self) -> List[str]:
        """الحصول على سجل الاستماع"""
        return self._history.copy()
    
    async def close(self):
        """إغلاق جميع الاتصالات"""
        await asyncio.gather(
            self.radio_browser.close(),
            self.shoutcast.close(),
            self.icecast.close(),
            self.onlineradiobox.close(),
            self.mytuner.close()
        )
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# مثال للاستخدام
async def main():
    async with RadioAggregator() as aggregator:
        # البحث في جميع المصادر
        print("البحث عن محطات إخبارية...")
        stations = await aggregator.search_all_sources(
            query="news",
            limit=20
        )
        print(f"تم العثور على {len(stations)} محطة")
        
        for station in stations[:5]:
            print(f"  - {station.name} ({station.source}) - {station.country}")
        
        # الحصول على أفضل المحطات
        print("\nأفضل المحطات:")
        top = await aggregator.get_top_stations(limit=10)
        for station in top[:5]:
            print(f"  - {station.name} (شعبية: {station.popularity})")


if __name__ == "__main__":
    asyncio.run(main())
