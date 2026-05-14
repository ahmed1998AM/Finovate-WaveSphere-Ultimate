# 🌊 Finovate WaveSphere Ultimate

<div dir="rtl" align="right">

## منصة راديو عالمية متقدمة

**الإصدار:** 1.0.0  
**المطور:** Ahmed Mostafa Ibrahim  
**العلامة التجارية:** Finovate – AHMED EG  

---

## 📋 المحتويات

- [نظرة عامة](#نظرة-عامة)
- [المميزات الرئيسية](#المميزات-الرئيسية)
- [الهيكل البرمجي](#الهيكل-البرمجي)
- [التثبيت](#التثبيت)
- [الاستخدام](#الاستخدام)
- [الوحدات النمطية](#الوحدات-النمطية)
- [التقنيات المستخدمة](#التقنيات-المستخدمة)
- [معلومات المطور](#معلومات-المطور)

---

## نظرة عامة

Finovate WaveSphere Ultimate هي منصة بث إذاعي عالمية متطورة تم بناؤها بالكامل باستخدام Python، featuring:

- 🎵 **محطات راديو عالمية** - وصول إلى +30,000 محطة من 5 مصادر عالمية
- 🤖 **ذكاء اصطناعي** - توصيات ذكية، تحسين صوت، ترجمة تلقائية
- 🔊 **صوت متقدم** - تعزيز حتى 600%، معادل 31 نطاق، إزالة ضوضاء
- 🎨 **واجهة عصرية** - 6 سمات، تأثيرات بصرية، دعم RTL
- ☁️ **مزامنة سحابية** - مزامنة المفضلة، الإعدادات، سجل الاستماع
- 🔴 **تسجيل** - تسجيل مباشر، مجدول، تقسيم تلقائي
- 🔌 **إضافات** - تكامل Spotify، Discord، OBS

---

## المميزات الرئيسية

### 📻 نظام الراديو
- ✅ 5 مصادر عالمية (Radio Browser, Shoutcast, Icecast, OnlineRadioBox, MyTuner)
- ✅ دعم 30+ دولة و 30+ تصنيف
- ✅ بحث متقدم حسب الدولة، النوع، اللغة
- ✅ تحديث تلقائي للمحطات كل 6 ساعات
- ✅ إزالة الروابط المعطلة تلقائياً
- ✅ نظام مفضلة وسجل استماع

### 🤖 الذكاء الاصطناعي
- ✅ توصيات محطات مخصصة
- ✅ تحسين الصوت بالذكاء الاصطناعي (إزالة ضوضاء، إصلاح تشوهات)
- ✅ ترجمة البيانات الوصفية (9 لغات)
- ✅ كشف اللغة التلقائي
- ✅ تصنيف ذكي للمحطات
- ✅ تحسين جودة البث التكيفي

### 🔊 نظام الصوت
- ✅ تعزيز صوت حتى 600% مع anti-clipping
- ✅ معادل 31 نطاق مع 12 إعداد مسبق
- ✅ مؤثرات صوتية (3D Surround, Reverb, Echo)
- ✅ إزالة ضوضاء بالذكاء الاصطناعي
- ✅ ضغط ديناميكي ذكي
- ✅ دعم جميع الصيغ (MP3, AAC, FLAC, OGG, Opus)

### 🎨 واجهة المستخدم
- ✅ 6 سمات (Neon Cyberpunk, Glass Morphism, Dark Professional, etc.)
- ✅ مرئيات صوتية (Wave, Spectrum, Particles)
- ✅ دعم كامل لـ RTL (العربية)
- ✅ مشغل مصغر عائم
- ✅ أزرار بتأثير توهج
- ✅ تحريك سلس GPU-accelerated

### ☁️ المزامنة السحابية
- ✅ مزامنة المفضلة عبر الأجهزة
- ✅ مزامنة الإعدادات
- ✅ سجل استماع سحابي
- ✅ قوائم تشغيل سحابية
- ✅ نسخ احتياطي واستعادة

### 🔴 نظام التسجيل
- ✅ تسجيل مباشر للبث
- ✅ تسجيل مجدول (يومي، أسبوعي، لمرة واحدة)
- ✅ تقسيم تلقائي للأغاني
- ✅ صيغ متعددة (MP3, WAV, FLAC, AAC, OGG)
- ✅ تصدير وتحويل الصيغ

### 🔌 نظام الإضافات
- ✅ تكامل Spotify
- ✅ Discord Rich Presence
- ✅ OBS Studio Integration
- ✅ نظام إضافات قابل للتوسع

---

## الهيكل البرمجي

```
/workspace/
├── core/               # النواة الأساسية
│   ├── constants.py    # الثوابت والإعدادات
│   ├── config.py       # مدير التكوين
│   └── application.py  # وحدة التحكم الرئيسية
│
├── audio_engine/       # محرك الصوت
│   ├── engine.py       # محرك التشغيل VLC/FFmpeg
│   ├── equalizer.py    # المعادل 31 نطاق
│   ├── volume_boost.py # تعزيز الصوت 600%
│   └── dsp.py          # معالجة الإشارات
│
├── radio_sources/      # مصادر الراديو
│   ├── radio_browser.py
│   ├── shoutcast.py
│   ├── icecast.py
│   ├── onlineradiobox.py
│   ├── mytuner.py
│   └── aggregator.py   # المجمع الموحد
│
├── ai_system/          # نظام الذكاء الاصطناعي
│   ├── audio_enhancement.py
│   ├── station_recommender.py
│   ├── metadata_translator.py
│   ├── language_detector.py
│   ├── smart_categorizer.py
│   └── quality_optimizer.py
│
├── ui/                 # واجهة المستخدم
│   ├── main_window.py  # النافذة الرئيسية
│   ├── theme_manager.py # مدير السمات
│   └── widgets.py      # المكونات المخصصة
│
├── recording/          # التسجيل
│   ├── recorder.py     # المسجل
│   └── scheduler.py    # المجدول
│
├── cloud_sync/         # المزامنة السحابية
│   ├── sync_engine.py  # محرك المزامنة
│   └── models.py       # النماذج
│
├── plugins/            # الإضافات
│   ├── plugin_manager.py
│   └── plugins/
│       ├── spotify.py
│       ├── discord.py
│       └── obs.py
│
├── network/            # الشبكة
│   ├── stream_optimizer.py
│   ├── auto_reconnect.py
│   └── bandwidth_manager.py
│
├── security/           # الأمان
│   ├── url_filter.py
│   ├── sandbox.py
│   └── encryption.py
│
├── installer/          # التثبيت
└── assets/             # الموارد
```

---

## التثبيت

### المتطلبات
- Python 3.13+
- FFmpeg
- VLC Media Player

### تثبيت المكتبات
```bash
pip install pyside6 python-vlc ffmpeg-python numpy scipy \
            librosa sounddevice pyaudio aiohttp requests \
            websockets sqlalchemy psycopg2 redis torch \
            transformers whisper pyinstaller
```

### تشغيل التطبيق
```bash
python main.py
```

### بناء التطبيق
```bash
# Windows
pyinstaller --onefile --windowed main.spec

# Linux
flatpak build

# macOS
dmgbuild -s settings.py "WaveSphere.dmg"
```

---

## الاستخدام

### مثال بسيط
```python
from core.application import Application
from radio_sources.aggregator import RadioAggregator
from audio_engine.engine import AudioEngine

# إنشاء التطبيق
app = Application()

# الحصول على المحطات
aggregator = RadioAggregator()
stations = aggregator.search(country="Egypt", genre="Music")

# تشغيل محطة
engine = AudioEngine()
engine.play(stations[0]['url'])

# تعيين الصوت (600%)
engine.set_volume(600)
```

### استخدام الذكاء الاصطناعي
```python
from ai_system.station_recommender import StationRecommender
from ai_system.audio_enhancement import AudioEnhancement

# توصيات
recommender = StationRecommender()
recommendations = recommender.get_recommendations(user_history)

# تحسين الصوت
enhancer = AudioEnhancement()
enhanced_audio = enhancer.enhance(audio_data, remove_noise=True)
```

### التسجيل
```python
from recording.recorder import StreamRecorder
from recording.scheduler import RecordingScheduler

# تسجيل مباشر
recorder = StreamRecorder()
recorder.start_recording(stream_url, format='mp3')

# جدولة تسجيل
scheduler = RecordingScheduler()
scheduler.create_daily_recording(
    station_url="http://stream.url",
    hour=8, minute=0,
    duration_minutes=60,
    name="Morning Show"
)
```

---

## الوحدات النمطية

| الوحدة | الوصف | الحالة |
|--------|-------|--------|
| `core` | النواة الأساسية والتكوين | ✅ مكتمل |
| `audio_engine` | محرك الصوت والمعالجة | ✅ مكتمل |
| `radio_sources` | مصادر الراديو العالمية | ✅ مكتمل |
| `ai_system` | نظام الذكاء الاصطناعي | ✅ مكتمل |
| `ui` | واجهة المستخدم | ✅ مكتمل |
| `recording` | نظام التسجيل | ✅ مكتمل |
| `cloud_sync` | المزامنة السحابية | ✅ مكتمل |
| `plugins` | نظام الإضافات | ✅ مكتمل |
| `network` | تحسين الشبكة | ⏳ قيد التطوير |
| `security` | الأمان والحماية | ⏳ قيد التطوير |
| `visualizer` | المرئيات الصوتية | ⏳ قيد التطوير |

---

## التقنيات المستخدمة

### Backend
- Python 3.13+
- AsyncIO, Threading, Multiprocessing

### UI Framework
- PySide6 / Qt6
- QML / QtQuick

### Audio Engine
- FFmpeg, VLC, PyAudio
- sounddevice, librosa
- NumPy, SciPy

### AI Systems
- PyTorch, Transformers
- Whisper, TensorFlow

### Database
- SQLite, PostgreSQL, Redis

### Networking
- aiohttp, requests, websockets

---

## معلومات المطور

### 👨‍💻 Ahmed Mostafa Ibrahim
**Finovate – AHMED EG**

- 📧 **Email:** gogom8870@gmail.com
- 📱 **Phone:** 01225155329
- 💼 **GitHub:** [@ahmed1998AM](https://github.com/ahmed1998AM)
- 👥 **Facebook:** [AHMED EG](https://www.facebook.com/profile.php?id=100049475271023)

---

## الشعار والهوية

- **الشعار:** 🌊 WaveSphere - كرة صوتية نيون مستقبلية
- **الشعار اللفظي:** "اسمع العالم بلا حدود"
- **الألوان:**
  - الرئيسي: `#00F5FF` (سيان نيون)
  - الثانوي: `#FFD700` (ذهبي)
  - التمييز: `#FF00FF` (وردي نيون)

---

## الترخيص

© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved

---

## الدعم

للأسئلة أو المشاكل، يرجى فتح issue على GitHub أو التواصل مباشرة عبر email.

</div>
