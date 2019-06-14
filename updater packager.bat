
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
REM heat.exe dir "Goblin Care" -gg -sfrag -out windows.wxs
REM python xml editing script here
REM candle.exe "windows.wxs"
REM light.exe "windows.wixobj"
REM rd /s /q "Goblin Care"
REM del "goblin care.wixobj"
REM del "goblin care.wixpdb"
