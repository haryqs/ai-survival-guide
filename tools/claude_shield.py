"""
Claude Shield v2 — MITM proxy addon for mitmproxy.
Sanitizes all Anthropic API requests to remove China-detection signals.
Enhanced with telemetry stripping, IME/IME detection removal, and audit logging.

Usage:
    mitmdump -s claude_shield.py --mode upstream:http://127.0.0.1:7890 -p 8890
"""

import json
import os
import re
import time
from datetime import datetime
from mitmproxy import http

# ---- Audit log ----
LOG_DIR = os.path.join(os.path.expanduser("~"), ".claude-shield")
os.makedirs(LOG_DIR, exist_ok=True)

def audit_log(msg: str) -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(LOG_DIR, "sanitize.log"), "a") as f:
        f.write(f"[{ts}] {msg}\n")

# ---- Signal patterns to sanitize ----

SANITIZE_RULES = [
    # === Timezone ===
    (rb'Asia/Shanghai', b'America/Los_Angeles'),
    (rb'Asia/Urumqi', b'America/Los_Angeles'),
    (rb'Asia/Chongqing', b'America/Los_Angeles'),
    (rb'Asia/Harbin', b'America/Los_Angeles'),
    (rb'Asia/Macau', b'America/Los_Angeles'),
    (rb'Asia/Hong_Kong', b'America/Los_Angeles'),
    (rb'Asia/Taipei', b'America/Los_Angeles'),
    (rb'Asia/Beijing', b'America/Los_Angeles'),
    (rb'Asia/Singapore', b'America/Los_Angeles'),
    (rb'Asia/Tokyo', b'America/Los_Angeles'),
    (rb'Asia/Seoul', b'America/Los_Angeles'),
    (rb'%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4', b'Pacific%20Standard%20Time'),  # 中国标准时间 URL-encoded
    (rb'\xe4\xb8\xad\xe5\x9b\xbd\xe6\xa0\x87\xe5\x87\x86\xe6\x97\xb6\xe9\x97\xb4', b'Pacific Standard Time'),  # 中国标准时间 UTF-8

    # === Locale ===
    (rb'zh-CN', b'en-US'),
    (rb'zh-Hans', b'en-US'),
    (rb'zh-Hant', b'en-US'),
    (rb'zh_TW', b'en-US'),
    (rb'zh-HK', b'en-US'),
    (rb'zh-SG', b'en-US'),
    (rb'zh-MO', b'en-US'),
    (rb'"locale":[ \t]*"zh"', b'"locale":"en"'),
    (rb'"language":[ \t]*"zh"', b'"language":"en"'),
    (rb'"language":[ \t]*"Chinese"', b'"language":"English"'),
    (rb'"Chinese (Simplified)"', b'"English (United States)"'),
    (rb'"Chinese (Traditional)"', b'"English (United States)"'),
    (rb'"CHS"', b'"ENU"'),

    # === Code page / encoding ===
    (rb'CodePage":\s*936', b'CodePage":1252'),
    (rb'CodePage":\s*54936', b'CodePage":1252'),
    (rb'CodePage":\s*20936', b'CodePage":1252'),
    (rb'CodePage":\s*950', b'CodePage":1252'),
    (rb'code_page":\s*936', b'code_page":1252'),
    (rb'"codepage":\s*936', b'"codepage":1252'),
    (rb'GB2312', b'Windows-1252'),
    (rb'gb2312', b'windows-1252'),
    (rb'GB18030', b'Windows-1252'),
    (rb'gb18030', b'windows-1252'),
    (rb'GBK', b'Windows-1252'),
    (rb'gbk', b'windows-1252'),
    (rb'BIG5', b'Windows-1252'),
    (rb'big5', b'windows-1252'),

    # === Keyboard layout ===
    (rb'0x0804', b'0x0409'),      # Chinese (PRC) → US
    (rb'0x0404', b'0x0409'),      # Chinese (Taiwan) → US
    (rb'0x0c04', b'0x0409'),      # Chinese (Hong Kong) → US
    (rb'0x1004', b'0x0409'),      # Chinese (Singapore) → US
    (rb'0x0411', b'0x0409'),      # Japanese → US
    (rb'0x0412', b'0x0409'),      # Korean → US
    (rb'"0804"', b'"0409"'),

    # === IME (Input Method Editor) ===
    (rb'Microsoft Pinyin', b'Microsoft English (US)'),
    (rb'Microsoft Wubi', b'Microsoft English (US)'),
    (rb'Sogou Pinyin', b'Microsoft English (US)'),
    (rb'Chinese (Simplified) - Microsoft Pinyin', b''),
    (rb'Chinese (Simplified) - Sogou', b''),

    # === System font detection ===
    (rb'SimSun', b'Times New Roman'),
    (rb'SimHei', b'Arial'),
    (rb'Microsoft YaHei', b'Arial'),
    (rb'FangSong', b'Times New Roman'),
    (rb'KaiTi', b'Arial'),
    (rb'NSimSun', b'Courier New'),
    (rb'DengXian', b'Arial'),

    # === Network detection ===
    (rb'127.0.0.1:7890', b'127.0.0.1:0'),
    (rb'http://127.0.0.1:7890', b''),
    (rb'https://127.0.0.1:7890', b''),
    (rb'HTTP_PROXY=http://127.0.0.1', b'HTTP_PROXY='),
    (rb'HTTPS_PROXY=http://127.0.0.1', b'HTTPS_PROXY='),
    (rb'NO_PROXY=', b'NO_PROXY='),
    (rb'http_proxy=http://127.0.0.1', b'http_proxy='),
    (rb'https_proxy=http://127.0.0.1', b'https_proxy='),

    # === IP geography detection ===
    (rb'"country":[ \t]*"CN"', b'"country":"US"'),
    (rb'"countryCode":[ \t]*"CN"', b'"countryCode":"US"'),
    (rb'"region":[ \t]*"CN"', b'"region":"US"'),
    (rb'geoip_country_code.*CN', b'geoip_country_code: "US"'),

    # === Date format signals ===
    (rb'2026/07/', b'2026-07-'),
    (rb'2026/06/', b'2026-06-'),
    (rb'2026/08/', b'2026-08-'),

    # === Unicode apostrophe trick ===
    (b'\xe2\x80\x98', b"'"),   # LEFT SINGLE QUOTATION MARK
    (b'\xe2\x80\x99', b"'"),   # RIGHT SINGLE QUOTATION MARK
    (b'\xe2\x80\x9c', b'"'),   # LEFT DOUBLE QUOTATION MARK
    (b'\xe2\x80\x9d', b'"'),   # RIGHT DOUBLE QUOTATION MARK

    # === Chinese text in system prompt ===
    (rb'\xe4\xb8\xad\xe5\x9b\xbd', b'United States'),  # 中国 → United States

    # === Claude Code version signature (if it embeds info) ===
    (rb'"claude_code_version":[ \t]*"[^"]*"', b''),
    (rb'"cli_version":[ \t]*"[^"]*"', b''),

    # === Telemetry / metadata stripping ===
    (rb'"user_agent":[ \t]*"[^"]*"', b'"user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"'),
    (rb'"client_timestamp":[ \t]*[0-9]+', b'"client_timestamp":0'),
]


def sanitize_text(text: bytes) -> tuple[bytes, int]:
    """Apply all sanitization rules. Returns (sanitized_text, count_of_replacements)."""
    modified = text
    count = 0
    for pattern, replacement in SANITIZE_RULES:
        if pattern in modified:
            n = modified.count(pattern)
            count += n
            modified = modified.replace(pattern, replacement)
    return modified, count


def sanitize_json_system(data: dict) -> tuple[dict, int]:
    """Recursively sanitize the 'system' field in nested JSON structures."""
    count = 0
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "system" and isinstance(value, str):
                sanitized, c = sanitize_text(value.encode("utf-8"))
                if c > 0:
                    data[key] = sanitized.decode("utf-8")
                    count += c
            elif isinstance(value, (dict, list)):
                _, c = sanitize_json_system(value)
                count += c
    elif isinstance(data, list):
        for item in data:
            _, c = sanitize_json_system(item)
            count += c
    return data, count


def request(flow: http.HTTPFlow) -> None:
    """Intercept requests and sanitize China-detection signals."""
    content_type = flow.request.headers.get("content-type", "")
    if "json" not in content_type:
        return

    try:
        body = flow.request.get_content()
        if not body:
            return

        # 1. Raw byte-level sanitization
        sanitized_body, raw_count = sanitize_text(body)

        # 2. JSON-level sanitization (for system prompt in nested structures)
        try:
            data = json.loads(sanitized_body)
            _, json_count = sanitize_json_system(data)
            sanitized_body = json.dumps(data).encode()
            total_count = raw_count + json_count
        except (json.JSONDecodeError, UnicodeDecodeError):
            total_count = raw_count

        if total_count > 0:
            flow.request.set_content(sanitized_body)
            audit_log(f"SANITIZED {total_count} signals → {flow.request.pretty_url[:80]}")
    except Exception as e:
        audit_log(f"ERROR: {e}")
