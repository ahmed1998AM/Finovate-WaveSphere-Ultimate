"""
Finovate WaveSphere Ultimate - Stream Recorder
مسجل البث الإذاعي

المطور: Ahmed Mostafa Ibrahim
العلامة التجارية: Finovate – AHMED EG
"""

import os
import time
import threading
from datetime import datetime
from typing import Optional, Callable
from PySide6.QtCore import QObject, Signal


class StreamRecorder(QObject):
    """مسجل البث المباشر"""
    
    recording_started = Signal(str)  # مسار الملف
    recording_stopped = Signal(str)  # مسار الملف النهائي
    recording_error = Signal(str)    # رسالة الخطأ
    progress_updated = Signal(float) # نسبة التقدم
    
    SUPPORTED_FORMATS = ['mp3', 'wav', 'flac', 'aac', 'ogg']
    
    def __init__(self, output_dir: str = None):
        super().__init__()
        self.output_dir = output_dir or self._get_default_output_dir()
        self.is_recording = False
        self.current_file = None
        self.start_time = None
        self.duration = 0
        self._thread = None
        self._stop_flag = False
        
        # إنشاء مجلد التسجيل
        os.makedirs(self.output_dir, exist_ok=True)
        
    def _get_default_output_dir(self) -> str:
        """الحصول على مجلد التسجيل الافتراضي"""
        import platform
        if platform.system() == 'Windows':
            return os.path.join(os.environ['USERPROFILE'], 'Music', 'WaveSphere Recordings')
        else:
            return os.path.join(os.path.expanduser('~'), 'Music', 'WaveSphere Recordings')
            
    def start_recording(self, stream_url: str, format: str = 'mp3', 
                       filename: str = None, auto_split: bool = False) -> bool:
        """
        بدء التسجيل
        
        Args:
            stream_url: رابط البث
            format: صيغة الملف (mp3, wav, flac, aac, ogg)
            filename: اسم الملف (اختياري)
            auto_split: التقسيم التلقائي للأغاني
            
        Returns:
            bool: نجاح العملية
        """
        if self.is_recording:
            return False
            
        if format not in self.SUPPORTED_FORMATS:
            self.recording_error.emit(f"صيغة غير مدعومة: {format}")
            return False
            
        try:
            # إنشاء اسم الملف
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"recording_{timestamp}.{format}"
            elif not filename.endswith(f".{format}"):
                filename += f".{format}"
                
            self.current_file = os.path.join(self.output_dir, filename)
            
            # بدء خيط التسجيل
            self._stop_flag = False
            self._thread = threading.Thread(
                target=self._record_thread,
                args=(stream_url, self.current_file, format, auto_split),
                daemon=True
            )
            self._thread.start()
            
            self.is_recording = True
            self.start_time = time.time()
            self.recording_started.emit(self.current_file)
            
            return True
            
        except Exception as e:
            self.recording_error.emit(str(e))
            return False
            
    def _record_thread(self, stream_url: str, output_file: str, format: str, auto_split: bool):
        """خيط التسجيل"""
        # سيتم تنفيذ تسجيل البث باستخدام FFmpeg هنا
        # مثال: subprocess.run(['ffmpeg', '-i', stream_url, '-codec', 'copy', output_file])
        
        while not self._stop_flag:
            time.sleep(0.1)
            self.duration = time.time() - self.start_time
            # تحديث التقدم يمكن تنفيذه هنا
            
        # حفظ الملف النهائي
        self.recording_stopped.emit(output_file)
        
    def stop_recording(self) -> Optional[str]:
        """
        إيقاف التسجيل
        
        Returns:
            str: مسار الملف المسجل أو None
        """
        if not self.is_recording:
            return None
            
        self._stop_flag = True
        if self._thread:
            self._thread.join(timeout=5.0)
            
        final_file = self.current_file
        self.is_recording = False
        self.current_file = None
        self.duration = 0
        
        return final_file
        
    def pause_recording(self):
        """إيقاف مؤقت للتسجيل"""
        pass
        
    def resume_recording(self):
        """استئناف التسجيل"""
        pass
        
    def get_recording_duration(self) -> float:
        """الحصول على مدة التسجيل الحالية"""
        if self.is_recording:
            return time.time() - self.start_time
        return self.duration
        
    def set_output_directory(self, directory: str):
        """تعيين مجلد التسجيل"""
        os.makedirs(directory, exist_ok=True)
        self.output_dir = directory
        
    def get_recordings_list(self) -> list:
        """الحصول على قائمة التسجيلات"""
        recordings = []
        if os.path.exists(self.output_dir):
            for file in os.listdir(self.output_dir):
                if any(file.endswith(f".{fmt}") for fmt in self.SUPPORTED_FORMATS):
                    filepath = os.path.join(self.output_dir, file)
                    recordings.append({
                        'name': file,
                        'path': filepath,
                        'size': os.path.getsize(filepath),
                        'created': datetime.fromtimestamp(os.path.getctime(filepath))
                    })
        return sorted(recordings, key=lambda x: x['created'], reverse=True)
        
    def delete_recording(self, filepath: str) -> bool:
        """حذف تسجيل"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception:
            return False
            
    def export_recording(self, input_path: str, output_format: str, 
                        output_path: str = None) -> Optional[str]:
        """
        تصدير تسجيل بصيغة مختلفة
        
        Args:
            input_path: مسار الملف الأصلي
            output_format: الصيغة المطلوبة
            output_path: مسار الملف الجديد (اختياري)
            
        Returns:
            str: مسار الملف الجديد أو None
        """
        if output_path is None:
            basename = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(
                self.output_dir,
                f"{basename}_exported.{output_format}"
            )
            
        # سيتم تنفيذ التحويل باستخدام FFmpeg هنا
        return output_path
