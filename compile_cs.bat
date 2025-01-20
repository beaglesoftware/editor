@echo off
echo Note: You need to install Visual Studio or Visual Studio Build Tools with .NET desktop development workflow
set /p "VS_VERSION_BEAGLEEDITOR=Enter Visual Studio Edition:"
set /p "BEAGLEEDITOR_ARCH=Enter your architecture (Just 32 or 64):"
call "C:\Program Files\Microsoft Visual Studio\%VS_VERSION_BEAGLEEDITOR%\Enterprise\VC\Auxiliary\Build\vcvarsall.bat" x%BEAGLEEDITOR_ARCH%
set BEAGLEEDITOR_CS_FILENAME=%1
csc %BEAGLEEDITOR_CS_FILENAME%
pause