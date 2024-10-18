#!/bin/bash
# deep-translator
# see https://github.com/nidhaloff/deep-translator
WORKDIR=~/python-trans
install_packages(){
sudo apt update
sudo apt -y install python3-pip python3-venv ffmpeg
}
install_deep-translator(){
#create venv
python3 -m venv $WORKDIR
#install deep-translator in venv
$WORKDIR/bin/pip3 install wheel
$WORKDIR/bin/pip3 install deep-translator deep-translator[docx] deep-translator[pdf]  deep-translator[ai] semantic-text-splitter openai-whisper
cp scripts/translate_audacity_files.py $WORKDIR/bin
sed -i "1 i\#\!$WORKDIR/bin/python3" $WORKDIR/bin/translate_audacity_files.py
chmod a+x $WORKDIR/bin/translate_audacity_files.py
cp scripts/transcribe_translate.py $WORKDIR/bin
sed -i "1 i\#\!$WORKDIR/bin/python3" $WORKDIR/bin/transcribe_translate.py
chmod a+x $WORKDIR/bin/transcribe_translate.py
}
install_argos_tranlator(){
# install Argos Translate (https://github.com/argosopentech/argos-translate)
$WORKDIR/bin/pip3 install argostranslate argostranslategui
cp scripts/translate_argos.py $WORKDIR/bin
cp scripts/argos_list_lang.py $WORKDIR/bin
sed -i "1 i\#\!$WORKDIR/bin/python3" $WORKDIR/bin/translate_argos.py
chmod a+x $WORKDIR/bin/translate_argos.py
sed -i "1 i\#\!$WORKDIR/bin/python3" $WORKDIR/bin/argos_list_lang.py
chmod a+x $WORKDIR/bin/argos_list_lang.py
}
install_packages
install_deep-translator
install_argos_tranlator


