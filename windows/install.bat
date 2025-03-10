@echo off
cls
echo ##############################################################
echo #------------------------------------------------------------#
echo                      autologin-iitk                           
echo #------------------------------------------------------------#
echo ################## Author: cipherswami #######################
echo ##############################################################
echo.
setlocal

set "SERVICE_NAME=autologin-iitk"
set "SCRIPT_FILE=autologin-iitk.py"
set "SCRIPT_FILE_LOCATION=..\src"
set "DESCRIPTION=Auto login script for IITK's firewall authentication page."
set "INSTALL_DIR=%ProgramFiles%\%SERVICE_NAME%"
set "NSSM_DIR=%ProgramData%\nssm"
set "APPLICATION_TO_RUN=python"

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] This script must be run as administrator.
    echo.
    pause
    exit /b 1
)

REM Check for Python executables (system-wide)
for /f "delims=" %%i in ('where python') do (
    echo %%i | findstr /i "Microsoft\\WindowsApps" >nul
    if errorlevel 1 (
        set "APPLICATION_TO_RUN=%%i"
        goto :PythonFound
    )
)

echo Error: Valid Python executable not found (Don't use Microsoft Store versions).
echo.
pause
exit /b 1

:PythonFound

REM Creating NSSM directory in system-wide location
echo [+] Installing NSSM ...
if not exist "%NSSM_DIR%" (
    mkdir "%NSSM_DIR%" || (
        echo Error: Failed to create NSSM directory.
        echo.
        pause
        exit /b 1
    )
)

REM Copy the nssm.exe to NSSM directory
if not exist "%NSSM_DIR%\nssm.exe" (
    copy /Y "%~dp0\nssm.exe" "%NSSM_DIR%" || (
        echo Error: Failed to copy nssm.exe
        echo.
        pause
        exit /b 1
    )
)

echo.
echo [+] NSSM installed successfully: %NSSM_DIR%
echo.

REM Ensure installation directory exists in system-wide location
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%" || (
        echo Error: Failed to create installation directory.
        echo.
        pause
        exit /b 1
    )
)

echo [+] Installation directory created successfully: %INSTALL_DIR%
echo.

REM Copy the Python script to the installation directory
echo [+] Copying %SCRIPT_FILE% to installation directory...
copy /Y "%~dp0%SCRIPT_FILE_LOCATION%\%SCRIPT_FILE%" "%INSTALL_DIR%" || (
    echo Error: Failed to copy Python script to installation directory.
    echo.
    pause
    exit /b 1
)

echo.

"%NSSM_DIR%\nssm.exe" install "%SERVICE_NAME%" "%APPLICATION_TO_RUN%" "\"%INSTALL_DIR%\%SCRIPT_FILE%\"" || (
    echo Error: Failed to install the service.
    echo.
    pause
    exit /b 1
)

REM Set service properties
"%NSSM_DIR%\nssm.exe" set "%SERVICE_NAME%" Description "%DESCRIPTION%"
"%NSSM_DIR%\nssm.exe" set "%SERVICE_NAME%" AppDirectory "%INSTALL_DIR%"
"%NSSM_DIR%\nssm.exe" set "%SERVICE_NAME%" AppStdout "%INSTALL_DIR%\autologin-iitk.log"
"%NSSM_DIR%\nssm.exe" set "%SERVICE_NAME%" AppStderr "%INSTALL_DIR%\autologin-iitk.log"
"%NSSM_DIR%\nssm.exe" set "%SERVICE_NAME%" AppStdoutCreationDisposition 2
"%NSSM_DIR%\nssm.exe" set "%SERVICE_NAME%" AppStderrCreationDisposition 2
"%NSSM_DIR%\nssm.exe" set "%SERVICE_NAME%" AppExit 1 Exit
"%NSSM_DIR%\nssm.exe" set "%SERVICE_NAME%" Start SERVICE_AUTO_START

REM Start the service
"%NSSM_DIR%\nssm.exe" start "%SERVICE_NAME%" || (
    echo Error: Failed to start the service.
    echo.
    pause
    exit /b 1
)

echo.
echo [#] Installation complete
echo.
pause
