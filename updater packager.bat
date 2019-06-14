
cd %~dp0
mkdir "temp pyinstaller build"
mkdir "Goblin Care"
cd "temp pyinstaller build"
set PATH=%PATH%;C:\Windows\System32\downlevel
pyinstaller "C:\repos\goblin-care\updater.py"
del "dist\updater\updater.exe.manifest"
cd..
xcopy "temp pyinstaller build\dist\updater" "Goblin Care" /E /Y /I
rd /s /q "temp pyinstaller build"
REM candle.exe "goblin care.wxs"
REM light.exe "goblin care.wixobj"
REM rd /s /q "Goblin Care"
REM del "goblin care.wixobj"
REM del "goblin care.wixpdb"
