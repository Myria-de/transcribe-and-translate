@echo off&setlocal
REM  deep-translator
REM  see https://github.com/nidhaloff/deep-translator
REM Python for Windows -> https://www.python.org/downloads/windows

set PATH="%USERPROFILE%\AppData\Local\Programs\Python\Python310";%PATH%
set PYTHON="%USERPROFILE%\AppData\Local\Programs\Python\Python310\python.exe"
set WORKDIR=%USERPROFILE%\python-trans
set CURDIR=%~dp0
cd /D %CURDIR%
goto :start

:install_transcribe_translate
REM Nvidia Cuda -> https://pytorch.org/get-started/locally/
echo Creating Python venv
%PYTHON% -m venv %WORKDIR%
set PYTHON_VENV=%WORKDIR%\Scripts\Python.exe
echo Updating Pip
%PYTHON_VENV% -m pip install --upgrade pip
REM With Cuda (Nvidia GPU)
echo Installing torch...
%WORKDIR%\Scripts\pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
REM CPU only
REM %WORKDIR%\Scripts\pip3 install torch torchvision torchaudio
echo Installing transcribe_translate...
set PIP_USE_PEP517=1
%WORKDIR%\Scripts\pip3 install transcribe_translate-0.2.0-py3-none-any.whl
echo Copy additional files...
copy scripts\src\transcribe_translate\transcribe_translate_config.ini %WORKDIR%\Scripts
copy scripts\src\transcribe_translate\translate_audacity_config.ini %WORKDIR%\Scripts
xcopy  /e/i/s/c Subtitle-Demo %WORKDIR%\Scripts\Subtitle-Demo
xcopy  /e/i/s/c GUI %WORKDIR%\Scripts\GUI
REM copy ffmpeg needed by Whisper
REM Get newer ffmpeg from https://github.com/BtbN/FFmpeg-Builds/releases
copy ffmpeg\ffmpeg.exe %WORKDIR%\Scripts\ffmpeg.exe
copy ffmpeg\ffmpeg.exe %WORKDIR%\Scripts\GUI\Tools\windows\ffmpeg.exe
goto :eof
REM ##########################
:start
goto :install_transcribe_translate
:eof
pause
