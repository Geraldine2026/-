# 📺 追剧日历管家 (Drama Calendar Manager)

> 一个 AI 驱动的智能追剧管理工具，帮你统一管理所有在追的剧集，自动追踪更新进度、预测完结时间，并在剧荒时智能推荐下一部好剧。


## 📌 选题说明

### 选题背景
当代年轻人普遍同时追多部剧，经常面临以下痛点：
- 记不住每部剧的更新日和当前集数
- 不知道本周哪几部剧更新
- 猜不透剧集什么时候完结
- 剧荒时不知道看什么
- 隔太久忘了上一集讲了什么

### AI 核心价值

| 传统方式 | AI 方式 | AI 不可替代性 |
|----------|---------|---------------|
| 手动记录每部剧的更新日、集数 | 自然语言录入"我在看XXX，更新到第X集" | ✅ 语义理解+信息提取 |
| 自己去查"这周哪几部更新" | 自动生成本周追剧日程表 | ✅ 多源信息聚合+结构化输出 |
| 凭感觉猜"下一集哪天出" | 根据播出规律智能预测 | ✅ 模式识别+推算 |
| 剧荒时到处问别人推荐 | 根据你的追剧历史智能推荐 | ✅ 兴趣画像+个性化匹配 |
| 记不住上一集讲了什么 | 自动生成前情提要 | ✅ 自动摘要生成 |

**核心结论：没有 AI，这就是一个普通的 Excel 表格；有 AI，它变成了一个"懂你的追剧管家"。**


## 🎯 功能简介

| 功能 | 说明 | 触发示例 | 调用脚本 |
|------|------|----------|----------|
| 📺 **追剧录入** | 自然语言解析，自动提取剧名+集数并持久化 | "我在看《黑暗荣耀》，更新到第8集" | `parser.py` |
| 📅 **日程生成** | 基于真实追剧数据，自动生成本周追剧日历 | "本周追剧日历" | `scheduler.py` |
| 🔮 **进度预测** | 预测每部剧的完结日期，给出追剧建议 | "《繁花》什么时候完结" | `predictor.py` |
| 💡 **智能推荐** | 基于追剧历史，多维度评分推荐5部剧 | "剧荒了，推荐几部" | `recommender.py` |
| 📝 **前情提要** | AI自动生成剧情摘要，结合追剧进度 | "《黑暗荣耀》第7集讲了什么" | `recap.py` |


## 📁 项目结构

```
追剧日历管家/
├── README.md                  # 项目说明
├── skill/                     # Skill 文件
│   ├── SKILL.md               # 技能定义文件（含 yaml 前端配置）
│   ├── scripts/               # 脚本/工具代码
│   │   ├── __init__.py        # 模块入口
│   │   ├── data_manager.py    # 数据管理核心（被所有脚本引用）
│   │   ├── parser.py          # 追剧录入（引用 data_manager）
│   │   ├── scheduler.py       # 日程生成（引用 data_manager）
│   │   ├── predictor.py       # 完结预测（引用 data_manager）
│   │   ├── recommender.py     # 智能推荐（引用 data_manager）
│   │   └── recap.py           # 前情提要（引用 data_manager）
│   └── references/            # 参考文件/配置文件
│       ├── schedule_rules.yaml    # 剧集播出规律配置
│       ├── sample_history.json    # 示例追剧历史
│       └── usage_guide.md         # 使用指南
├── data/                      # 数据存储
│   ├── drama_data.json        # 追剧数据（脚本共享）
│   └── test_inputs.json       # 20个测试用例
├── tests/                     # 测试记录
│   └── test_record.md         # 测试执行记录（21个用例，100%通过）
└── iteration/                 # 迭代升级说明
    └── iteration_log.md       # 4轮迭代记录（V1.0→V2.1）
```


## 🔧 脚本引用关系

所有脚本通过 `data_manager.py` 共享数据，形成完整闭环：

```
用户录入 → parser.py → data_manager.py → data/drama_data.json
                                                    ↓
                                    scheduler.py 读取 → 生成真实日程
                                    predictor.py 读取 → 真实进度预测
                                    recommender.py 读取 → 基于真实历史推荐
                                    recap.py 读取 → 显示真实追剧进度
```

| 脚本 | 功能 | 引用 data_manager | 调用命令 |
|------|------|-------------------|----------|
| `data_manager.py` | 数据管理核心 | 被所有脚本引用 | `python data_manager.py` |
| `parser.py` | 追剧录入 | `add_or_update_drama()`, `get_summary()` | `python parser.py "《剧名》我X集，最新X集"` |
| `scheduler.py` | 日程生成 | `get_all_dramas()` | `python scheduler.py` |
| `predictor.py` | 完结预测 | `get_drama_info()`, `get_all_dramas()` | `python predictor.py "剧名"` |
| `recommender.py` | 智能推荐 | `get_all_dramas()` | `python recommender.py` |
| `recap.py` | 前情提要 | `get_drama_info()`, `get_all_dramas()` | `python recap.py "剧名" 集数` |


## 🚀 使用方式

### 方式一：命令行直接运行

```bash
# 进入脚本目录
cd skill/scripts

# 1. 录入追剧进度
python parser.py "《黑暗荣耀》我看到第8集，最新16集"
python parser.py "《繁花》我看到第12集，最新30集"

# 2. 查看本周追剧日程
python scheduler.py

# 3. 预测完结日期
python predictor.py "黑暗荣耀"

# 4. 获取智能推荐
python recommender.py

# 5. 查看前情提要
python recap.py "黑暗荣耀" 7

# 6. 查看数据汇总
python data_manager.py
```

### 方式二：在 Hermes Agent 中使用

将 `skill/` 目录放置到 Hermes Agent 的 skills 目录下，Agent 会自动识别并加载。用户发送自然语言即可触发对应功能：

| 你想做的事 | 说一句话 | 调用的脚本 |
|------------|----------|-----------|
| 记录追剧进度 | "我在看《黑暗荣耀》，更新到第8集" | `parser.py` |
| 查看本周日程 | "本周追剧日历" | `scheduler.py` |
| 预测完结时间 | "《繁花》什么时候完结" | `predictor.py` |
| 求推荐 | "剧荒了，推荐几部" | `recommender.py` |
| 回忆剧情 | "《庆余年2》第20集讲了什么" | `recap.py` |
| 查看汇总 | "显示追剧清单" | `data_manager.py` |

### 方式三：作为 Python 模块导入

```python
from skill.scripts.data_manager import get_all_dramas, add_or_update_drama
from skill.scripts.scheduler import generate_schedule
from skill.scripts.predictor import predict_completion
from skill.scripts.recommender import recommend_dramas
from skill.scripts.recap import generate_recap
from skill.scripts.parser import parse_user_input

# 录入
add_or_update_drama("黑暗荣耀", 8, 16)

# 日程
print(generate_schedule())

# 预测
print(predict_completion("繁花"))

# 推荐
print(recommend_dramas(5))

# 前情提要
print(generate_recap("黑暗荣耀", 7))
```

## 📊 测试说明

本项目包含 21 个测试用例，覆盖全部 6 个脚本，通过率 100%：

| 功能模块 | 脚本 | 测试用例数 | 通过率 |
|----------|------|-----------|--------|
| 数据管理 | `data_manager.py` | 3 | 100% |
| 追剧录入 | `parser.py` | 6 | 100% |
| 日程生成 | `scheduler.py` | 2 | 100% |
| 完结预测 | `predictor.py` | 4 | 100% |
| 智能推荐 | `recommender.py` | 2 | 100% |
| 前情提要 | `recap.py` | 4 | 100% |
| **合计** | | **21** | **100%** |

详细测试记录请查看 `tests/test_record.md`

## 🔄 迭代记录

本项目经历了 4 轮迭代，从 V1.0 演进到 V2.1：

| 版本 | 迭代主题 | 核心改进 |
|------|----------|----------|
| V1.0 | 初始版本 | 5个独立脚本，基础功能完整 |
| V1.1 | 解析优化 | 修复"开始看"无法解析问题，通过率 85.7%→100% |
| V1.2 | 数据持久化 | 新增 data_manager，数据永不丢失 |
| V2.0 | 数据共享闭环 | 所有脚本统一读写 data_manager |
| V2.1 | 脚本联动升级 | 推荐动态过滤、待更新提醒、多维度评分 |

详细迭代记录请查看 `iteration/iteration_log.md`

## 📝 技术栈

- Python 3.8+：所有脚本基于 Python 开发
- JSON：数据持久化存储格式
- 正则表达式：自然语言解析
- PyYAML（可选）：配置文件解析


## 📄 许可证

仅供学习交流使用
