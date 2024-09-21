# transcribe
# https://github.com/openai/whisper
# translate
# https://github.com/nidhaloff/deep-translator
import whisper
import torch
import csv
import os
from deep_translator import GoogleTranslator, ChatGptTranslator
#, LingueeTranslator, PonsTranslator
from os import listdir
from os.path import isfile, join
from pathlib import Path
from semantic_text_splitter import TextSplitter
from whisper.utils import get_writer
HOMEDIR = os.environ["HOME"]
####################
## Configuration ##
####################
# directory containing audio files (mp3)
Source_Path=HOMEDIR + "/Audio/ToTranslate"
# target path for your transcribed files (txt)
Target_Path=HOMEDIR + "/Audio/Translated"
# language you want to translate to
# supported languages: see at the end of this file
target_language="german" #deep translator
# language of your audio files
source_language="" #whisper, empty for automatic detection
# whisper model: tiny, base, small, medium, large-v1, large-v2, large-v3
# Download in "~./cache/whisper
WhisperModel="medium"
# output format
format='txt' # or srt, tsv
# choose translator see https://github.com/nidhaloff/deep-translator
UseTranslator="GoogleTranslator" # or ChatGptTranslator requires API key
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
    # check device, Nvidia hardware acceleration if available
    #device = "cuda" if torch.cuda.is_available() else "cpu"
    if torch.cuda.is_available():
        device = "cuda"
    elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    print("using device: " + device)    
    # transcribe
    model = whisper.load_model(WhisperModel, device=f"{device}") # or cuda (nvidia)
    if not source_language:
            result = model.transcribe(fname, task='transcribe',verbose=False) # automatic language detection
    else:        
        result = model.transcribe(fname, language=f"{source_language}", task='transcribe',verbose=False)
    # save transcribed file   
    print ("saving text: " + target_file + "." + format)
    writer = get_writer(format, Target_Path)
    writer(result, f'{target_file}.{format}')
        
def semantic_split(text: str, limit: int) -> list[str]:
    """Return a list of chunks from the given text, splitting it at semantically sensible boundaries while applying the specified character length limit for each chunk."""
    splitter = TextSplitter(limit)
    chunks = splitter.chunks(text)
    return chunks
        
def translate(fname):
    """Translate files"""
    print("translating...")
    source_file=Target_Path + "/" + Path(fname).stem + "." + format
    target_file=Target_Path + "/" + Path(fname).stem + "_translated_." + format
    if UseTranslator == "ChatGptTranslator":
        #ChatGPT API key required
        translator = ChatGptTranslator(api_key=gptkey, target=f"{target_language}")
    else:
        # Google Translator
        translator = GoogleTranslator(source="auto", target=f"{target_language}")
    # text length max 5000
    LIMIT = 3000
    # translate and save file
    with open(source_file, "r") as f:
        content = f.read()
        if len(content) > LIMIT:
            print("File splitting required")
            chunks = semantic_split(content, LIMIT)
            translated = translator.translate_batch(chunks)
            with open(target_file, "a") as f:
                for part in translated:
                    f.write(part)
        else:
            translated = translator.translate(text=content)           
            with open(target_file, "w") as f:
                f.write(translated)

########### main program starts here ##################
# create list of all files in "Source_Path"
files = [f for f in listdir(Source_Path) if isfile(join(Source_Path, f))]
files.sort(reverse=False)

# process files
for file in files:
    print("processing: " + file)
    transcribe(Source_Path + "/" + file)
    translate(Source_Path + "/" + file)
print("done.")    
##### Google supported output languages #####
"""
Get language list:
langs_list = GoogleTranslator().get_supported_languages() 
print(langs_list)

['afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'assamese', 'aymara', 'azerbaijani', 'bambara', 'basque', 'belarusian', 'bengali', 'bhojpuri', 'bosnian', 'bulgarian', 'catalan', 'cebuano', 'chichewa', 'chinese (simplified)', 'chinese (traditional)', 'corsican', 'croatian', 'czech', 'danish', 'dhivehi', 'dogri', 'dutch', 'english', 'esperanto', 'estonian', 'ewe', 'filipino', 'finnish', 'french', 'frisian', 'galician', 'georgian', 'german', 'greek', 'guarani', 'gujarati', 'haitian creole', 'hausa', 'hawaiian', 'hebrew', 'hindi', 'hmong', 'hungarian', 'icelandic', 'igbo', 'ilocano', 'indonesian', 'irish', 'italian', 'japanese', 'javanese', 'kannada', 'kazakh', 'khmer', 'kinyarwanda', 'konkani', 'korean', 'krio', 'kurdish (kurmanji)', 'kurdish (sorani)', 'kyrgyz', 'lao', 'latin', 'latvian', 'lingala', 'lithuanian', 'luganda', 'luxembourgish', 'macedonian', 'maithili', 'malagasy', 'malay', 'malayalam', 'maltese', 'maori', 'marathi', 'meiteilon (manipuri)', 'mizo', 'mongolian', 'myanmar', 'nepali', 'norwegian', 'odia (oriya)', 'oromo', 'pashto', 'persian', 'polish', 'portuguese', 'punjabi', 'quechua', 'romanian', 'russian', 'samoan', 'sanskrit', 'scots gaelic', 'sepedi', 'serbian', 'sesotho', 'shona', 'sindhi', 'sinhala', 'slovak', 'slovenian', 'somali', 'spanish', 'sundanese', 'swahili', 'swedish', 'tajik', 'tamil', 'tatar', 'telugu', 'thai', 'tigrinya', 'tsonga', 'turkish', 'turkmen', 'twi', 'ukrainian', 'urdu', 'uyghur', 'uzbek', 'vietnamese', 'welsh', 'xhosa', 'yiddish', 'yoruba', 'zulu']
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


