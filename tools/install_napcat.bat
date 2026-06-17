@echo off
chcp 65001 >nul
title 下载 NapCat Framework...

echo ===========================================
echo   下载 NapCat Framework (含 QCE)
echo ===========================================
echo.
echo NapCat Framework = NapCat + QCE 一体化包
echo 既可以登录 QQ 小号，也可以导出聊天记录
echo.
echo 正在用浏览器打开下载页...
echo.

echo [下载1] NapCat Shell (QQ注入框架)
echo https://github.com/NapNeko/NapCatQQ/releases
echo 下载 NapCat.Shell.Windows.OneKey.zip
echo.
echo [下载2] 解压后运行 NapCatInstaller.exe
echo 会自动下载 QQ + NapCat + QCE
echo.
echo 安装完成后运行: napiLoader.bat
echo 打开浏览器: http://localhost:40653/qce-v4-tool

start https://github.com/NapNeko/NapCatQQ/releases

pause
