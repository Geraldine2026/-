"""
追剧日历管家 - 核心脚本模块
"""

from .parser import parse_drama_input
from .scheduler import generate_schedule
from .predictor import predict_completion
from .recommender import recommend_dramas
from .recap import generate_recap
from .data_manager import (
    load_data,
    save_data,
    add_or_update_drama,
    get_all_dramas,
    get_drama_info,
    get_summary,
    delete_drama
)

__all__ = [
    # 用户功能接口
    'parse_drama_input',
    'generate_schedule',
    'predict_completion',
    'recommend_dramas',
    'generate_recap',
    # 数据管理接口
    'load_data',
    'save_data',
    'add_or_update_drama',
    'get_all_dramas',
    'get_drama_info',
    'get_summary',
    'delete_drama'
]
