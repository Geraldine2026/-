"""
data_manager.py - 数据管理模块
AI核心价值：持久化存储，追剧数据CRUD操作
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional


DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    "data", "watch_data.json"
)

# 回退路径
if not os.path.exists(os.path.dirname(DATA_FILE)):
    DATA_FILE = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "..", "data", "watch_data.json"
    )


def _get_default_data() -> Dict:
    return {
        "watch_list": {},  # {"剧名": {"my_episode": 8, "latest_episode": 16, "last_update": "2026-07-12"}}
        "history": [],
        "total_count": 0
    }


def load_data() -> Dict:
    """加载追剧数据"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return _get_default_data()


def save_data(data: Dict) -> None:
    """保存追剧数据"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_or_update_drama(drama_name: str, my_episode: int, latest_episode: int) -> Dict:
    """添加或更新追剧记录"""
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    data = load_data()
    
    if drama_name in data["watch_list"]:
        old = data["watch_list"][drama_name]
        data["watch_list"][drama_name] = {
            "my_episode": my_episode,
            "latest_episode": latest_episode,
            "last_update": date
        }
        action = "更新"
        message = f"✅ 已更新：《{drama_name}》{old['my_episode']}集 → {my_episode}集，最新{latest_episode}集"
    else:
        data["watch_list"][drama_name] = {
            "my_episode": my_episode,
            "latest_episode": latest_episode,
            "last_update": date
        }
        action = "新增"
        message = f"✅ 已添加：《{drama_name}》看到第{my_episode}集，最新第{latest_episode}集"
    
    data["history"].append({
        "drama_name": drama_name,
        "action": action,
        "my_episode": my_episode,
        "latest_episode": latest_episode,
        "date": date
    })
    data["total_count"] += 1
    
    save_data(data)
    return {"success": True, "message": message}


def get_drama_info(drama_name: str) -> Optional[Dict]:
    """获取单部剧信息"""
    data = load_data()
    return data.get("watch_list", {}).get(drama_name)


def get_all_dramas() -> Dict:
    """获取所有追剧记录"""
    data = load_data()
    return data.get("watch_list", {})


def get_history() -> list:
    """获取操作历史记录"""
    data = load_data()
    return data.get("history", [])


def get_summary() -> str:
    """生成追剧概览摘要"""
    data = load_data()
    watch_list = data.get("watch_list", {})
    
    if not watch_list:
        return "📭 暂无追剧记录"

    lines = []
    lines.append("-" * 50)
    lines.append("📺 追剧概览")
    lines.append("-" * 50)
    
    total = len(watch_list)
    behind_count = 0
    total_behind = 0
    
    for name, info in watch_list.items():
        my_ep = info.get('my_episode', 0)
        latest = info.get('latest_episode', 0)
        behind = latest - my_ep
        if behind > 0:
            behind_count += 1
            total_behind += behind
            lines.append(f"  📌 《{name}》第{my_ep}集 / 最新{latest}集（落后{behind}集）")
        else:
            lines.append(f"  ✅ 《{name}》第{my_ep}集（已追平）")
    
    lines.append("")
    lines.append(f"📊 共 {total} 部在追，{behind_count} 部待更新，累计落后 {total_behind} 集")
    
    return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 50)
    print("📊 数据管理测试")
    print("=" * 50)
    print()
    
    # 测试默认数据
    data = load_data()
    print(f"当前追剧列表：{len(data['watch_list'])} 部")
    print(f"历史记录：{len(data['history'])} 条")
    print()
    
    # 测试添加
    result = add_or_update_drama("黑暗荣耀", 8, 16)
    print(result["message"])
    
    result = add_or_update_drama("繁花", 12, 30)
    print(result["message"])
    
    result = add_or_update_drama("庆余年2", 15, 36)
    print(result["message"])
    print()
    
    # 测试更新
    result = add_or_update_drama("黑暗荣耀", 9, 16)
    print(result["message"])
    print()
    
    # 测试查询
    info = get_drama_info("黑暗荣耀")
    print(f"📺 《黑暗荣耀》信息：{info}")
    
    info = get_drama_info("不存在的剧")
    print(f"📺 《不存在的剧》信息：{info}")
