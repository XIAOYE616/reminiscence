# 👻 ex-bot — 让前任「活过来」的 QQ 聊天机器人

> 💡 把你们曾经的聊天记录变成 AI 人格，用 DeepSeek 驱动，通过 QQ 小号 7×24 陪你聊天。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![平台](https://img.shields.io/badge/平台-Windows%2010%2F11-lightgrey)]()

---

## 🤔 这是什么？

你有没有想过——把前任的聊天记录喂给 AI，让它学会「用 ta 的语气回复你」？

ex-bot 就是干这个的：

```
你的 QQ 聊天记录 (.txt)
        ↓  自动分析
   ta 的人格画像 (persona)
        ↓  喂给 AI
   DeepSeek + persona = ta 的语气
        ↓  自动回复
   QQ 小号 → 你的大号 ← 就像 ta 在和你聊
```

**全程自动**，你只需要：
1. 导出 QQ 聊天记录（点几下鼠标）
2. 准备一个 DeepSeek API Key（免费注册就有）
3. 准备一个 QQ 小号（和大号是好友）
4. 运行 `python setup.py`

---

## 📋 你需要准备

| 东西 | 怎么获取 | 花费 |
|------|---------|------|
| **QQ 聊天记录** | QQ 消息管理器导出 `.txt` | 免费 |
| **DeepSeek API Key** | [platform.deepseek.com](https://platform.deepseek.com) 注册→API Keys | 注册送 500 万 token（够聊很久） |
| **QQ 小号** | 注册一个新 QQ，加大号为好友 | 免费 |
| **Windows 电脑** | Win10/11 都行 | 你有 |
| **Python** | [python.org](https://python.org) 下载 3.10+ | 免费 |

---

## 🚀 5 分钟上手

### 第一步：下载项目

```bash
# 打开 PowerShell 或 CMD，输入：
git clone https://github.com/XIAOYE616/reminiscence.git
cd reminiscence
```

> 没有 git？点页面右上角绿色 `Code` → `Download ZIP` → 解压也行

### 第二步：运行安装向导

```bash
python setup.py
```

然后跟着提示走：

```
  👻 ex-bot v1.0

  [1/5] 请输入 DeepSeek API Key: sk-xxxx
        （去 platform.deepseek.com 注册就有）

  [2/5] QQ 聊天记录在哪里？
        [1] 我用 QCE 导出了（推荐）
        [2] 文件已经在桌面了
        [3] 我用 QQ 自带的消息管理器导出了

  [3/5] ta 叫什么？→ 焙焙
        你叫什么？ → 折白菊
        正在分析 13363 条消息...
        ✅ persona 已生成

  [4/5] 正在配置 NapCat...
        请输入 QQ 小号：1460673995
        请用手机 QQ 扫描屏幕上的二维码

  [5/5] 🎉 Bot 启动！给 QQ 小号发消息试试
```

### 第三步：聊天！

打开 QQ，给你的**小号**发消息——ta 会用 DeepSeek + 前任语气自动回复你。

---

## 📊 怎么导出 QQ 聊天记录？

### 方法 A：QQ 自带消息管理器（最简单）

1. 打开 QQ，找到和 ta 的聊天窗口
2. 右键消息区域 → **消息管理器** → **导出消息记录**
3. 格式选 **文本文件 (.txt)**
4. 时间范围选 **全部**
5. 保存到桌面

### 方法 B：QCE（功能更强，支持所有格式）

如果你已经装了 NapCat Framework（含 QCE）：

1. 打开 `http://localhost:40653/qce-v4-tool`
2. Token 在 `C:\Users\你的用户名\.qq-chat-exporter\security.json`
3. 选择联系人 → 导出

---

## 🏗 原理架构

```
┌──────────┐    发消息     ┌──────────┐   WebSocket   ┌──────────┐
│ 你的大号  │ ──────────→  │ QQ 小号   │ ───────────→  │ ex-bot   │
│ 4775...  │ ←────────── │(NapCat)  │ ←─────────── │ (Python) │
└──────────┘   自动回复    └──────────┘   HTTP API    └────┬─────┘
                                                          │
                                                    调用 DeepSeek
                                                          │
                                                   ┌──────┴──────┐
                                                   │  DeepSeek   │
                                                   │ + persona   │
                                                   └─────────────┘
```

**关键组件：**

| 组件 | 作用 |
|------|------|
| **NapCat** | 让 QQ 能被程序控制（注入 QQ NT 进程） |
| **OneBot** | QQ 机器人的标准接口协议 |
| **bot.py** | 监听消息 → 调 AI → 发回复 |
| **DeepSeek** | 国产大模型，便宜好用，中文理解力强 |
| **Persona** | 从聊天记录里提取的人格画像（system prompt） |

---

## 📁 项目结构

```
reminiscence/
├── setup.py                ← 🎯 主控脚本（一键安装/配置/启动）
├── scripts/
│   └── bot.py              ← QQ bot 核心（WebSocket 服务端）
├── persona/
│   └── SKILL.md.sample     ← 角色卡模板（生成后在这里）
├── config/
│   └── config.json         ← 你的配置（自动生成，不要提交！）
├── tools/                  ← NapCat 自动下载到这里
├── README.md               ← 你正在看的这个
├── LICENSE                 ← MIT
└── .gitignore
```

---

## 🎮 命令参考

| 命令 | 作用 |
|------|------|
| `python setup.py` | 首次安装向导 |
| `python setup.py bot` | 只启动 bot（已配置过的话） |
| `python setup.py persona` | 只重新生成 persona |

**Bot 运行时支持的聊天指令：**

| 指令 | 效果 |
|------|------|
| `/reset` | 清空对话记忆（ta 会忘记刚才聊了什么） |
| `/status` | 查看 bot 运行状态 |

---

## 🔧 常见问题

<details>
<summary><b>Q: DeepSeek 要钱吗？</b></summary>

注册就送 500 万 token。一条消息大约消耗 500 token，也就是能聊 **1 万条消息**。用完之后：
- 充值 10 块钱 ≈ 聊到天荒地老
- 或者换用其他兼容 OpenAI 格式的 API（如 Qwen、GLM 等）
</details>

<details>
<summary><b>Q: QQ 小号会被封吗？</b></summary>

正常使用不会。但注意：
- 不要用 bot 发广告、骚扰
- 控制消息频率（bot 默认正常语速回复）
- 建议用小号而非主号
</details>

<details>
<summary><b>Q: 导出聊天记录失败怎么办？</b></summary>

1. 关掉 QQ 重试
2. 换 `.mht` 格式试试
3. 用 QCE 工具（methods B）
4. 直接把导出文件拖到项目文件夹，运行 `python setup.py persona`
</details>

<details>
<summary><b>Q: Bot 不回复怎么办？</b></summary>

1. 确认 QQ 小号已经扫码登录（能看到 QQ 在线）
2. 确认 `python setup.py bot` 的窗口没关
3. 确认 DeepSeek API Key 没输错
4. 确认大号和小号是好友关系
5. 看看 bot 窗口有没有报错日志
</details>

<details>
<summary><b>Q: ta 的语气不像怎么办？</b></summary>

1. 导出更多聊天记录（越多越像）
2. 导出时选「全部时间」
3. 运行 `python setup.py persona` 重新生成
4. 在 persona/SKILL.md 里手动调整
</details>

<details>
<summary><b>Q: 能支持微信群聊吗？</b></summary>

目前只支持私聊（一对一）。群聊支持计划中。
</details>

<details>
<summary><b>Q: Mac/Linux 能用吗？</b></summary>

NapCat（QQ 注入框架）目前只支持 Windows。因为 QQ NT 只有 Windows 版本能用 NapCat 注入。
</details>

---

## ⚠️ 免责声明

- 本项目仅供 **个人回忆整理、情感回顾、创作实验**
- **严禁**用于：骚扰真人、冒充真人、侵犯隐私、报复或任何违法用途
- 生成的一切内容都是基于本地材料的 AI 模拟，**不代表真实人物本人**
- 请尊重真实沟通、真实边界和真实生活
- 使用者自行承担一切后果

---

## 🙏 致谢

站在巨人的肩膀上：

- [NapCatQQ](https://github.com/NapNeko/NapCatQQ) — QQ NT 协议框架
- [QCE (QQ Chat Exporter)](https://github.com/shuakami/qq-chat-exporter) — QQ 聊天导出神器
- [DeepSeek](https://platform.deepseek.com) — 国产良心大模型
- [OneBot 11](https://github.com/botuniverse/onebot-11) — 机器人标准协议

---

## 📄 License

MIT © 2026

---

⭐ 如果帮到你了，给个 Star 呗~
