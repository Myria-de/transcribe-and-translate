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

cp scripts/src/transcribe_translate/transcribe_translate_config.ini $WORKDIR/bin
cp scripts/src/transcribe_translate/translate_audacity_config.ini $WORKDIR/bin
cp -r Subtitle-Demo $WORKDIR/bin/
cp -r GUI $WORKDIR/bin/
}
install_packages
install_transcribe_translate
echo "Fertig"
