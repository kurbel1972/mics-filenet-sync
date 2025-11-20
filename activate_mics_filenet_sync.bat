@echo off
REM Change console code page to UTF-8
chcp 65001 > nul

REM Generate a unique execution ID using date and time
set exec_id=%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set exec_id=%exec_id: =0%

REM Print log header
echo 🔍 5_MICS_FILENET_SYNC - Running Python script on %date% %time% [ID:%exec_id%]

REM Get today's date in YYYY-MM-DD format
for /f %%i in ('powershell -Command "(Get-Date).ToString('yyyy-MM-dd')"') do set today_date=%%i

REM Navigate to the project folder
cd /d C:\Pessoal\Trabalho\GIT\mics-filenet-sync

REM Create a logs folder if it doesn't exist
if not exist logs (
    mkdir logs
)

REM Define the log file name
set log_file=logs\run_%today_date%.log

REM Log start of execution with ID
echo 🔍 [START] %date% %time% [ID:%exec_id%] >> %log_file%

REM Run the Python script with today's date as an argument using the venv Python
echo 🔍 Executing script with Python from .venv... %date% %time% [ID:%exec_id%] >> %log_file%
.venv\Scripts\python.exe main.py %today_date% >> %log_file% 2>&1

REM Log end of execution with ID
echo 🔧 [END] %date% %time% [ID:%exec_id%] >> %log_file%