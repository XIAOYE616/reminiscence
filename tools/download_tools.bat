@echo off
chcp 65001 >nul
title 下载 QCE + NapCat 一体化包...

echo ============================
echo   下载 QCE 聊天导出工具
echo ============================
echo.
echo 正在打开下载页面...
echo.

echo [1] NapCat Shell (QQ 注入框架)
echo     下载: https://github.com/NapNeko/NapCatQQ/releases
echo     找到 NapCat.Shell.Windows.OneKey.zip
echo.
echo [2] QCE (QQ Chat Exporter)
echo     下载: https://github.com/shuakami/qq-chat-exporter/releases
echo     找到最新的 qq-chat-exporter 版本
echo.
echo [3] 或者用一体化版本 (NapCat Framework + QCE)
echo     已在桌面 huiyi-master\tools\NapCat-Framework

start https://github.com/NapNeko/NapCatQQ/releases
start https://github.com/shuakami/qq-chat-exporter/releases

pause
