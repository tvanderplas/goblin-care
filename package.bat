
cd %~dp0
mkdir "temp pyinstaller build"
cd "temp pyinstaller build"
set PATH=%PATH%;C:\Windows\System32\downlevel
pyinstaller "C:\repos\goblin-care\goblin care.py"
del "dist\goblin care\goblin care.exe.manifest"
cd..
xcopy "temp pyinstaller build\dist\goblin care" "Goblin Care" /E /Y /I
xcopy "game art" "Goblin Care\game art" /Y /I
xcopy "fonts" "Goblin Care\fonts" /Y /I
rd /s /q "temp pyinstaller build"
REM heat.exe dir "Goblin Care" -gg -sfrag -out windows.wxs
REM python xml editing script here
candle.exe "goblin care.wxs"
light.exe "goblin care.wixobj"
rd /s /q "Goblin Care"
del "goblin care.wixobj"
del "goblin care.wixpdb"
