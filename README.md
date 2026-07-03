# AI 工具生存指南

从中国安全、低成本使用海外 AI 工具（Claude、ChatGPT 等）的实战经验库。

## 📂 目录

| 场景 | 文档 | 状态 |
|------|------|------|
| Claude Pro 安全注册与长期使用 | [claude-pro-guide.md](docs/claude-pro-guide.md) | ✅ 完整 |
| 低成本 VPS 对比 | [vps-comparison.md](docs/vps-comparison.md) | ✅ 完整 |
| 家宽 IP 获取方案 | [residential-ip.md](docs/residential-ip.md) | ✅ 完整 |
| Claude 封号原因分析 | [claude-ban-analysis.md](docs/claude-ban-analysis.md) | 🆕 |
| Claude Shield 防护代理 | [tools/claude_shield.py](tools/claude_shield.py) | 🆕 v2 |

## 🎯 核心思路

```
注册阶段 → 真实美国家宽 IP（Mysterium）
日常使用 → 干净稳定的代理/VPS + Claude Shield 防护
关键原则 → 注册 IP ≠ 日常 IP 可以，但不能来回跳
CLI 使用 → 永远通过 Claude Shield MITM 代理（改写系统环境信息）
```

## 🛡️ Claude Shield v2

MITM 代理，自动改写 Claude Code/API 请求中的中国检测信号：
- 时区：Asia/Shanghai → America/Los_Angeles
- 编码：GB2312/GBK → Windows-1252
- 键盘：中文布局 → US 布局
- 字体：SimSun/微软雅黑 → Arial/Times New Roman
- 系统语言：zh-CN → en-US
- 代理信息：IP/端口全部隐藏
- Unicode 旁路：曲线引号归一化

**启动：** 双击 `tools/start-claude-shield.bat`  
**使用：** `set HTTPS_PROXY=http://127.0.0.1:8890 && claude`

## 🔧 环境

- 主机：Windows
- 日常 VPN：魔戒（机场）
- 注册 IP：Mysterium（P2P 家宽网络）
- 手机验证：HeroSMS（美国物理手机号）
- 支付：美区 Apple ID + 礼品卡 → App Store 内购 Claude Pro
- 防护：Claude Shield MITM 代理（端口 8890）

## ⚠️ 关键发现

1. **Mysterium + 魔戒 TUN 不可行**：双重 NAT 导致 P2P 穿透失败。Mysterium 必须直连才能工作。
2. **Claude Code CLI 是封号主因**：-p 模式的 API 调用模式与 Web 使用完全不同，触发风控。
3. **Claude 风控是 AI 驱动的**，零人工申诉。系统环境信息被编码进 system prompt 作为检测依据。
4. **社区证实**：HN/Reddit 大量报告 v2.1.91 起 Claude Code 内置中国用户检测。
