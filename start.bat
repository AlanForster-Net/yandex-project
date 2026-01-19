@echo off
echo Running a game "Run from antivirus!"

powershell -ExecutionPolicy Bypass -Command "python3 main.py type='dialog'; if ($LASTEXITCODE -ne 0) {python main.py type='dialog'}"

powershell -ExecutionPolicy Bypass -Command "python3 main.py type='run'; if ($LASTEXITCODE -ne 0) {python main.py type='run'}"
