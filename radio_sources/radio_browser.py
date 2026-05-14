"""
Radio Browser API Integration
API: https://www.radio-browser.info/
دعم ملايين المحطات مع فلترة متقدمة
المطور: Ahmed Mostafa Ibrahim - Finovate – AHMED EG
"""

import aiohttp
import asyncio
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class RadioStation:
    """بيانات محطة الراديو"""
    station_uuid: str
    name: str
    url: str
    url_resolved: str
    homepage: str
    favicon: str
    country: str
    countrycode: str
    state: str
    language: str
    languagecodes: List[str]
    tags: List[str]
    codec: str
    bitrate: int
    hls: int
    lastchangeok: int
    lastcheckok: int
    lastchecktime: str
    lastchangetime: str
    clicktimestamp: str
    clickcount: int
    clicktrend: int
    ssl_error: int
    geo_lat: float
    geo_long: float
    has_extended_info: bool


class RadioBrowserAPI:
    """
    واجهة برمجة تطبيقات Radio Browser
    تدعم أكثر من 30,000 محطة راديو عالمية
    """
    
    BASE_URL = "https://de1.api.radio-browser.info/json"
    MIRROR_URLS = [
        "https://nl1.api.radio-browser.info/json",
        "https://at1.api.radio-browser.info/json",
        "https://fr1.api.radio-browser.info/json"
    ]
    
    def __init__(self):
        self.current_url = self.BASE_URL
        self.session: Optional[aiohttp.ClientSession] = None
        self._mirror_index = 0
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """الحصول على جلسة HTTP"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={
                    'User-Agent': 'Finovate-WaveSphere/1.0 (Ahmed Mostafa Ibrahim)'
                }
            )
        return self.session
    
    async def _request(self, endpoint: str, params: Optional[Dict] = None) -> List[Dict]:
        """إجراء طلب API مع failover للمرايا"""
        session = await self._get_session()
        
        for attempt in range(len(self.MIRROR_URLS) + 1):
            try:
                url = f"{self.current_url}{endpoint}"
                async with session.get(url, params=params, timeout=30) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.warning(f"API error: {response.status}")
            except Exception as e:
                logger.error(f"Request failed to {self.current_url}: {e}")
                # الانتقال للمرآة التالية
                self._mirror_index = (self._mirror_index + 1) % len(self.MIRROR_URLS)
                self.current_url = self.MIRROR_URLS[self._mirror_index]
                continue
        
        raise ConnectionError("All radio browser mirrors failed")
    
    async def get_stations_by_country(
        self, 
        country: str, 
        limit: int = 100,
        order: str = "clickcount",
        reverse: bool = True
    ) -> List[RadioStation]:
        """الحصول على المحطات حسب الدولة"""
        params = {
            'limit': limit,
            'order': order,
            'reverse': str(reverse).lower()
        }
        results = await self._request(f"/stations/bycountry/{country}", params)
        return [self._parse_station(s) for s in results]
    
    async def get_stations_by_tag(
        self,
        tag: str,
        limit: int = 100,
        order: str = "clickcount"
    ) -> List[RadioStation]:
        """الحصول على المحطات حسب التصنيف"""
        params = {'limit': limit, 'order': order}
        results = await self._request(f"/stations/bytag/{tag}", params)
        return [self._parse_station(s) for s in results]
    
    async def get_stations_by_language(
        self,
        language: str,
        limit: int = 100
    ) -> List[RadioStation]:
        """الحصول على المحطات حسب اللغة"""
        params = {'limit': limit}
        results = await self._request(f"/stations/bylanguage/{language}", params)
        return [self._parse_station(s) for s in results]
    
    async def search_stations(
        self,
        name: Optional[str] = None,
        country: Optional[str] = None,
        tag: Optional[str] = None,
        language: Optional[str] = None,
        codec: Optional[str] = None,
        bitrate_min: int = 0,
        limit: int = 100,
        order: str = "clickcount",
        reverse: bool = True
    ) -> List[RadioStation]:
        """بحث متقدم عن المحطات"""
        params = {
            'limit': limit,
            'order': order,
            'reverse': str(reverse).lower(),
            'bitrate_min': bitrate_min
        }
        
        if name:
            params['name'] = name
        if country:
            params['country'] = country
        if tag:
            params['tag'] = tag
        if language:
            params['language'] = language
        if codec:
            params['codec'] = codec
        
        results = await self._request("/stations/search", params)
        return [self._parse_station(s) for s in results]
    
    async def get_top_stations(
        self,
        limit: int = 50,
        order: str = "clickcount"
    ) -> List[RadioStation]:
        """الحصول على أفضل المحطات"""
        params = {'limit': limit, 'order': order}
        results = await self._request("/stations/topclick", params)
        return [self._parse_station(s) for s in results]
    
    async def get_all_countries(self) -> List[Dict]:
        """الحصول على قائمة جميع الدول"""
        return await self._request("/countries")
    
    async def get_all_tags(self) -> List[Dict]:
        """الحصول على قائمة جميع التصنيفات"""
        return await self._request("/tags")
    
    async def get_all_languages(self) -> List[Dict]:
        """الحصول على قائمة جميع اللغات"""
        return await self._request("/languages")
    
    async def get_all_codecs(self) -> List[Dict]:
        """الحصول على قائمة جميع الصيغ"""
        return await self._request("/codecs")
    
    async def click_station(self, station_uuid: str) -> bool:
        """تسجيل نقرة على محطة لزيادة شعبيتها"""
        try:
            session = await self._get_session()
            url = f"{self.current_url}/json/url/{station_uuid}"
            async with session.get(url, timeout=10):
                return True
        except Exception as e:
            logger.error(f"Failed to click station: {e}")
            return False
    
    def _parse_station(self, data: Dict) -> RadioStation:
        """تحويل البيانات الخام إلى كائن RadioStation"""
        return RadioStation(
            station_uuid=data.get('stationuuid', ''),
            name=data.get('name', 'Unknown'),
            url=data.get('url', ''),
            url_resolved=data.get('url_resolved', ''),
            homepage=data.get('homepage', ''),
            favicon=data.get('favicon', ''),
            country=data.get('country', ''),
            countrycode=data.get('countrycode', ''),
            state=data.get('state', ''),
            language=data.get('language', ''),
            languagecodes=data.get('languagecodes', []).split(',') if data.get('languagecodes') else [],
            tags=data.get('tags', '').split(',') if data.get('tags') else [],
            codec=data.get('codec', ''),
            bitrate=data.get('bitrate', 0),
            hls=data.get('hls', 0),
            lastchangeok=data.get('lastchangeok', 0),
            lastcheckok=data.get('lastcheckok', 0),
            lastchecktime=data.get('lastchecktime', ''),
            lastchangetime=data.get('lastchangetime', ''),
            clicktimestamp=data.get('clicktimestamp', ''),
            clickcount=data.get('clickcount', 0),
            clicktrend=data.get('clicktrend', 0),
            ssl_error=data.get('ssl_error', 0),
            geo_lat=data.get('geo_lat', 0.0),
            geo_long=data.get('geo_long', 0.0),
            has_extended_info=data.get('has_extended_info', False)
        )
    
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
    async with RadioBrowserAPI() as api:
        # الحصول على أفضل المحطات
        top_stations = await api.get_top_stations(limit=10)
        print(f"أفضل 10 محطات:")
        for station in top_stations:
            print(f"  - {station.name} ({station.country}) - {station.bitrate}kbps")
        
        # البحث عن محطات مصرية
        egypt_stations = await api.get_stations_by_country("Egypt", limit=20)
        print(f"\nمحطات مصرية: {len(egypt_stations)}")
        
        # البحث عن محطات إسلامية
        islamic_stations = await api.get_stations_by_tag("Islamic", limit=20)
        print(f"محطات إسلامية: {len(islamic_stations)}")


if __name__ == "__main__":
    asyncio.run(main())
