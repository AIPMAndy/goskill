<div align="center">

# GoSkill

**把“一次调用的 Skill”升级成“围绕目标持续推进，直到达标或超时”的执行模式。**

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Tests](https://github.com/AIPMAndy/goskill/actions/workflows/tests.yml/badge.svg)](https://github.com/AIPMAndy/goskill/actions/workflows/tests.yml)

**[English](README_EN.md) | 简体中文**

*不是魔法 Agent，而是一种更适合长任务、复杂任务、需要明确验收标准的执行封装。*

</div>

---

## 为什么会有 GoSkill？

很多任务不是“不会做”，而是：

- 做一轮就停
- 没有明确完成标准
- 任务很长，但中间没有阶段性验证
- 最终只返回“做完了”，却没人知道到底算不算真的完成

GoSkill 想解决的是这个问题：

> **把任务从“一次性函数调用”变成“围绕目标持续推进，直到满足成功标准”。**

它更像一个 **goal-driven execution helper**，而不是一个什么都能自动完成的神奇框架。

---

## 一句话理解

如果普通 Skill 像“执行一次就返回”，那 GoSkill 更像：

- 先定义目标
- 再定义成功标准
- 然后持续尝试 / 检查 / 重试
- 直到达标或超时

---

## 🆚 适合什么，不适合什么？

| 场景 | 普通函数 / Skill | GoSkill |
|------|------------------|---------|
| 一次性短任务 | ✅ | — |
| 长任务持续推进 | — | ✅ |
| 需要明确验收标准 | 🟡 | ✅ |
| 需要状态追踪 | 🟡 | ✅ |
| 复杂任务分阶段完成 | 🟡 | ✅ |

**GoSkill 的价值不在“更聪明”，而在“更会围绕目标管理执行过程”。**

---

## 🚀 快速开始

### 安装

```bash
pip install -e .
```

### 装饰器方式

```python
from goskill import goskill

@goskill(
    goal="将项目从 Android 迁移到鸿蒙",
    criteria={
        "compile": "0 errors",
        "test": "100% pass",
        "performance": ">= 90%"
    },
    max_hours=48
)
def migrate():
    # 你的任务逻辑
    return {"done": True}

migrate()
```

### 类方式

```python
from goskill import GoSkill

skill = GoSkill(
    goal="分析 1000 份财报",
    criteria={
        "coverage": ">= 90%",
        "report": "complete"
    },
    max_hours=24,
    max_attempts=20,
    verbose=False,  # 可选：关闭运行日志
)

result = skill.run(lambda: {"coverage": 95, "report": "complete"})
print(result)
print(skill.status)

structured = skill.run_with_result(lambda: {"coverage": 95, "report": "complete"})
print(structured)
```

---

## 🎬 最小可运行示例

仓库里已经放了一个最小 demo：

```bash
python examples/basic_usage.py
```

它会演示：
- 如何定义 goal
- 如何定义 criteria
- 如何执行并读取 status

---

## 核心能力

现在库里已经有两层返回方式：
- `run()`：返回原始任务结果
- `run_with_result()`：返回结构化结果对象（success / status / attempts / criteria_report）


### 1) 目标驱动
你不是只传一个函数，而是把任务表述成：
- **goal**：要达成什么
- **criteria**：怎样才算完成
- **max_hours**：最多跑多久
- **max_attempts**：最多尝试多少次（可选）

### 2) 持续尝试
如果没有达标，它不会默认“执行一次就结束”，而是继续推进，直到：
- 成功
- 超时
- 或你主动停止

### 3) 状态可追踪
内建 `status`，方便查看：
- 当前 goal
- 已尝试次数
- 已运行时长
- 最大允许时长
- 终态原因（`terminal_status`）
- 上一次 criteria 检查结果
- 上一次执行结果

---

## 工作方式

```text
定义目标 + 成功标准
        ↓
执行任务函数
        ↓
检查结果是否达标
        ↓
达标 → 返回结果
未达标 → 等待并继续尝试
        ↓
直到成功或超时
```

---

## 适用场景

### 适合
- 大规模重构
- 长时间分析任务
- 需要明确验收标准的自动化流程
- 研究型 / 迭代型任务
- 想把“执行 + 校验 + 重试”包装在一起的场景

### 不适合
- 单次问答
- 很小的同步函数
- 完全没有验收标准的任务
- 需要复杂分布式调度的生产级系统

---

## 项目边界

GoSkill 现在解决的是“单机、单进程、轻量 goal-driven execution loop”。

它**不**负责：
- 分布式调度
- 多节点任务编排
- 复杂持久化恢复
- 企业级队列系统

这个边界写清楚，反而有助于建立信任。

---

## 当前项目状态

GoSkill 现在更适合作为：

- **一个执行模式原型**
- **一个轻量 Python helper**
- **一个面向 OpenClaw / Agent workflow 的实验性封装**

它还不是完整的“长时间自治 Agent 平台”。

这点说清楚反而更好：
**预期对齐，可信度更高。**

---

## 开发

```bash
make install-dev
make test
make build
make version
```

---

## 相关文档

- [README_EN.md](README_EN.md) — English version
- [CONTRIBUTING.md](CONTRIBUTING.md) — 如何参与贡献
- [CHANGELOG.md](CHANGELOG.md) — 更新记录
- [SECURITY.md](SECURITY.md) — 安全说明
- [RELEASE.md](RELEASE.md) — 发布流程
- [Makefile](Makefile) — 常用开发命令
- [SKILL.md](SKILL.md) — OpenClaw Skill 版本说明

---

## License

[Apache-2.0](LICENSE)

---

<div align="center">

**如果你也在做长任务、复杂任务、目标驱动执行，欢迎给个 Star ⭐**

</div>
