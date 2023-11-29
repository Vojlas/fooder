@ECHO OFF
call ".\env\Scripts\activate.bat"
pyinstaller -F --onefile ./main.py
pause