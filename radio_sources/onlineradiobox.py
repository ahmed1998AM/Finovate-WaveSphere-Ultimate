"""
Online Radio Box API Integration
API: https://onlineradiobox.com/
محطات راديو عالمية مع فلترة إقليمية
المطور: Ahmed Mostafa Ibrahim - Finovate – AHMED EG
"""

import aiohttp
import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class OnlineRadioBoxStation:
    """بيانات محطة Online Radio Box"""
    id: str
    name: str
    url: str
    stream_url: str
    country: str
    city: str
    genre: str
    description: str
    logo: str
    website: str
    bitrate: int
    codec: str
    language: str
    is_live: bool
    current_track: str
    listeners: int


class OnlineRadioBoxAPI:
    """
    واجهة برمجة تطبيقات Online Radio Box
    محطات راديو من جميع أنحاء العالم
    """
    
    BASE_URL = "https://onlineradiobox.com"
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """الحصول على جلسة HTTP"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
        return self.session
    
    async def search_stations(
        self,
        query: str,
        country: Optional[str] = None,
        limit: int = 50
    ) -> List[OnlineRadioBoxStation]:
        """البحث عن المحطات"""
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/search"
            params = {'q': query}
            if country:
                params['country'] = country
            
            async with session.get(url, params=params, timeout=30) as response:
                if response.status == 200:
                    html = await response.text()
                    return self._parse_search_results(html, limit)
        except Exception as e:
            logger.error(f"OnlineRadioBox search error: {e}")
        
        return []
    
    async def get_stations_by_country(
        self,
        country: str,
        limit: int = 50
    ) -> List[OnlineRadioBoxStation]:
        """الحصول على المحطات حسب الدولة"""
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/{country.lower().replace(' ', '-')}"
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    html = await response.text()
                    return self._parse_country_page(html, limit)
        except Exception as e:
            logger.error(f"OnlineRadioBox by country error: {e}")
        
        return []
    
    async def get_stations_by_genre(
        self,
        genre: str,
        limit: int = 50
    ) -> List[OnlineRadioBoxStation]:
        """الحصول على المحطات حسب النوع"""
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/genre/{genre.lower().replace(' ', '-')}"
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    html = await response.text()
                    return self._parse_genre_page(html, limit)
        except Exception as e:
            logger.error(f"OnlineRadioBox by genre error: {e}")
        
        return []
    
    async def get_all_countries(self) -> List[Dict]:
        """الحصول على قائمة جميع الدول"""
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}"
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    html = await response.text()
                    return self._parse_countries(html)
        except Exception as e:
            logger.error(f"OnlineRadioBox countries error: {e}")
        
        return []
    
    async def get_station_stream(self, station_id: str) -> Optional[str]:
        """الحصول على رابط البث للمحطة"""
        session = await self._get_session()
        
        try:
            url = f"{self.BASE_URL}/api/station/{station_id}/stream"
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('url')
        except Exception as e:
            logger.error(f"Get stream error: {e}")
        
        return None
    
    def _parse_search_results(self, html: str, limit: int) -> List[OnlineRadioBoxStation]:
        """تحليل نتائج البحث"""
        stations = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            # تحليل عناصر المحطة من HTML
            # هذا تبسيط - يحتاج لتحليل فعلي للصفحة
        except Exception as e:
            logger.error(f"Parse search results error: {e}")
        
        return stations
    
    def _parse_country_page(self, html: str, limit: int) -> List[OnlineRadioBoxStation]:
        """تحليل صفحة الدولة"""
        stations = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            # تحليل المحطات من صفحة الدولة
        except Exception as e:
            logger.error(f"Parse country page error: {e}")
        
        return stations
    
    def _parse_genre_page(self, html: str, limit: int) -> List[OnlineRadioBoxStation]:
        """تحليل صفحة النوع"""
        stations = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            # تحليل المحطات من صفحة النوع
        except Exception as e:
            logger.error(f"Parse genre page error: {e}")
        
        return stations
    
    def _parse_countries(self, html: str) -> List[Dict]:
        """تحليل قائمة الدول"""
        countries = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            # استخراج قائمة الدول
        except Exception as e:
            logger.error(f"Parse countries error: {e}")
        
        return countries
    
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
    async with OnlineRadioBoxAPI() as api:
        print("Online Radio Box API جاهز للاستخدام")
        # يمكن إضافة اختبارات فعلية هنا


if __name__ == "__main__":
    asyncio.run(main())
