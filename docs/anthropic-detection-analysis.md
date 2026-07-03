# Anthropic Claude 检测体系全分析

> 2026年7月最新调研。来源：Reddit逆向分析、V2EX 中文社区、explainx.ai、微信技术文章

---

## 🔬 五层检测体系

### Layer 1：客户端环境信号
| 信号 | 触发值 | 风险 |
|------|--------|------|
| 系统时区 | `Asia/Shanghai`, `Asia/Urumqi` | ☠️ 直接触发 Layer 2 |
| 键盘布局 | `0x0804`（中文PRC） | ⚠️ 高 |
| 系统编码 | CodePage 936 (GB2312) | ⚠️ 高 |
| 系统语言 | `zh-CN`, `CHS` | ⚠️ 高 |
| 字体列表 | SimSun, 微软雅黑 | ⚠️ 中 |
| 代理 URL | `127.0.0.1:7890` | ⚠️ 中 |

### Layer 2：Unicode 隐写术（v2.1.91+）
- 撇号 `'` (U+0027) → `ʼ` (U+02BC) 等 3 种变体
- 日期 `-` → `/`（仅 Asia/Shanghai, Asia/Urumqi 触发）
- XOR 加密（key=91）+ base64 编码在二进制中
- 在 system prompt 文本体内，非 headers

### Layer 3：IP 与网络
- 机房 IP vs 家宽 IP
- 邮件追踪像素（Gmail 有图片代理保护但不完全）
- 代理 hostname 模式匹配

### Layer 4：行为分析
- CLI `-p` 模式调用频率
- 活跃时间分布（暴露时区）
- 对话内容分析（项目名、公司名、语言习惯）
- 14 个中文 AI 实验室关键词

### Layer 5：账号关联
- 同 IP 多账号 → 集中封
- 旧号残留信息 → 新号关联
- 付款区域异常

---

## 🛡️ 防护策略

### 根本方案：系统底层伪装
```
Windows 设置：
  时区 → Pacific Time (UTC-8)
  区域 → United States
  语言 → English (US) + 删除中文
  键盘 → US English only
  系统区域设置 → English (US)
```

### 辅助方案：Claude Shield
- 改写 Layer 1 信号（headers/params）
- 剥离 Layer 2 隐写（system prompt 体内的 Unicode 变体）
- 注意：自身 MITM 可能被 TLS 指纹检测

### 禁忌
- ❌ 打开 Anthropic 邮件（追踪像素）
- ❌ 养号期内跑 CLI
- ❌ 频繁切换节点
- ❌ 申诉 = 关联更多信息

---

## 📅 关键时间线

| 日期 | 事件 |
|------|------|
| 2026-04-02 | v2.1.91 发布，隐写检测上线 |
| 2026-06-29 | Reddit 用户逆向发现隐写术 |
| 2026-06-30 | 各大媒体报道，V2EX 大规模讨论 |
| 2026-07-01 | GtAIGateway 加入隐写剥离 |
| 2026-07-07 | Fable 5 恢复日期（封号可能与此相关） |

---

## 📚 来源
- Reddit r/ClaudeAI 逆向分析原帖（100万+ 浏览）
- V2EX 1223862（封号潮讨论，77 回复）
- V2EX 1224022（存活配置讨论，113 回复）
- explainx.ai: "Claude Code Hidden China Fingerprinting"
- 微信「数字生命卡兹克」技术分析文章
- HN 多项讨论（48641160, 47853021, 47852834）
