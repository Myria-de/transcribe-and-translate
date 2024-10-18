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
warnings.filterwarnings('ignore')
from string import Template
from deep_translator import GoogleTranslator, ChatGptTranslator
#, LingueeTranslator, PonsTranslator
from os import listdir
from os.path import isfile, join
from pathlib import Path
from semantic_text_splitter import TextSplitter
from whisper.utils import get_writer
# check device, Nvidia hardware acceleration if available
if torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"
    # set argos device

os.environ['ARGOS_DEVICE_TYPE'] = device
import translate_argos

HOMEDIR = os.environ["HOME"]
####################
## Configuration ##
####################
# directory containing audio files (mp3)
Source_Path=HOMEDIR + "/Audio/ToTranscribe"
# target path for your transcribed files (txt)
Target_Path=HOMEDIR + "/Audio/Transcribed"
# language you want to translate from/to
# supported languages: see at the end of this file
source_language="en" # Argos/deep translator
target_language="de" # Argos/deep translator
# language of your audio files
source_language_whisper="" #whisper, empty for automatic detection
whisper_task="transcribe"
#whisper_task="translate" # to english only
# whisper model: tiny, base, small, medium, large-v1, large-v2, large-v3
# Required VRAM see https://github.com/openai/whisper
# Download in "~./cache/whisper
WhisperModel="medium"
# output format
format='vtt' # or srt, vtt
# choose translator see https://github.com/nidhaloff/deep-translator
#UseTranslator="GoogleTranslator" # or ChatGptTranslator requires API key
UseTranslator="Argos"
#ChatGPT API key https://platform.openai.com/account/api-keys
gptkey="<your key here>"
#######################
## Configuration end ##
#######################
def transcribe(fname):
    """Transcribe audio file"""
    print ("transcribing...")
    # file name without extension
    target_file=Target_Path + "/" + Path(fname).stem

    print("using device: " + device)    
    # transcribe
    model = whisper.load_model(WhisperModel, device=f"{device}") # or cuda (nvidia)
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


def translate(source_file, target_file,source_language,target_language):
    """Translate files"""
    print("translating...")
    #source_file=Target_Path + "/" + Path(fname).stem + "." + format
    #target_file=Target_Path + "/" + Path(fname).stem + ".translated." + UseTranslator +'.'+ target_language + '.' + format
    #print(target_file)
    translator=translator_init(source_language,target_language)
    if format == 'vtt':
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
                
    elif format == 'srt':
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
                    #print(x)
                    was_id = False
                elif len(x) == 0:
                    f.write("\n")
                    was_empty_line = True
                else:
                    
                    text_translated=translate_text(x,source_language,target_language)
                    #print(text_translated)
                    f.write(text_translated + "\n")
            #if counter % 100 == 0:
            #    print ("Processed %d / %d lines" % (counter, len(source_file_content)))
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
        #transcribe(Source_Path + "/" + file)
        if not whisper_task == "translate":
            translate(source_file, target_file, source_language, target_language)
    print("done.")    

if __name__ == '__main__':
    main()  

"""
##### Google supported output languages #####
Get language list:
get_lang_list_google()
afrikaans:af
albanian:sq
amharic:am
arabic:ar
armenian:hy
assamese:as
aymara:ay
azerbaijani:az
bambara:bm
basque:eu
belarusian:be
bengali:bn
bhojpuri:bho
bosnian:bs
bulgarian:bg
catalan:ca
cebuano:ceb
chichewa:ny
chinese (simplified):zh-CN
chinese (traditional):zh-TW
corsican:co
croatian:hr
czech:cs
danish:da
dhivehi:dv
dogri:doi
dutch:nl
english:en
esperanto:eo
estonian:et
ewe:ee
filipino:tl
finnish:fi
french:fr
frisian:fy
galician:gl
georgian:ka
german:de
greek:el
guarani:gn
gujarati:gu
haitian creole:ht
hausa:ha
hawaiian:haw
hebrew:iw
hindi:hi
hmong:hmn
hungarian:hu
icelandic:is
igbo:ig
ilocano:ilo
indonesian:id
irish:ga
italian:it
japanese:ja
javanese:jw
kannada:kn
kazakh:kk
khmer:km
kinyarwanda:rw
konkani:gom
korean:ko
krio:kri
kurdish (kurmanji):ku
kurdish (sorani):ckb
kyrgyz:ky
lao:lo
latin:la
latvian:lv
lingala:ln
lithuanian:lt
luganda:lg
luxembourgish:lb
macedonian:mk
maithili:mai
malagasy:mg
malay:ms
malayalam:ml
maltese:mt
maori:mi
marathi:mr
meiteilon (manipuri):mni-Mtei
mizo:lus
mongolian:mn
myanmar:my
nepali:ne
norwegian:no
odia (oriya):or
oromo:om
pashto:ps
persian:fa
polish:pl
portuguese:pt
punjabi:pa
quechua:qu
romanian:ro
russian:ru
samoan:sm
sanskrit:sa
scots gaelic:gd
sepedi:nso
serbian:sr
sesotho:st
shona:sn
sindhi:sd
sinhala:si
slovak:sk
slovenian:sl
somali:so
spanish:es
sundanese:su
swahili:sw
swedish:sv
tajik:tg
tamil:ta
tatar:tt
telugu:te
thai:th
tigrinya:ti
tsonga:ts
turkish:tr
turkmen:tk
twi:ak
ukrainian:uk
urdu:ur
uyghur:ug
uzbek:uz
vietnamese:vi
welsh:cy
xhosa:xh
yiddish:yi
yoruba:yo
zulu:zu
"""
#
##### Whisper supported input languages #####
#####     Output is always english      #####
"""
LANGUAGES = {
    "en": "english",
    "zh": "chinese",
    "de": "german",
    "es": "spanish",
    "ru": "russian",
    "ko": "korean",
    "fr": "french",
    "ja": "japanese",
    "pt": "portuguese",
    "tr": "turkish",
    "pl": "polish",
    "ca": "catalan",
    "nl": "dutch",
    "ar": "arabic",
    "sv": "swedish",
    "it": "italian",
    "id": "indonesian",
    "hi": "hindi",
    "fi": "finnish",
    "vi": "vietnamese",
    "he": "hebrew",
    "uk": "ukrainian",
    "el": "greek",
    "ms": "malay",
    "cs": "czech",
    "ro": "romanian",
    "da": "danish",
    "hu": "hungarian",
    "ta": "tamil",
    "no": "norwegian",
    "th": "thai",
    "ur": "urdu",
    "hr": "croatian",
    "bg": "bulgarian",
    "lt": "lithuanian",
    "la": "latin",
    "mi": "maori",
    "ml": "malayalam",
    "cy": "welsh",
    "sk": "slovak",
    "te": "telugu",
    "fa": "persian",
    "lv": "latvian",
    "bn": "bengali",
    "sr": "serbian",
    "az": "azerbaijani",
    "sl": "slovenian",
    "kn": "kannada",
    "et": "estonian",
    "mk": "macedonian",
    "br": "breton",
    "eu": "basque",
    "is": "icelandic",
    "hy": "armenian",
    "ne": "nepali",
    "mn": "mongolian",
    "bs": "bosnian",
    "kk": "kazakh",
    "sq": "albanian",
    "sw": "swahili",
    "gl": "galician",
    "mr": "marathi",
    "pa": "punjabi",
    "si": "sinhala",
    "km": "khmer",
    "sn": "shona",
    "yo": "yoruba",
    "so": "somali",
    "af": "afrikaans",
    "oc": "occitan",
    "ka": "georgian",
    "be": "belarusian",
    "tg": "tajik",
    "sd": "sindhi",
    "gu": "gujarati",
    "am": "amharic",
    "yi": "yiddish",
    "lo": "lao",
    "uz": "uzbek",
    "fo": "faroese",
    "ht": "haitian creole",
    "ps": "pashto",
    "tk": "turkmen",
    "nn": "nynorsk",
    "mt": "maltese",
    "sa": "sanskrit",
    "lb": "luxembourgish",
    "my": "myanmar",
    "bo": "tibetan",
    "tl": "tagalog",
    "mg": "malagasy",
    "as": "assamese",
    "tt": "tatar",
    "haw": "hawaiian",
    "ln": "lingala",
    "ha": "hausa",
    "ba": "bashkir",
    "jw": "javanese",
    "su": "sundanese",
    "yue": "cantonese",

# language code lookup by name, with a few language aliases
    "burmese": "my",
    "valencian": "ca",
    "flemish": "nl",
    "haitian": "ht",
    "letzeburgesch": "lb",
    "pushto": "ps",
    "panjabi": "pa",
    "moldavian": "ro",
    "moldovan": "ro",
    "sinhalese": "si",
    "castilian": "es",
    "mandarin": "zh",
"""


