# 📺 追剧日历管家 (Drama Calendar Manager)

> 一个 AI 驱动的智能追剧管理工具，帮你统一管理所有在追的剧集，自动追踪更新进度、预测完结时间，并在剧荒时智能推荐下一部好剧。

---

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

---

## 🎯 功能简介

| 功能 | 说明 | 触发示例 |
|------|------|----------|
| 📺 **追剧录入** | 自然语言解析，自动提取剧名+集数 | "我在看《黑暗荣耀》，更新到第8集" |
| 📅 **日程生成** | 自动生成本周追剧日历 | "本周追剧日历" |
| 🔮 **进度预测** | 预测每部剧的完结日期 | "《繁花》什么时候完结" |
| 💡 **智能推荐** | 根据追剧历史推荐3-5部剧 | "剧荒了，推荐几部" |
| 📝 **前情提要** | AI自动生成剧情摘要 | "《黑暗荣耀》第7集讲了什么" |

---

## 📁 项目结构

```
追剧日历管家/
├── README.md                  # 项目说明
├── skill/                     # Skill 文件
│   ├── SKILL.md               # 技能定义文件（含 yaml 前端配置）
│   ├── scripts/               # 脚本/工具代码
│   │   ├── __init__.py        # 模块入口
│   │   ├── parser.py          # 自然语言解析
│   │   ├── scheduler.py       # 日程生成
│   │   ├── predictor.py       # 完结预测
│   │   ├── recommender.py     # 智能推荐
│   │   └── recap.py           # 前情提要生成
│   └── references/            # 参考文件/配置文件
│       ├── schedule_rules.yaml    # 剧集播出规律配置
│       ├── sample_history.json    # 示例追剧历史
│       └── usage_guide.md         # 使用指南
├── data/                      # 测试数据
│   └── test_inputs.json       # 20个测试用例
├── tests/                     # 测试记录
│   └── test_record.md         # 测试执行记录
└── iteration/                 # 迭代升级说明
    └── iteration_log.md       # 2轮迭代记录
```

---

## 🚀 使用方式

### 方式一：在 Hermes Agent 中使用

将 `skill/` 目录放置到 Hermes Agent 的 skills 目录下，Agent 会自动识别并加载。

### 方式二：命令行测试

```bash
# 进入脚本目录
cd skill/scripts

# 测试录入功能
python parser.py

# 测试日程生成
python scheduler.py

# 测试完结预测
python predictor.py

# 测试智能推荐
python recommender.py

# 测试前情提要
python recap.py
```

### 方式三：作为 Python 模块导入

```python
from skill.scripts import (
    parse_drama_input,
    generate_schedule,
    predict_completion,
    recommend_dramas,
    generate_recap
)

# 录入
result = parse_drama_input("我在看《黑暗荣耀》，更新到第8集")
print(result)

# 日程
schedule = generate_schedule()
print(schedule)

# 预测
prediction = predict_completion("繁花")
print(prediction)

# 推荐
recommendations = recommend_dramas(3)
print(recommendations)

# 前情提要
recap = generate_recap("《黑暗荣耀》第7集讲了什么")
print(recap)
```

---

## 📊 测试说明

本项目包含 20 个测试用例，覆盖所有功能模块：

| 功能模块 | 测试用例数 |
|----------|-----------|
| 追剧录入 | 7 |
| 日程生成 | 3 |
| 进度预测 | 3 |
| 智能推荐 | 3 |
| 前情提要 | 3 |
| 边界测试 | 1 |
| **合计** | **20** |

详细测试记录请查看 `tests/test_record.md`

---

## 🔄 迭代记录

本项目经历了 2 轮迭代优化，详细记录请查看 `iteration/iteration_log.md`

- **V1.0 → V1.1**：优化自然语言解析的准确率（80% → 95%）
- **V1.1 → V1.2**：推荐算法从关键词匹配升级为 AI 语义推荐

---

## 📝 技术栈

- Python 3.8+
- PyYAML（配置文件解析）
- AI API（自然语言处理、摘要生成、智能推荐）

---

## 📄 许可证

仅供学习交流使用
