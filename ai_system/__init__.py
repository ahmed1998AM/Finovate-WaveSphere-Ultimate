"""
Finovate WaveSphere Ultimate - نظام الذكاء الاصطناعي
AI System for audio enhancement and smart features
المطور: Ahmed Mostafa Ibrahim - Finovate – AHMED EG
"""

from .audio_enhancement import AudioEnhancerAI
from .station_recommender import StationRecommenderAI
from .metadata_translator import MetadataTranslatorAI
from .language_detector import LanguageDetectorAI
from .smart_categorizer import SmartCategorizerAI
from .quality_optimizer import QualityOptimizerAI

__all__ = [
    'AudioEnhancerAI',
    'StationRecommenderAI',
    'MetadataTranslatorAI',
    'LanguageDetectorAI',
    'SmartCategorizerAI',
    'QualityOptimizerAI'
]

__version__ = "1.0.0"
__author__ = "Ahmed Mostafa Ibrahim"
__copyright__ = "© 2025 Ahmed Mostafa Ibrahim — All Rights Reserved"
