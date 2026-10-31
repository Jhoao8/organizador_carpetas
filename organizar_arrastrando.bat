@echo off
setlocal
set "PYTHONPATH=%~dp0;%PYTHONPATH%"
set "PY=%~dp0.venv\Scripts\python.exe"

if "%~1"=="" (
    echo Arrastra una carpeta sobre este archivo para organizarla.
    pause
    exit /b 1
)

echo Carpeta: %~1
echo.
"%PY%" -m organizador.cli "%~1" --simular
if errorlevel 1 goto fin

echo.
set "CONFIRMA="
set /p CONFIRMA=Ejecutar de verdad? (S/N): 
if /i "%CONFIRMA%"=="S" "%PY%" -m organizador.cli "%~1"

:fin
echo.
pause