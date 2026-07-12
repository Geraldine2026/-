"""
parser.py - 追剧录入
用法：python parser.py "《黑暗荣耀》我看到第8集，最新16集"
"""

import re
import sys
from data_manager import add_or_update_drama, get_summary


def parse_user_input(user_text: str):
    """解析用户输入，提取剧名、我的集数、最新集数"""
    if not user_text:
        return None
    
    drama_name = None
    
    # 提取剧名
    match = re.search(r'[《「](.+?)[》」]', user_text)
    if match:
        drama_name = match.group(1).strip()
    
    if not drama_name:
        patterns = [
            r'^(.+?)[，,、\s]+我',
            r'^(.+?)[，,、\s]+更新',
            r'^(.+?)\s+第',
            r'^(.+?)[/／]',
        ]
        for pattern in patterns:
            match = re.search(pattern, user_text)
            if match:
                drama_name = match.group(1).strip()
                break
    
    if not drama_name:
        return None
    
    # 提取我的集数
    my_episode = None
    patterns_my = [
        r'我[看到]?第?(\d+)集',
        r'看到第?(\d+)集',
        r'追到第?(\d+)集',
        r'我[看]?\s*(\d+)\s*集',
    ]
    for pattern in patterns_my:
        match = re.search(pattern, user_text)
        if match:
            my_episode = int(match.group(1))
            break
    
    # 提取最新集数
    latest_episode = None
    patterns_latest = [
        r'最新到第?(\d+)集',
        r'最新\s*(\d+)集',
        r'更新到第?(\d+)集',
        r'\d+\s*[/／]\s*(\d+)',
    ]
    for pattern in patterns_latest:
        match = re.search(pattern, user_text)
        if match:
            latest_episode = int(match.group(1))
            break
    
    # 如果我的集数没提取到，尝试从 8/16 格式提取
    if not my_episode:
        match = re.search(r'(\d+)\s*[/／]\s*(\d+)', user_text)
        if match:
            my_episode = int(match.group(1))
            if not latest_episode:
                latest_episode = int(match.group(2))
    
    if not my_episode:
        return None
    if not latest_episode:
        latest_episode = my_episode
    
    return (drama_name, my_episode, latest_episode)


def main():
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        print("=" * 50)
        print("📺 追剧录入工具")
        print("=" * 50)
        print()
        print("支持格式：")
        print("  《黑暗荣耀》我看到第8集，最新16集")
        print("  黑暗荣耀 我8 更新16")
        print("  繁花 12/30")
        print()
        user_input = input("请输入追剧信息：").strip()
    
    if not user_input:
        print("❌ 未输入任何内容")
        return
    
    result = parse_user_input(user_input)
    if not result:
        print("❌ 无法解析，请按格式输入")
        print("   示例：《黑暗荣耀》我看到第8集，最新16集")
        return
    
    drama_name, my_episode, latest_episode = result
    save_result = add_or_update_drama(drama_name, my_episode, latest_episode)
    print()
    print(save_result["message"])
    
    behind = latest_episode - my_episode
    if behind > 0:
        print(f"⏳ 你落后 {behind} 集，加油追！")
    elif behind == 0:
        print("🎉 已追平最新更新！")
    else:
        print("🚀 你比平台更新还超前！")
    
    print()
    print(get_summary())


if __name__ == "__main__":
    main()
