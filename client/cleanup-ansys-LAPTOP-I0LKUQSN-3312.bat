@echo off
set LOCALHOST=%COMPUTERNAME%
if /i "%LOCALHOST%"=="LAPTOP-I0LKUQSN" (taskkill /f /pid 9360)
if /i "%LOCALHOST%"=="LAPTOP-I0LKUQSN" (taskkill /f /pid 3312)

del /F cleanup-ansys-LAPTOP-I0LKUQSN-3312.bat
