"""
scheduler.py - 本周追剧日程
用法：python scheduler.py
"""

from datetime import datetime, timedelta
from data_manager import get_all_dramas

WEEKDAY_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def generate_schedule() -> str:
    watch_list = get_all_dramas()
    if not watch_list:
        return "📭 暂无追剧记录，请先用 parser.py 录入数据"
    
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    
    output = []
    output.append("=" * 50)
    output.append("📅 本周追剧日程")
    output.append(f"（{week_start.strftime('%Y-%m-%d')} ~ {(week_start + timedelta(days=6)).strftime('%Y-%m-%d')}）")
    output.append("=" * 50)
    output.append("")
    
    drama_names = list(watch_list.keys())
    for i, day in enumerate(WEEKDAY_CN):
        output.append(f"【{day}】")
        day_dramas = []
        for idx, name in enumerate(drama_names):
            info = watch_list[name]
            my_ep = info.get('my_episode', 0)
            latest = info.get('latest_episode', 0)
            if idx % 7 == i:
                if my_ep < latest:
                    day_dramas.append(f"  《{name}》第 {my_ep + 1} 集（最新{latest}集）")
                else:
                    day_dramas.append(f"  《{name}》已追平 ✅")
        if day_dramas:
            output.extend(day_dramas)
        else:
            output.append("  休息一下，今天没更新")
        output.append("")
    
    total = len(drama_names)
    behind = sum(1 for n in drama_names if watch_list[n].get('my_episode', 0) < watch_list[n].get('latest_episode', 0))
    output.append("-" * 50)
    output.append(f"📊 共 {total} 部在追，{behind} 部待更新")
    
    return "\n".join(output)


def main():
    print(generate_schedule())


if __name__ == "__main__":
    main()
