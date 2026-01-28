@echo off
setlocal

set DIRECTORY=.venv

if exist "%DIRECTORY%" (
    echo Found a venv
) else (
    echo Can't find a venv. Creating
    python -m venv .venv
    if errorlevel 1 (
        python3 -m venv .venv
    )
)
call .venv\Scripts\activate.bat
pip show arcade >nul 2>&1
if errorlevel 1 (
    pip install arcade[full]
)
echo Venv contains a valid arcade
echo Running a game "Run from antivirus!"
python main.py type=dialog
if errorlevel 1 (
    python3 main.py type=dialog
)
python main.py type=run
if errorlevel 1 (
    python3 main.py type=run
)
deactivate

endlocal
