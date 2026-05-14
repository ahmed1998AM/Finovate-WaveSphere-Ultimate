"""
Finovate WaveSphere Ultimate - Recording Scheduler
مجدول التسجيلات التلقائية

المطور: Ahmed Mostafa Ibrahim
العلامة التجارية: Finovate – AHMED EG
"""

import os
import json
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from PySide6.QtCore import QObject, Signal, QTimer


class RecordingSchedule:
    """جدول تسجيل واحد"""
    
    def __init__(self, station_url: str, start_time: datetime, duration_minutes: int,
                 name: str = "", days: list = None, enabled: bool = True):
        self.station_url = station_url
        self.start_time = start_time
        self.duration_minutes = duration_minutes
        self.name = name or f"Recording_{start_time.strftime('%Y%m%d_%H%M')}"
        self.days = days or []  # أيام الأسبوع (0=الاثنين, 6=الأحد)
        self.enabled = enabled
        self.last_recorded = None
        self.id = datetime.now().timestamp()
        
    def to_dict(self) -> dict:
        """تحويل إلى قاموس"""
        return {
            'station_url': self.station_url,
            'start_time': self.start_time.isoformat(),
            'duration_minutes': self.duration_minutes,
            'name': self.name,
            'days': self.days,
            'enabled': self.enabled,
            'last_recorded': self.last_recorded.isoformat() if self.last_recorded else None,
            'id': self.id
        }
        
    @classmethod
    def from_dict(cls, data: dict) -> 'RecordingSchedule':
        """إنشاء من قاموس"""
        obj = cls(
            station_url=data['station_url'],
            start_time=datetime.fromisoformat(data['start_time']),
            duration_minutes=data['duration_minutes'],
            name=data.get('name', ''),
            days=data.get('days', []),
            enabled=data.get('enabled', True)
        )
        obj.id = data.get('id', datetime.now().timestamp())
        if data.get('last_recorded'):
            obj.last_recorded = datetime.fromisoformat(data['last_recorded'])
        return obj
        
    def should_run_today(self) -> bool:
        """هل يجب التشغيل اليوم؟"""
        if not self.days:  # كل يوم
            return True
        today = datetime.now().weekday()
        return today in self.days
        
    def is_due(self) -> bool:
        """هل حان وقت التشغيل؟"""
        if not self.enabled:
            return False
            
        now = datetime.now()
        if not self.should_run_today():
            return False
            
        # التحقق من الوقت
        time_match = (now.hour == self.start_time.hour and 
                     now.minute == self.start_time.minute)
                     
        # التأكد من عدم التشغيل بالفعل اليوم
        if self.last_recorded:
            today = datetime.now().date()
            if self.last_recorded.date() == today:
                return False
                
        return time_match


class RecordingScheduler(QObject):
    """مجدول التسجيلات التلقائية"""
    
    schedule_triggered = Signal(object)  # جدول التسجيل
    schedule_completed = Signal(object)  # جدول اكتمل
    
    def __init__(self):
        super().__init__()
        self.schedules: List[RecordingSchedule] = []
        self.config_file = self._get_config_path()
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_schedules)
        self.timer.start(60000)  # فحص كل دقيقة
        
        self.load_schedules()
        
    def _get_config_path(self) -> str:
        """الحصول على مسار ملف التكوين"""
        import platform
        if platform.system() == 'Windows':
            base = os.path.join(os.environ['APPDATA'], 'WaveSphere')
        else:
            base = os.path.join(os.path.expanduser('~'), '.wavesphere')
            
        os.makedirs(base, exist_ok=True)
        return os.path.join(base, 'recording_schedules.json')
        
    def load_schedules(self):
        """تحميل الجداول المحفوظة"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.schedules = [RecordingSchedule.from_dict(d) for d in data]
            except Exception as e:
                print(f"Error loading schedules: {e}")
                self.schedules = []
                
    def save_schedules(self):
        """حفظ الجداول"""
        try:
            data = [s.to_dict() for s in self.schedules]
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving schedules: {e}")
            
    def add_schedule(self, schedule: RecordingSchedule):
        """إضافة جدول جديد"""
        self.schedules.append(schedule)
        self.save_schedules()
        
    def remove_schedule(self, schedule_id: float):
        """إزالة جدول"""
        self.schedules = [s for s in self.schedules if s.id != schedule_id]
        self.save_schedules()
        
    def update_schedule(self, schedule_id: float, updates: dict):
        """تحديث جدول"""
        for schedule in self.schedules:
            if schedule.id == schedule_id:
                for key, value in updates.items():
                    if hasattr(schedule, key):
                        setattr(schedule, key, value)
                self.save_schedules()
                break
                
    def enable_schedule(self, schedule_id: float):
        """تفعيل جدول"""
        self.update_schedule(schedule_id, {'enabled': True})
        
    def disable_schedule(self, schedule_id: float):
        """تعطيل جدول"""
        self.update_schedule(schedule_id, {'enabled': False})
        
    def get_schedules(self) -> List[RecordingSchedule]:
        """الحصول على جميع الجداول"""
        return self.schedules.copy()
        
    def get_enabled_schedules(self) -> List[RecordingSchedule]:
        """الحصول على الجداول المفعلة"""
        return [s for s in self.schedules if s.enabled]
        
    def check_schedules(self):
        """فحص الجداول المستحقة"""
        for schedule in self.schedules:
            if schedule.is_due():
                self.schedule_triggered.emit(schedule)
                schedule.last_recorded = datetime.now()
                self.save_schedules()
                
    def create_daily_recording(self, station_url: str, hour: int, minute: int,
                               duration_minutes: int = 60, name: str = "") -> RecordingSchedule:
        """إنشاء تسجيل يومي"""
        schedule = RecordingSchedule(
            station_url=station_url,
            start_time=datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0),
            duration_minutes=duration_minutes,
            name=name,
            days=list(range(7)),  # كل الأيام
            enabled=True
        )
        self.add_schedule(schedule)
        return schedule
        
    def create_weekday_recording(self, station_url: str, hour: int, minute: int,
                                 duration_minutes: int = 60, name: str = "") -> RecordingSchedule:
        """إنشاء تسجيل لأيام الأسبوع فقط"""
        schedule = RecordingSchedule(
            station_url=station_url,
            start_time=datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0),
            duration_minutes=duration_minutes,
            name=name,
            days=[0, 1, 2, 3, 4],  # الإثنين إلى الجمعة
            enabled=True
        )
        self.add_schedule(schedule)
        return schedule
        
    def create_one_time_recording(self, station_url: str, date: datetime,
                                  duration_minutes: int = 60, name: str = "") -> RecordingSchedule:
        """إنشاء تسجيل لمرة واحدة"""
        schedule = RecordingSchedule(
            station_url=station_url,
            start_time=date,
            duration_minutes=duration_minutes,
            name=name,
            days=[],
            enabled=True
        )
        self.add_schedule(schedule)
        return schedule
        
    def get_next_scheduled(self) -> Optional[RecordingSchedule]:
        """الحصول على الجدول التالي"""
        enabled = self.get_enabled_schedules()
        if not enabled:
            return None
            
        # ترتيب حسب الوقت
        now = datetime.now()
        future_schedules = []
        
        for s in enabled:
            next_run = s.start_time.replace(
                year=now.year, month=now.month, day=now.day
            )
            if next_run < now:
                next_run += timedelta(days=1)
            future_schedules.append((next_run, s))
            
        if not future_schedules:
            return None
            
        future_schedules.sort(key=lambda x: x[0])
        return future_schedules[0][1]
