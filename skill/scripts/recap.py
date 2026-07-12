"""
recap.py - 前情提要生成模块
AI核心价值：剧情摘要自动生成
"""

import re
from typing import Dict, Optional


def call_ai_recap(drama_name: str, episode: int) -> Dict:
    """
    调用AI生成前情提要（模拟）
    真实场景：调用LLM API，输入剧名+集数，返回剧情摘要
    """
    
    # 模拟AI生成的剧情摘要
    # 真实场景下，这里会调用OpenAI/智谱/通义千问等API
    mock_summaries = {
        "黑暗荣耀": {
            7: {
                "events": [
                    "文东恩发现河道英的真实身份背景",
                    "朴妍珍开始暗中调查文东恩的过去",
                    "朱如炡向文东恩表白，但被委婉拒绝"
                ],
                "key_lines": "『你以为你赢了？游戏才刚刚开始。』",
                "foreshadowing": "河道英的过去将在下一集揭晓，新的复仇计划正在酝酿"
            },
            8: {
                "events": [
                    "文东恩的复仇计划进入关键阶段",
                    "朴妍珍的丈夫发现真相，家庭关系破裂",
                    "朱如炡决定全力帮助文东恩"
                ],
                "key_lines": "『我不需要你的同情，我只需要你的帮助。』",
                "foreshadowing": "朴妍珍即将面临重大危机"
            }
        },
        "繁花": {
            12: {
                "events": [
                    "宝总在股市中遭遇重大挫折",
                    "汪小姐与宝总的关系出现裂痕",
                    "爷叔暗中布局，为宝总谋划新的出路"
                ],
                "key_lines": "『上海滩的繁荣，不是一个人的戏。』",
                "foreshadowing": "宝总的对手即将浮出水面"
            }
        },
        "庆余年2": {
            15: {
                "events": [
                    "范闲与二皇子的矛盾升级",
                    "林婉儿发现范闲的秘密",
                    "五竹叔出手相助，展现强大实力"
                ],
                "key_lines": "『这朝堂之上，每一步都是棋局。』",
                "foreshadowing": "范闲即将面临更大的阴谋"
            }
        }
    }
    
    # 查找该剧的摘要
    drama_summaries = mock_summaries.get(drama_name, {})
    summary = drama_summaries.get(episode, None)
    
    if summary:
        return {
            "found": True,
            "drama_name": drama_name,
            "episode": episode,
            **summary
        }
    else:
        # AI智能生成（模拟）
        return {
            "found": True,
            "drama_name": drama_name,
            "episode": episode,
            "events": [
                f"{drama_name} 第{episode}集剧情继续推进",
                "主要角色面临新的挑战和抉择",
                "关键情节线正在深入发展"
            ],
            "key_lines": "『精彩继续，不容错过！』",
            "foreshadowing": f"第{episode+1}集将有重要突破",
            "ai_generated": True
        }


def generate_recap(input_text: str) -> str:
    """
    生成前情提要
    
    Args:
        input_text: 用户输入，如 "《黑暗荣耀》第7集讲了什么"
        
    Returns:
        str: 格式化的前情提要
    """
    
    # 解析剧名和集数
    # 模式：《剧名》第X集
    pattern = r'[《「](.+?)[》」]第?(\d+)集'
    match = re.search(pattern, input_text)
    
    if not match:
        return "❌ 请提供剧名和集数，例如：『《黑暗荣耀》第7集讲了什么』"
    
    drama_name = match.group(1).strip()
    episode = int(match.group(2))
    
    # 调用AI生成摘要
    result = call_ai_recap(drama_name, episode)
    
    if not result.get('found'):
        return f"❌ 未找到《{drama_name}》第{episode}集的信息"
    
    # 格式化输出
    output = []
    output.append(f"📝 《{drama_name}》第 {episode} 集 前情提要")
    output.append("")
    output.append("📌 主要事件：")
    
    for event in result.get('events', []):
        output.append(f"  - {event}")
    
    output.append("")
    output.append(f'💬 关键台词：')
    output.append(f'  "{result.get("key_lines", "剧情精彩继续")}"')
    output.append("")
    output.append("🔮 本集伏笔：")
    output.append(f"  - {result.get('foreshadowing', '新的剧情线索正在展开')}")
    output.append("")
    
    if result.get('ai_generated'):
        output.append("🤖 （本摘要由AI自动生成）")
    
    output.append("👉 继续看下一集吧！")
    
    return "\n".join(output)


if __name__ == "__main__":
    print("=" * 50)
    print("📝 前情提要生成测试")
    print("=" * 50)
    print()
    
    test_inputs = [
        "《黑暗荣耀》第7集讲了什么",
        "《黑暗荣耀》第8集讲了什么", 
        "《繁花》第12集讲了什么",
        "《庆余年2》第15集讲了什么"
    ]
    
    for test in test_inputs:
        print(f"用户：{test}")
        print(generate_recap(test))
        print()
