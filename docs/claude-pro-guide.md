# Claude Pro 安全注册与长期使用指南

> 适用于：从中国注册 Claude Pro，追求最低封号风险，预算 ¥200/年以内

## 📋 最终方案

```
注册用：Mysterium 美国家宽 IP（一次性）
日常用：魔戒 VPN（已有）
```

**分期流**：注册时全程 Mysterium，日常 Claude 走 Mysterium / 魔戒。
**总成本**：Mysterium $3 + 魔戒（已有年付）

---

## 🔧 准备工作

### 1. 美区 Apple ID + 礼品卡

- 创建全新美区 Apple ID（不要用旧号）
- 购买美区 App Store 礼品卡（$20 起）
- 在 iPhone 上兑换到 Apple ID 余额

### 2. 美国手机号

- 推荐：HeroSMS（美国物理 SIM 卡，非 VOIP）
- 备选：Ultra Mobile PayGo（$3/月）、Tello（$5/月起）
- **必须**能在注册 Gmail 和 Claude 时接收验证码

### 3. 全新 Gmail

- 不要用旧 Gmail（可能关联旧 Claude 封号记录）
- 不要用点号变体（`name@gmail.com` → `na.me@gmail.com`，Google 视为同一邮箱）
- 不要用 QQ/163 邮箱

---

## 🚀 注册流程（按顺序）

### 步骤 1：Mysterium 安装与充值

```bash
# 下载（Windows）
https://github.com/mysteriumnetwork/mysterium-vpn-desktop/releases/latest
→ 找到 MysteriumDark-Setup-*.exe

# 注意：GitHub 在国内直连可能失败，需先开魔戒/代理下载
```

安装后：
1. 创建账号（邮箱注册）
2. 充值 $3（PayPal / MYST 加密货币）
3. 连接美国 → 选带 **Residential** 标签的节点

**验证 IP 质量**：连上后浏览器打开 `http://ip-api.com/json/`
- ISP 应该是 `Comcast` / `Spectrum` / `AT&T` / `Verizon` 等家宽运营商
- 不应该是 `DigitalOcean` / `AWS` / `FDCservers` / `Psychz` 等机房

### 步骤 2：注册 Gmail

```
全程保持 Mysterium 连着！

1. 全新浏览器无痕窗口
2. 访问 mail.google.com → 创建账号
3. 名字用拼音（如 Dawei Zhang）
4. 手机验证 → HeroSMS 接码
```

### 步骤 3：注册 Claude

```
全程保持 Mysterium 连着！

1. 浏览器访问 claude.ai → 点注册
2. 用新 Gmail 邮箱注册（不要 Google 登录）
3. 手机验证 → HeroSMS 再接一次码
```

### 步骤 4：iPhone 订阅 Pro

```
1. iPhone App Store 登录美区 Apple ID（余额已充 $20）
2. 下载 Claude App
3. 用新注册的 Claude 账号登录
4. App 内点「Upgrade to Pro」→ 用 Apple ID 余额支付
5. $20/月 自动扣款（每月提前充好礼品卡）
```

---

## ⚠️ 养号期（前 7 天）

| 天数 | 行为 |
|------|------|
| Day 1-2 | 每天 5-10 条普通对话，不传文件 |
| Day 3-4 | 可用到 20-30 条/天，可传小文件 |
| Day 5-7 | 正常使用，避免极限压测 |
| Day 7+ | 完全解禁，但不要切换 IP |

---

## 🛡️ 长期安全守则

| 规则 | 说明 |
|------|------|
| 不切换 IP | 始终用同一个出口 |
| 不频繁登录 | 不要多个设备同时登录 |
| 不敏感内容 | 避免触发人工审核 |
| 每月按时续费 | 付费账号容忍度高得多 |
| Mysterium 备用 | 如果魔戒节点被标黑，切到 Mysterium |

---

## 🔄 如果被封了怎么办

1. **不要申诉**（申诉会关联更多信息）
2. 全新 Apple ID + 新 Gmail + 新 HeroSMS 号 + 新 Mysterium IP
3. 旧号的任何信息都不要复用
4. 旧 iPhone 上完全退出旧 Apple ID

---

## 💡 关键认知

- **Apple ID 邮箱 ≠ Claude 注册邮箱**，两者不需要相同
- App Store 只是付款工具，Claude 账号完全独立
- 注册时的 IP 是最关键的审计点
- **家用 IP > 机房 IP**，Fraud Score 低 ≠ 安全
- 付费用户被封的概率远低于免费用户

---

## 📚 相关文档

- [VPS 选购对比](vps-comparison.md)
- [家宽 IP 获取方案](residential-ip.md)
