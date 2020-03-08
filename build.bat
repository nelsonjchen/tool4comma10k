VERIFY OTHER 2>nul
SETLOCAL ENABLEEXTENSIONS

del /s /f /q dist
pyinstaller -y server.spec
if %errorlevel% neq 0 exit /b %errorlevel%
