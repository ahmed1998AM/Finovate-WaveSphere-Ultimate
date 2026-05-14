"""
Icecast Directory API Integration
API: https://dir.xiph.org/
محطات راديو مفتوحة المصدر ومحطات المجتمع
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
class IcecastStation:
    """بيانات محطة Icecast"""
    server_name: str
    server_description: str
    server_type: str
    server_url: str
    listen_url: str
    mount_point: str
    bitrate: int
    format: str
    channels: int
    sample_rate: int
    genre: str
    country: str
    language: str
    listeners_peak: int
    listeners_current: int
    server_admin: str
    server_icon: str
    stream_title: str
    stream_description: str


class IcecastAPI:
    """
    واجهة برمجة تطبيقات Icecast Directory
    محطات راديو مجتمعية ومفتوحة
    """
    
    DIRECTORY_URL = "https://dir.xiph.org"
    API_BASE = "https://api.xiph.org"
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """الحصول على جلسة HTTP"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={
                    'User-Agent': 'Finovate-WaveSphere/1.0 (Ahmed Mostafa Ibrahim)'
                }
            )
        return self.session
    
    async def search_stations(
        self,
        query: str,
        limit: int = 50
    ) -> List[IcecastStation]:
        """البحث عن المحطات"""
        session = await self._get_session()
        
        try:
            # البحث في دليل Icecast
            url = f"{self.DIRECTORY_URL}/search.json"
            params = {'search': query, 'limit': limit}
            async with session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_stations(data.get('stations', []))
        except Exception as e:
            logger.error(f"Icecast search error: {e}")
        
        return []
    
    async def get_stations_by_genre(
        self,
        genre: str,
        limit: int = 50
    ) -> List[IcecastStation]:
        """الحصول على المحطات حسب النوع"""
        session = await self._get_session()
        
        try:
            url = f"{self.DIRECTORY_URL}/genre/{genre}.json"
            params = {'limit': limit}
            async with session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_stations(data.get('stations', []))
        except Exception as e:
            logger.error(f"Icecast by genre error: {e}")
        
        return []
    
    async def get_all_genres(self) -> List[str]:
        """الحصول على جميع الأنواع"""
        session = await self._get_session()
        
        try:
            url = f"{self.DIRECTORY_URL}/genres.json"
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('genres', [])
        except Exception as e:
            logger.error(f"Icecast genres error: {e}")
        
        return []
    
    async def get_top_stations(
        self,
        limit: int = 50
    ) -> List[IcecastStation]:
        """الحصول على أفضل المحطات"""
        session = await self._get_session()
        
        try:
            url = f"{self.DIRECTORY_URL}/top.json"
            params = {'limit': limit}
            async with session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_stations(data.get('stations', []))
        except Exception as e:
            logger.error(f"Icecast top stations error: {e}")
        
        return []
    
    async def get_server_status(self, server_url: str) -> Optional[Dict]:
        """الحصول على حالة الخادم"""
        session = await self._get_session()
        
        try:
            # طلب حالة الخادم Icecast
            status_url = f"{server_url}/status-json.xsl"
            async with session.get(status_url, timeout=10) as response:
                if response.status == 200:
                    return await response.json()
        except Exception as e:
            logger.error(f"Server status error: {e}")
        
        return None
    
    async def parse_directory_html(self) -> List[IcecastStation]:
        """تحليل صفحة الدليل HTML (fallback)"""
        session = await self._get_session()
        
        try:
            url = self.DIRECTORY_URL
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    html = await response.text()
                    return self._parse_html(html)
        except Exception as e:
            logger.error(f"Parse directory HTML error: {e}")
        
        return []
    
    def _parse_stations(self, data: List[Dict]) -> List[IcecastStation]:
        """تحويل البيانات إلى كائنات IcecastStation"""
        stations = []
        for item in data:
            try:
                station = IcecastStation(
                    server_name=item.get('server_name', 'Unknown'),
                    server_description=item.get('server_description', ''),
                    server_type=item.get('server_type', 'Icecast'),
                    server_url=item.get('server_url', ''),
                    listen_url=item.get('listen_url', ''),
                    mount_point=item.get('mount_point', '/stream'),
                    bitrate=int(item.get('bitrate', 0)),
                    format=item.get('format', 'MP3'),
                    channels=int(item.get('channels', 2)),
                    sample_rate=int(item.get('sample_rate', 44100)),
                    genre=item.get('genre', ''),
                    country=item.get('country', ''),
                    language=item.get('language', ''),
                    listeners_peak=int(item.get('listeners_peak', 0)),
                    listeners_current=int(item.get('listeners_current', 0)),
                    server_admin=item.get('server_admin', ''),
                    server_icon=item.get('server_icon', ''),
                    stream_title=item.get('stream_title', ''),
                    stream_description=item.get('stream_description', '')
                )
                stations.append(station)
            except Exception as e:
                logger.error(f"Error parsing icecast station: {e}")
        
        return stations
    
    def _parse_html(self, html: str) -> List[IcecastStation]:
        """تحليل HTML لاستخراج المحطات"""
        stations = []
        try:
            # تحليل بسيط لـ HTML
            # يمكن توسيع هذا لتحليل أكثر تعقيداً
            pass
        except Exception as e:
            logger.error(f"HTML parsing error: {e}")
        
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
    async with IcecastAPI() as api:
        # الحصول على أفضل المحطات
        top_stations = await api.get_top_stations(limit=10)
        print(f"أفضل محطات Icecast: {len(top_stations)}")
        for station in top_stations[:5]:
            print(f"  - {station.server_name} ({station.genre}) - {station.bitrate}kbps")
        
        # الحصول على الأنواع
        genres = await api.get_all_genres()
        print(f"\nالأنواع المتاحة: {len(genres)}")


if __name__ == "__main__":
    asyncio.run(main())
