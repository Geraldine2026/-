"""
predictor.py - 完结预测模块
AI核心价值：模式识别 + 智能推算
"""

import yaml
from datetime import datetime, timedelta
from typing import Dict, Optional
import os


def load_schedule_rules() -> Dict:
    """加载播出规律配置"""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "references", "schedule_rules.yaml"
    )
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return {d['name']: d for d in data.get('dramas', [])}
    except FileNotFoundError:
        return {}


def predict_completion(drama_name: str, current_episode: Optional[int] = None) -> str:
    """
    预测剧集的完结日期
    
    Args:
        drama_name: 剧名
        current_episode: 当前集数（可选，默认使用模拟数据）
        
    Returns:
        str: 格式化的预测结果
    """
    
    # 模拟当前进度（如果未提供）
    if current_episode is None:
        mock_progress = {
            "黑暗荣耀": 8,
            "繁花": 12,
            "庆余年2": 15,
            "狂飙": 39,
            "三体": 20,
            "莲花楼": 30,
            "长相思2": 5,
            "边水往事": 10,
        }
        current_episode = mock_progress.get(drama_name, 0)
    
    rules = load_schedule_rules()
    
    if drama_name not in rules:
        return f"❌ 未找到《{drama_name}》的播出规律，请先添加配置"
    
    drama = rules[drama_name]
    total = drama.get('total_episodes', 0)
    per_week = drama.get('episodes_per_week', 1)
    air_days = drama.get('air_days', [])
    
    if current_episode >= total:
        return f"✅ 《{drama_name}》已完结！共 {total} 集"
    
    remaining = total - current_episode
    weeks_needed = (remaining + per_week - 1) // per_week  # 向上取整
    
    # 计算预计完结日期
    today = datetime.now()
    # 找最近的播出日
    weekday_map = {"周一": 0, "周二": 1, "周三": 2, "周四": 3, "周五": 4, "周六": 5, "周日": 6}
    
    if air_days:
        # 计算离最近播出日的天数
        today_weekday = today.weekday()
        target_weekday = weekday_map.get(air_days[0], 0)
        days_until = (target_weekday - today_weekday) % 7
        if days_until == 0:
            days_until = 7  # 今天不是播出日，推到下周
        next_air = today + timedelta(days=days_until)
        
        # 计算完结日期
        completion_date = next_air + timedelta(weeks=weeks_needed - 1)
        completion_str = completion_date.strftime("%Y-%m-%d")
        
        # 计算周数
        weeks_from_now = weeks_needed
    else:
        completion_str = "未知（请配置播出日）"
        weeks_from_now = weeks_needed
    
    # AI智能分析：生成个性化预测报告
    progress_percent = (current_episode / total) * 100
    
    output = []
    output.append(f"🔮 《{drama_name}》完结预测")
    output.append("")
    output.append(f"📺 总集数：{total} 集")
    output.append(f"📌 当前进度：第 {current_episode} 集（已追 {progress_percent:.1f}%）")
    output.append(f"📅 播出规律：每周 {per_week} 集，更新日 {', '.join(air_days)}")
    output.append(f"⏳ 剩余集数：{remaining} 集")
    output.append(f"📆 预计完结日期：{completion_str}（距今约 {weeks_from_now} 周）")
    output.append(f"⚡ 距离完结还有：{remaining} 集 / {weeks_from_now} 周")
    output.append("")
    
    # AI建议
    if progress_percent < 30:
        output.append("🌟 才刚开始追，慢慢享受！")
    elif progress_percent < 60:
        output.append("🔥 剧情渐入佳境，继续追！")
    elif progress_percent < 90:
        output.append("⚡ 快追完了，冲刺！")
    else:
        output.append("🎉 马上追完了，期待大结局！")
    
    return "\n".join(output)


if __name__ == "__main__":
    print("=" * 50)
    print("🔮 完结预测测试")
    print("=" * 50)
    print()
    
    test_dramas = ["黑暗荣耀", "繁花", "庆余年2", "长相思2"]
    for drama in test_dramas:
        print(predict_completion(drama))
        print()
