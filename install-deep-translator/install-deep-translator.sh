#!/bin/bash
# deep-translator
# see https://github.com/nidhaloff/deep-translator
WORKDIR=~/deep-translator
sudo apt update
sudo apt -y install python3-pip python3-venv ffmpeg
#create venv
python3 -m venv $WORKDIR
# install deep-translator in venv
$WORKDIR/bin/pip3 install deep-translator deep-translator[docx] deep-translator[pdf]  deep-translator[ai] semantic-text-splitter openai-whisper
cp translate_audacity_files.py ~/deep-translator/bin
sed -i "1 i\#\!$HOME/deep-translator/bin/python3" ~/deep-translator/bin/translate_audacity_files.py
chmod a+x ~/deep-translator/bin/translate_audacity_files.py
cp transcribe_translate.py ~/deep-translator/bin
sed -i "1 i\#\!$HOME/deep-translator/bin/python3" ~/deep-translator/bin/transcribe_translate.py
chmod a+x ~/deep-translator/bin/transcribe_translate.py

