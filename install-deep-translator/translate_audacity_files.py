# translate
# https://github.com/nidhaloff/deep-translator
import sys
import csv
import os
from deep_translator import GoogleTranslator, LingueeTranslator, PonsTranslator, ChatGptTranslator
from os import listdir
from os.path import isfile, join
from pathlib import Path
from semantic_text_splitter import TextSplitter
HOMEDIR = os.environ["HOME"]
###################
## Configuration ##
###################
# target path for your translated files (txt)
Target_Path=HOMEDIR + "/Audio/Translated"
Source_Path=Target_Path
# supported languages: see at the end of this file
target_language="german" #deep translator
# output format
format='txt'
# remove Audacity timestamp
# The translator removes some timestamps!
Remove_Timestamp=True
# choose translator see https://github.com/nidhaloff/deep-translator
UseTranslator="GoogleTranslator" # GoogleTranslator or ChatGptTranslator requires API key
#ChatGPT API key https://platform.openai.com/account/api-keys
gptkey="<your key here>"
#######################
## Configuration end ##
#######################
def semantic_split(text: str, limit: int) -> list[str]:
    """Return a list of chunks from the given text, splitting it at semantically sensible boundaries while applying the specified character length limit for each chunk."""
    splitter = TextSplitter(limit)
    chunks = splitter.chunks(text)
    return chunks
    
def translate(fname):
    """Translate files"""
    print("translating...")
    #source_file=Target_Path + "/" + Path(fname).stem + "." + format
    source_file=fname
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
        chunks = semantic_split(content, LIMIT)
        translated = translator.translate_batch(chunks)
        with open(target_file, "a") as f:
            for part in translated:
                f.write(part)

########### main program starts here ##################
# create list of all files in "Source_Path"
files = [f for f in listdir(Source_Path) if isfile(join(Source_Path, f))]
files.sort(reverse=False)
# new folder for converted files and translations
if not os.path.exists(Target_Path + '/CovertedAndTranslated'):
    os.makedirs(Target_Path + '/CovertedAndTranslated')
Target_Path=Target_Path + '/CovertedAndTranslated'
# process files
for file in files:    
    # remove timestamp
    if Remove_Timestamp:
        with open(Source_Path + "/" + file,'r') as infile:
            column23 = [ cols[2:3] for cols in csv.reader(infile, delimiter="\t") ]
            target_file=Target_Path + "/" + Path(file).stem + "_converted_." + format
            with open(target_file, "w") as f:
                for line in column23:
                    txt="".join(line)
                    f.write(f"{txt}\n")
        print("processing: " + target_file)        
        translate(target_file)
    else:
        translate(Source_Path + "/" + file)        
print("done.") 
##### Google supported output languages #####
"""
Get language list:
langs_list = GoogleTranslator().get_supported_languages() 
print(langs_list)

['afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'assamese', 'aymara', 'azerbaijani', 'bambara', 'basque', 'belarusian', 'bengali', 'bhojpuri', 'bosnian', 'bulgarian', 'catalan', 'cebuano', 'chichewa', 'chinese (simplified)', 'chinese (traditional)', 'corsican', 'croatian', 'czech', 'danish', 'dhivehi', 'dogri', 'dutch', 'english', 'esperanto', 'estonian', 'ewe', 'filipino', 'finnish', 'french', 'frisian', 'galician', 'georgian', 'german', 'greek', 'guarani', 'gujarati', 'haitian creole', 'hausa', 'hawaiian', 'hebrew', 'hindi', 'hmong', 'hungarian', 'icelandic', 'igbo', 'ilocano', 'indonesian', 'irish', 'italian', 'japanese', 'javanese', 'kannada', 'kazakh', 'khmer', 'kinyarwanda', 'konkani', 'korean', 'krio', 'kurdish (kurmanji)', 'kurdish (sorani)', 'kyrgyz', 'lao', 'latin', 'latvian', 'lingala', 'lithuanian', 'luganda', 'luxembourgish', 'macedonian', 'maithili', 'malagasy', 'malay', 'malayalam', 'maltese', 'maori', 'marathi', 'meiteilon (manipuri)', 'mizo', 'mongolian', 'myanmar', 'nepali', 'norwegian', 'odia (oriya)', 'oromo', 'pashto', 'persian', 'polish', 'portuguese', 'punjabi', 'quechua', 'romanian', 'russian', 'samoan', 'sanskrit', 'scots gaelic', 'sepedi', 'serbian', 'sesotho', 'shona', 'sindhi', 'sinhala', 'slovak', 'slovenian', 'somali', 'spanish', 'sundanese', 'swahili', 'swedish', 'tajik', 'tamil', 'tatar', 'telugu', 'thai', 'tigrinya', 'tsonga', 'turkish', 'turkmen', 'twi', 'ukrainian', 'urdu', 'uyghur', 'uzbek', 'vietnamese', 'welsh', 'xhosa', 'yiddish', 'yoruba', 'zulu']
"""


