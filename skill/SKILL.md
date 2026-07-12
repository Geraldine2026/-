---
name: drama-calendar-manager
description: 追剧日历管家 - 管理在追剧集、生成日程、预测完结、智能推荐、生成前情摘要
version: 2.1.0
triggers:
  - 追剧|在追|剧集|更新|剧荒
  - "我在看xxx，已经更新到xx集"
  - 本周追剧|追剧日历|这周看什么
  - 推荐xxx剧|剧荒了|有什么好看的
  - 前情提要|上一集讲了什么| recap
scripts:
  - scripts/parser.py
  - scripts/scheduler.py
  - scripts/predictor.py
  - scripts/recommender.py
  - scripts/recap.py
  - scripts/data_manager.py
references:
  - references/schedule_rules.yaml
  - references/sample_history.json
  - references/usage_guide.md
---

# 追剧日历管家 (Drama Calendar Manager)

技能简介

追剧日历管家是一个 AI 驱动的智能追剧管理工具。它帮你统一管理所有在追的剧集，自动追踪更新进度、预测完结时间，并在剧荒时智能推荐下一部好剧。

AI 核心价值：没有 AI，这就是一个普通的 Excel 表格；有 AI，它变成了一个懂你的追剧管家。


## 核心功能

### 功能1：追剧录入（智能解析）

功能描述：
用户用自然语言描述追剧进度，AI 自动提取关键信息并持久化存储。

触发示例：
- 我在看《黑暗荣耀》，更新到第8集
- 最近在追《繁花》，看到第12集了
- 《庆余年2》看到第15集了
- 《黑暗荣耀》我看到第8集，最新16集

AI 提取字段：
- 剧名
- 我看到第几集（my_episode）
- 平台最新更新到第几集（latest_episode）
- 录入日期（自动填入当天）

调用的脚本：scripts/parser.py

脚本路径：scripts/parser.py
引用脚本：from data_manager import add_or_update_drama, get_summary
调用命令：python parser.py "《黑暗荣耀》我看到第8集，最新16集"
输入：自然语言文本
输出：解析结果 + 数据持久化 + 追剧汇总
写入数据：data/drama_data.json

脚本执行流程：
1. 用户输入自然语言
2. parser.py 解析自然语言，提取剧名、我的集数、最新集数
3. 调用 data_manager.add_or_update_drama() 保存数据到 data/drama_data.json
4. 调用 data_manager.get_summary() 显示当前追剧汇总

代码引用示例：
from data_manager import add_or_update_drama, get_summary
save_result = add_or_update_drama(drama_name, my_episode, latest_episode)
print(get_summary())

输出格式：
✅ 已添加：《黑暗荣耀》看到第8集，最新第16集
⏳ 你落后 8 集，加油追！

📊 我的追剧清单：
  《黑暗荣耀》
    我看到：第 8 集
    最新到：第 16 集
    状态：⏳ 落后 8 集


### 功能2：日程生成（聚合推送）

功能描述：
根据各剧的播出规律和你的追剧进度，自动生成本周追剧日程表。

触发示例：
- 本周追剧日历
- 这周看什么
- 给我追剧日程

调用的脚本：scripts/scheduler.py

脚本路径：scripts/scheduler.py
引用脚本：from data_manager import get_all_dramas
调用命令：python scheduler.py
输入：无（自动读取本地数据）
输出：本周追剧日历
读取数据：data/drama_data.json

脚本执行流程：
1. scheduler.py 运行
2. 调用 data_manager.get_all_dramas() 读取所有追剧数据
3. 按周分配每部剧的更新日
4. 统计待更新数量
5. 格式化输出日程表

代码引用示例：
from data_manager import get_all_dramas
watch_list = get_all_dramas()

输出格式：
==================================================
📅 本周追剧日程
（2026-07-10 ~ 2026-07-16）
==================================================

【周一】
  《繁花》第 13 集（最新30集）

【周三】
  《庆余年2》第 16 集（最新36集）

【周五】
  《黑暗荣耀》第 9 集（最新16集）

【周日】
  《繁花》第 14 集（最新30集）

--------------------------------------------------
📊 共 3 部在追，3 部待更新


### 功能3：进度预测（完结预测）

功能描述：
根据剧集总集数和你的追剧进度，智能预测完结日期。

触发示例：
- 《黑暗荣耀》什么时候完结
- 预测一下《繁花》的完结时间
- 距离《庆余年2》完结还有多久

AI 计算逻辑：
- 剩余集数 = 最新集数 - 我看到集数
- 按每天1集推算完结日期
- 生成个性化建议

调用的脚本：scripts/predictor.py

脚本路径：scripts/predictor.py
引用脚本：from data_manager import get_drama_info, get_all_dramas
调用命令：python predictor.py "黑暗荣耀"
输入：剧名
输出：完结日期预测报告
读取数据：data/drama_data.json

脚本执行流程：
1. 用户输入剧名
2. predictor.py 调用 data_manager.get_drama_info() 读取该剧进度
3. 计算剩余集数 = latest - my
4. 按每天1集推算完结日期
5. 生成个性化建议

代码引用示例：
from data_manager import get_drama_info, get_all_dramas
info = get_drama_info(drama_name)
all_dramas = list(get_all_dramas().keys())

输出格式：
==================================================
🔮 《黑暗荣耀》完结预测
==================================================

📌 你看到：第 8 集
📌 最新到：第 16 集
⏳ 剩余：8 集
📆 按每天1集，预计 2026-07-20 追完
🔥 一周内能追完，坚持！


### 功能4：智能推荐（剧荒模式）

功能描述：
基于每日更新的追剧数据，分析用户偏好，智能推荐 5 部你可能喜欢的剧。

触发示例：
- 剧荒了，推荐几部剧
- 有什么好看的推荐一下
- 我该看什么

AI 分析维度：
- 用户追剧偏好分析（类型、标签）
- 追剧速度评估
- 多维度评分（类型匹配 + 标签匹配 + 评分 + 年份 + 集数）
- 过滤已追剧集
- 生成个性化推荐理由

调用的脚本：scripts/recommender.py

脚本路径：scripts/recommender.py
引用脚本：from data_manager import get_all_dramas
调用命令：python recommender.py
输入：无（自动读取本地数据）
输出：5部推荐剧集 + 推荐理由 + 用户画像
读取数据：data/drama_data.json

脚本执行流程：
1. recommender.py 运行
2. 调用 data_manager.get_all_dramas() 读取所有追剧数据
3. 分析用户偏好：类型、标签、追剧速度
4. 从推荐池中过滤已追剧集
5. 多维度评分：类型+标签+评分+年份+集数
6. 排序取前5，生成个性化推荐理由

代码引用示例：
from data_manager import get_all_dramas
watch_list = get_all_dramas()

输出格式：
============================================================
💡 智能推荐报告
============================================================

📊 基于你的追剧数据：
   在追剧集：3 部
   偏好类型：悬疑, 古装, 年代
   待更新集数：26 集
   追剧速度：快

------------------------------------------------------------
🎯 为你推荐：

1. 【狂飙】
   类型：犯罪悬疑
   评分：8.5 分
   集数：39 集
   平台：爱奇艺
   简介：扫黑除恶题材，张译主演
   推荐理由：你喜欢悬疑类型，豆瓣8.5+口碑佳作

（共5部）

------------------------------------------------------------
⏳ 你还有 26 集待追，建议先追完再开新剧


### 功能5：前情提要生成（一键回顾）

功能描述：
输入剧名和集数，AI 自动生成该集的内容摘要，同时结合每日更新的追剧进度数据。

触发示例：
- 《黑暗荣耀》第7集讲了什么
- 帮我回忆一下《繁花》第10集
- 前情提要：《庆余年2》第20集

AI 能力：
- 从 data_manager.py 读取追剧进度
- 查询预设摘要数据（覆盖10+部剧，50+集）
- 无数据时 AI 动态生成
- 结构化输出：主要事件 + 关键台词 + 伏笔提示 + 追剧进度

调用的脚本：scripts/recap.py

脚本路径：scripts/recap.py
引用脚本：from data_manager import get_drama_info, get_all_dramas
调用命令：python recap.py "黑暗荣耀" 7
输入：剧名 + 集数
输出：剧情摘要 + 追剧进度
读取数据：data/drama_data.json

脚本执行流程：
1. 用户输入剧名和集数
2. recap.py 调用 data_manager.get_drama_info() 读取追剧进度
3. 查询预设摘要数据（MOCK_RECAPS）
4. 若无预设，AI 动态生成摘要
5. 结构化输出：事件 + 台词 + 伏笔 + 进度

代码引用示例：
from data_manager import get_drama_info, get_all_dramas
info = get_drama_info(drama_name)
my_ep = info.get('my_episode', 0)
latest = info.get('latest_episode', 0)
all_dramas = list(get_all_dramas().keys())

输出格式：
============================================================
📝 《黑暗荣耀》第 7 集 前情提要
============================================================

📊 追剧进度：
   你看到：第 8 集
   最新更新：第 16 集
   你还落后 8 集

------------------------------------------------------------

📌 主要事件：
  文东恩发现河道英的真实身份
  朴妍珍开始调查文东恩的过去
  朱如炡表白被拒

💬 关键台词：
  "你以为你赢了？游戏才刚刚开始。"

🔮 本集伏笔：
  河道英的过去即将揭晓

👉 继续看下一集吧！
📌 提示：用 parser.py 更新你的追剧进度


### 功能6：数据管理（底层支持）

功能描述：
所有脚本的数据读写核心，提供统一的数据接口。

调用的脚本：scripts/data_manager.py

脚本路径：scripts/data_manager.py
被谁引用：parser.py, scheduler.py, predictor.py, recommender.py, recap.py
提供功能：load_data、save_data、add_or_update_drama、get_all_dramas、get_drama_info、get_summary
数据文件：data/drama_data.json
调用命令：python data_manager.py（查看汇总）

提供的数据接口：

1. load_data
   功能：加载 data/drama_data.json
   被谁调用：内部函数

2. save_data
   功能：保存 data/drama_data.json
   被谁调用：内部函数

3. add_or_update_drama
   功能：添加或更新追剧记录
   被谁调用：parser.py

4. get_all_dramas
   功能：获取所有在追剧集
   被谁调用：scheduler.py, predictor.py, recommender.py, recap.py

5. get_drama_info
   功能：获取单部剧信息
   被谁调用：predictor.py, recap.py

6. get_summary
   功能：获取追剧汇总
   被谁调用：parser.py

数据格式示例：
{
  "watch_list": {
    "黑暗荣耀": {
      "my_episode": 8,
      "latest_episode": 16,
      "last_update": "2026-07-12 14:30"
    }
  },
  "history": [],
  "total_count": 2
}


## 脚本调用关系

脚本引用关系图：

data_manager.py（数据管理核心）
  功能：读写 data/drama_data.json，提供数据接口
  提供函数：load_data、save_data、add_or_update_drama、get_all_dramas、get_drama_info、get_summary

被以下脚本引用：

1. parser.py（追剧录入）
   引用：add_or_update_drama, get_summary
   功能：解析自然语言，保存追剧数据

2. scheduler.py（日程生成）
   引用：get_all_dramas
   功能：读取追剧数据，生成日程表

3. predictor.py（完结预测）
   引用：get_drama_info, get_all_dramas
   功能：读取进度，预测完结日期

4. recommender.py（智能推荐）
   引用：get_all_dramas
   功能：读取追剧数据，生成推荐

5. recap.py（前情提要）
   引用：get_drama_info, get_all_dramas
   功能：读取进度，生成剧情摘要


## 使用方式

在 Hermes Agent 中，直接向 AI 发送自然语言指令即可触发对应功能：

1. 记录追剧进度
   用户说："我在看《黑暗荣耀》，更新到第8集"
   调用的脚本：parser.py

2. 查看本周日程
   用户说："本周追剧日历"
   调用的脚本：scheduler.py

3. 预测完结时间
   用户说："《繁花》什么时候完结"
   调用的脚本：predictor.py

4. 求推荐
   用户说："剧荒了，推荐几部"
   调用的脚本：recommender.py

5. 回忆剧情
   用户说："《庆余年2》第20集讲了什么"
   调用的脚本：recap.py

6. 查看汇总
   用户说："显示追剧清单"
   调用的脚本：data_manager.py


## 技术实现

1. 自然语言解析：正则表达式 + 语义理解，提取剧名和集数
2. 数据持久化：JSON 文件存储，所有脚本共享数据
3. 日程生成：基于追剧进度和播出规律，格式化输出
4. 完结预测：基于当前进度和每天1集的速度推算
5. 智能推荐：多维度评分（类型+标签+评分+年份+集数）
6. 前情提要：预设摘要数据 + AI 动态生成


## 配置文件说明

1. references/schedule_rules.yaml：剧集播出规律配置（29部剧）
2. references/sample_history.json：示例追剧历史数据（26部剧）
3. references/usage_guide.md：详细使用指南


## AI 核心价值总结

1. 追剧录入
   没有 AI：手动填Excel表格
   有 AI：自然语言一句话录入
   AI 不可替代性：语义理解+信息提取

2. 日程生成
   没有 AI：自己去查每部剧更新日
   有 AI：自动生成结构化日程
   AI 不可替代性：多源信息聚合+格式化

3. 完结预测
   没有 AI：凭感觉猜测
   有 AI：智能推算完结日期
   AI 不可替代性：模式识别+时间推算

4. 智能推荐
   没有 AI：到处问别人
   有 AI：基于追剧历史个性化推荐
   AI 不可替代性：用户画像+兴趣匹配

5. 前情提要
   没有 AI：翻半天找上一集
   有 AI：一键生成剧情摘要
   AI 不可替代性：自动摘要生成

核心结论：没有 AI，这就是一个普通的 Excel 表格；有 AI，它变成了一个懂你的追剧管家。


## 与 WorkBuddy 交互记录

### 交互记录1：创建项目文件结构

交互时间：2026-07-12

用户指令：
请帮我在当前工作目录 E:\jianxi\追剧日历管家 下，创建完整的项目文件结构

AI 执行过程：
1. 创建 skill、data、tests、iteration 四个文件夹
2. 创建 SKILL.md、README.md 等核心文件
3. 创建 scripts 和 references 子目录及其文件

脚本使用情况：
本阶段未使用具体脚本，仅创建文件结构，为后续脚本编写做准备。


### 交互记录2：编写核心脚本

交互时间：2026-07-12

用户指令：
请编写 data_manager.py、parser.py、scheduler.py、predictor.py、recommender.py、recap.py 六个核心脚本

AI 执行过程：
1. 编写 data_manager.py，提供数据持久化管理，统一的读写接口
2. 编写 parser.py，实现自然语言解析，支持"开始看"默认第1集
3. 编写 scheduler.py，基于真实数据生成追剧日程
4. 编写 predictor.py，智能预测完结日期
5. 编写 recommender.py，多维度评分，推荐5部剧
6. 编写 recap.py，查询预设摘要，无数据时AI动态生成

脚本使用情况：
1. data_manager.py：被 parser.py、scheduler.py、predictor.py、recommender.py、recap.py 引用
2. parser.py：调用 data_manager.add_or_update_drama 保存数据
3. scheduler.py：调用 data_manager.get_all_dramas 读取数据
4. predictor.py：调用 data_manager.get_drama_info 读取进度
5. recommender.py：调用 data_manager.get_all_dramas 读取数据
6. recap.py：调用 data_manager.get_drama_info 读取进度


### 交互记录3：更新 SKILL.md 脚本调用说明

交互时间：2026-07-12

用户指令：
请在每个功能中增加调用的脚本说明，体现哪个功能用了哪个脚本

AI 执行过程：
1. 为每个功能新增调用的脚本表格
2. 包含脚本路径、引用方式、调用命令、输入输出、数据依赖
3. 新增脚本调用关系总图展示完整链路

脚本使用情况：
本阶段修改 SKILL.md 文档，未执行具体脚本。明确了6个脚本与6个功能的对应关系。


### 交互记录4：迭代日志更新（4轮迭代）

交互时间：2026-07-12

用户指令：
请写4轮迭代日志

AI 执行过程：
1. V1.0到V1.1：修复"开始看"无法解析问题，通过率从85.7%提升到100%
2. V1.1到V1.2：新增 data_manager，实现数据持久化
3. V1.2到V2.0：所有脚本统一读写 data_manager，形成数据闭环
4. V2.0到V2.1：推荐联动、待更新提醒、多维度评分

脚本使用情况：
1. 各阶段均涉及脚本修改和优化
2. parser.py 在 V1.1 阶段修改，增加"开始看"模式
3. data_manager.py 在 V1.2 阶段新增
4. 所有脚本在 V2.0 阶段统一引用 data_manager.py
5. recommender.py 在 V2.1 阶段增加动态过滤和多维度评分


### 交互记录5：测试验证

交互时间：2026-07-12

用户指令：
请测试所有脚本是否正常运行

AI 执行过程：
1. 运行 python parser.py "《黑暗荣耀》我看到第8集，最新16集"，测试通过
2. 运行 python scheduler.py，生成日程，测试通过
3. 运行 python predictor.py "黑暗荣耀"，预测完结，测试通过
4. 运行 python recommender.py，推荐5部剧，测试通过
5. 运行 python recap.py "黑暗荣耀" 7，生成前情提要，测试通过

脚本使用情况：
1. parser.py：输入"《黑暗荣耀》我看到第8集，最新16集"，输出录入成功
2. scheduler.py：读取 data/drama_data.json，输出本周日程
3. predictor.py：读取 data/drama_data.json，输出完结预测
4. recommender.py：读取 data/drama_data.json，输出5部推荐
5. recap.py：读取 data/drama_data.json，输出剧情摘要


### 交互记录6：更新 test_record.md

交互时间：2026-07-12

用户指令：
请根据测试结果，更新 test_record.md

AI 执行过程：
1. 记录21个测试用例，100%通过
2. 验证所有脚本引用关系正常
3. 附上完整执行日志

脚本使用情况：
本阶段记录测试结果，未执行具体脚本。确认了6个脚本全部测试通过。


### 交互记录7：更新 README.md

交互时间：2026-07-12

用户指令：
请更新 README.md，包含脚本引用关系和使用说明

AI 执行过程：
1. 新增脚本引用关系章节
2. 展示数据流闭环图
3. 更新使用方式和测试说明

脚本使用情况：
本阶段修改 README.md 文档，未执行具体脚本。明确了6个脚本的数据流向。


### 交互记录8：扩充配置文件

交互时间：2026-07-12

用户指令：
请更新 sample_history.json 和 schedule_rules.yaml，多一些数据

AI 执行过程：
1. sample_history.json 从12部扩充到26部，新增 platform、total_episodes、statistics 字段
2. schedule_rules.yaml 从10部扩充到29部，新增 genre、tags 字段

脚本使用情况：
本阶段修改配置文件，未执行具体脚本。配置文件供 scheduler.py 和 recommender.py 读取使用。


### 交互记录9：更新 __init__.py

交互时间：2026-07-12

用户指令：
请更新 __init__.py，导出 data_manager 的所有函数

AI 执行过程：
1. 新增 from .data_manager import load_data, save_data, add_or_update_drama, get_all_dramas, get_drama_info, get_summary, delete_drama
2. __all__ 从5个函数扩展到10个函数

脚本使用情况：
修改 __init__.py 模块入口文件，未执行具体脚本。使 data_manager.py 的函数可以被外部直接导入使用。


### 交互记录10：推送代码到 GitHub

交互时间：2026-07-12

用户指令：
请帮我推送代码到 GitHub

AI 执行过程：
1. 执行 git add . 暂存所有文件
2. 执行 git commit -m "追剧日历管家 v2.1: 完整版本，包含4轮迭代、21个测试用例、数据持久化、脚本联动"
3. 执行 git push origin master 推送到远程仓库
4. 确认推送成功，所有7项提交内容完整

脚本使用情况：
本阶段进行 Git 操作，未执行具体脚本。所有6个脚本和3个配置文件均已提交到 GitHub。


## 交互统计

1. 创建或修改文件：12次
   包括 scripts、references、SKILL.md、README.md 等

2. 功能测试：5次
   parser、scheduler、predictor、recommender、recap

3. 迭代优化：4轮
   V1.0 到 V1.1 到 V1.2 到 V2.0 到 V2.1

4. 数据扩充：2次
   sample_history.json 和 schedule_rules.yaml

5. GitHub 操作：3次
   add、commit、push

总计交互次数：约30次以上，整理一下这些信息，重新写SKILL.md
