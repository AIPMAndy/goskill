# GoSkill

[![PyPI](https://img.shields.io/badge/pypi-v1.0.0-blue)](https://pypi.org/project/goskill/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://github.com/AIPMAndy/goskill/blob/main/LICENSE)

**让 Skill 持续运行，直到目标达成。**

GoSkill 是一个目标驱动的多智能体执行框架，专为 OpenClaw 设计。它让你的 Skill 能够持续运行数小时甚至数天，自动验证进度，不达目标绝不停止。

---

## ✨ 核心特性

### 🎯 目标驱动
- 明确设定目标和成功标准
- Skill 自动分解任务并持续执行
- 严格验证，不达标准不停止

### ⏱️ 持久运行
- 支持 100+ 小时连续执行
- 自动保存进度，随时恢复
- 遇到错误自动重试，智能恢复

### ✅ 自动验证
- 每 5 分钟检查一次进度
- 自动对比实际结果与成功标准
- 达标立即停止，不达标继续优化

---

## 🚀 快速开始

### 安装

```bash
pip install goskill
```

### 基础用法

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
def migrate():
    # 你的迁移代码
    pass

migrate()  # 持续运行直到达标
```

### 高级用法

```python
from goskill import GoSkill

skill = GoSkill(
    goal="分析 1000 份财报",
    criteria={
        "coverage": "100%",
        "accuracy": ">= 95%",
        "insights": "complete"
    },
    max_hours=100
)

result = skill.run()
```

---

## 📊 对比

| 特性 | 普通 Skill | GoSkill |
|------|-----------|---------|
| 执行时间 | 几分钟 | 数小时/数天 |
| 错误处理 | 停止并报告 | 自动重试恢复 |
| 完成验证 | 无 | 严格标准检查 |
| 进度跟踪 | 无 | 每 5 分钟报告 |
| 适用任务 | 简单/短时 | 复杂/长期 |

---

## 💡 使用场景

### 场景 1：大规模代码重构
```python
@goskill(
    goal="将 10 万行 Android 代码重构为鸿蒙代码",
    criteria={
        "compile": "0 errors, 0 warnings",
        "test": "100% pass rate",
        "performance": ">= 90% of original",
        "docs": "complete API documentation"
    },
    max_hours=100
)
def refactor():
    # 自动持续重构，直到所有标准达标
    pass
```

### 场景 2：深度数据分析
```python
@goskill(
    goal="分析过去 5 年 AI 行业投资趋势",
    criteria={
        "coverage": "Top 500 companies",
        "accuracy": ">= 95%",
        "insights": "10 high-potential tracks identified",
        "strategy": "executable investment strategy",
        "backtest": "annual return > 20%"
    }
)
def analyze():
    # 自动持续分析，直到达标
    pass
```

### 场景 3：复杂系统设计
```python
@goskill(
    goal="设计一个高并发交易系统",
    criteria={
        "architecture": "complete documentation",
        "code": "core modules implemented",
        "test": "stress test passed",
        "security": "no high-risk vulnerabilities"
    },
    max_hours=200
)
def design():
    # 自动持续设计开发，直到达标
    pass
```

---

## 🔧 工作原理

```
你设定目标 + 成功标准
        ↓
Master Agent 创建 Subagent
        ↓
Subagent 持续工作
        ↓
每 5 分钟验证进度
        ↓
达标 → 停止，交付结果
不达标 → 继续工作
        ↓
循环直到成功
```

---

## 🛡️ 注意事项

⚠️ **这会消耗大量时间和 Token**
- 复杂任务可能需要运行数小时甚至数天
- 确保你有足够的 API 额度
- 我会定期汇报进度

⚠️ **需要明确的成功标准**
- 目标必须清晰可验证
- 标准必须量化
- 不能是模糊的要求

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

## 📞 联系

- **Twitter**: @AIPMAndy
- **微信**: AI PMAndy
- **邮箱**: andy@aipm.com

---

**现在就可以用 → [快速开始](#快速开始)**

---

*让 Skill 不再半途而废*