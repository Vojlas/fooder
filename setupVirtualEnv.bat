:: For windows only
@ECHO OFF

ECHO The batch file was run from: %CMDCMDLINE%

:: Check if the "./env" directory already exists
IF EXIST "./env" (
    ECHO "env already exists."
) ELSE (
    ECHO "env does not exist - creating new"
    python -m venv env
)

:: Check if the batch file is run from cmd.exe
ECHO %CMDCMDLINE% | FINDSTR /C:"cmd.exe" >NUL
IF %ERRORLEVEL% EQU 0 (
    ECHO "Running from Windows Command Prompt (cmd.exe)."
    
    :: Activate the virtual environment if running from cmd.exe
    call ".\env\Scripts\activate.bat"
    py -m pip install -r requirements.txt
) ELSE (
    ECHO "Not running from Windows Command Prompt. Skipping activation."
)


