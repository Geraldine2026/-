---
name: drama-calendar-manager
description: 追剧日历管家 - 管理在追剧集、生成日程、预测完结、智能推荐、生成前情摘要
version: 2.0.0

triggers:
  - 追剧|在追|剧集|更新|剧荒
  - "我在看.*更新到.*集"
  - 本周追剧|追剧日历|这周看什么
  - 推荐.*剧|剧荒了|有什么好看的
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

## 技能简介

追剧日历管家是一个 AI 驱动的智能追剧管理工具。它帮你统一管理所有在追的剧集，自动追踪更新进度、预测完结时间，并在剧荒时智能推荐下一部好剧。

**AI 核心价值：没有 AI，这就是一个普通的 Excel 表格；有 AI，它变成了一个"懂你的追剧管家"。**


## 核心功能

### 📺 功能1：追剧录入（智能解析）

**功能描述：**
用户用自然语言描述追剧进度，AI 自动提取关键信息并持久化存储。

**触发示例：**
- "我在看《黑暗荣耀》，更新到第8集"
- "最近在追《繁花》，看到第12集了"
- "《庆余年2》看到第15集了"
- "《黑暗荣耀》我看到第8集，最新16集"

**AI 提取字段：**
- 剧名
- 我看到第几集（my_episode）
- 平台最新更新到第几集（latest_episode）
- 录入日期（自动填入当天）

**调用的脚本：`scripts/parser.py`**

| 项目 | 说明 |
|------|------|
| **脚本路径** | `scripts/parser.py` |
| **引用脚本** | `from data_manager import add_or_update_drama, get_summary` |
| **调用命令** | `python parser.py "《黑暗荣耀》我看到第8集，最新16集"` |
| **输入** | 自然语言文本 |
| **输出** | 解析结果 + 数据持久化 + 追剧汇总 |
| **写入数据** | `data/drama_data.json` |

**脚本执行流程：**
用户输入 → parser.py 解析自然语言
↓
提取剧名、我的集数、最新集数
↓
调用 data_manager.add_or_update_drama() 保存数据
↓
调用 data_manager.get_summary() 显示汇总

text

**代码引用示例：**
```python
# parser.py 中的引用
from data_manager import add_or_update_drama, get_summary

# 调用 data_manager 保存数据
save_result = add_or_update_drama(drama_name, my_episode, latest_episode)

# 调用 data_manager 显示汇总
print(get_summary())
输出格式：

text
✅ 已添加：《黑暗荣耀》看到第8集，最新第16集
⏳ 你落后 8 集，加油追！

📊 我的追剧清单：
  《黑暗荣耀》
    我看到：第 8 集
    最新到：第 16 集
    状态：⏳ 落后 8 集
📅 功能2：日程生成（聚合推送）
功能描述：
根据各剧的播出规律和你的追剧进度，自动生成本周追剧日程表。

触发示例：

"本周追剧日历"

"这周看什么"

"给我追剧日程"

调用的脚本：scripts/scheduler.py

项目	说明
脚本路径	scripts/scheduler.py
引用脚本	from data_manager import get_all_dramas
调用命令	python scheduler.py
输入	无（自动读取本地数据）
输出	本周追剧日历
读取数据	data/drama_data.json
脚本执行流程：

text
scheduler.py 运行
       ↓
调用 data_manager.get_all_dramas() 读取所有追剧数据
       ↓
按周分配每部剧的更新日
       ↓
统计待更新数量
       ↓
格式化输出日程表
代码引用示例：

python
# scheduler.py 中的引用
from data_manager import get_all_dramas

# 调用 data_manager 读取所有追剧数据
watch_list = get_all_dramas()
输出格式：

text
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
🔮 功能3：进度预测（完结预测）
功能描述：
根据剧集总集数和你的追剧进度，智能预测完结日期。

触发示例：

"《黑暗荣耀》什么时候完结"

"预测一下《繁花》的完结时间"

"距离《庆余年2》完结还有多久"

AI 计算逻辑：

剩余集数 = 最新集数 - 我看到集数

按每天1集推算完结日期

生成个性化建议

调用的脚本：scripts/predictor.py

项目	说明
脚本路径	scripts/predictor.py
引用脚本	from data_manager import get_drama_info, get_all_dramas
调用命令	python predictor.py "黑暗荣耀"
输入	剧名
输出	完结日期预测报告
读取数据	data/drama_data.json
脚本执行流程：

text
用户输入剧名 → predictor.py 运行
              ↓
       调用 data_manager.get_drama_info() 读取该剧进度
              ↓
       计算剩余集数 = latest - my
              ↓
       按每天1集推算完结日期
              ↓
       生成个性化建议
代码引用示例：

python
# predictor.py 中的引用
from data_manager import get_drama_info, get_all_dramas

# 调用 data_manager 读取单部剧信息
info = get_drama_info(drama_name)

# 调用 data_manager 获取所有剧名（用于交互模式）
all_dramas = list(get_all_dramas().keys())
输出格式：

text
==================================================
🔮 《黑暗荣耀》完结预测
==================================================

📌 你看到：第 8 集
📌 最新到：第 16 集
⏳ 剩余：8 集
📆 按每天1集，预计 2026-07-20 追完
🔥 一周内能追完，坚持！
💡 功能4：智能推荐（剧荒模式）
功能描述：
基于每日更新的追剧数据，分析用户偏好，智能推荐 5 部你可能喜欢的剧。

触发示例：

"剧荒了，推荐几部剧"

"有什么好看的推荐一下"

"我该看什么"

AI 分析维度：

用户追剧偏好分析（类型、标签）

追剧速度评估

多维度评分（类型匹配 + 标签匹配 + 评分 + 年份 + 集数）

过滤已追剧集

生成个性化推荐理由

调用的脚本：scripts/recommender.py

项目	说明
脚本路径	scripts/recommender.py
引用脚本	from data_manager import get_all_dramas
调用命令	python recommender.py
输入	无（自动读取本地数据）
输出	5部推荐剧集 + 推荐理由 + 用户画像
读取数据	data/drama_data.json
脚本执行流程：

text
recommender.py 运行
       ↓
调用 data_manager.get_all_dramas() 读取所有追剧数据
       ↓
分析用户偏好：类型、标签、追剧速度
       ↓
从20部推荐池中过滤已追剧集
       ↓
多维度评分：类型+标签+评分+年份+集数+随机
       ↓
排序取前5，生成个性化推荐理由
代码引用示例：

python
# recommender.py 中的引用
from data_manager import get_all_dramas

# 调用 data_manager 读取所有追剧数据
watch_list = get_all_dramas()
输出格式：

text
============================================================
💡 智能推荐报告
============================================================

📊 基于你的追剧数据：
   ├─ 在追剧集：3 部
   ├─ 偏好类型：悬疑, 古装, 年代
   ├─ 待更新集数：26 集
   └─ 追剧速度：快

------------------------------------------------------------
🎯 为你推荐：

1. 🎬 【狂飙】
   ├─ 类型：犯罪悬疑
   ├─ 评分：⭐ 8.5 分
   ├─ 集数：39 集
   ├─ 平台：爱奇艺
   ├─ 简介：扫黑除恶题材，张译主演
   └─ 推荐理由：你喜欢悬疑类型，豆瓣8.5+口碑佳作

2. 🎬 【三体】
   ├─ 类型：科幻悬疑
   ├─ 评分：⭐ 8.7 分
   ├─ 集数：30 集
   ├─ 平台：腾讯视频
   ├─ 简介：科幻巨制，刘慈欣同名小说改编
   └─ 推荐理由：你喜欢悬疑类型，豆瓣8.5+口碑佳作

...（共5部）

------------------------------------------------------------
⏳ 你还有 26 集待追，建议先追完再开新剧
📝 功能5：前情提要生成（一键回顾）
功能描述：
输入剧名和集数，AI 自动生成该集的内容摘要，同时结合每日更新的追剧进度数据。

触发示例：

"《黑暗荣耀》第7集讲了什么"

"帮我回忆一下《繁花》第10集"

"前情提要：《庆余年2》第20集"

AI 能力：

从 data_manager.py 读取追剧进度

查询预设摘要数据（覆盖10+部剧，50+集）

无数据时 AI 动态生成

结构化输出：主要事件 + 关键台词 + 伏笔提示 + 追剧进度

调用的脚本：scripts/recap.py

项目	说明
脚本路径	scripts/recap.py
引用脚本	from data_manager import get_drama_info, get_all_dramas
调用命令	python recap.py "黑暗荣耀" 7
输入	剧名 + 集数
输出	剧情摘要 + 追剧进度
读取数据	data/drama_data.json
脚本执行流程：

text
用户输入剧名+集数 → recap.py 运行
              ↓
       调用 data_manager.get_drama_info() 读取追剧进度
              ↓
       查询预设摘要数据（MOCK_RECAPS）
              ↓
       若无预设，AI 动态生成摘要
              ↓
       结构化输出：事件 + 台词 + 伏笔 + 进度
代码引用示例：

python
# recap.py 中的引用
from data_manager import get_drama_info, get_all_dramas

# 调用 data_manager 读取追剧进度
info = get_drama_info(drama_name)
my_ep = info.get('my_episode', 0)
latest = info.get('latest_episode', 0)

# 调用 data_manager 获取所有剧名（用于交互模式）
all_dramas = list(get_all_dramas().keys())
输出格式：

text
============================================================
📝 《黑暗荣耀》第 7 集 前情提要
============================================================

📊 追剧进度：
   ├─ 你看到：第 8 集
   ├─ 最新更新：第 16 集
   └─ 你还落后 8 集

------------------------------------------------------------

📌 主要事件：
  - 文东恩发现河道英的真实身份
  - 朴妍珍开始调查文东恩的过去
  - 朱如炡表白被拒

💬 关键台词：
  "『你以为你赢了？游戏才刚刚开始。』"

🔮 本集伏笔：
  - 河道英的过去即将揭晓

👉 继续看下一集吧！
📌 提示：用 parser.py 更新你的追剧进度
🗄️ 功能6：数据管理（底层支持）
功能描述：
所有脚本的数据读写核心，提供统一的数据接口。

调用的脚本：scripts/data_manager.py

项目	说明
脚本路径	scripts/data_manager.py
被谁引用	parser.py, scheduler.py, predictor.py, recommender.py, recap.py
提供功能	load_data()、save_data()、add_or_update_drama()、get_all_dramas()、get_drama_info()、get_summary()
数据文件	data/drama_data.json
调用命令	python data_manager.py（查看汇总）
提供的数据接口：

函数名	功能	被谁调用
load_data()	加载 data/drama_data.json	内部函数
save_data()	保存 data/drama_data.json	内部函数
add_or_update_drama()	添加或更新追剧记录	parser.py
get_all_dramas()	获取所有在追剧集	scheduler.py, predictor.py, recommender.py, recap.py
get_drama_info()	获取单部剧信息	predictor.py, recap.py
get_summary()	获取追剧汇总	parser.py
数据格式示例：

json
{
  "watch_list": {
    "黑暗荣耀": {
      "my_episode": 8,
      "latest_episode": 16,
      "last_update": "2026-07-12 14:30"
    }
  },
  "history": [...],
  "total_count": 2
}
脚本调用关系总图
text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          脚本引用关系图                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        data_manager.py                              │   │
│  │                        （数据管理核心）                             │   │
│  │  功能：读写 data/drama_data.json，提供数据接口                     │   │
│  │  提供函数：load_data()、save_data()、add_or_update_drama()、       │   │
│  │           get_all_dramas()、get_drama_info()、get_summary()        │   │
│  └──────────────────────────┬──────────────────────────────────────────┘   │
│                             │                                              │
│          ┌──────────────────┼──────────────────┐                           │
│          ▼                  ▼                  ▼                           │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐                  │
│  │  parser.py    │  │  scheduler.py │  │  predictor.py │                  │
│  │  追剧录入     │  │  日程生成     │  │  完结预测     │                  │
│  │  引用：       │  │  引用：       │  │  引用：       │                  │
│  │  add_or_      │  │  get_all_     │  │  get_drama_   │                  │
│  │  update_      │  │  dramas()     │  │  info()       │                  │
│  │  drama()      │  │               │  │  get_all_     │                  │
│  │  get_summary()│  │               │  │  dramas()     │                  │
│  └───────────────┘  └───────────────┘  └───────────────┘                  │
│                                                                             │
│  ┌───────────────┐  ┌───────────────┐                                      │
│  │ recommender.py│  │   recap.py    │                                      │
│  │  智能推荐     │  │  前情提要     │                                      │
│  │  引用：       │  │  引用：       │                                      │
│  │  get_all_     │  │  get_drama_   │                                      │
│  │  dramas()     │  │  info()       │                                      │
│  │               │  │  get_all_     │                                      │
│  │               │  │  dramas()     │                                      │
│  └───────────────┘  └───────────────┘                                      │
└─────────────────────────────────────────────────────────────────────────────┘
使用方式
在 Hermes Agent 中，直接向 AI 发送自然语言指令即可触发对应功能：

你想做的事	说一句话	调用的脚本
记录追剧进度	"我在看《黑暗荣耀》，更新到第8集"	parser.py
查看本周日程	"本周追剧日历"	scheduler.py
预测完结时间	"《繁花》什么时候完结"	predictor.py
求推荐	"剧荒了，推荐几部"	recommender.py
回忆剧情	"《庆余年2》第20集讲了什么"	recap.py
查看汇总	"显示追剧清单"	data_manager.py
技术实现
自然语言解析：正则表达式 + 语义理解，提取剧名和集数

数据持久化：JSON 文件存储，所有脚本共享数据

日程生成：基于追剧进度和播出规律，格式化输出

完结预测：基于当前进度和每天1集的速度推算

智能推荐：多维度评分（类型+标签+评分+年份+集数）

前情提要：预设摘要数据 + AI 动态生成

配置文件说明
references/schedule_rules.yaml：剧集播出规律配置

references/sample_history.json：示例追剧历史数据



🎯 AI 核心价值总结
功能	没有 AI	有 AI	AI 不可替代性
追剧录入	手动填Excel表格	自然语言一句话录入	✅ 语义理解+信息提取
日程生成	自己去查每部剧更新日	自动生成结构化日程	✅ 多源信息聚合+格式化
完结预测	凭感觉猜测	智能推算完结日期	✅ 模式识别+时间推算
智能推荐	到处问别人	基于追剧历史个性化推荐	✅ 用户画像+兴趣匹配
前情提要	翻半天找上一集	一键生成剧情摘要	✅ 自动摘要生成
核心结论：没有 AI，这就是一个普通的 Excel 表格；有 AI，它变成了一个"懂你的追剧管家"。


## 🤖 与 WorkBuddy 交互记录

### 交互记录1：创建项目文件结构

**用户指令：**
请帮我在当前工作目录 E:\jianxi\追剧日历管家 下，创建完整的项目文件结构

```text
```

**AI 执行过程：**
1. 创建 `skill/`、`data/`、`tests/`、`iteration/` 文件夹
2. 创建 `SKILL.md`、`README.md` 等核心文件
3. 创建 `scripts/` 和 `references/` 子目录及其文件


### 交互记录2：编写核心脚本

**用户指令：**
请编写 data_manager.py、parser.py、scheduler.py、predictor.py、recommender.py、recap.py 六个核心脚本

```text
```

**AI 执行过程：**
1. 编写 `data_manager.py`：数据持久化管理，提供统一的读写接口
2. 编写 `parser.py`：自然语言解析，支持 "开始看" 默认第1集
3. 编写 `scheduler.py`：基于真实数据生成追剧日程
4. 编写 `predictor.py`：智能预测完结日期
5. 编写 `recommender.py`：多维度评分，推荐5部剧
6. 编写 `recap.py`：查询预设摘要 + AI 动态生成


### 交互记录3：更新 SKILL.md 脚本调用说明

**用户指令：**
请在每个功能中增加「调用的脚本」说明，体现哪个功能用了哪个脚本

```text
```

**AI 执行过程：**
1. 为每个功能新增「调用的脚本」表格
2. 包含：脚本路径、引用方式、调用命令、输入输出、数据依赖
3. 新增「脚本调用关系总图」展示完整链路


### 交互记录4：迭代日志更新（4轮迭代）

**用户指令：**
请写4轮迭代日志，不要提到老师

```text
```

**AI 执行过程：**
1. V1.0→V1.1：修复"开始看"无法解析问题，通过率 85.7%→100%
2. V1.1→V1.2：新增 data_manager，实现数据持久化
3. V1.2→V2.0：所有脚本统一读写 data_manager，形成数据闭环
4. V2.0→V2.1：推荐联动、待更新提醒、多维度评分


### 交互记录5：测试验证

**用户指令：**
请测试所有脚本是否正常运行

```text
```

**AI 执行过程：**
1. 运行 `python parser.py "《黑暗荣耀》我看到第8集，最新16集"` → ✅ 成功
2. 运行 `python scheduler.py` → ✅ 生成日程
3. 运行 `python predictor.py "黑暗荣耀"` → ✅ 预测完结
4. 运行 `python recommender.py` → ✅ 推荐5部剧
5. 运行 `python recap.py "黑暗荣耀" 7` → ✅ 前情提要


### 交互记录6：test_record.md 测试记录

**用户指令：**
请根据测试结果，更新 test_record.md

```text
```

**AI 执行过程：**
1. 记录21个测试用例，100%通过
2. 验证所有脚本引用关系正常
3. 附上完整执行日志


### 交互记录7：README.md 更新

**用户指令：**
请更新 README.md，包含脚本引用关系和使用说明

```text
```

**AI 执行过程：**
1. 新增「脚本引用关系」章节
2. 展示数据流闭环图
3. 更新使用方式和测试说明


### 交互记录8：references/ 配置文件扩充

**用户指令：**
请更新 sample_history.json 和 schedule_rules.yaml，多一些数据

```text
```

**AI 执行过程：**
1. `sample_history.json`：12部→26部，新增 platform、total_episodes、statistics
2. `schedule_rules.yaml`：10部→29部，新增 genre、tags


### 交互记录9：__init__.py 更新

**用户指令：**
请更新 init.py，导出 data_manager 的所有函数

```text
```

**AI 执行过程：**
1. 新增 `from .data_manager import load_data, save_data, add_or_update_drama, get_all_dramas, get_drama_info, get_summary, delete_drama`
2. __all__ 从 5 个函数扩展到 10 个函数


### 交互记录10：GitHub 推送

**用户指令：**
请帮我推送代码到 GitHub

```text
```

**AI 执行过程：**
1. 执行 `git add .` 暂存所有文件
2. 执行 `git commit -m "追剧日历管家 v2.1: 完整版本，包含4轮迭代、21个测试用例、数据持久化、脚本联动"`
3. 执行 `git push origin master` 推送到远程仓库
4. 确认推送成功，所有 7 项提交内容完整

---

## 📊 交互统计

| 类别 | 次数 | 说明 |
|------|------|------|
| 创建/修改文件 | 12 次 | 包括 scripts、references、SKILL.md、README.md 等 |
| 功能测试 | 5 次 | parser、scheduler、predictor、recommender、recap |
| 迭代优化 | 4 轮 | V1.0→V1.1→V1.2→V2.0→V2.1 |
| 数据扩充 | 2 次 | sample_history.json 和 schedule_rules.yaml |
| GitHub 操作 | 3 次 | add、commit、push |

**总计交互次数：约 30+ 次**
