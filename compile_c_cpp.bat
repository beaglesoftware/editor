@echo off
echo Note: BeagleEditor's One-Click Compile needs MSVC to work! Make sure you installed Visual Studio or Visual Studio Build Tools with Desktop development with C++ workflow and MSVC component to compile
set /p "VS_VERSION_BEAGLEEDITOR=Enter Visual Studio Edition:"
set /p "BEAGLEEDITOR_ARCH=Enter your architecture (Just 32 or 64):"
call "C:\Program Files\Microsoft Visual Studio\%VS_VERSION_BEAGLEEDITOR%\Enterprise\VC\Auxiliary\Build\vcvarsall.bat" x%BEAGLEEDITOR_ARCH%
set BEAGLEEDITOR_C_CPP_FILENAME=%1
set BEAGLEEDITOR_OUTDIR=%2
cl /Fo"%2" /Fe"%2" %BEAGLEEDITOR_C_CPP_FILENAME%
pause