"""
predictor.py - 完结预测
用法：python predictor.py "剧名"
"""

import sys
from datetime import datetime, timedelta
from data_manager import get_drama_info, get_all_dramas


def predict_completion(drama_name: str) -> str:
    info = get_drama_info(drama_name)
    if not info:
        return f"❌ 未找到《{drama_name}》，请先录入"
    
    my_ep = info.get('my_episode', 0)
    latest = info.get('latest_episode', 0)
    remaining = latest - my_ep
    
    output = []
    output.append("=" * 50)
    output.append(f"🔮 《{drama_name}》完结预测")
    output.append("=" * 50)
    output.append("")
    output.append(f"📌 你看到：第 {my_ep} 集")
    output.append(f"📌 最新到：第 {latest} 集")
    output.append(f"⏳ 剩余：{remaining} 集")
    
    if remaining <= 0:
        output.append("🎉 你已经追平了！")
    else:
        today = datetime.now()
        finish_date = today + timedelta(days=remaining)
        output.append(f"📆 按每天1集，预计 {finish_date.strftime('%Y-%m-%d')} 追完")
        if remaining <= 3:
            output.append("💪 快追完了，加油！")
        elif remaining <= 7:
            output.append("🔥 一周内能追完，坚持！")
        else:
            output.append(f"📺 还有 {remaining} 集，慢慢享受")
    
    return "\n".join(output)


def main():
    if len(sys.argv) > 1:
        drama_name = sys.argv[1]
    else:
        print("=" * 50)
        print("🔮 完结预测工具")
        print("=" * 50)
        print()
        all_dramas = list(get_all_dramas().keys())
        if all_dramas:
            print("在追剧集：")
            for i, name in enumerate(all_dramas, 1):
                print(f"  {i}. {name}")
            print()
        drama_name = input("请输入剧名：").strip()
    
    if not drama_name:
        print("❌ 请提供剧名")
        return
    
    print()
    print(predict_completion(drama_name))


if __name__ == "__main__":
    main()
