@echo off
REM === Claude Shield Proxy ===
REM MITM proxy that sanitizes China-detection signals from Claude Code API requests.
REM
REM Requires: mitmproxy (pip install mitmproxy)
REM CA cert: auto-installed on first run, trust at ~/.mitmproxy/mitmproxy-ca-cert.pem
REM
REM Usage: start-claude-shield.bat
REM Then: set HTTPS_PROXY=http://127.0.0.1:8890 before running claude

set PROXY_PORT=8890
set UPSTREAM_PROXY=http://127.0.0.1:7890
set SCRIPT_DIR=%~dp0
set ADDON=%SCRIPT_DIR%claude_shield.py

echo ========================================
echo   Claude Shield Proxy
echo   Listening: 127.0.0.1:%PROXY_PORT%
echo   Upstream:  %UPSTREAM_PROXY%
echo ========================================
echo.
echo Set your environment:
echo   set HTTPS_PROXY=http://127.0.0.1:%PROXY_PORT%
echo   set HTTP_PROXY=http://127.0.0.1:%PROXY_PORT%
echo.
echo Then run Claude Code normally.
echo Press Ctrl+C to stop.
echo.

mitmdump -s "%ADDON%" --mode upstream:%UPSTREAM_PROXY% -p %PROXY_PORT% --set block_global=false
