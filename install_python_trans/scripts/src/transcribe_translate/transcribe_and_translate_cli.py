#!/home/te/python-trans/bin/python3
# transcribe
# https://github.com/openai/whisper
# translate
# https://github.com/nidhaloff/deep-translator
import whisper
import torch
import csv
import os
import sys
import re
import warnings
import argparse
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
    
# set argos device
os.environ['ARGOS_DEVICE_TYPE'] = device
from transcribe_translate import translate_argos

def transcribe(fname, target_path, WhisperModel,source_language_whisper,whisper_task, format) -> str:
    """Transcribe audio file"""
    print ("transcribing...")
    # file name without extension
    target_file = os.path.join(target_path, Path(fname).stem)
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
    print ("saving text: " + f'{target_file}.{format}')
    writer = get_writer(format, target_path)
    writer(result, f'{target_file}.{format}')
    return f'{target_file}.{format}'
        
def semantic_split(text: str, limit: int) -> list[str]:
    """Return a list of chunks from the given text, splitting it at semantically sensible boundaries while applying the specified character length limit for each chunk."""
    splitter = TextSplitter(limit)
    chunks = splitter.chunks(text)
    return chunks

def translator_init(source_language,target_language, UseTranslator, gpt_key):
    if UseTranslator == "ChatGptTranslator":
        #ChatGPT API key required
        translator = ChatGptTranslator(api_key=gpt_key, target=f"{target_language}")
        return translator
    elif UseTranslator == "Argos":
        translate_argos.check_installed(source_language, target_language)
    else:
        # Google Translator
        translator = GoogleTranslator(source=f"{source_language}", target=f"{target_language}")
        return translator
        
def translate_chunks(chunks,source_language,target_language,UseTranslator):
    if UseTranslator == "Argos":
         translated = translate_argos.translate_batch(chunks,source_language, target_language)
    else:    
        translated = translator.translate_batch(chunks)
    return translated

def translate_text(text,source_language,target_language,UseTranslator, gpt_key,translator):
    """Translate text"""
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
    return re.match(r"((\d\d:)\d\d).(\d{3}) --> ((\d\d:)\d\d).(\d{3})", content) is not None


def translate(source_file, target_file, source_language, target_language, text_format, UseTranslator, gpt_key):
    """Translate files"""
    
    print ("Using translator: " + UseTranslator)
    print("translating...")
    translator=translator_init(source_language,target_language,UseTranslator, gpt_key)
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
                    text_translated=translate_text(x,source_language,target_language,UseTranslator, gpt_key,translator)
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
                    #print(x)
                # Timestamp:
                elif was_id:
                    f.write(x + "\n")
                    was_id = False
                elif len(x) == 0:
                    f.write("\n")
                    was_empty_line = True
                else:
                    
                    text_translated=translate_text(x,source_language,target_language,UseTranslator, gpt_key,translator)
                    f.write(text_translated + "\n")
             
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
    # supported languages: -> Argos_Languages.txt and Google_whisper_Languages.txt
    parser = argparse.ArgumentParser(
    prog="transcribe_translate_cli.py",
    description="Transcribe and translate video files",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("files",nargs="+", type=str, default="", help = "source file")
    parser.add_argument("--output-directory","-o", type=str, default="", help = "destination path")
    parser.add_argument("--source_lang","-s", type=str, default="en", help = "source language")
    parser.add_argument("--target_lang","-t", type=str, default="de", help = "target language")
    parser.add_argument("--source_whisper_lang","-w", type=str, default="", help = "whisper source language")
    parser.add_argument("--whisper_task","-p", type=str, default="transcribe", help = "whisper task (transcribe, translate)")
    parser.add_argument("--whisper_model","-m", type=str, default="medium", help = "whisper model")
    parser.add_argument("--output_format","-f", type=str, default="srt", help = "output format (txt, srt, vtt)")    
    parser.add_argument("--translator","-r", type=str, default="GoogleTranslator", help = "translator to use")
    parser.add_argument("--api_key","-a", type=str, default="", help = "api key chatgpt")
    parser.add_argument("--translate_only","-n",  action='store_true', default=False, help = "translation only")
    args = parser.parse_args().__dict__
    Source_Files=args["files"]
    Target_Path=(args["output_directory"].rstrip(os.sep))
    source_language=args["source_lang"]
    target_language=args["target_lang"]
    source_language_whisper=args["source_whisper_lang"]
    whisper_task=args["whisper_task"]
    WhisperModel=args["whisper_model"]
    format=args["output_format"]
    UseTranslator=args["translator"]
    api_key=args["api_key"]
    api_key=args["api_key"]
    translate_only=args["translate_only"]
    if not os.path.exists(Target_Path):
        print('Error: The path ' + Target_Path + ' does not exist. Please check the configuration.')
        sys.exit(1)    
    for file in Source_Files:
        print("processing: " + file)
        if translate_only != True:
            transcribed_file=transcribe(file, Target_Path, WhisperModel, source_language_whisper, whisper_task,format)
        else:
            transcribed_file = os.path.join(Target_Path, Path(file).stem)+"." + format
        if not UseTranslator == "":
            if not whisper_task == "translate":
                translated_file=os.path.join(Target_Path, Path(file).stem) + ".translated." + UseTranslator +'.'+ target_language + '.' + format
                translate(transcribed_file, translated_file, source_language, target_language, format,UseTranslator,api_key)

    print("done.")    

if __name__ == '__main__':
    main()  

