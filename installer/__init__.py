"""
Finovate WaveSphere Ultimate - Installer Module
وحدة التثبيت والحزم
© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional, Dict
import json
import logging

logger = logging.getLogger(__name__)


class InstallerConfig:
    """إعدادات المثبت"""
    
    APP_NAME = "WaveSphere"
    VERSION = "1.0.0"
    AUTHOR = "Ahmed Mostafa Ibrahim"
    COMPANY = "Finovate – AHMED EG"
    DESCRIPTION = "Professional Global Desktop Radio Streaming Platform"
    EMAIL = "gogom8870@gmail.com"
    WEBSITE = "https://github.com/ahmed1998AM"
    
    # متطلبات النظام
    MIN_PYTHON_VERSION = (3, 13)
    REQUIRED_PACKAGES = [
        "pyside6",
        "python-vlc",
        "ffmpeg-python",
        "numpy",
        "scipy",
        "librosa",
        "sounddevice",
        "pyaudio",
        "aiohttp",
        "requests",
        "websockets",
        "sqlalchemy",
        "torch",
        "transformers",
    ]


class BaseInstaller:
    """فئة المثبت الأساسية"""
    
    def __init__(self, config: InstallerConfig):
        self.config = config
        self.install_path: Optional[Path] = None
    
    def check_python_version(self) -> bool:
        """التحقق من إصدار Python"""
        current = sys.version_info[:2]
        required = self.config.MIN_PYTHON_VERSION
        if current < required:
            logger.error(f"Python {required[0]}.{required[1]}+ مطلوب، الحالي: {current[0]}.{current[1]}")
            return False
        logger.info(f"✓ Python {current[0]}.{current[1]} مدعوم")
        return True
    
    def install_packages(self, packages: List[str]) -> bool:
        """تثبيت الحزم المطلوبة"""
        try:
            cmd = [sys.executable, "-m", "pip", "install", "--upgrade"] + packages
            subprocess.run(cmd, check=True)
            logger.info("✓ تم تثبيت الحزم المطلوبة")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"فشل تثبيت الحزم: {e}")
            return False
    
    def create_shortcut(self, name: str, target: str, icon: str = ""):
        """إنشاء اختصار (يتم تنفيذه حسب النظام)"""
        raise NotImplementedError


class WindowsInstaller(BaseInstaller):
    """مثبت Windows باستخدام PyInstaller و Inno Setup"""
    
    def __init__(self, config: InstallerConfig):
        super().__init__(config)
        self.spec_file = "wavesphere.spec"
        self.iss_file = "installer.iss"
    
    def create_pyinstaller_spec(self) -> str:
        """إنشاء ملف مواصفات PyInstaller"""
        spec_content = f'''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('themes', 'themes'),
    ],
    hiddenimports={json.dumps(self.config.REQUIRED_PACKAGES)},
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{self.config.APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)
'''
        with open(self.spec_file, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        
        logger.info(f"✓ تم إنشاء {self.spec_file}")
        return self.spec_file
    
    def build_exe(self) -> bool:
        """بناء ملف EXE"""
        try:
            subprocess.run([sys.executable, "-m", "PyInstaller", self.spec_file], check=True)
            logger.info("✓ تم بناء WaveSphere.exe")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"فشل البناء: {e}")
            return False
    
    def create_inno_setup_script(self) -> str:
        """إنشاء سكربت Inno Setup"""
        iss_content = f'''
#define MyAppName "{self.config.APP_NAME}"
#define MyAppVersion "{self.config.VERSION}"
#define MyAppPublisher "{self.config.COMPANY}"
#define MyAppExeName "{self.config.APP_NAME}.exe"

[Setup]
AppId={{{{D1A3B5C7-E9F1-4A3B-8C5D-7E9F1A3B5C7D}}}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={self.config.WEBSITE}
AppSupportURL={self.config.WEBSITE}
AppUpdatesURL={self.config.WEBSITE}
DefaultDirName={{autopf}}\\{{#MyAppName}}
DefaultGroupName={{#MyAppName}}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=output
OutputBaseFilename=WaveSphere_Setup
SetupIconFile=assets\\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "arabic"; MessagesFile: "compiler:Languages\\Arabic.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "dist\\{self.config.APP_NAME}\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{autodesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon
Name: "{{userappdata}}\\QuickLaunch\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: quicklaunchicon

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
var
  Version: TVersion;
begin
  GetWindowsVersion(Version);
  if Version.Major < 10 then
  begin
    MsgBox('Windows 10 or higher is required!', mbError, MB_OK);
    Result := False;
  end
  else
    Result := True;
end;
'''
        with open(self.iss_file, 'w', encoding='utf-8') as f:
            f.write(iss_content)
        
        logger.info(f"✓ تم إنشاء {self.iss_file}")
        return self.iss_file
    
    def full_install(self) -> bool:
        """عملية التثبيت الكاملة"""
        print("=" * 50)
        print(f"📦 تثبيت {self.config.APP_NAME} v{self.config.VERSION}")
        print("=" * 50)
        
        # التحقق من Python
        if not self.check_python_version():
            return False
        
        # تثبيت الحزم
        if not self.install_packages(self.config.REQUIRED_PACKAGES):
            return False
        
        # إنشاء spec file
        self.create_pyinstaller_spec()
        
        # بناء EXE
        if not self.build_exe():
            return False
        
        # إنشاء Inno Setup script
        self.create_inno_setup_script()
        
        print("\n✅ اكتمل التثبيت!")
        print(f"📁 الملف الناتج: output/WaveSphere_Setup.exe")
        return True


class LinuxInstaller(BaseInstaller):
    """مثبت Linux باستخدام AppImage و Flatpak"""
    
    def __init__(self, config: InstallerConfig):
        super().__init__(config)
        self.desktop_file = "wavesphere.desktop"
        self.appimage_recipe = "AppImage.yml"
    
    def create_desktop_file(self) -> str:
        """إنشاء ملف .desktop"""
        desktop_content = f'''[Desktop Entry]
Version=1.0
Type=Application
Name={self.config.APP_NAME}
GenericName=Radio Streaming
Comment={self.config.DESCRIPTION}
Exec=wavesphere %U
Icon=wavesphere
Categories=AudioVideo;Audio;Player;
Keywords=radio;streaming;music;podcast;
MimeType=x-scheme-handler/radio;
StartupNotify=true
StartupWMClass=wavesphere
'''
        with open(self.desktop_file, 'w') as f:
            f.write(desktop_content)
        
        logger.info(f"✓ تم إنشاء {self.desktop_file}")
        return self.desktop_file
    
    def create_appimage_recipe(self) -> str:
        """إنشاء وصفة AppImage"""
        recipe = f'''app: {self.config.APP_NAME}

ingredients:
  dist: focal
  sources:
    - deb http://archive.ubuntu.com/ubuntu/ focal main universe
  apt:
    - python3
    - python3-pip
    - libvlc-dev
    - ffmpeg
  ppas:
    - deafbox/ppa

script:
  - cp {self.desktop_file} ./usr/share/applications/
  - mkdir -p ./usr/share/icons/hicolor/256x256/apps
  - cp assets/icon.png ./usr/share/icons/hicolor/256x256/apps/wavesphere.png
'''
        with open(self.appimage_recipe, 'w') as f:
            f.write(recipe)
        
        logger.info(f"✓ تم إنشاء {self.appimage_recipe}")
        return self.appimage_recipe
    
    def create_flatpak_manifest(self) -> dict:
        """إنشاء manifest لـ Flatpak"""
        manifest = {
            "id": "com.finovate.wavesphere",
            "runtime": "org.freedesktop.Platform",
            "runtime-version": "22.08",
            "sdk": "org.freedesktop.Sdk",
            "command": "wavesphere",
            "finish-args": [
                "--share=network",
                "--share=ipc",
                "--socket=fallback-x11",
                "--socket=wayland",
                "--device=dri",
                "--socket=pulseaudio"
            ],
            "modules": [
                {
                    "name": "wavesphere",
                    "buildsystem": "simple",
                    "build-commands": [
                        "pip3 install --prefix=/app " + " ".join(self.config.REQUIRED_PACKAGES),
                        "install -Dm755 main.py /app/bin/wavesphere",
                        f"install -Dm644 {self.desktop_file} /app/share/applications/{self.desktop_file}",
                        "install -Dm644 assets/icon.png /app/share/icons/hicolor/256x256/apps/wavesphere.png"
                    ]
                }
            ]
        }
        
        with open("flatpak-manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info("✓ تم إنشاء flatpak-manifest.json")
        return manifest


class MacOSInstaller(BaseInstaller):
    """مثبت macOS باستخدام DMG Builder"""
    
    def __init__(self, config: InstallerConfig):
        super().__init__(config)
        self.plist_file = "Info.plist"
        self.dmg_config = "dmg-config.json"
    
    def create_plist(self) -> str:
        """إنشاء ملف Info.plist"""
        plist_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>{self.config.APP_NAME}</string>
    <key>CFBundleDisplayName</key>
    <string>{self.config.APP_NAME}</string>
    <key>CFBundleIdentifier</key>
    <string>com.finovate.wavesphere</string>
    <key>CFBundleVersion</key>
    <string>{self.config.VERSION}</string>
    <key>CFBundleShortVersionString</key>
    <string>{self.config.VERSION}</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>CFBundleExecutable</key>
    <string>{self.config.APP_NAME}</string>
    <key>CFBundleIconFile</key>
    <string>icon.icns</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
    <key>NSSupportsAutomaticGraphicsSwitching</key>
    <true/>
</dict>
</plist>
'''
        with open(self.plist_file, 'w') as f:
            f.write(plist_content)
        
        logger.info(f"✓ تم إنشاء {self.plist_file}")
        return self.plist_file
    
    def create_dmg_config(self) -> str:
        """إنشاء تكوين DMG"""
        config = {
            "title": f"{self.config.APP_NAME} {self.config.VERSION}",
            "icon": "assets/icon.icns",
            "background": "assets/dmg-background.png",
            "volume_icon": "assets/volume-icon.icns",
            "contents": [
                {"x": 448, "y": 344, "type": "link", "path": "/Applications"},
                {"x": 192, "y": 344, "type": "file", "path": f"dist/{self.config.APP_NAME}.app"}
            ],
            "window_rect": ((200, 120), (640, 480)),
            "format": "UDZO",
            "compression_level": 9
        }
        
        with open(self.dmg_config, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"✓ تم إنشاء {self.dmg_config}")
        return self.dmg_config


def get_installer() -> BaseInstaller:
    """الحصول على المثبت المناسب للنظام"""
    config = InstallerConfig()
    
    if sys.platform == "win32":
        return WindowsInstaller(config)
    elif sys.platform == "linux":
        return LinuxInstaller(config)
    elif sys.platform == "darwin":
        return MacOSInstaller(config)
    else:
        raise OSError(f"نظام غير مدعوم: {sys.platform}")


# اختبار الوحدة
if __name__ == "__main__":
    print("📦 Finovate WaveSphere Installer Module")
    print("=" * 40)
    
    config = InstallerConfig()
    print(f"\n✓ التطبيق: {config.APP_NAME} v{config.VERSION}")
    print(f"✓ المطور: {config.AUTHOR}")
    print(f"✓ الشركة: {config.COMPANY}")
    print(f"✓ الحد الأدنى Python: {config.MIN_PYTHON_VERSION[0]}.{config.MIN_PYTHON_VERSION[1]}+")
    print(f"✓ الحزم المطلوبة: {len(config.REQUIRED_PACKAGES)} حزمة")
    
    installer = get_installer()
    print(f"\n✓ نوع المثبت: {type(installer).__name__}")
    print(f"✓ النظام: {sys.platform}")
    
    # التحقق من Python
    python_ok = installer.check_python_version()
    print(f"✓ التحقق من Python: {'PASS' if python_ok else 'FAIL'}")
    
    print("\n✅ وحدة التثبيت جاهزة!")
    print("\n📝 ملاحظة: للتثبيت الكامل، قم بتشغيل:")
    print("   python -m pip install -r requirements.txt")
    print("   ثم استخدم المثبت المناسب لنظامك")
