@echo off&setlocal
for %%I in ("%~dp0.") do for %%J in ("%%~dpI.") do set ParentFolder=%%~dpnxJ
REM Set FFMPEG path (%USERPROFILE%\python-trans\Scripts)
set PATH=%ParentFolder%;%PATH%
set CURDIR=%~dp0
set TRANS="%USERPROFILE%\python-trans\Scripts\transcribe_translate_cli.exe"
%TRANS% "%CURDIR%\ToTranscribe\Sintel.2010.720p_part.mp4" -o "%CURDIR%\Transcribed" --source_lang en --target_lang de --translator "Argos" -f srt
REM  --translator "Argos"
REM --translator "GoogleTranslator"
REM --translate_only 

pause
