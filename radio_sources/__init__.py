"""
Finovate WaveSphere Ultimate - Radio Sources Module
مصادر محطات الراديو العالمية
المطور: Ahmed Mostafa Ibrahim - Finovate – AHMED EG
"""

from .radio_browser import RadioBrowserAPI
from .shoutcast import ShoutcastAPI
from .icecast import IcecastAPI
from .onlineradiobox import OnlineRadioBoxAPI
from .mytuner import MyTunerAPI
from .aggregator import RadioAggregator

__all__ = [
    'RadioBrowserAPI',
    'ShoutcastAPI', 
    'IcecastAPI',
    'OnlineRadioBoxAPI',
    'MyTunerAPI',
    'RadioAggregator'
]

__version__ = "1.0.0"
__author__ = "Ahmed Mostafa Ibrahim"
__copyright__ = "© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved"
