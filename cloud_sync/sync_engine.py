"""
Finovate WaveSphere Ultimate - Cloud Sync Engine
محرك المزامنة السحابية

المطور: Ahmed Mostafa Ibrahim
العلامة التجارية: Finovate – AHMED EG
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from PySide6.QtCore import QObject, Signal


class CloudSyncEngine(QObject):
    """محرك المزامنة السحابية"""
    
    sync_started = Signal()
    sync_completed = Signal(bool)  # نجاح/فشل
    sync_error = Signal(str)       # رسالة الخطأ
    data_updated = Signal(str)     # نوع البيانات المحدثة
    
    def __init__(self, user_id: str = None):
        super().__init__()
        self.user_id = user_id or self._generate_user_id()
        self.sync_token = None
        self.last_sync = None
        self.is_syncing = False
        
        # بيانات المستخدم المحلية
        self.favorites = []
        self.history = []
        self.playlists = {}
        self.settings = {}
        
        # حالة المزامنة
        self.pending_changes = {
            'favorites': [],
            'history': [],
            'playlists': [],
            'settings': []
        }
        
    def _generate_user_id(self) -> str:
        """توليد معرف مستخدم فريد"""
        import uuid
        return str(uuid.uuid4())
        
    def authenticate(self, token: str) -> bool:
        """
        المصادقة مع الخادم السحابي
        
        Args:
            token: رمز المصادقة
            
        Returns:
            bool: نجاح المصادقة
        """
        # سيتم تنفيذ المصادقة الفعلية هنا
        self.sync_token = token
        return True
        
    def logout(self):
        """تسجيل الخروج"""
        self.sync_token = None
        self.last_sync = None
        
    def set_favorites(self, favorites: list):
        """تعيين المفضلة"""
        self.favorites = favorites
        self.pending_changes['favorites'].append({
            'action': 'update',
            'timestamp': datetime.now().isoformat(),
            'data': favorites
        })
        
    def add_favorite(self, station: dict):
        """إضافة محطة للمفضلة"""
        if station not in self.favorites:
            self.favorites.append(station)
            self.pending_changes['favorites'].append({
                'action': 'add',
                'timestamp': datetime.now().isoformat(),
                'data': station
            })
            
    def remove_favorite(self, station_id: str):
        """إزالة من المفضلة"""
        self.favorites = [s for s in self.favorites if s.get('id') != station_id]
        self.pending_changes['favorites'].append({
            'action': 'remove',
            'timestamp': datetime.now().isoformat(),
            'station_id': station_id
        })
        
    def add_to_history(self, station: dict, duration: int = 0):
        """إضافة إلى سجل الاستماع"""
        entry = {
            'station': station,
            'timestamp': datetime.now().isoformat(),
            'duration': duration
        }
        self.history.insert(0, entry)
        
        # الاحتفاظ بآخر 1000 إدخال فقط
        if len(self.history) > 1000:
            self.history = self.history[:1000]
            
        self.pending_changes['history'].append({
            'action': 'add',
            'timestamp': datetime.now().isoformat(),
            'data': entry
        })
        
    def get_history(self, limit: int = 100) -> list:
        """الحصول على سجل الاستماع"""
        return self.history[:limit]
        
    def create_playlist(self, name: str, stations: list = None) -> str:
        """إنشاء قائمة تشغيل"""
        playlist_id = hashlib.md5(f"{name}{datetime.now()}".encode()).hexdigest()[:12]
        self.playlists[playlist_id] = {
            'id': playlist_id,
            'name': name,
            'stations': stations or [],
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat()
        }
        
        self.pending_changes['playlists'].append({
            'action': 'create',
            'timestamp': datetime.now().isoformat(),
            'data': self.playlists[playlist_id]
        })
        
        return playlist_id
        
    def add_to_playlist(self, playlist_id: str, station: dict):
        """إضافة محطة لقائمة التشغيل"""
        if playlist_id in self.playlists:
            self.playlists[playlist_id]['stations'].append(station)
            self.playlists[playlist_id]['modified'] = datetime.now().isoformat()
            
            self.pending_changes['playlists'].append({
                'action': 'update',
                'timestamp': datetime.now().isoformat(),
                'playlist_id': playlist_id,
                'data': station
            })
            
    def remove_from_playlist(self, playlist_id: str, station_id: str):
        """إزالة محطة من قائمة التشغيل"""
        if playlist_id in self.playlists:
            self.playlists[playlist_id]['stations'] = [
                s for s in self.playlists[playlist_id]['stations']
                if s.get('id') != station_id
            ]
            self.playlists[playlist_id]['modified'] = datetime.now().isoformat()
            
    def delete_playlist(self, playlist_id: str):
        """حذف قائمة التشغيل"""
        if playlist_id in self.playlists:
            del self.playlists[playlist_id]
            self.pending_changes['playlists'].append({
                'action': 'delete',
                'timestamp': datetime.now().isoformat(),
                'playlist_id': playlist_id
            })
            
    def get_playlists(self) -> Dict[str, dict]:
        """الحصول على جميع قوائم التشغيل"""
        return self.playlists.copy()
        
    def update_settings(self, settings: dict):
        """تحديث الإعدادات"""
        self.settings.update(settings)
        self.pending_changes['settings'].append({
            'action': 'update',
            'timestamp': datetime.now().isoformat(),
            'data': settings
        })
        
    def sync_now(self) -> bool:
        """
        تنفيذ المزامنة الفورية
        
        Returns:
            bool: نجاح المزامنة
        """
        if self.is_syncing or not self.sync_token:
            return False
            
        self.is_syncing = True
        self.sync_started.emit()
        
        try:
            # رفع التغييرات المعلقة
            if any(self.pending_changes.values()):
                self._upload_changes()
                
            # تنزيل التحديثات من الخادم
            self._download_updates()
            
            self.last_sync = datetime.now()
            self.sync_completed.emit(True)
            return True
            
        except Exception as e:
            self.sync_error.emit(str(e))
            self.sync_completed.emit(False)
            return False
            
        finally:
            self.is_syncing = False
            
    def _upload_changes(self):
        """رفع التغييرات المعلقة"""
        # سيتم تنفيذ الرفع الفعلي للخادم هنا
        # مثال: requests.post(cloud_url, json=self.pending_changes)
        
        # بعد النجاح، مسح التغييرات المعلقة
        for key in self.pending_changes:
            self.pending_changes[key] = []
            
    def _download_updates(self):
        """تنزيل التحديثات من الخادم"""
        # سيتم تنفيذ التنزيل الفعلي من الخادم هنا
        # مثال: response = requests.get(cloud_url)
        pass
        
    def get_sync_status(self) -> dict:
        """الحصول على حالة المزامنة"""
        return {
            'user_id': self.user_id,
            'authenticated': self.sync_token is not None,
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'is_syncing': self.is_syncing,
            'pending_changes': sum(len(v) for v in self.pending_changes.values())
        }
        
    def export_data(self) -> dict:
        """تصدير جميع البيانات"""
        return {
            'user_id': self.user_id,
            'favorites': self.favorites,
            'history': self.history,
            'playlists': self.playlists,
            'settings': self.settings,
            'exported_at': datetime.now().isoformat()
        }
        
    def import_data(self, data: dict):
        """استيراد بيانات"""
        if 'favorites' in data:
            self.favorites = data['favorites']
        if 'history' in data:
            self.history = data['history']
        if 'playlists' in data:
            self.playlists = data['playlists']
        if 'settings' in data:
            self.settings = data['settings']
            
        self.data_updated.emit('all')
        
    def backup_to_file(self, filepath: str):
        """حفظ نسخة احتياطية في ملف"""
        data = self.export_data()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def restore_from_file(self, filepath: str):
        """استعادة من ملف نسخة احتياطية"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.import_data(data)


# Singleton instance
_sync_engine_instance = None

def get_sync_engine(user_id: str = None) -> CloudSyncEngine:
    """الحصول على مثيل محرك المزامنة"""
    global _sync_engine_instance
    if _sync_engine_instance is None:
        _sync_engine_instance = CloudSyncEngine(user_id)
    return _sync_engine_instance
