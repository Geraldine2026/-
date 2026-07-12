"""
recommender.py - 智能推荐模块
AI核心价值：兴趣画像分析 + 个性化推荐
"""

import json
import os
import random
from typing import List, Dict


def load_watch_history() -> Dict:
    """加载追剧历史"""
    history_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "skill", "references", "sample_history.json"
    )
    
    # 如果找不到，尝试相对路径
    if not os.path.exists(history_path):
        history_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "references", "sample_history.json"
        )
    
    try:
        with open(history_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # 返回默认数据
        return {
            "watch_history": [
                {"drama_name": "黑暗荣耀", "status": "watching", "current_episode": 8, "rating": 9, "tags": ["悬疑", "复仇", "韩剧"]},
                {"drama_name": "繁花", "status": "watching", "current_episode": 12, "rating": 8, "tags": ["年代", "商战", "国产剧"]},
                {"drama_name": "庆余年2", "status": "watching", "current_episode": 15, "rating": 7, "tags": ["古装", "权谋"]},
                {"drama_name": "狂飙", "status": "completed", "current_episode": 39, "rating": 10, "tags": ["犯罪", "悬疑"]},
            ],
            "preferences": {"favorite_genres": ["悬疑", "古装", "国产剧"]}
        }


def recommend_dramas(limit: int = 3) -> str:
    """
    基于追剧历史智能推荐
    """
    
    data = load_watch_history()
    history = data.get('watch_history', [])
    prefs = data.get('preferences', {})
    
    # AI模拟推荐池
    candidate_pool = [
        {"name": "狂飙", "genre": "犯罪悬疑", "rating": 8.5, "desc": "扫黑除恶题材，张译主演"},
        {"name": "漫长的季节", "genre": "悬疑年代", "rating": 9.4, "desc": "东北悬疑，豆瓣高分"},
        {"name": "三体", "genre": "科幻悬疑", "rating": 8.7, "desc": "科幻巨制，刘慈欣原著"},
        {"name": "莲花楼", "genre": "武侠悬疑", "rating": 8.3, "desc": "江湖探案，成毅主演"},
        {"name": "甄嬛传", "genre": "古装宫斗", "rating": 9.4, "desc": "宫斗巅峰，经典永不过时"},
        {"name": "琅琊榜", "genre": "古装权谋", "rating": 9.4, "desc": "权谋巅峰，胡歌主演"},
        {"name": "去有风的地方", "genre": "治愈爱情", "rating": 8.0, "desc": "慢生活治愈，刘亦菲主演"},
        {"name": "边水往事", "genre": "悬疑犯罪", "rating": 8.2, "desc": "悬疑犯罪，郭麒麟主演"},
    ]
    
    # 获取用户已看过的剧名
    watched_names = [h['drama_name'] for h in history]
    
    # 过滤：移除已看过的剧
    candidates = [c for c in candidate_pool if c['name'] not in watched_names]
    
    # 如果候选为空，补充一些
    if not candidates:
        candidates = [
            {"name": "白夜追凶", "genre": "悬疑犯罪", "rating": 9.0, "desc": "经典悬疑，潘粤明主演"},
            {"name": "隐秘的角落", "genre": "悬疑", "rating": 8.8, "desc": "国产悬疑佳作"},
            {"name": "沉默的真相", "genre": "悬疑犯罪", "rating": 9.0, "desc": "社会派悬疑"},
        ]
    
    # AI分析用户偏好
    favorite_genres = prefs.get('favorite_genres', ['悬疑', '古装', '国产剧'])
    
    # AI计算匹配分
    scored = []
    for candidate in candidates:
        score = 0
        # 偏好匹配
        for genre in favorite_genres:
            if genre in candidate['genre']:
                score += 3
            if genre in candidate.get('desc', ''):
                score += 2
        
        # 评分加分
        if candidate['rating'] >= 9.0:
            score += 3
        elif candidate['rating'] >= 8.0:
            score += 2
        
        # 随机因素
        score += random.randint(0, 2)
        
        scored.append({**candidate, "score": score})
    
    # 按分数排序
    scored.sort(key=lambda x: x['score'], reverse=True)
    recommendations = scored[:limit]
    
    # 生成推荐输出
    output = []
    output.append("💡 根据你的追剧历史，AI为你推荐：")
    output.append("")
    
    if not recommendations:
        output.append("😅 暂时没有找到合适的推荐，试试先录入一些追剧记录吧！")
        return "\n".join(output)
    
    for i, rec in enumerate(recommendations, 1):
        # AI生成推荐理由
        if history:
            fav_drama = history[0]['drama_name']
            reason = f"因为你喜欢《{fav_drama}》的{rec['genre']}风格"
        else:
            reason = f"因为你喜欢{rec['genre']}类型的剧"
        
        if rec['rating'] >= 9.0:
            reason += "，且该剧是豆瓣高分神作"
        elif rec['rating'] >= 8.5:
            reason += "，口碑质量有保障"
        
        output.append(f"{i}. 🎬 《{rec['name']}》")
        output.append(f"   📌 推荐理由：{reason}")
        output.append(f"   ⭐ 豆瓣评分：{rec['rating']}")
        output.append(f"   📝 简介：{rec['desc']}")
        output.append("")
    
    output.append("---")
    output.append("👉 回复 '想看《剧名》' 加入追剧清单")
    output.append("💬 或者告诉我你更喜欢什么类型，我再帮你找找")
    
    return "\n".join(output)


if __name__ == "__main__":
    print("=" * 50)
    print("💡 智能推荐测试")
    print("=" * 50)
    print()
    print(recommend_dramas(3))
