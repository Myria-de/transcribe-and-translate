cd %USERPROFILE%\python-trans\Scripts
SET WHISPER=%USERPROFILE%/python-trans/Lib/site-packages/whisper
SET TRANS=%USERPROFILE%/python-trans/Lib/site-packages/transcribe_translate
SET ARGOS=%USERPROFILE%/python-trans/Lib/site-packages/argostranslate
SET MYSCRIPT=%USERPROFILE%/python-trans/Lib/site-packages/transcribe_translate/transcribe_and_translate_cli.py
%USERPROFILE%\python-trans\Scripts\pip install pyinstaller

%USERPROFILE%\python-trans\Scripts\pyinstaller --python-option u --recursive-copy-metadata "openai-whisper" --add-data %WHISPER%:whisper --add-data %TRANS%:transcribe_translate --add-data %ARGOS%:argostranslate --console %MYSCRIPT%
pause

REM --onefile if you prefer one big (and slow) file
