# 👻 ex-bot — 回忆 QQ 聊天机器人

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)

> 把回忆的聊天记录变成 persona，用 DeepSeek 驱动，通过 QQ 小号 7×24 小时陪你聊天。

---

## 🎬 5 分钟快速开始

```
# 1. 下载项目
git clone https://github.com/你的用户名/ex-bot.git
cd ex-bot

# 2. 运行（全程引导，不需要手配任何东西）
python setup.py
```

setup.py 会引导你完成：
1. 输入 DeepSeek API Key
2. 导出 QQ 聊天记录（支持 QCE / 消息管理器 / 手动文件）
3. 自动分析对话 → 生成回忆 persona
4. 自动下载 NapCat → 扫码登录 QQ 小号
5. 一键启动 bot

---

## 🏗 架构

```
你的 QQ (大号)
    │  发消息给 QQ小号
    ▼
QQ小号 (NapCat 注入)
    │  OneBot WebSocket
    ▼
ex-bot (Python)
    │  回忆 persona + 对话上下文
    ▼
DeepSeek API
    │  AI 生成回复
    ▼
QQ小号 → 自动回复你的大号
```

---

## 📦 项目结构

```
ex-bot/
├── setup.py              # 主控脚本（安装/配置/启动）
├── scripts/
│   ├── bot.py            # QQ bot 核心（WebSocket 服务器）
│   ├── parser.py         # QQ 聊天记录解析器
│   └── persona.py        # Persona 生成器
├── persona/
│   └── SKILL.md.sample   # 角色卡模板
├── config/
│   └── config.json       # 配置文件（自动生成）
├── tools/
│   └── (NapCat 自动下载到这里)
└── README.md
```

---

## 🔧 依赖

- Python 3.10+
- Windows 10/11（QQ 必须在 Windows 跑）
- DeepSeek API Key（[获取](https://platform.deepseek.com)）
- 一个 QQ 小号（和大号是好友）

---

## 🎮 命令

| 命令 | 作用 |
|------|------|
| `python setup.py` | 首次安装引导 |
| `python setup.py start` | 启动 bot |
| `python setup.py stop` | 停止 bot |
| `python setup.py persona` | 重新生成 persona |
| `python setup.py config` | 修改配置 |

Bot 运行时支持的聊天命令：
- `/reset` — 重置对话记忆
- `/status` — 查看 bot 状态

---

## 📊 工作原理

### 1. 聊天记录 → Persona
```
QQ聊天导出文件 (.txt)
    ↓ parser.py 解析
消息时间线 + 统计
    ↓ persona.py 分析
人物画像 (5层人格模型)
    ↓
系统 Prompt → DeepSeek
```

### 2. 消息处理流程
```
收到私聊消息
    ↓ 过滤（只回复大号）
加载 persona + 对话历史
    ↓
调用 DeepSeek API
    ↓
返回回复 → 发送
```

---

## ⚠️ 免责声明

- 本项目仅供个人回忆整理、情感回顾和创作实验
- **禁止**用于骚扰真人、冒充真人、侵犯隐私或任何滥用
- 生成的内容基于本地材料的模拟与重组，不代表真实人物
- 请尊重真实沟通、真实边界和真实生活

---

## 🙏 致谢

- [NapCatQQ](https://github.com/NapNeko/NapCatQQ) — QQ NT 协议框架
- [QCE (QQ Chat Exporter)](https://github.com/shuakami/qq-chat-exporter) — QQ 聊天导出工具
- [DeepSeek](https://platform.deepseek.com) — AI 模型
- [OneBot 11](https://github.com/botuniverse/onebot-11) — 机器人标准

---

## 📄 License

MIT © 2026
