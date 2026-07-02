"""
Claude Shield — MITM proxy addon for mitmproxy.

Sanitizes Anthropic API requests to remove China-detection signals
from the system prompt before they reach Anthropic's servers.

Usage:
    mitmdump -s claude_shield.py --mode upstream:http://127.0.0.1:7890 -p 8890

Then set HTTPS_PROXY=http://127.0.0.1:8890 for Claude Code.
"""

import json
import re
from mitmproxy import http

# ---- Signal patterns to sanitize ----
# These are the patterns identified from community research
# that Claude Code allegedly embeds into the system prompt.

SANITIZE_RULES = [
    # Timezone: Asia/Shanghai, Asia/Urumqi → America/Los_Angeles
    (rb'Asia/Shanghai', b'America/Los_Angeles'),
    (rb'Asia/Urumqi', b'America/Los_Angeles'),
    (rb'Asia/Chongqing', b'America/Los_Angeles'),
    (rb'Asia/Harbin', b'America/Los_Angeles'),
    (rb'Asia/Macau', b'America/Los_Angeles'),
    (rb'Asia/Hong_Kong', b'America/Los_Angeles'),
    (rb'Asia/Taipei', b'America/Los_Angeles'),

    # Locale: zh-CN, zh-Hans, zh-Hant → en-US
    (rb'zh-CN', b'en-US'),
    (rb'zh-Hans', b'en-US'),
    (rb'zh-Hant', b'en-US'),
    (rb'zh_TW', b'en-US'),
    (rb'zh-HK', b'en-US'),
    (rb'zh-SG', b'en-US'),

    # Code page / encoding: bare 936 and with field names
    (rb'"codepage": 936', b'"codepage": 1252'),
    (rb'"CodePage": 936', b'"CodePage": 1252'),
    (rb'codepage 936', b'codepage 1252'),
    (rb'CodePage 936', b'CodePage 1252'),
    (rb'GB2312', b'Windows-1252'),
    (rb'gb2312', b'windows-1252'),
    (rb'GB18030', b'Windows-1252'),

    # System language: Chinese → English
    (rb'Chinese (Simplified)', b'English (United States)'),
    (rb'Chinese (Traditional)', b'English (United States)'),
    (rb'CHS', b'ENU'),

    # Keyboard layout: 0804 (Chinese) → 0409 (US)
    (rb'0x0804', b'0x0409'),
    (rb'"0804"', b'"0409"'),

    # Proxy detection patterns
    (rb'127.0.0.1:7890', b'127.0.0.1:0'),           # FlClash port
    (rb'http://127.0.0.1:7890', b''),                 # proxy URL in system prompt
    (rb'HTTP_PROXY=http://127.0.0.1', b'HTTP_PROXY='),
    (rb'HTTPS_PROXY=http://127.0.0.1', b'HTTPS_PROXY='),

    # Date format: if Claude Code encodes YYYY/MM/DD as China signal
    # replace with YYYY-MM-DD
    (rb'2026/06/', b'2026-06-'),
    (rb'2026/07/', b'2026-07-'),
    (rb'2026/05/', b'2026-05-'),

    # Unicode apostrophe detection (alleged encoding trick)
    # \u2018 \u2019 are curly quotes, \u0027 is straight
    # If the system prompt uses these as signals, we normalize them
    (b'\xe2\x80\x98', b"'"),   # LEFT SINGLE QUOTATION MARK → straight
    (b'\xe2\x80\x99', b"'"),   # RIGHT SINGLE QUOTATION MARK → straight
    (b'\xe2\x80\x9c', b'"'),   # LEFT DOUBLE QUOTATION MARK → straight
    (b'\xe2\x80\x9d', b'"'),   # RIGHT DOUBLE QUOTATION MARK → straight
]

# ---- Hosts to intercept ----
TARGET_HOSTS = [
    "api.anthropic.com",
    "claude.ai",
]


def request(flow: http.HTTPFlow) -> None:
    """Intercept requests and sanitize China-detection signals from the body."""
    # Sanitize ALL requests that go through this proxy.
    # The proxy is only used for Claude Code, so no need for host filtering.

    content_type = flow.request.headers.get("content-type", "")
    if "json" not in content_type:
        return

    # Parse request body
    try:
        body = flow.request.get_content()
        if not body:
            return

        # Apply sanitization rules
        modified = body
        sanitized_count = 0
        for pattern, replacement in SANITIZE_RULES:
            if pattern in modified:
                sanitized_count += modified.count(pattern)
                modified = modified.replace(pattern, replacement)

        if sanitized_count > 0:
            flow.request.set_content(modified)
            # Log (only in verbose)
            if flow.request.path and "messages" in (flow.request.path or ""):
                print(f"🛡️  [Claude Shield] Sanitized {sanitized_count} signals in request to {flow.request.pretty_url}")

        # Also check the actual JSON content for system messages
        try:
            data = json.loads(modified)
            if "system" in data:
                original_system = str(data["system"])
                sanitized_system = original_system
                for pattern_bytes, replacement_bytes in SANITIZE_RULES:
                    pattern_str = pattern_bytes.decode("utf-8", errors="replace")
                    replacement_str = replacement_bytes.decode("utf-8", errors="replace")
                    if pattern_str in sanitized_system:
                        sanitized_system = sanitized_system.replace(pattern_str, replacement_str)
                if sanitized_system != original_system:
                    data["system"] = sanitized_system
                    flow.request.set_content(json.dumps(data).encode())
                    print(f"🛡️  [Claude Shield] Sanitized system prompt for {flow.request.pretty_url}")
        except (json.JSONDecodeError, UnicodeDecodeError, KeyError):
            pass

    except Exception as e:
        print(f"⚠️  [Claude Shield] Error processing request: {e}")
