@echo off
cd /d "%~dp0"

cd

:: check if python is installed
>nul 2>nul assoc .py

if errorlevel 1 (
    :: python is not installed
    echo Python not installed, downloading installer...
    powershell -c "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe' -OutFile '%USERPROFILE%\AppData\Local\Temp\python-3.11.1.exe'"
    echo Launching installer, please make sure to follow the correct setup instructions Adding python to environment variables!
    echo:

    "%USERPROFILE%\AppData\Local\Temp\python-3.11.1.exe"
    pause
    echo Please press any button once you have completed the python setup, so we can continue installing the depedencies.

) else (
    echo Python is already installed. Please make sure its of version 3.10 or higher, using an older version will NOT work!
)



:: get depedencies, not worth checking worst case they are already installed.
echo Installing dependencies...
py -m pip install -r requirements.txt

echo Finished installing dependencies.

echo Setup finished.
pause