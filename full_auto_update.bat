@echo off
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "%~dp0full_auto_update.ps1"
