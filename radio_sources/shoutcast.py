"""
Shoutcast Directory API Integration
API: https://directory.shoutcast.com/
محطات عالية الجودة واكتشاف الأنواع الموسيقية
المطور: Ahmed Mostafa Ibrahim - Finovate – AHMED EG
"""

import aiohttp
import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


@dataclass
class ShoutcastStation:
    """بيانات محطة Shoutcast"""
    id: str
    name: str
    url: str
    homepage: str
    genre: str
    bitrate: int
    listeners: int
    max_listeners: int
    status: str
    description: str
    country: str
    language: str
    server_version: str
    is_nsv: bool
    media_type: str
    mime_type: str


class ShoutcastAPI:
    """
    واجهة برمجة تطبيقات Shoutcast Directory
    محطات راديو عالية الجودة
    """
    
    BASE_URL = "https://api.shoutcast.com"
    LEGACY_URL = "https://yp.shoutcast.com"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """الحصول على جلسة HTTP"""
        if self.session is None or self.session.closed:
            headers = {}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            self.session = aiohttp.ClientSession(headers=headers)
        return self.session
    
    async def search_stations(
        self,
        query: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[ShoutcastStation]:
        """البحث عن المحطات"""
        session = await self._get_session()
        
        params = {
            'search': query,
            'limit': limit,
            'offset': offset
        }
        
        try:
            url = f"{self.BASE_URL}/legacy/station/search"
            async with session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_stations(data.get('stations', []))
        except Exception as e:
            logger.error(f"Shoutcast search error: {e}")
        
        return []
    
    async def get_top_stations(
        self,
        limit: int = 50,
        genre: Optional[str] = None
    ) -> List[ShoutcastStation]:
        """الحصول على أفضل المحطات"""
        session = await self._get_session()
        
        params = {'limit': limit}
        if genre:
            params['genre'] = genre
        
        try:
            url = f"{self.BASE_URL}/legacy/station/toplist"
            async with session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_stations(data.get('stations', []))
        except Exception as e:
            logger.error(f"Shoutcast toplist error: {e}")
        
        return []
    
    async def get_genres(self) -> List[str]:
        """الحصول على قائمة الأنواع الموسيقية"""
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/legacy/genre/list"
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return [g['name'] for g in data.get('genres', [])]
        except Exception as e:
            logger.error(f"Shoutcast genres error: {e}")
        
        return []
    
    async def get_stations_by_genre(
        self,
        genre: str,
        limit: int = 50
    ) -> List[ShoutcastStation]:
        """الحصول على المحطات حسب النوع الموسيقي"""
        session = await self._get_session()
        
        params = {'genre': genre, 'limit': limit}
        
        try:
            url = f"{self.BASE_URL}/legacy/station/bygenre"
            async with session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_stations(data.get('stations', []))
        except Exception as e:
            logger.error(f"Shoutcast bygenre error: {e}")
        
        return []
    
    async def get_station_info(self, station_id: str) -> Optional[ShoutcastStation]:
        """الحصول على معلومات محطة محددة"""
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/legacy/station/info"
            params = {'id': station_id}
            async with session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    stations = self._parse_stations([data.get('station', {})])
                    return stations[0] if stations else None
        except Exception as e:
            logger.error(f"Shoutcast info error: {e}")
        
        return None
    
    def _parse_stations(self, data: List[Dict]) -> List[ShoutcastStation]:
        """تحويل البيانات الخام إلى كائنات ShoutcastStation"""
        stations = []
        for item in data:
            try:
                station = ShoutcastStation(
                    id=str(item.get('ID', '')),
                    name=item.get('Name', 'Unknown'),
                    url=item.get('URL', ''),
                    homepage=item.get('Homepage', ''),
                    genre=item.get('Genre', ''),
                    bitrate=int(item.get('Bitrate', 0)),
                    listeners=int(item.get('Listeners', 0)),
                    max_listeners=int(item.get('MaxListeners', 0)),
                    status=item.get('Status', 'offline'),
                    description=item.get('Description', ''),
                    country=item.get('Country', ''),
                    language=item.get('Language', ''),
                    server_version=item.get('ServerVersion', ''),
                    is_nsv=bool(item.get('IsNSV', False)),
                    media_type=item.get('MediaType', 'audio'),
                    mime_type=item.get('MimeType', 'audio/mpeg')
                )
                stations.append(station)
            except Exception as e:
                logger.error(f"Error parsing station: {e}")
        
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
    async with ShoutcastAPI() as api:
        # البحث عن محطات
        stations = await api.search_stations("news", limit=10)
        print(f"نتائج البحث: {len(stations)} محطات")
        for station in stations[:5]:
            print(f"  - {station.name} ({station.genre}) - {station.bitrate}kbps")
        
        # الحصول على الأنواع
        genres = await api.get_genres()
        print(f"\nالأنواع المتاحة: {len(genres)}")
        print(f"أول 10 أنواع: {genres[:10]}")


if __name__ == "__main__":
    asyncio.run(main())
