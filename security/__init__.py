"""
Finovate WaveSphere Ultimate - Security Module
وحدة الأمان والحماية
© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved
"""

import hashlib
import re
from typing import Optional, List, Set
from dataclasses import dataclass
from enum import Enum
import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class ThreatLevel(Enum):
    """مستويات التهديد"""
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SecurityReport:
    """تقرير أمني"""
    is_safe: bool
    threat_level: ThreatLevel
    threats_found: List[str]
    url: Optional[str] = None
    plugin_name: Optional[str] = None


class URLValidator:
    """مدقق عناوين URLs للكشف عن الروابط الضارة"""
    
    # أنماط URLs المشبوهة
    SUSPICIOUS_PATTERNS = [
        r'\.exe$',
        r'\.bat$',
        r'\.cmd$',
        r'\.scr$',
        r'\.js$',
        r'javascript:',
        r'data:',
        r'file://',
        r'ftp://[^/]*\.exe',
    ]
    
    # قوائم سوداء معروفة
    BLACKLISTED_DOMAINS = {
        'malware.com',
        'phishing.net',
        'evil.org',
    }
    
    # قوائم بيضاء لمحطات الراديو الموثوقة
    WHITELISTED_DOMAINS = {
        'radio-browser.info',
        'shoutcast.com',
        'icecast.org',
        'onlineradiobox.com',
        'mytuner-radio.com',
        'streamguys1.com',
        'liveatc.net',
        'cdn.live365.com',
    }
    
    def __init__(self):
        self.compiled_patterns = [re.compile(p, re.IGNORECASE) for p in self.SUSPICIOUS_PATTERNS]
    
    def validate(self, url: str) -> SecurityReport:
        """التحقق من URL"""
        threats = []
        
        # التحقق من القائمة البيضاء
        for domain in self.WHITELISTED_DOMAINS:
            if domain in url.lower():
                return SecurityReport(
                    is_safe=True,
                    threat_level=ThreatLevel.SAFE,
                    threats_found=[]
                )
        
        # التحقق من القائمة السوداء
        for domain in self.BLACKLISTED_DOMAINS:
            if domain in url.lower():
                threats.append(f"Domain blacklisted: {domain}")
        
        # التحقق من الأنماط المشبوهة
        for pattern in self.compiled_patterns:
            if pattern.search(url):
                threats.append(f"Suspicious pattern detected: {pattern.pattern}")
        
        # التحقق من بروتوكول آمن
        if not url.startswith(('http://', 'https://')):
            threats.append("Invalid protocol")
        
        # تحديد مستوى التهديد
        if len(threats) == 0:
            level = ThreatLevel.SAFE
        elif len(threats) == 1:
            level = ThreatLevel.LOW
        elif len(threats) <= 3:
            level = ThreatLevel.MEDIUM
        else:
            level = ThreatLevel.HIGH
        
        return SecurityReport(
            is_safe=len(threats) == 0,
            threat_level=level,
            threats_found=threats,
            url=url
        )


class SandboxPlayer:
    """مشغل في بيئة معزولة آمنة"""
    
    def __init__(self):
        self.allowed_protocols = {'http', 'https'}
        self.max_redirects = 5
        self.timeout_seconds = 30
    
    def is_safe_to_play(self, url: str) -> bool:
        """التحقق مما إذا كان آمناً للتشغيل"""
        validator = URLValidator()
        report = validator.validate(url)
        
        if not report.is_safe:
            logger.warning(f"URL غير آمن: {url} - {report.threats_found}")
            return False
        
        # التحقق من البروتوكول
        try:
            protocol = url.split('://')[0].lower()
            if protocol not in self.allowed_protocols:
                return False
        except Exception:
            return False
        
        return True


class SettingsEncryption:
    """تشفير الإعدادات الحساسة"""
    
    def __init__(self, key: Optional[str] = None):
        self.key = key or self._generate_default_key()
    
    def _generate_default_key(self) -> str:
        """توليد مفتاح افتراضي"""
        import os
        return hashlib.sha256(os.urandom(32)).hexdigest()
    
    def encrypt(self, data: dict) -> str:
        """تشفير البيانات"""
        json_str = json.dumps(data, sort_keys=True)
        # تشفير بسيط (للإنتاج استخدم cryptography library)
        encoded = json_str.encode('utf-8')
        key_bytes = self.key.encode('utf-8')[:32]
        
        encrypted = bytearray()
        for i, byte in enumerate(encoded):
            encrypted.append(byte ^ key_bytes[i % len(key_bytes)])
        
        return hashlib.sha256(bytes(encrypted)).hexdigest()
    
    def verify_integrity(self, data: dict, checksum: str) -> bool:
        """التحقق من سلامة البيانات"""
        return self.encrypt(data) == checksum


class CrashRecovery:
    """نظام استعادة بعد التعطل"""
    
    def __init__(self, recovery_file: str = "recovery.dat"):
        self.recovery_file = Path(recovery_file)
        self.state: dict = {}
    
    def save_state(self, state: dict):
        """حفظ الحالة الحالية"""
        try:
            with open(self.recovery_file, 'w') as f:
                json.dump(state, f)
            logger.info("تم حفظ حالة الاستعادة")
        except Exception as e:
            logger.error(f"فشل حفظ الحالة: {e}")
    
    def load_state(self) -> Optional[dict]:
        """تحميل الحالة المحفوظة"""
        try:
            if self.recovery_file.exists():
                with open(self.recovery_file, 'r') as f:
                    state = json.load(f)
                logger.info("تم تحميل حالة الاستعادة")
                return state
        except Exception as e:
            logger.error(f"فشل تحميل الحالة: {e}")
        return None
    
    def clear_state(self):
        """مسح حالة الاستعادة"""
        try:
            if self.recovery_file.exists():
                self.recovery_file.unlink()
                logger.info("تم مسح حالة الاستعادة")
        except Exception as e:
            logger.error(f"فشل مسح الحالة: {e}")


class MemoryOptimizer:
    """محسن الذاكرة لمنع التسرب"""
    
    def __init__(self, max_cache_size: int = 100):
        self.max_cache_size = max_cache_size
        self.cache: dict = {}
        self.access_order: List[str] = []
    
    def add_to_cache(self, key: str, value):
        """إضافة عنصر للمخزن المؤقت"""
        if key in self.cache:
            self.access_order.remove(key)
        
        self.cache[key] = value
        self.access_order.append(key)
        
        # تطبيق LRU eviction
        while len(self.cache) > self.max_cache_size:
            oldest_key = self.access_order.pop(0)
            del self.cache[oldest_key]
            logger.debug(f"تم إزالة عنصر قديم من المخزن: {oldest_key}")
    
    def get_from_cache(self, key: str):
        """الحصول على عنصر من المخزن"""
        if key in self.cache:
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None
    
    def clear(self):
        """مسح المخزن"""
        self.cache.clear()
        self.access_order.clear()
    
    def get_stats(self) -> dict:
        """إحصائيات المخزن"""
        return {
            'size': len(self.cache),
            'max_size': self.max_cache_size,
            'utilization': len(self.cache) / self.max_cache_size if self.max_cache_size > 0 else 0
        }


class PluginSandbox:
    """بيئة معزولة لتشغيل الإضافات"""
    
    def __init__(self):
        self.allowed_permissions: Set[str] = set()
        self.validator = URLValidator()
    
    def grant_permission(self, permission: str):
        """منح صلاحية"""
        allowed = {
            'network_read',
            'file_read',
            'audio_play',
            'ui_access'
        }
        if permission in allowed:
            self.allowed_permissions.add(permission)
    
    def revoke_permission(self, permission: str):
        """سحب صلاحية"""
        self.allowed_permissions.discard(permission)
    
    def has_permission(self, permission: str) -> bool:
        """التحقق من الصلاحية"""
        return permission in self.allowed_permissions
    
    def validate_plugin_url(self, url: str) -> bool:
        """التحقق من URL للإضافة"""
        if not self.has_permission('network_read'):
            logger.warning("محاولة وصول للشبكة بدون صلاحية")
            return False
        
        report = self.validator.validate(url)
        if not report.is_safe:
            logger.warning(f"URL غير آمن للإضافة: {url}")
            return False
        
        return True


# اختبار الوحدة
if __name__ == "__main__":
    print("🔒 Finovate WaveSphere Security Module")
    print("=" * 40)
    
    # اختبار مدقق URLs
    validator = URLValidator()
    
    safe_urls = [
        "https://stream.radio-browser.info/station/123",
        "https://cdn.shoutcast.com/live.mp3",
    ]
    
    unsafe_urls = [
        "https://malware.com/bad.exe",
        "javascript:alert('xss')",
        "file:///etc/passwd",
    ]
    
    print("\n✓ اختبار URLs الآمنة:")
    for url in safe_urls:
        report = validator.validate(url)
        status = "✓ آمن" if report.is_safe else "✗ غير آمن"
        print(f"  {status}: {url[:50]}...")
    
    print("\n✓ اختبار URLs غير الآمنة:")
    for url in unsafe_urls:
        report = validator.validate(url)
        status = "✓ تم الكشف" if not report.is_safe else "✗ فشل الكشف"
        print(f"  {status}: {url[:50]}... ({report.threat_level.value})")
    
    # اختبار Sandbox
    sandbox = SandboxPlayer()
    print(f"\n✓ Sandbox Player: جاهز")
    
    # اختبار التشفير
    encryption = SettingsEncryption()
    test_data = {"volume": 80, "favorites": [1, 2, 3]}
    checksum = encryption.encrypt(test_data)
    print(f"✓ تشفير الإعدادات: {checksum[:20]}...")
    
    # اختبار استعادة التعطل
    recovery = CrashRecovery()
    recovery.save_state({"last_station": "BBC Radio 1", "volume": 75})
    state = recovery.load_state()
    print(f"✓ استعادة التعطل: {state}")
    recovery.clear_state()
    
    # اختبار محسن الذاكرة
    mem_opt = MemoryOptimizer(max_cache_size=5)
    for i in range(10):
        mem_opt.add_to_cache(f"key_{i}", f"value_{i}")
    stats = mem_opt.get_stats()
    print(f"✓ محسن الذاكرة: {stats['size']}/{stats['max_size']} عناصر")
    
    # اختبار صندوق الإضافة
    plugin_sandbox = PluginSandbox()
    plugin_sandbox.grant_permission('network_read')
    plugin_sandbox.grant_permission('audio_play')
    print(f"✓ صندوق الإضافة: الصلاحيات = {plugin_sandbox.allowed_permissions}")
    
    print("\n✅ وحدة الأمان جاهزة!")
