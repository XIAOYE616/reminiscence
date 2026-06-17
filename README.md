# 👻 reminiscence — 让回忆「活过来」的 QQ 聊天机器人

> 💡 把你们曾经的聊天记录变成 AI 人格，用 DeepSeek 驱动，通过 QQ 小号 7×24 陪你聊天。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)

---

## 🤔 这是什么

你有没有想过——把过去的聊天记录喂给 AI，让它学会「用 ta 的语气回复你」？

reminiscence 就是干这个的：

`
你的 QQ 聊天记录 (.txt)
        ↓  自动分析
   ta 的人格画像 (persona)
        ↓  喂给 AI
   DeepSeek + persona = ta 的语气
        ↓  自动回复
   QQ 小号 → 你的大号 ← 就像 ta 在和你聊
`

**全程自动**，你只需要：
1. 导出 QQ 聊天记录（点几下鼠标）
2. 准备一个 DeepSeek API Key（免费注册就有）
3. 准备一个 QQ 小号（和大号是好友）
4. 运行 python setup.py

---

## 📋 你需要准备

| 东西 | 怎么获取 | 花费 |
|------|---------|------|
| **QQ 聊天记录** | QQ 消息管理器导出 .txt | 免费 |
| **DeepSeek API Key** | platform.deepseek.com 注册→API Keys | 注册送 500 万 token |
| **QQ 小号** | 注册一个新 QQ，加大号为好友 | 免费 |
| **Windows 电脑** | Win10/11 都行 | 你有 |
| **Python** | python.org 下载 3.10+ | 免费 |

---

## 🚀 5 分钟上手

### 第一步：下载项目

`ash
git clone https://github.com/XIAOYE616/reminiscence.git
cd reminiscence
`

### 第二步：运行安装向导

`ash
python setup.py
`

然后跟着提示走：输入 API Key → 选聊天记录 → 自动生成 persona → 扫码登录 QQ 小号 → Bot 上线。

### 第三步：聊天！

打开 QQ，给你的**小号**发消息——ta 会用 DeepSeek + 回忆的语气自动回复你。

---

## 📊 怎么导出 QQ 聊天记录？

### 方法 A：QQ 自带消息管理器（最简单）

1. 打开 QQ，找到和 ta 的聊天窗口
2. 右键消息区域 → **消息管理器** → **导出消息记录**
3. 格式选 **文本文件 (.txt)**
4. 时间范围选 **全部**
5. 保存到桌面

### 方法 B：QCE — QQ Chat Exporter（推荐，功能最强）

QCE 是最强的 QQ 聊天导出工具，配合 NapCat 使用：
https://github.com/shuakami/qq-chat-exporter

1. 确保 NapCat Framework 已启动（NapCat + QCE 一体化）
2. 打开浏览器访问 http://localhost:40653/qce-v4-tool
3. Token 在 C:\\Users\\你的用户名\\.qq-chat-exporter\\security.json 的 accessToken 字段
4. 选择要导出的人 → 设置时间范围 → 导出为 .txt
5. 导出的文件就是 setup.py 需要的格式

已打包好的 NapCat+QCE 一体化版本见最新 Release。

如果已安装 NapCat Framework（含 QCE）：

1. 打开 http://localhost:40653/qce-v4-tool
2. Token 在 %USERPROFILE%\.qq-chat-exporter\security.json
3. 选择联系人 → 导出

---

## 🏗 原理架构

`
你的大号 ──发消息──→ QQ小号(NapCat) ──WebSocket──→ bot.py
                                                      │
                                                 调用 DeepSeek
                                                      │
                                               ┌──────┴──────┐
                                               │  DeepSeek   │
                                               │ + persona   │
                                               └─────────────┘
    你的大号 ←──自动回复── QQ小号 ←──HTTP API──┘
`

---

## 🎮 命令参考

| 命令 | 作用 |
|------|------|
| python setup.py | 首次安装向导 |
| python setup.py bot | 只启动 bot |
| python setup.py persona | 重新生成 persona |

**Bot 聊天指令：**

| 指令 | 效果 |
|------|------|
| /reset | 清空对话记忆 |
| /status | 查看 bot 状态 |

---

## 🔧 常见问题

**Q: DeepSeek 要钱吗？**

注册就送 500 万 token。一条消息大约消耗 500 token，也就是能聊 **1 万条消息**。用完之后充值 10 块钱够用很久。

**Q: QQ 小号会被封吗？**

正常使用不会。不要用 bot 发广告、骚扰，控制消息频率。建议用小号而非主号。

**Q: Bot 不回复怎么办？**

1. 确认 QQ 小号已扫码登录
2. 确认 bot 窗口没关
3. 确认 API Key 正确
4. 确认大号和小号是好友

**Q: ta 的语气不像？**

导出更多记录 → python setup.py persona 重新生成。

**Q: 支持群聊吗？**

目前只支持私聊。

**Q: Mac/Linux 能用吗？**

NapCat 目前只支持 Windows。

---

## ⚠️ 免责声明

- 仅供 **个人回忆整理、情感回顾、创作实验**
- **严禁**用于骚扰、冒充、侵犯隐私或违法用途
- 生成内容是 AI 模拟，**不代表真实人物本人**
- 使用者自行承担一切后果

---

## 🙏 致谢

- [NapCatQQ](https://github.com/NapNeko/NapCatQQ) — QQ NT 协议框架
- [QCE](https://github.com/shuakami/qq-chat-exporter) — QQ 聊天导出神器
- [DeepSeek](https://platform.deepseek.com) — AI 模型
- [OneBot 11](https://github.com/botuniverse/onebot-11) — 机器人标准

---

## 📄 License

MIT © 2026

⭐ 如果帮到你了，给个 Star 呗~