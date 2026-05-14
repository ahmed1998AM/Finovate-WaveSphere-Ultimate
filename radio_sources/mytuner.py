"""
MyTuner Radio API Integration
API: https://mytuner-radio.com/
كتالوج راديو متميز مع شعارات المحطات والبيانات الوصفية
المطور: Ahmed Mostafa Ibrahim - Finovate – AHMED EG
"""

import aiohttp
import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class MyTunerStation:
    """بيانات محطة MyTuner"""
    id: str
    name: str
    url: str
    stream_url: str
    country: str
    country_code: str
    state: str
    city: str
    genres: List[str]
    logo: str
    website: str
    description: str
    bitrate: int
    codec: str
    language: str
    tags: List[str]
    is_favorite: bool
    popularity: int


class MyTunerAPI:
    """
    واجهة برمجة تطبيقات MyTuner Radio
    كتالوج راديو متميز
    """
    
    BASE_URL = "https://api.mytunerradio.com"
    WEB_URL = "https://mytuner-radio.com"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """الحصول على جلسة HTTP"""
        if self.session is None or self.session.closed:
            headers = {
                'User-Agent': 'Finovate-WaveSphere/1.0 (Ahmed Mostafa Ibrahim)'
            }
            if self.api_key:
                headers['X-API-Key'] = self.api_key
            
            self.session = aiohttp.ClientSession(headers=headers)
        return self.session
    
    async def search_stations(
        self,
        query: str,
        country: Optional[str] = None,
        genre: Optional[str] = None,
        limit: int = 50
    ) -> List[MyTunerStation]:
        """البحث عن المحطات"""
        session = await self._get_session()
        
        params = {
            'search': query,
            'limit': limit
        }
        
        if country:
            params['country'] = country
        if genre:
            params['genre'] = genre
        
        try:
            url = f"{self.BASE_URL}/stations/search"
            async with session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_stations(data.get('stations', []))
        except Exception as e:
            logger.error(f"MyTuner search error: {e}")
        
        return []
    
    async def get_stations_by_country(
        self,
        country: str,
        limit: int = 50
    ) -> List[MyTunerStation]:
        """الحصول على المحطات حسب الدولة"""
        session = await self._get_session()
        
        params = {'limit': limit}
        
        try:
            url = f"{self.BASE_URL}/stations/country/{country}"
            async with session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_stations(data.get('stations', []))
        except Exception as e:
            logger.error(f"MyTuner by country error: {e}")
        
        return []
    
    async def get_stations_by_genre(
        self,
        genre: str,
        limit: int = 50
    ) -> List[MyTunerStation]:
        """الحصول على المحطات حسب النوع"""
        session = await self._get_session()
        
        params = {'limit': limit}
        
        try:
            url = f"{self.BASE_URL}/stations/genre/{genre}"
            async with session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_stations(data.get('stations', []))
        except Exception as e:
            logger.error(f"MyTuner by genre error: {e}")
        
        return []
    
    async def get_top_stations(
        self,
        country: Optional[str] = None,
        limit: int = 50
    ) -> List[MyTunerStation]:
        """الحصول على أفضل المحطات"""
        session = await self._get_session()
        
        params = {'limit': limit}
        if country:
            params['country'] = country
        
        try:
            url = f"{self.BASE_URL}/stations/top"
            async with session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_stations(data.get('stations', []))
        except Exception as e:
            logger.error(f"MyTuner top stations error: {e}")
        
        return []
    
    async def get_all_countries(self) -> List[Dict]:
        """الحصول على قائمة جميع الدول"""
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/countries"
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('countries', [])
        except Exception as e:
            logger.error(f"MyTuner countries error: {e}")
        
        return []
    
    async def get_all_genres(self) -> List[str]:
        """الحصول على قائمة جميع الأنواع"""
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/genres"
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('genres', [])
        except Exception as e:
            logger.error(f"MyTuner genres error: {e}")
        
        return []
    
    async def get_station_details(self, station_id: str) -> Optional[MyTunerStation]:
        """الحصول على تفاصيل محطة محددة"""
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/stations/{station_id}"
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    stations = self._parse_stations([data.get('station', {})])
                    return stations[0] if stations else None
        except Exception as e:
            logger.error(f"MyTuner station details error: {e}")
        
        return None
    
    async def get_stream_url(self, station_id: str) -> Optional[str]:
        """الحصول على رابط البث"""
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/stations/{station_id}/stream"
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('stream_url')
        except Exception as e:
            logger.error(f"Get stream URL error: {e}")
        
        return None
    
    def _parse_stations(self, data: List[Dict]) -> List[MyTunerStation]:
        """تحويل البيانات إلى كائنات MyTunerStation"""
        stations = []
        for item in data:
            try:
                station = MyTunerStation(
                    id=str(item.get('id', '')),
                    name=item.get('name', 'Unknown'),
                    url=item.get('url', ''),
                    stream_url=item.get('stream_url', ''),
                    country=item.get('country', ''),
                    country_code=item.get('country_code', ''),
                    state=item.get('state', ''),
                    city=item.get('city', ''),
                    genres=item.get('genres', []).split(',') if isinstance(item.get('genres'), str) else item.get('genres', []),
                    logo=item.get('logo', ''),
                    website=item.get('website', ''),
                    description=item.get('description', ''),
                    bitrate=int(item.get('bitrate', 0)),
                    codec=item.get('codec', ''),
                    language=item.get('language', ''),
                    tags=item.get('tags', []),
                    is_favorite=bool(item.get('is_favorite', False)),
                    popularity=int(item.get('popularity', 0))
                )
                stations.append(station)
            except Exception as e:
                logger.error(f"Error parsing mytuner station: {e}")
        
        return stations
    
    async def close(self):
        """إغلاق الجلسة"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# مثال للاستخدام
async def main():
    async with MyTunerAPI() as api:
        print("MyTuner API جاهز للاستخدام")
        # يمكن إضافة اختبارات فعلية هنا


if __name__ == "__main__":
    asyncio.run(main())
