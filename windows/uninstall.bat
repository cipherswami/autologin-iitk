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
set "INSTALL_DIR=C:\Users\%USERNAME%\AppData\Local\%SERVICE_NAME%"
set "NSSM_DIR=C:\Users\%USERNAME%\AppData\Local\nssm"

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] This script must be run as administrator.
    echo.
    pause
    exit /b 1
)

REM Stop and remove the service using NSSM
"%NSSM_DIR%\nssm.exe" stop "%SERVICE_NAME%" > nul 2>&1

REM Removing Temp file
del /f /q "C:\Windows\Temp\iitk_logout_url.txt"

"%NSSM_DIR%\nssm.exe" remove "%SERVICE_NAME%" confirm > nul 2>&1 || (
    echo Error: Failed to remove the service.
    echo.
    pause
    exit /b 1
)

echo.
echo [+] Service removed successfully.
echo.

REM Delete installation directory
if exist "%INSTALL_DIR%" (
    rmdir /s /q "%INSTALL_DIR%" || (
        echo Error: Failed to delete installation directory.
        echo.
        pause
        exit /b 1
    )
    echo [+] Installation directory deleted successfully.
    echo.
)

REM Delete NSSM
if exist "%NSSM_DIR%" (
    rmdir /s /q "%NSSM_DIR%" || (
        echo Error: Failed to delete NSSM directory.
        echo.
        pause
        exit /b 1
    )
    echo [+] NSSM directory deleted successfully.
)

echo.
echo [#] Uninstallation complete
echo.
pause
