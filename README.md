# GoSkill

> 让 Skill 持续运行，直到目标达成

[![Apache 2.0 License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/Built%20for-OpenClaw-purple)](https://github.com/openclaw/openclaw)

---

## 💡 为什么需要 GoSkill？

**普通 Agent：一问一答，用完即走**

**GoSkill：持续运行 100+ 小时，不达目标不停止**

```
你：帮我重构这个项目
普通 Agent：好的，我看看... [分析完成，给出建议] [结束]

GoSkill：开始执行...
[持续运行 72 小时]
[自动编译验证]
[自动测试验证]
[自动性能验证]
[全部达标，交付完整代码]
```

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
    goal="分析1000份财报",
    criteria={
        "coverage": "100%",
        "accuracy": ">= 95%"
    },
    max_hours=100
)

result = skill.run()
```

---

## 📚 文档

- [快速开始](docs/quickstart.md)
- [API文档](docs/api.md)
- [示例](examples/)

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

## 📞 联系

- **Twitter**: @AIPMAndy
- **微信**: AI PMAndy

---

**让 Skill 不再半途而废 → [快速开始](#快速开始)**
