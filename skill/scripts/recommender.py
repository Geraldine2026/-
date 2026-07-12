"""
recommender.py - 智能推荐
基于每日更新的追剧数据，生成个性化推荐
用法：python recommender.py
"""

import random
from datetime import datetime
from data_manager import get_all_dramas, get_history


# 扩展推荐池（包含更多维度信息）
RECOMMENDATION_POOL = [
    {
        "name": "狂飙",
        "genre": "犯罪悬疑",
        "rating": 8.5,
        "year": 2023,
        "platform": "爱奇艺",
        "episodes": 39,
        "tags": ["扫黑除恶", "张译", "高启强", "爆款"],
        "desc": "扫黑除恶题材，张译主演，2023年现象级爆款"
    },
    {
        "name": "漫长的季节",
        "genre": "悬疑年代",
        "rating": 9.4,
        "year": 2023,
        "platform": "腾讯视频",
        "episodes": 12,
        "tags": ["范伟", "秦昊", "东北", "豆瓣高分"],
        "desc": "东北悬疑，豆瓣9.4分，2023年口碑神作"
    },
    {
        "name": "三体",
        "genre": "科幻悬疑",
        "rating": 8.7,
        "year": 2023,
        "platform": "腾讯视频",
        "episodes": 30,
        "tags": ["刘慈欣", "科幻", "张鲁一", "于和伟"],
        "desc": "科幻巨制，刘慈欣同名小说改编"
    },
    {
        "name": "莲花楼",
        "genre": "武侠悬疑",
        "rating": 8.3,
        "year": 2023,
        "platform": "爱奇艺",
        "episodes": 40,
        "tags": ["成毅", "武侠", "探案", "古装"],
        "desc": "江湖探案，成毅主演，武侠与悬疑的结合"
    },
    {
        "name": "甄嬛传",
        "genre": "古装宫斗",
        "rating": 9.4,
        "year": 2011,
        "platform": "优酷",
        "episodes": 76,
        "tags": ["孙俪", "宫斗", "经典", "必看"],
        "desc": "宫斗巅峰之作，孙俪主演，经典永不过时"
    },
    {
        "name": "琅琊榜",
        "genre": "古装权谋",
        "rating": 9.4,
        "year": 2015,
        "platform": "腾讯视频",
        "episodes": 54,
        "tags": ["胡歌", "权谋", "经典", "必看"],
        "desc": "权谋巅峰之作，胡歌主演，国产剧天花板"
    },
    {
        "name": "去有风的地方",
        "genre": "治愈爱情",
        "rating": 8.0,
        "year": 2023,
        "platform": "芒果TV",
        "episodes": 40,
        "tags": ["刘亦菲", "治愈", "大理", "慢生活"],
        "desc": "慢生活治愈剧，刘亦菲主演，大理取景"
    },
    {
        "name": "边水往事",
        "genre": "悬疑犯罪",
        "rating": 8.2,
        "year": 2024,
        "platform": "优酷",
        "episodes": 21,
        "tags": ["郭麒麟", "犯罪", "悬疑", "新剧"],
        "desc": "悬疑犯罪剧，郭麒麟主演，2024年新剧"
    },
    {
        "name": "白夜追凶",
        "genre": "悬疑犯罪",
        "rating": 9.0,
        "year": 2017,
        "platform": "优酷",
        "episodes": 32,
        "tags": ["潘粤明", "经典悬疑", "高分", "必看"],
        "desc": "经典悬疑剧，潘粤明一人分饰两角"
    },
    {
        "name": "隐秘的角落",
        "genre": "悬疑",
        "rating": 8.8,
        "year": 2020,
        "platform": "爱奇艺",
        "episodes": 12,
        "tags": ["秦昊", "悬疑", "短剧", "高分"],
        "desc": "国产悬疑佳作，秦昊主演，『爬山』梗出处"
    },
    {
        "name": "沉默的真相",
        "genre": "悬疑犯罪",
        "rating": 9.0,
        "year": 2020,
        "platform": "爱奇艺",
        "episodes": 12,
        "tags": ["廖凡", "白宇", "社会派", "高分"],
        "desc": "社会派悬疑，廖凡、白宇主演，豆瓣9.0"
    },
    {
        "name": "父母爱情",
        "genre": "家庭生活",
        "rating": 9.5,
        "platform": "腾讯视频",
        "episodes": 44,
        "tags": ["郭涛", "梅婷", "温暖", "经典"],
        "desc": "温暖治愈的家庭剧，豆瓣9.5分"
    },
    {
        "name": "山海情",
        "genre": "年代现实",
        "rating": 9.2,
        "year": 2021,
        "platform": "腾讯视频",
        "episodes": 23,
        "tags": ["黄轩", "扶贫", "正午阳光", "高分"],
        "desc": "扶贫题材，正午阳光出品，豆瓣9.2"
    },
    {
        "name": "人世间",
        "genre": "年代现实",
        "rating": 8.4,
        "year": 2022,
        "platform": "爱奇艺",
        "episodes": 58,
        "tags": ["雷佳音", "辛柏青", "年代剧", "亲情"],
        "desc": "平民史诗，雷佳音主演，获多项大奖"
    },
    {
        "name": "唐朝诡事录",
        "genre": "古装悬疑",
        "rating": 8.0,
        "year": 2022,
        "platform": "爱奇艺",
        "episodes": 36,
        "tags": ["杨旭文", "杨志刚", "探案", "唐朝"],
        "desc": "唐朝探案剧，古装悬疑，口碑黑马"
    },
    {
        "name": "繁花",
        "genre": "年代商战",
        "rating": 8.2,
        "year": 2023,
        "platform": "腾讯视频",
        "episodes": 30,
        "tags": ["胡歌", "王家卫", "上海", "商战"],
        "desc": "王家卫执导，胡歌主演，上海滩商战"
    },
    {
        "name": "我是刑警",
        "genre": "犯罪悬疑",
        "rating": 7.8,
        "year": 2024,
        "platform": "爱奇艺",
        "episodes": 38,
        "tags": ["于和伟", "刑警", "真实案件", "新剧"],
        "desc": "真实案件改编，于和伟主演，2024年新剧"
    },
    {
        "name": "风起洛阳",
        "genre": "古装悬疑",
        "rating": 7.5,
        "year": 2021,
        "platform": "爱奇艺",
        "episodes": 39,
        "tags": ["黄轩", "王一博", "古装", "悬疑"],
        "desc": "古装悬疑探案，黄轩、王一博主演"
    },
    {
        "name": "御赐小仵作",
        "genre": "古装悬疑",
        "rating": 8.0,
        "year": 2021,
        "platform": "腾讯视频",
        "episodes": 36,
        "tags": ["苏晓彤", "王子奇", "探案", "口碑"],
        "desc": "口碑黑马，古装探案甜宠剧"
    },
    {
        "name": "苍兰诀",
        "genre": "古装仙侠",
        "rating": 8.1,
        "year": 2022,
        "platform": "爱奇艺",
        "episodes": 36,
        "tags": ["虞书欣", "王鹤棣", "仙侠", "爆款"],
        "desc": "仙侠爆款，虞书欣、王鹤棣主演"
    }
]


def analyze_user_preference(watch_list: dict) -> dict:
    """
    分析用户偏好
    返回：喜欢的类型、喜欢的演员、追剧节奏等
    """
    if not watch_list:
        return {}
    
    genres = []
    tags = []
    total_behind = 0
    total_episodes = 0
    
    for name, info in watch_list.items():
        my_ep = info.get('my_episode', 0)
        latest = info.get('latest_episode', 0)
        
        # 从推荐池中查找该剧的类型
        for rec in RECOMMENDATION_POOL:
            if rec['name'] == name:
                genres.append(rec['genre'])
                tags.extend(rec.get('tags', []))
                break
        
        total_behind += (latest - my_ep) if latest > my_ep else 0
        total_episodes += 1
    
    # 统计最常看的类型
    genre_count = {}
    for g in genres:
        genre_count[g] = genre_count.get(g, 0) + 1
    
    tag_count = {}
    for t in tags:
        tag_count[t] = tag_count.get(t, 0) + 1
    
    top_genres = sorted(genre_count.items(), key=lambda x: x[1], reverse=True)[:3]
    top_tags = sorted(tag_count.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "top_genres": [g[0] for g in top_genres],
        "top_tags": [t[0] for t in top_tags],
        "total_behind": total_behind,
        "total_episodes": total_episodes,
        "watch_speed": "快" if total_behind < total_episodes else "慢"
    }


def recommend_dramas(limit: int = 5) -> str:
    """
    基于每日更新的追剧数据，生成智能推荐
    """
    watch_list = get_all_dramas()
    history = get_history()
    
    if not watch_list:
        return "📭 暂无追剧记录，请先用 parser.py 录入数据"
    
    # 分析用户偏好
    preference = analyze_user_preference(watch_list)
    watched_names = list(watch_list.keys())
    
    # 过滤已追的剧
    candidates = [c for c in RECOMMENDATION_POOL if c['name'] not in watched_names]
    
    if not candidates:
        return "🎉 你已经把推荐池里的剧都追完了！去发现更多新剧吧！"
    
    # 计算推荐分数
    scored = []
    for c in candidates:
        score = 0
        
        # 1. 类型匹配（基于用户偏好的类型）
        for genre in preference.get('top_genres', []):
            if genre in c['genre']:
                score += 5
        
        # 2. 标签匹配
        for tag in preference.get('top_tags', []):
            if tag in c.get('tags', []):
                score += 3
        
        # 3. 评分加成
        if c['rating'] >= 9.0:
            score += 4
        elif c['rating'] >= 8.5:
            score += 3
        elif c['rating'] >= 8.0:
            score += 2
        
        # 4. 年份加成（新剧优先）
        year = c.get('year', 2000)
        if year >= 2024:
            score += 3
        elif year >= 2023:
            score += 2
        elif year >= 2020:
            score += 1
        
        # 5. 如果用户追剧快，推荐集数少的（更快看完）
        if preference.get('watch_speed') == '快':
            if c['episodes'] <= 20:
                score += 2
        else:
            if c['episodes'] >= 30:
                score += 2
        
        # 6. 随机因素（增加多样性）
        score += random.randint(0, 3)
        
        scored.append({**c, "score": score})
    
    # 按分数排序
    scored.sort(key=lambda x: x['score'], reverse=True)
    recommendations = scored[:limit]
    
    # 生成推荐报告
    output = []
    output.append("=" * 60)
    output.append("💡 智能推荐报告")
    output.append("=" * 60)
    output.append("")
    
    # 用户画像
    output.append("📊 基于你的追剧数据：")
    output.append(f"   ├─ 在追剧集：{len(watch_list)} 部")
    output.append(f"   ├─ 偏好类型：{', '.join(preference.get('top_genres', ['未识别']))}")
    output.append(f"   ├─ 待更新集数：{preference.get('total_behind', 0)} 集")
    output.append(f"   └─ 追剧速度：{preference.get('watch_speed', '中等')}")
    output.append("")
    output.append("-" * 60)
    output.append("🎯 为你推荐：")
    output.append("")
    
    for i, rec in enumerate(recommendations, 1):
        # 生成推荐理由
        reasons = []
        for genre in preference.get('top_genres', []):
            if genre in rec['genre']:
                reasons.append(f"你喜欢{genre}类型")
                break
        
        if rec['rating'] >= 9.0:
            reasons.append("豆瓣9分+神作")
        elif rec['rating'] >= 8.5:
            reasons.append("豆瓣8.5+口碑佳作")
        
        if rec.get('year', 0) >= 2024:
            reasons.append("2024年新剧")
        
        if not reasons:
            reasons = ["综合匹配度高"]
        
        output.append(f"{i}. 🎬 【{rec['name']}】")
        output.append(f"   ├─ 类型：{rec['genre']}")
        output.append(f"   ├─ 评分：⭐ {rec['rating']} 分")
        output.append(f"   ├─ 集数：{rec['episodes']} 集")
        output.append(f"   ├─ 平台：{rec['platform']}")
        output.append(f"   ├─ 简介：{rec['desc']}")
        output.append(f"   └─ 推荐理由：{'，'.join(reasons)}")
        output.append("")
    
    output.append("-" * 60)
    
    # 每日更新建议
    behind_total = preference.get('total_behind', 0)
    if behind_total > 0:
        output.append(f"⏳ 你还有 {behind_total} 集待追，建议先追完再开新剧")
    else:
        output.append("🎉 你已经全部追平！尽情开新剧吧！")
    
    output.append("")
    output.append("📌 操作提示：")
    output.append("   python parser.py '《剧名》我看到第X集，最新X集'  # 录入新剧")
    output.append("   python scheduler.py    # 查看本周追剧日程")
    output.append("   python predictor.py '剧名'  # 预测完结时间")
    
    return "\n".join(output)


def main():
    print(recommend_dramas(5))


if __name__ == "__main__":
    main()
