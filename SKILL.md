---
name: goskill
description: |
  GoSkill - Let your Skill keep running until goal achieved.
  Continuous execution (100+ hours) with automatic verification.
  Goal-driven: Master monitors, Sub executes until success criteria met.
  Best for: complex coding, system design, large-scale refactoring.
license: Apache-2.0
metadata:
  author: Andy (AI PM)
  version: "1.0.0"
  tags:
    - goskill
    - long-running
    - goal-driven
    - persistence
    - complex-tasks
---

# GoSkill

> 让 Skill 持续运行，直到目标达成

## 核心概念

**GoSkill = 普通 Skill 的增强版**

| 普通 Skill | GoSkill |
|-----------|---------|
| 一问一答 | 持续运行 100+ 小时 |
| 容易放弃 | 不达目标不停止 |
| 质量不稳定 | 严格按标准验证 |
| 被动响应 | 主动推进直到成功 |

## 使用方式

### 方式1：装饰器（推荐）

```python
from goskill import goskill

@goskill(
    goal="将项目从 Android 迁移到鸿蒙",
    criteria={
        "compile": "0 errors",
        "test": "100% pass",
        "performance": ">= 90%"
    }
)
def my_task():
    # 你的任务逻辑
    pass

my_task()  # 持续运行直到达标
```

### 方式2：直接调用

```python
from goskill import GoSkill

skill = GoSkill(
    goal="分析1000份财报",
    criteria={
        "coverage": "100%",
        "accuracy": ">= 95%",
        "report": "complete"
    }
)

skill.run()  # 开始持续执行
```

## 工作原理

```
你设定目标 + 成功标准
    ↓
Master Agent 创建 Subagent
    ↓
Subagent 持续工作
    ↓
每5分钟验证进度
    ↓
达标 → 停止，交付结果
不达标 → 继续工作
    ↓
循环直到成功
```

## 适用场景

✅ **完美适合：**
- 大型代码重构/迁移
- 复杂系统架构设计
- 深度数据分析（1000+文件）
- 长期研究项目
- 自动化测试覆盖

❌ **不适合：**
- 简单的问答对话
- 一次性的小任务
- 没有明确成功标准的任务

## 示例

### 示例1：代码迁移

```python
@goskill(
    goal="将AIFireHome从Android迁移到鸿蒙",
    criteria={
        "compile": "0 errors, 0 warnings",
        "test": "100% pass rate",
        "performance": ">= 90% of original",
        "docs": "API documentation complete"
    },
    max_hours=100
)
def migrate_aifirehome():
    # 自动持续执行，直到所有标准达标
    pass
```

### 示例2：数据分析

```python
@goskill(
    goal="分析过去5年AI行业投资趋势",
    criteria={
        "coverage": "Top 500 companies",
        "insights": "10 high-potential tracks identified",
        "strategy": "executable investment strategy",
        "backtest": "annual return > 20%"
    }
)
def analyze_ai_investment():
    # 持续分析直到达标
    pass
```

## 注意事项

⚠️ **这会消耗大量时间和Token**
- 复杂任务可能需要运行数小时甚至数天
- 确保你有足够的API额度
- 我会定期汇报进度

⚠️ **需要明确的成功标准**
- 目标必须清晰可验证
- 标准必须量化
- 不能是模糊的要求

## 现在就可以用

我已经安装了这个Skill，你可以直接说：

> "圆圆，用GoSkill模式，帮我完成XXX，成功标准是YYY"

我会自动进入持续工作模式，不达目标不停止！
