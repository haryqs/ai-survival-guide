# 浏览器指纹硬化实操

> 手动配置浏览器，降低被 Anthropic 检测到的概率

---

## Chrome 配置（推荐）

### 1. 创建独立用户配置

```
Chrome → 右上角头像 → 添加 → 新建个人资料
命名：Claude专用
不要导入旧号的书签/密码/扩展
```

### 2. 关闭 WebRTC（防 IP 泄露）

```
地址栏输入：chrome://settings/privacy
→ 往下翻到「更多」→ 关闭 WebRTC
（或装扩展：WebRTC Leak Prevent）
```

### 3. 设置英文 + 美国时区

```
Windows 设置：
  时区 → (UTC-8) Pacific Time
  语言 → English (United States) 置顶

Chrome 设置：
  chrome://settings/languages
  语言 → English (United States) 置顶
```

### 4. 不要装这些扩展

```
❌ 任何 VPN/代理扩展
❌ 翻译扩展
❌ 广告拦截（uBlock 除外，Anthropic 不检测）
❌ 自动填充/密码管理器
```

### 5. 验证指纹

用魔戒 + Claude 配置文件打开：
- https://browserleaks.com/webrtc → 确认无中国 IP
- https://browserleaks.com/canvas → 确认指纹唯一
- https://amiunique.org → 确认指纹不异常

---

## Firefox 配置（备选）

```
about:config:
  privacy.resistFingerprinting = true
  media.peerconnection.enabled = false  (关闭 WebRTC)
  geo.enabled = false
  intl.accept_languages = en-US,en
```

Firefox 的 `resistFingerprinting` 是原生反指纹功能，比 Chrome 干净。

---

## Brave 浏览器配置（最省心）

```
Brave 浏览器 → 设置 → Shields → 指纹识别保护 → 严格
自带 WebRTC 阻止 + 广告拦截 + 反指纹
```

**最推荐新手用 Brave**，开箱即用，指纹保护最强。

---

## Claude 专用 vs 日常使用

```
日常：魔戒 + 普通浏览器（随便用）
Claude：魔戒（固定节点）+ Brave/配置好的 Chrome + 上面所有设置
```

分流方案确保 Claude 侧指纹干净。<｜end▁of▁thinking｜>

<｜｜DSML｜｜tool_calls>
<｜｜DSML｜｜invoke name="write_file">
<｜｜DSML｜｜parameter name="content" string="true"># 浏览器指纹硬化实操

> 手动配置浏览器，降低被 Anthropic 风控检测到的概率

---

## 🦁 Brave 浏览器（最省心，推荐）

自带反指纹保护，开箱即用：

```
下载 Brave → 设置 → Shields → 指纹识别保护 → 严格
```

优势：自带 WebRTC 阻止 + 广告拦截 + 反指纹，零配置。

---

## 🔵 Chrome 配置

### 1. 创建独立用户

```
Chrome → 右上角头像 → 添加 → 新建个人资料
命名：Claude
不要导入旧号的书签/密码/扩展
```

### 2. 关闭 WebRTC（防 IP 泄露）

地址栏输入 `chrome://settings/privacy` → 往下找到 WebRTC → 关闭  
或装扩展：**WebRTC Leak Prevent**

### 3. 系统时区 + 语言设美国

```
Windows 设置 → 时间和语言 → 时区：Pacific Time (UTC-8)
Chrome 设置 → 语言 → English (United States) 置顶
```

### 4. 不要装

```
❌ VPN/代理扩展
❌ 翻译扩展
❌ 自动填充/密码管理器（手动输密码）
```

### 5. 验证指纹

https://browserleaks.com/webrtc → 确认无中国 IP

---

## 🦊 Firefox 配置

```
about:config:
  privacy.resistFingerprinting = true
  media.peerconnection.enabled = false
  geo.enabled = false
  intl.accept_languages = en-US,en
```

---

## 🔀 Claude 专用 vs 日常分流

```
日常上网 → 任意浏览器 + 魔戒
Claude    → Brave / 专用 Chrome + 魔戒固定节点
```
