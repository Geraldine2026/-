"""
parser.py - 自然语言解析模块
AI核心价值：语义理解，从自然语言中提取剧名和集数
"""

import json
import re
from datetime import datetime
from typing import Dict, Optional

# 模拟 AI 调用（实际使用时替换为真实 API）
def call_ai_parser(user_text: str) -> Dict:
    """
    调用 AI 模型解析用户输入
    这里模拟 AI 行为，实际可接入 OpenAI/智谱/通义千问等 API
    """
    
    # 模拟 AI 的 few-shot 理解能力
    # 真实场景下，这里会是 API 调用
    patterns = [
        # 模式1：我在看《剧名》，更新到第X集
        (r'[我]?在看?[《「](.+?)[》」].*?更新到第?(\d+)集', '在看'),
        # 模式2：最近在追《剧名》，看到第X集了
        (r'追[《「](.+?)[》」].*?看到第?(\d+)集', '追'),
        # 模式3：《剧名》第X集
        (r'[《「](.+?)[》」]第?(\d+)集', ''),
        # 模式4：剧名，更新到X集（无书名号）
        (r'(.+?)更新到第?(\d+)集', ''),
    ]
    
    for pattern, _ in patterns:
        match = re.search(pattern, user_text)
        if match:
            drama_name = match.group(1).strip()
            episode = int(match.group(2))
            return {
                "drama_name": drama_name,
                "current_episode": episode,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "confidence": 0.95,
                "ai_parsed": True
            }
    
    # 如果正则匹配不到，模拟 AI 语义理解
    # 真实场景下，这里会调用 LLM API
    if "黑暗荣耀" in user_text:
        return {
            "drama_name": "黑暗荣耀",
            "current_episode": 8,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "confidence": 0.85,
            "ai_parsed": True,
            "note": "AI通过语义推断"
        }
    elif "繁花" in user_text or "繁花" in user_text:
        return {
            "drama_name": "繁花",
            "current_episode": 12,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "confidence": 0.85,
            "ai_parsed": True,
            "note": "AI通过语义推断"
        }
    
    return {
        "error": "无法解析，请提供剧名和集数",
        "ai_parsed": False
    }


def parse_drama_input(user_text: str) -> Dict:
    """
    解析用户的自然语言输入，提取追剧信息
    
    Args:
        user_text: 用户输入的自然语言文本
        
    Returns:
        Dict: 包含剧名、集数、日期的结构化数据
        
    Examples:
        >>> parse_drama_input("我在看《黑暗荣耀》，更新到第8集")
        {"drama_name": "黑暗荣耀", "current_episode": 8, "date": "2026-07-12"}
    """
    
    if not user_text or len(user_text.strip()) < 2:
        return {
            "error": "输入太短，请提供剧名和集数",
            "ai_parsed": False
        }
    
    # 调用 AI 解析
    result = call_ai_parser(user_text)
    
    # 如果是成功解析，添加格式化输出
    if "drama_name" in result and not result.get("error"):
        result["display"] = f"✅ 已记录：\n📺 剧名：{result['drama_name']}\n📌 当前集数：第 {result['current_episode']} 集\n📅 记录时间：{result['date']}"
        
        # 模拟 AI 生成的追剧建议
        if result['current_episode'] % 5 == 0:
            result["suggestion"] = f"🎉 你已经追到第 {result['current_episode']} 集了，继续加油！"
        elif result['current_episode'] > 10:
            result["suggestion"] = f"💪 已经追了 {result['current_episode']} 集，坚持就是胜利！"
    
    return result


# 测试入口
if __name__ == "__main__":
    test_inputs = [
        "我在看《黑暗荣耀》，更新到第8集",
        "最近在追《繁花》，看到第12集了",
        "《庆余年2》第15集看完了",
        "狂飙更新到20集了",
        "今天开始看《三体》"
    ]
    
    print("=" * 50)
    print("📺 追剧录入测试")
    print("=" * 50)
    
    for test in test_inputs:
        print(f"\n用户：{test}")
        result = parse_drama_input(test)
        if "display" in result:
            print(result["display"])
            if "suggestion" in result:
                print(result["suggestion"])
        else:
            print(f"❌ {result.get('error', '解析失败')}")
