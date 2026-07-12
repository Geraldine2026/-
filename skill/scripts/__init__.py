"""
追剧日历管家 - 核心脚本模块
"""

from .parser import parse_drama_input
from .scheduler import generate_schedule
from .predictor import predict_completion
from .recommender import recommend_dramas
from .recap import generate_recap

__all__ = [
    'parse_drama_input',
    'generate_schedule',
    'predict_completion',
    'recommend_dramas',
    'generate_recap'
]
