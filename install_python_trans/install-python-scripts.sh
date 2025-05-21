#!/bin/bash
# deep-translator
# see https://github.com/nidhaloff/deep-translator
# Configuration
WORKDIR=~/python-trans
# Intel Linux NPU Driver installation
# -> https://github.com/intel/linux-npu-driver/releases
USE_NPU="no"
# Configuration end

install_packages(){
sudo apt update
sudo apt -y install python3-pip python3-venv ffmpeg
}
install_transcribe_translate(){
#create venv
python3 -m venv $WORKDIR
if [ "$USE_NPU" == "yes" ]
then
$WORKDIR/bin/pip3 install intel_npu_acceleration_library
fi
$WORKDIR/bin/pip3 install transcribe_translate-0.2.0-py3-none-any.whl

#install deep-translator in venv
#$WORKDIR/bin/pip3 install wheel
#$WORKDIR/bin/pip3 install deep-translator deep-translator[docx] deep-translator[pdf]  deep-translator[ai] semantic-text-splitter openai-whisper
#if [ ! -z $USE_NPU ] then
#$WORKDIR/bin/pip3 install intel_npu_acceleration_library
#fi
#cp scripts/translate_audacity_files.py $WORKDIR/bin
#sed -i "1 i\#\!$WORKDIR/bin/python3" $WORKDIR/bin/translate_audacity_files.py
#chmod a+x $WORKDIR/bin/translate_audacity_files.py
#cp scripts/transcribe_translate.py $WORKDIR/bin
#sed -i "1 i\#\!$WORKDIR/bin/python3" $WORKDIR/bin/transcribe_translate.py
#chmod a+x $WORKDIR/bin/transcribe_translate.py
#if [ ! -z $USE_NPU ] then
#  cp scripts/transcribe_translate_npu.py $WORKDIR/bin
#  sed -i "1 i\#\!$WORKDIR/bin/python3" $WORKDIR/bin/transcribe_translate_npu.py
#  chmod a+x $WORKDIR/bin/transcribe_translate_npu.py
#fi  
#cp scripts/transcribe_translate_cli.py $WORKDIR/bin
#sed -i "1 i\#\!$WORKDIR/bin/python3" $WORKDIR/bin/transcribe_translate_cli.py
#chmod a+x $WORKDIR/bin/transcribe_translate_cli.py
# cp scripts/Languages.txt $WORKDIR/bin
cp scripts/src/transcribe_translate/transcribe_translate_config.ini $WORKDIR/bin
cp scripts/src/transcribe_translate/translate_audacity_config.ini $WORKDIR/bin
cp -r Subtitle-Demo $WORKDIR/bin/

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
#install_packages
install_transcribe_translate
#install_deep-translator
#install_argos_tranlator
echo "Fertig"
