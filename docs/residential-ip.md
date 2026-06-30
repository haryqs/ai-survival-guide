# 家宽 IP 获取方案

> 注册 AI 服务时使用真实美国家宽 IP，大幅降低封号风险

## 🥇 Mysterium（推荐）

P2P 网络，你的流量从真实美国人家庭路由器出去。

| 项目 | 说明 |
|------|------|
| IP 类型 | 真·美国家宽（Comcast/AT&T 等） |
| 费用 | 按流量，$3 够用很久 |
| 支付 | PayPal / 加密货币（MYST） |
| 客户端 | Windows/Mac 免费 |

### 充值方式

1. **PayPal**（最方便）：绑银联储蓄卡直接付
2. **MYST 代币**（无 PayPal）：
   - OKX/Binance C2C 买 USDT → 换 MYST → 提到 Mysterium 钱包地址（Polygon 链）
   - 或用 MetaMask + QuickSwap：买 MATIC → 提到 MetaMask → QuickSwap 换 MYST → 打到 Mysterium 地址

### 验证 IP

连上后浏览器打开 `http://ip-api.com/json/`，确认：
- ISP 是家宽运营商（Comcast/Spectrum/AT&T/Verizon）
- 不是机房（DigitalOcean/AWS/FDCservers/Psychz）

---

## 🥈 ISP 静态代理

商业住宅 IP 代理服务，拿到一个 Socks5 代理地址直接用。

| 服务 | 价格 | 特点 |
|------|------|------|
| IPRoyal | ~$2.7/月 | 正规厂商，IP 干净 |
| Proxy-Seller | ~$4-6/月 | ISP 类型静态 IP |
| 淘宝/咸鱼 | ¥10-30/月 | 便宜但需挑靠谱卖家 |

---

## 🥉 自建家宽节点

在美国朋友家里放树莓派/软路由，搭 WireGuard。

| 优点 | 缺点 |
|------|------|
| 完全掌控，最安全 | 需要美国有可靠朋友 |
| 零月费 | 维护麻烦 |

---

## ✅ IP 质量检测标准

| 检测项 | 好 | 坏 |
|--------|-----|-----|
| ISP 运营商 | Comcast/AT&T/Spectrum | DigitalOcean/AWS/FDCservers |
| Fraud Score | < 30 | > 50 |
| 是否识别为 VPN | 否 | 是 |

测试站：`http://ip-api.com/json/` 和 `https://scamalytics.com/ip`

---

## ⚠️ 注意事项

- 不要频繁切换 IP（注册时和日常用时保持一致）
- 不要用数据中心 IP 注册 AI 服务（必死）
- 注册阶段的 IP 是最关键的一次性审查
- 如果买淘宝静态代理，先验 ISP 再付款
