TRANS_VENV=$HOME/python-trans
cd $TRANS_VENV
# your Python version here
PYTHON_VERSION=python3.10
$TRANS_VENV/bin/pip install pyinstaller
$TRANS_VENV/bin/pyinstaller --onefile --python-option u  --recursive-copy-metadata "openai-whisper" --add-data "$TRANS_VENV/lib/$PYTHON_VERSION/site-packages/whisper:whisper/" --add-data "$TRANS_VENV/lib/$PYTHON_VERSION/site-packages/transcribe_translate:transcribe_and_translate/" --console $TRANS_VENV/lib/$PYTHON_VERSION/site-packages/transcribe_translate/transcribe_and_translate_cli.py

# optional: --onefile
