# transcribe
# https://github.com/openai/whisper
# translate
# https://github.com/nidhaloff/deep-translator
import whisper
import torch
import csv
import os
import sys
import platform
import re
import configparser
import warnings
warnings.filterwarnings('ignore')
from string import Template
from deep_translator import GoogleTranslator, ChatGptTranslator
#, LingueeTranslator, PonsTranslator
from os import listdir
from os.path import isfile, join
from pathlib import Path
from semantic_text_splitter import TextSplitter
from whisper.utils import get_writer
import importlib.util
# check device, Nvidia hardware acceleration if available
if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"
# use intel NPU if lib ist installed
intel_npu_lib = importlib.util.find_spec("intel_npu_acceleration_library")
npu_lib_found = intel_npu_lib is not None
if npu_lib_found:
    import intel_npu_acceleration_library
    from intel_npu_acceleration_library.compiler import CompilerConfig

os.environ['ARGOS_DEVICE_TYPE'] = device
from transcribe_translate import translate_argos
if sys.platform == "win32":
    HOMEDIR = os.environ["USERPROFILE"]
else:
    HOMEDIR = os.environ["HOME"]

cfg = configparser.ConfigParser()
if os.path.isfile('transcribe_translate_config.ini'):
    cfg.read('transcribe_translate_config.ini')
else:
    print ('Error: Please create/edit transcribe_translate_config.ini')
    sys.exit(1)    
####################
## Configuration ##
####################
# directory containing audio/video files (mp4, mp3, ...)
# absolute Path in the ini file, set both
# i.Ex. /home/user/...
ABS_Source_Path=cfg.get('Settings', 'ABS_Source_Path')
ABS_Target_Path=cfg.get('Settings', 'ABS_Target_Path')
# or leave ist empty and set
# path with trailing "/" in the ini file
# i.Ex. /python-trans/...
# HOMEDIR will be added now
if ABS_Source_Path == "":
    Source_Path = HOMEDIR + cfg.get('Settings', 'Source_Path')   
    # target path for your transcribed files (txt)
    Target_Path = HOMEDIR + cfg.get('Settings', 'Target_Path')
else:
    Source_Path = ABS_Source_Path
    Target_Path = ABS_Target_Path
# language you want to translate from/to
# supported languages: -> Argos_Languages.txt and Google_whisper_Languages.txt
source_language=cfg.get('Settings', 'source_language')   
target_language=cfg.get('Settings', 'target_language')   
# language of your audio files
source_language_whisper=cfg.get('Settings', 'source_language_whisper')   
#whisper_task="translate" # to english only
whisper_task=cfg.get('Settings', 'whisper_task')   
# whisper model: tiny, base, small, medium, large-v1, large-v2, large-v3
# Required VRAM see https://github.com/openai/whisper
# Download in "~./cache/whisper
WhisperModel=cfg.get('Settings', 'WhisperModel')   
# output format
format=cfg.get('Settings', 'format')
# choose translator see https://github.com/nidhaloff/deep-translator
# UseTranslator="GoogleTranslator" # or ChatGptTranslator requires API key
UseTranslator=cfg.get('Settings', 'UseTranslator')
#ChatGPT API key https://platform.openai.com/account/api-keys
api_key=cfg.get('Settings', 'api_key')

#######################
## Configuration end ##
#######################
def transcribe(fname):
    """Transcribe audio file"""
    print ("transcribing...")
    # file name without extension
    target_file=Target_Path + "/" + Path(fname).stem
    if npu_lib_found:
        print("using device: npu")
        model = whisper.load_model(WhisperModel)
        compiler_conf = CompilerConfig(dtype=torch.int8)
        model_compiled = intel_npu_acceleration_library.compile(model, compiler_conf)
        if not source_language_whisper:
            result = model_compiled.transcribe(fname, task=f"{whisper_task}",verbose=False) # automatic language detection
        else:        
            result = model_compiled.transcribe(fname, language=f"{source_language_whisper}", task=f"{whisper_task}",verbose=False)
    else:
        print("using device: " + device)    
        # transcribe
        model = whisper.load_model(WhisperModel, device=f"{device}") # cpu or cuda (nvidia)
        if not source_language_whisper:
            result = model.transcribe(fname, task=f"{whisper_task}",verbose=False) # automatic language detection
        else:        
            result = model.transcribe(fname, language=f"{source_language_whisper}", task=f"{whisper_task}",verbose=False)

    # save transcribed file   
    print ("saving text: " + target_file + "." + format)
    writer = get_writer(format, Target_Path)
    writer(result, f'{target_file}.{format}')
        
def semantic_split(text: str, limit: int) -> list[str]:
    """Return a list of chunks from the given text, splitting it at semantically sensible boundaries while applying the specified character length limit for each chunk."""
    splitter = TextSplitter(limit)
    chunks = splitter.chunks(text)
    return chunks

def translator_init(source_language,target_language):
    if UseTranslator == "ChatGptTranslator":
        #ChatGPT API key required
        translator = ChatGptTranslator(api_key=gptkey, target=f"{target_language}")
        return translator
    elif UseTranslator == "Argos":
        translate_argos.check_installed(source_language, target_language)
    else:
        # Google Translator
        translator = GoogleTranslator(source=f"{source_language}", target=f"{target_language}")
        return translator
        
def translate_chunks(chunks,source_language,target_language):
    translator=translator_init(source_language, target_language)
    #print(chunks)
    if UseTranslator == "Argos":
         translated = translate_argos.translate_batch(chunks,source_language, target_language)
    else:    
        translated = translator.translate_batch(chunks)
    #print(translated)
    return translated

def translate_text(text,source_language,target_language):
    """Translate text"""
    #translator=translator_init(source_language, target_language)
    LIMIT = 4000
    if len(text) > LIMIT:
        print("File splitting required")
        chunks = semantic_split(text, LIMIT)
        if UseTranslator == "Argos":
             translated = translate_argos.translate_batch(chunks,source_language, target_language)
        else:    
            translated = translator.translate_batch(chunks)
    else:
        if UseTranslator == "Argos":
            translated = translate_argos.translate_text(text, source_language, target_language)
        else:
            translated = translator.translate(text=text)
    return translated

def get_content(filename):
    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content

def has_timestamp(content: str) -> bool:
    """Check if line is a timestamp srt format

    :contents -- contents of vtt file
    """
    #return re.match(r"((\d\d:){2}\d\d),(\d{3}) --> ((\d\d:){2}\d\d),(\d{3})", content) is not None
    return re.match(r"((\d\d:)\d\d).(\d{3}) --> ((\d\d:)\d\d).(\d{3})", content) is not None


def translate(source_file, target_file, source_language, target_language, text_format):
    """Translate files"""
    print("translating...")
    translator=translator_init(source_language,target_language)
    if text_format == 'vtt':
        source_file_content=get_content(source_file)
        with open(target_file, "w") as f:
            f.write("WEBVTT\n")
            for x in source_file_content[1:]:
                if has_timestamp(x):
                    f.write(x + "\n")
                elif len(x) == 0:
                    f.write("\n")
                else:
                    text_translated=translate_text(x,source_language,target_language)
                    f.write(text_translated + "\n")
                
    elif text_format == 'srt':
        source_file_content=get_content(source_file)
        with open(target_file, "w") as f:
            was_empty_line = False
            was_id = False
            counter = 0
            for x in source_file_content:
                counter = counter + 1
                # ID
                if counter == 1 or was_empty_line:
                    f.write(x + "\n")
                    was_id = True
                    was_empty_line = False
                # Timestamp:
                elif was_id:
                    f.write(x + "\n")
                    was_id = False
                elif len(x) == 0:
                    f.write("\n")
                    was_empty_line = True
                else:
                    
                    text_translated=translate_text(x,source_language,target_language)
                    f.write(text_translated + "\n")
    else:    
        LIMIT = 4000
        # translate and save file
        with open(source_file, "r") as f:
            content = f.read()
        if len(content) > LIMIT:
            print("File splitting required")
            chunks = semantic_split(content, LIMIT)
            if UseTranslator == "Argos":
                translated = translate_argos.translate_batch(chunks,source_language, target_language)
            else:    
                translated = translator.translate_batch(chunks)
            with open(target_file, "a") as f:
                for part in translated:
                    f.write(part)
        else:
            if UseTranslator == "Argos":
                translated = translate_argos.translate_text(content, source_language, target_language)
            else:
                translated = translator.translate(text=content)
            with open(target_file, "w") as f:
                f.write(translated)
                
def get_lang_list_google():
    langs_dict = GoogleTranslator().get_supported_languages(as_dict=True) 
    for key in langs_dict:
        print(key + ':' + langs_dict[key])

########### main program starts here ##################
def main():
    # check configured paths
    if not os.path.exists(Source_Path):
        print('Error: The path ' + Source_Path + ' does not exist. Please check the configuration.')
        sys.exit(1)
    if not os.path.exists(Target_Path):
        print('Error: The path ' + Target_Path + ' does not exist. Please check the configuration.')
        sys.exit(1)    
    # create list of files in "Source_Path"
    files = [f for f in listdir(Source_Path) if isfile(join(Source_Path, f))]
    files.sort(reverse=False)
    # process files
    for file in files:
        print("processing: " + file)
        source_file=Target_Path + "/" + Path(Source_Path + "/" + file).stem + "." + format
        target_file=Target_Path + "/" + Path(Source_Path + "/" + file).stem + ".translated." + UseTranslator +'.'+ target_language + '.' + format
        transcribe(Source_Path + "/" + file)
        if not whisper_task == "translate":
            translate(source_file, target_file, source_language, target_language, format)
    print("done.")    

if __name__ == '__main__':
    main()  

