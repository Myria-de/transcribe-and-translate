#!/home/te/python-trans/bin/python3
#
# Remove timestamps für Audacity transcriptions and translate
#
import sys
import csv
import os
import subprocess
import re, datetime
import glob
from os import listdir
from os.path import isfile, join
from pathlib import Path
import transcribe_translate
import warnings
warnings.filterwarnings('ignore')

#PROCESS_TIMEOUT = 4 * 60 * 60
HOMEDIR = os.environ["HOME"]
###################
## Configuration ##
###################
# target path for your translated files (txt)
Source_Path=HOMEDIR + "/Audio/Transcribed/Audacity"
Target_Path=HOMEDIR + "/Audio/Transcribed/Audacity/Translated"
# Configure translator in transcribe_translate.py
# supported languages: see at the end of this file
source_language="en" #Argos/deep translator
target_language="de" #Argos/deep translator
# input format
# srt translate srt files
# or
# txt remove timestamps from text files and translate
format='txt'
#######################
## Configuration end ##
#######################
def get_content(filename):
    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content
    
def translate_srt_file(source_file, target_file, source_language, target_language):
    """
    read srt file and translate 
    """
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
            # Text only
            else:
                text_translated=transcribe_translate.translate_text(x,source_language,target_language)
                f.write(text_translated + "\n")

            if counter % 100 == 0:
                print ("Processed %d / %d lines" % (counter, len(source_file_content)))
    
def translate_txt_file(source_file, target_file, source_language, target_language):
    with open(source_file,'r') as infile:
        column23 = [ cols[2:3] for cols in csv.reader(infile, delimiter="\t") ]
        converted_file=Target_Path + "/" + Path(source_file).stem + ".converted." + format
    with open(converted_file, "w") as f:
        for line in column23:
            txt="".join(line)
            f.write(f"{txt}\n")
    target_file=Target_Path + "/" + Path(source_file).stem + ".translated." + target_language + '.' + format
    target_file=Target_Path + "/" + Path(converted_file).stem + ".translated." +target_language + '.' + format
    print("processing: " + converted_file) 
    transcribe_translate.translate(converted_file, target_file, source_language, target_language) 

########### main program starts here ##################
def main():
    # check configured paths
    if not os.path.exists(Source_Path):
        print('Error: The path ' + Source_Path + ' does not exist. Please check the configuration.')
        sys.exit(1)
    if not os.path.exists(Target_Path):
        print('Error: The path ' + Target_Path + ' does not exist. Please check the configuration.')
        sys.exit(1)   
    #print('getcwd:      ', os.getcwd())
#    print('__file__:    ', __file__)
    #WORKDIR=os.path.dirname(__file__)
    #print(WORKDIR)
    #statement_delimiters: list = [".", "?", "!"]
    # create list of all files in "Source_Path"
    #files = [f for f in listdir(Source_Path) if isfile(join(Source_Path, f))]
    #files.sort(reverse=False)
    # init translator
    #translator=transcribe_translate.translator_init(source_language, target_language)
    if format == "srt":
        path = f'{Source_Path}/*.srt'
    if format == "txt":
        path = f'{Source_Path}/*.txt'
    files = glob.glob(path)    
    
    for file in files:
        translated_file=Target_Path + "/" + Path(file).stem + ".translated." + target_language + '.' + format
        if format == "srt":
            translate_srt_file(file, translated_file, source_language, target_language)
        if format == "txt":
            translate_txt_file(file, translated_file, source_language, target_language)
    print("Translation done.") 

if __name__ == '__main__':
    main()  

"""
##### Google supported output languages #####
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

