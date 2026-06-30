# 低成本美国 VPS 对比

> 用于自建 WireGuard VPN 隧道，作为日常访问 Claude 的出口

## 📊 实测对比

| | **RackNerd 512** | **CloudCone VPS 1** | **BuyVM Slice 512** | **CloudCone VPS 2** |
|---|---|---|---|---|
| 年付 | $26.99 | $12.99 | $24 | $19.59 |
| 月折 | $2.25 | $1.08 | $2.00 | $1.63 |
| 内存 | 512MB | 1GB | 512MB | **2GB** |
| SSD | 30GB | 14GB | 10GB | **26GB** |
| 流量 | 500GB | 1TB | 无限 | **2TB** |
| 带宽 | 1Gbps | 1Gbps | 1Gbps | 1Gbps |
| 机房 | ✅ 洛杉矶 | ⚠️ 密苏里 | 拉斯维加斯 | ⚠️ 密苏里 |
| 延迟（国内） | ~150ms | ~250ms | ~180ms | ~250ms |
| 库存 | ✅ 有货 | ❌ 缺货 | ❌ 缺货 | ❌ 缺货 |
| **推荐** | **⭐ 首选** | 性价比高但缺货 | 无限流量 | 配置最强但缺货 |

---

## 🎯 结论

**RackNerd 512MB** 是目前唯一有货且性价比不错的方案：
- $26.99/年（约 ¥200）
- 洛杉矶机房，国内延迟最低
- 512MB 跑 WireGuard 完全够用

如果预算极其敏感，等 CloudCone 补货（$12.99/年）。

---

## 🔧 搭建步骤（RackNerd 为例）

### 1. 下单

```
https://my.racknerd.com/cart.php?a=add&pid=1
→ 选 Los Angeles 机房
→ 注册账号、付款
→ 等邮件收 IP 和 root 密码
```

### 2. 装 WireGuard（服务端）

```bash
ssh root@你的IP

# Debian/Ubuntu
apt update && apt install -y wireguard

# 生成密钥
wg genkey | tee /etc/wireguard/privatekey | wg pubkey > /etc/wireguard/publickey

# 配置 /etc/wireguard/wg0.conf
cat > /etc/wireguard/wg0.conf << 'EOF'
[Interface]
PrivateKey = <服务器私钥>
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey = <客户端公钥>
AllowedIPs = 10.0.0.2/32
EOF

# 开启转发
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf && sysctl -p

# 启动
systemctl enable --now wg-quick@wg0
```

### 3. Windows 客户端配置

下载 WireGuard Windows 客户端 → 新建隧道 → 填入客户端配置：

```ini
[Interface]
PrivateKey = <客户端私钥>
Address = 10.0.0.2/24
DNS = 8.8.8.8

[Peer]
PublicKey = <服务器公钥>
Endpoint = 服务器IP:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25
```

---

## ⚠️ VPS 的风险

即使 Fraud Score 0，机房 IP 仍能被 Anthropic 识别为"非家庭用户"。
最优方案是**注册用家宽、日常用 VPS**，组合使用。
