@ECHO OFF
call ".\env\Scripts\activate.bat"
pip freeze > requirements.txt
ECHO "requirements.txt created"
exit