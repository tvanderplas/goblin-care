cd %~dp0
mkdir "temp pyinstaller build"
cd "temp pyinstaller build"
set PATH=%PATH%;C:\Windows\System32\downlevel
pyinstaller "C:\repos\goblin-care\goblin care.py"
cd..
xcopy "temp pyinstaller build\dist\goblin care" "Goblin Care" /E /Y /I
xcopy "game art" "Goblin Care\game art" /Y /I
xcopy "fonts" "Goblin Care\fonts" /Y /I
rd /s /q "temp pyinstaller build"
7z a -o. "Goblin Care.zip" -r "goblin care"
rd /s /q "Goblin Care"
