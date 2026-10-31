@echo off
setlocal
rem Lanzador: ejecuta el organizador desde cualquier carpeta.
rem Uso: organizar RUTA [--reglas ARCHIVO.json] [--simular]
set "PYTHONPATH=%~dp0;%PYTHONPATH%"
"%~dp0.venv\Scripts\python.exe" -m organizador.cli %*