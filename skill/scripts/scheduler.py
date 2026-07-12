"""
scheduler.py - 日程生成模块
AI核心价值：多源信息聚合，自动生成结构化日程
"""

import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os

# 星期映射
WEEKDAY_MAP = {
    "周一": 0, "周二": 1, "周三": 2, "周四": 3,
    "周五": 4, "周六": 5, "周日": 6
}
WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def load_schedule_rules() -> List[Dict]:
    """加载播出规律配置"""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "references", "schedule_rules.yaml"
    )
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('dramas', [])
    except FileNotFoundError:
        # 如果文件不存在，使用默认配置
        return [
            {"name": "黑暗荣耀", "total_episodes": 16, "episodes_per_week": 2, "air_days": ["周五"]},
            {"name": "繁花", "total_episodes": 30, "episodes_per_week": 2, "air_days": ["周日", "周一"]},
            {"name": "庆余年2", "total_episodes": 36, "episodes_per_week": 1, "air_days": ["周三"]},
        ]


def generate_schedule(current_episodes: Dict[str, int] = None) -> str:
    """
    生成本周追剧日历
    
    Args:
        current_episodes: 当前各剧集数，格式 {"剧名": 当前集数}
        
    Returns:
        str: 格式化的本周追剧日程表
    """
    
    if current_episodes is None:
        # 默认进度（模拟用户已录入的数据）
        current_episodes = {
            "黑暗荣耀": 8,
            "繁花": 12,
            "庆余年2": 15,
            "狂飙": 39,
            "三体": 20,
            "莲花楼": 30,
            "长相思2": 5,
            "边水往事": 10,
        }
    
    rules = load_schedule_rules()
    
    # 构建本周日程
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    
    schedule = {day: [] for day in WEEKDAY_CN}
    
    for drama in rules:
        drama_name = drama['name']
        if drama_name not in current_episodes:
            continue
            
        current_ep = current_episodes[drama_name]
        total_ep = drama.get('total_episodes', 999)
        
        # 如果已完结，跳过
        if current_ep >= total_ep:
            continue
            
        for day in drama.get('air_days', []):
            if day in schedule:
                next_ep = current_ep + 1
                schedule[day].append({
                    "name": drama_name,
                    "episode": next_ep,
                    "total": total_ep,
                    "platform": drama.get('platform', '未知'),
                    "is_double": drama.get('episodes_per_week', 1) >= 2
                })
    
    # 生成格式化输出（模拟AI生成的日程表）
    output = []
    output.append("📅 本周追剧日历")
    output.append(f"（{week_start.strftime('%Y-%m-%d')} ~ {(week_start + timedelta(days=6)).strftime('%Y-%m-%d')}）")
    output.append("")
    output.append("┌─────────┬──────────────────────────────────────┐")
    
    for day in WEEKDAY_CN:
        entries = schedule.get(day, [])
        if entries:
            entry_texts = []
            for e in entries:
                text = f"《{e['name']}》更新第 {e['episode']} 集"
                if e.get('is_double'):
                    text += f" ⭐ 双更"
                entry_texts.append(text)
            content = "、".join(entry_texts)
            output.append(f"│ {day}     │ {content:<36} │")
        else:
            output.append(f"│ {day}     │ {'（无更新，休息一下）':<36} │")
    
    output.append("└─────────┴──────────────────────────────────────┘")
    
    # 统计信息（模拟AI生成分析）
    total_updates = sum(len(entries) for entries in schedule.values())
    output.append("")
    output.append(f"📊 本周共 {total_updates} 集更新")
    
    # AI智能建议
    if total_updates > 10:
        output.append("🔥 本周更新很多，追剧快乐！")
    elif total_updates > 5:
        output.append("📺 适中的更新量，轻松追剧")
    else:
        output.append("💤 本周更新较少，可以补补老剧")
    
    # AI推荐本周重点
    if "黑暗荣耀" in current_episodes and current_episodes["黑暗荣耀"] <= 10:
        output.append("⭐ 本周重点推荐：《黑暗荣耀》即将进入高潮")
    
    return "\n".join(output)


if __name__ == "__main__":
    print("=" * 50)
    print("📅 日程生成测试")
    print("=" * 50)
    print()
    print(generate_schedule())
