#!/bin/bash
# Audacity OpenVINO module build for Linux (Ubuntu 22.04/24.04)

# Ubuntu vesion 22 (jammy) or 24 (noble)
VERSION=24
AUDACITY_VERSION=3.6.4
# check also openVINO version in line 101
# Create workdir if not exist
WORKDIR=$HOME/audacity
if [ ! -e $WORKDIR ]
then 
mkdir -p $WORKDIR
fi

#**************************************
#* Build OpenVINO module and Audacity *
#**************************************
build() {

#dependencies
sudo apt update
sudo apt -y install build-essential git ocl-icd-opencl-dev cmake python3-pip libgtk2.0-dev libasound2-dev libjack-jackd2-dev uuid-dev python3-venv git-lfs

#OpenVINO
cd $WORKDIR
wget https://storage.openvinotoolkit.org/repositories/openvino/packages/2024.3/linux/l_openvino_toolkit_ubuntu${VERSION}_2024.3.0.16041.1e3b88e4e3f_x86_64.tgz
tar xvf l_openvino_toolkit_ubuntu${VERSION}_2024.3.0.16041.1e3b88e4e3f_x86_64.tgz
cd l_openvino_toolkit_ubuntu${VERSION}_2024.3.0.16041.1e3b88e4e3f_x86_64/install_dependencies/
sudo -E ./install_openvino_dependencies.sh
cd ..

#OpenVINO Tokenizers Extension 
cd $WORKDIR
wget https://storage.openvinotoolkit.org/repositories/openvino_tokenizers/packages/2024.3.0.0/openvino_tokenizers_ubuntu${VERSION}_2024.3.0.0_x86_64.tar.gz
tar xzvf openvino_tokenizers_ubuntu${VERSION}_2024.3.0.0_x86_64.tar.gz
cp -r runtime/lib/intel64/ l_openvino_toolkit_ubuntu${VERSION}_2024.3.0.16041.1e3b88e4e3f_x86_64/runtime/lib/

# Libtorch (C++ distribution of pytorch)
wget https://download.pytorch.org/libtorch/cpu/libtorch-cxx11-abi-shared-with-deps-2.4.1%2Bcpu.zip
unzip libtorch-cxx11-abi-shared-with-deps-2.4.1+cpu.zip
source $WORKDIR/l_openvino_toolkit_ubuntu${VERSION}_2024.3.0.16041.1e3b88e4e3f_x86_64/setupvars.sh
export LIBTORCH_ROOTDIR=$WORKDIR/libtorch

# Whisper.cpp
cd $WORKDIR
# Clone it & check out specific tag
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
git checkout v1.5.4
cd ..

# Create build folder
mkdir whisper-build
cd whisper-build

# Run CMake, specifying that you want to enable OpenVINO support.
cmake ../whisper.cpp/ -DWHISPER_OPENVINO=ON

# Build it:
make -j`nproc`

# Install built whisper collateral into a local 'installed' directory:
cmake --install . --config Release --prefix ./installed

export WHISPERCPP_ROOTDIR=$WORKDIR/whisper-build/installed
export LD_LIBRARY_PATH=${WHISPERCPP_ROOTDIR}/lib:$LD_LIBRARY_PATH

# create Python venv
cd $WORKDIR
python3 -m venv $WORKDIR/pytools
source pytools/bin/activate
pip3 install conan
deactivate

export PATH=$WORKDIR/pytools/bin:$PATH

cd $WORKDIR

# clone Audacity
git clone https://github.com/audacity/audacity.git

# It is recommended to check out specific tag / branch here, such as release-3.6.2
cd audacity
git checkout release-$AUDACITY_VERSION
cd ..

# Create build directory
mkdir audacity-build
cd audacity-build

# Run cmake (grab a coffee & a snack... this takes a while)
cmake -G "Unix Makefiles" ../audacity -DCMAKE_BUILD_TYPE=Release

# build it 
make -j`nproc`


# Build OpenVINO plugin
cd $WORKDIR
git clone https://github.com/intel/openvino-plugins-ai-audacity.git
git checkout v3.6.4-R3.4
cp -r openvino-plugins-ai-audacity/mod-openvino audacity/modules
echo "add_subdirectory(mod-openvino)" >> audacity/modules/CMakeLists.txt
source $WORKDIR/l_openvino_toolkit_ubuntu${VERSION}_2024.3.0.16041.1e3b88e4e3f_x86_64/setupvars.sh
# cd back to the same Audacity folder you used to build Audacity before
cd $WORKDIR/audacity-build

# and re-run cmake step (it will go faster this time)
cmake -G "Unix Makefiles" ../audacity -DCMAKE_BUILD_TYPE=Release

# and re-run make command
make -j`nproc`
}

models_install() {
#********************************
#* OpenVINO Models Installation *
#********************************
# Create an empty 'openvino-models' directory to start with
cd $WORKDIR
mkdir openvino-models

#************
#* MusicGen *
#************
mkdir openvino-models/musicgen

# clone the HF repo
git clone https://huggingface.co/Intel/musicgen-static-openvino

# unzip the 'base' set of models (like the EnCodec, tokenizer, etc.) into musicgen folder
unzip musicgen-static-openvino/musicgen_small_enc_dec_tok_openvino_models.zip -d openvino-models/musicgen

# unzip the mono-specific set of models
unzip musicgen-static-openvino/musicgen_small_mono_openvino_models.zip -d openvino-models/musicgen

# unzip the stereo-specific set of models
unzip musicgen-static-openvino/musicgen_small_stereo_openvino_models.zip -d openvino-models/musicgen

# Now that the required models are extracted, feel free to delete the cloned 'musicgen-static-openvino' directory.
# rm -rf musicgen-static-openvino

#*************************
#* Whisper Transcription *
#*************************
# clone the HF repo
git clone https://huggingface.co/Intel/whisper.cpp-openvino-models
# Extract the individual model packages into openvino-models directory
unzip whisper.cpp-openvino-models/ggml-base-models.zip -d openvino-models
unzip whisper.cpp-openvino-models/ggml-small-models.zip -d openvino-models
unzip whisper.cpp-openvino-models/ggml-small.en-tdrz-models.zip -d openvino-models
# medium models
unzip whisper.cpp-openvino-models/ggml-medium-models.zip -d openvino-models
# large models
#unzip whisper.cpp-openvino-models/ggml-large-v1-models.zip -d openvino-models
#unzip whisper.cpp-openvino-models/ggml-large-v2-models.zip -d openvino-models
#unzip whisper.cpp-openvino-models/ggml-large-v3-models.zip -d openvino-models

# Now that the required models are extracted, feel free to delete the cloned 'whisper.cpp-openvino-models' directory.
# rm -rf whisper.cpp-openvino-models

#********************
#* Music Separation *
#********************

# clone the HF repo
git clone https://huggingface.co/Intel/demucs-openvino

# Copy the demucs OpenVINO IR files
cp demucs-openvino/htdemucs_v4.bin openvino-models
cp demucs-openvino/htdemucs_v4.xml openvino-models

# Now that the required models are extracted, feel free to delete the cloned 'demucs-openvino' directory.
# rm -rf demucs-openvino

#*********************
#* Noise Suppression *
#*********************

# Clone the deepfilternet HF repo
git clone https://huggingface.co/Intel/deepfilternet-openvino

# extract deepfilter2 models
unzip deepfilternet-openvino/deepfilternet2.zip -d openvino-models

# extract deepfilter3 models
unzip deepfilternet-openvino/deepfilternet3.zip -d openvino-models

# For noise-suppression-denseunet-ll-0001, we can wget IR from openvino repo
cd openvino-models
wget https://storage.openvinotoolkit.org/repositories/open_model_zoo/2023.0/models_bin/1/noise-suppression-denseunet-ll-0001/FP16/noise-suppression-denseunet-ll-0001.xml
wget https://storage.openvinotoolkit.org/repositories/open_model_zoo/2023.0/models_bin/1/noise-suppression-denseunet-ll-0001/FP16/noise-suppression-denseunet-ll-0001.bin
cd ..
# copy models
cd $WORKDIR
sudo cp -R openvino-models /usr/local/lib/
}
#portable installation

portable_installation() {
cd $WORKDIR
mkdir "$WORKDIR/audacity-build/Release/bin/Portable Settings"
cp -r l_openvino_toolkit_ubuntu${VERSION}_2024.3.0.16041.1e3b88e4e3f_x86_64/runtime/lib/intel64/* audacity-build/Release/lib/audacity
cp -r l_openvino_toolkit_ubuntu${VERSION}_2024.3.0.16041.1e3b88e4e3f_x86_64/runtime/3rdparty/tbb/lib/* audacity-build/Release/lib/audacity
# create terminal starter
echo LD_LIBRARY_PATH=../lib/audacity ./audacity > $WORKDIR/audacity-build/Release/bin/start_audacity.sh
chmod a+x $WORKDIR/audacity-build/Release/bin/start_audacity.sh
# create desktop starter
cp $WORKDIR/audacity-build/src/audacity.desktop $HOME/.local/share/applications/audacity.desktop
sed -i "s|Exec=env GDK_BACKEND=x11 UBUNTU_MENUPROXY=0 audacity %F|Exec=/usr/bin/env GDK_BACKEND=x11 UBUNTU_MENUPROXY=0 LD_LIBRARY_PATH=$WORKDIR/audacity-build/Release/lib/audacity $WORKDIR/audacity-build/Release/bin/audacity %F|g" $HOME/.local/share/applications/audacity.desktop
}
usr_local_installation() {
# Install in /usr/local/lib
cd $WORKDIR/audacity-build
sudo make install
# copy libs to /usr/local/lib
cd $WORKDIR
sudo cp -r l_openvino_toolkit_ubuntu${VERSION}_2024.4.0.16579.c3152d32c9c_x86_64/runtime/lib/intel64/* /usr/local/lib/audacity
sudo echo /usr/local/lib/audacity.libs > /etc/ld.so.conf.d/audacity.conf
sudo ldconfig
#additional libs. All required? Try it.
#sudo cp -r libtorch/lib/* /usr/local/lib/audacity.libs
#sudo cp -r whisper-build/libwhisper.so /usr/local/lib/audacity.libs/libwhisper.so
#sudo cp -r l_openvino_toolkit_ubuntu${VERSION}_2024.3.0.16041.1e3b88e4e3f_x86_64/runtime/lib/intel64/ /usr/local/lib/audacity.libs
#sudo cp -r l_openvino_toolkit_ubuntu22_2024.3.0.16041.1e3b88e4e3f_x86_64/runtime/lib/intel64/* /usr/local/lib/audacity.libs
#sudo echo /usr/local/lib/audacity.libs > /etc/ld.so.conf.d/audacity.conf
#sudo ldconfig
}
#########################
## Program starts here ##
#########################
echo Build and install Audacity and OpenVINO plugin...
build
#echo Install Models...
# In case of update comment next line
models_install
echo portable installation
portable_installation
# or
# usr_local_installation
echo Done.
echo Start the audacity binary from $WORKDIR/audacity-build/Release/bin

