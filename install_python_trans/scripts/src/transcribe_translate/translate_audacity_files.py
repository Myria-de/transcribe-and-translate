#
# Remove timestamps für Audacity transcriptions and translate
#
import sys
import csv
import os
import subprocess
import re, datetime
import glob
import configparser
from os import listdir
from os.path import isfile, join
from pathlib import Path
from transcribe_translate import transcribe_and_translate
import warnings
warnings.filterwarnings('ignore')
if sys.platform == "win32":
    HOMEDIR = os.environ["USERPROFILE"]
else:
    HOMEDIR = os.environ["HOME"]

cfg = configparser.ConfigParser()
cfg.read('translate_audacity_config.ini')
###################
## Configuration ##
###################
# target path for your translated files (txt)
# absolute Path in the ini file, set both
# i.Ex. /home/user/...
ABS_Source_Path=cfg.get('Settings', 'ABS_Source_Path')
ABS_Target_Path=cfg.get('Settings', 'ABS_Target_Path')
# or leave it empty in the ini file and instead set
# home directory path with trailing "/" in the ini file
# i.Ex. /Audio/...
# HOMEDIR will be added now
if ABS_Source_Path == "":
    Source_Path = HOMEDIR + cfg.get('Settings', 'Source_Path')   
    # target path for your transcribed files (txt)
    Target_Path = HOMEDIR + cfg.get('Settings', 'Target_Path')
else:
    Source_Path = ABS_Source_Path
    Target_Path = ABS_Target_Path
# Configure translator in transcribe_translate_config.ini
# supported languages: -> Argos_Languages.txt and Google_whisper_Languages.txt
source_language=cfg.get('Settings', 'source_language')   
target_language=cfg.get('Settings', 'target_language') 
#######################
## Configuration end ##
#######################
def get_content(filename):
    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content

def has_timestamp(content: str) -> bool:
    """Check if line is a timestamp vtt format
    """
    return re.match(r"((\d\d:)\d\d).(\d{3}) --> ((\d\d:)\d\d).(\d{3})", content) is not None    

def translate_vtt_file(source_file, target_file, source_language, target_language):
    """
    read vtt file and translate 
    """
    source_file_content=get_content(source_file)
    print("processing: " + source_file)
    with open(target_file, "w") as f:
        f.write("WEBVTT\n")
        for x in source_file_content[1:]:
            if has_timestamp(x):
                f.write(x + "\n")
            elif len(x) == 0:
                f.write("\n")
            else:
                text_translated=transcribe_and_translate.translate_text(x,source_language,target_language)
                f.write(text_translated + "\n")

def translate_srt_file(source_file, target_file, source_language, target_language):
    """
    read srt file and translate 
    """
    source_file_content=get_content(source_file)
    print("processing: " + source_file)
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
                text_translated=transcribe_and_translate.translate_text(x,source_language,target_language)
                f.write(text_translated + "\n")

            if counter % 100 == 0:
                print ("Processed %d / %d lines" % (counter, len(source_file_content)))
    
def translate_txt_file(source_file, target_file, source_language, target_language):
    """
    read txt file and translate 
    """
    with open(source_file,'r') as infile:
        column23 = [ cols[2:3] for cols in csv.reader(infile, delimiter="\t") ]
        converted_file=Target_Path + "/" + Path(source_file).stem + ".converted.txt"
    
    with open(converted_file, "w") as f:
        for line in column23:
            txt="".join(line)
            f.write(f"{txt}\n")
    
    target_file=Target_Path + "/" + Path(converted_file).stem + ".translated." +target_language + '.txt'
    print("processing: " + converted_file) 
    transcribe_and_translate.translate(converted_file, target_file, source_language, target_language, "txt") 

########### main program starts here ##################
def main():
    # check configured paths
    if not os.path.exists(Source_Path):
        print('Error: The path ' + Source_Path + ' does not exist. Please check the configuration.')
        sys.exit(1)
    if not os.path.exists(Target_Path):
        print('Error: The path ' + Target_Path + ' does not exist. Please check the configuration.')
        sys.exit(1)   
    files = [f for f in listdir(Source_Path) if isfile(join(Source_Path, f))]
    files.sort(reverse=False)
    for file in files:
        filename, file_extension = os.path.splitext(Source_Path +'/'+ file )
        translated_file=Target_Path + "/" + Path(file).stem + ".translated." + target_language + file_extension
        source_file=Source_Path + '/' + file
        
        if file_extension == '.txt':
            translate_txt_file(source_file, translated_file, source_language, target_language)
        if file_extension == '.srt':
            translate_srt_file(source_file, translated_file, source_language, target_language)
        if file_extension == '.vtt':
            translate_vtt_file(source_file, translated_file, source_language, target_language)
    print("Translation done.") 

if __name__ == '__main__':
    main()

