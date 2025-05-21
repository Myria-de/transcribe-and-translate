import os.path
# set device
# os.environ['ARGOS_DEVICE_TYPE'] = 'cpu'
# or (nvidia)
# os.environ['ARGOS_DEVICE_TYPE'] = 'cuda'
from pathlib import Path
import argparse
from typing import List
import argostranslate.package, argostranslate.translate
from argostranslate import package, settings, translate, utils

def check_already_installed(lang_from_code, lang_to_code):
    lang_from_code_ok = False
    lang_to_code_ok = False
    packages = package.get_installed_packages()
    
    for i, pkg in enumerate(packages):
        from_code = pkg.from_code
        to_code = pkg.to_code
        if from_code == lang_from_code:
            lang_from_code_ok = True
            if to_code == lang_to_code:
                lang_to_code_ok = True
    if lang_from_code_ok == True and lang_to_code_ok == True: 
        print (lang_from_code + '->' + lang_to_code + ' is installed')
        return True
    else:
        return False
    
def install_package(from_code, to_code):
    if not check_already_installed(from_code, to_code):
        print ('Try Install ' + from_code + '->' + to_code)
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        
        package_to_install = next(
            filter(
                lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
            )
        )
        print('Install: ' + from_code + '->' + to_code)
        argostranslate.package.install_from_path(package_to_install.download())


def check_installed(lang_from_code, lang_to_code):
    if check_already_installed(lang_from_code, lang_to_code):
        print('Translation: ' + lang_from_code + '->' + lang_to_code)
    else:
        print('Package translate-' + lang_from_code + '_' + lang_to_code + ' missing.')
        if lang_to_code != 'en' and lang_from_code != 'en':
            install_package(lang_from_code, 'en')
            install_package('en', lang_to_code)
        else:
            install_package(lang_from_code, lang_to_code)        
        
            
def translate_batch(batch: List[str], from_lang, to_lang) -> List[str]:
    arr = []
    for i, text in enumerate(batch):
        translated = argostranslate.translate.translate(text, from_lang, to_lang)
        arr.append(translated)
    return arr

def translate_text(text, from_lang, to_lang):
    translated = argostranslate.translate.translate(text, from_lang, to_lang)
    return translated

def translate_text_and_save(text, target_file, from_lang, to_lang):
    translated = argostranslate.translate.translate(text, from_lang, to_lang)
    with open(target_file, "w") as f:
        f.write(translated)

def translate_file(file_name, target_file, from_lang, to_lang):
    installed_languages = argostranslate.translate.get_installed_languages()
    underlying_translation = from_lang.get_translation(to_lang)
    argostranslatefiles.translate_file(underlying_translation, os.path.abspath(file_name))

######### Main programm starts here #############
def main():
    parser = argparse.ArgumentParser(
    prog="translate-files.py",
    description="Translate files with argostranslate",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="+", type=str, help = "file to translate")
    parser.add_argument("--from_code","-f", type=str, default="de", help = "source language")
    parser.add_argument("--to_code","-t", type=str, default="en", help = "target language")
    parser.add_argument("--outputdir","-o", type=str, default="", help = "output directory")
    args = parser.parse_args().__dict__
    file_names: str = args.pop("file")
    lang_from_code = args["from_code"]
    lang_to_code = args["to_code"]
    out_dir = args["outputdir"]
    check_installed(lang_from_code, lang_to_code)

    for file_path in file_names:
        if out_dir == '':
            parent_path = os.path.dirname(os.path.abspath(file_path))
            target_file=parent_path + "/" + Path(file_path).stem + ".translated." + lang_to_code + '.txt'
        else:
            parent_path = out_dir
            target_file=parent_path + "/" + Path(file_path).stem + ".translated." + lang_to_code + '.txt'
            
        with open(file_path, "r") as f:
             content = f.read()
             translate_text_and_save(content, target_file, lang_from_code, lang_to_code)

if __name__ == '__main__':
    main()    
    
"""
Argostranslate supported languages (2024-10)
Create a new list with argos_list_lang.py
#
Albanian → English sq->en
Arabic → English ar->en
Azerbaijani → English az->en
Basque → English eu->en
Bengali → English bn->en
Bulgarian → English bg->en
Catalan → English ca->en
Chinese (traditional) → English zt->en
Chinese → English zh->en
Czech → English cs->en
Danish → English da->en
Dutch → English nl->en
English → Albanian en->sq
English → Arabic en->ar
English → Azerbaijani en->az
English → Basque en->eu
English → Bengali en->bn
English → Bulgarian en->bg
English → Catalan en->ca
English → Chinese en->zh
English → Chinese (traditional) en->zt
English → Czech en->cs
English → Danish en->da
English → Dutch en->nl
English → Esperanto en->eo
English → Estonian en->et
English → Finnish en->fi
English → French en->fr
English → Galician en->gl
English → German en->de
English → Greek en->el
English → Hebrew en->he
English → Hindi en->hi
English → Hungarian en->hu
English → Indonesian en->id
English → Irish en->ga
English → Italian en->it
English → Japanese en->ja
English → Korean en->ko
English → Latvian en->lv
English → Lithuanian en->lt
English → Malay en->ms
English → Norwegian en->nb
English → Persian en->fa
English → Polish en->pl
English → Portuguese en->pt
English → Romanian en->ro
English → Russian en->ru
English → Slovak en->sk
English → Slovenian en->sl
English → Spanish en->es
English → Swedish en->sv
English → Tagalog en->tl
English → Thai en->th
English → Turkish en->tr
English → Ukranian en->uk
English → Urdu en->ur
Esperanto → English eo->en
Estonian → English et->en
Finnish → English fi->en
French → English fr->en
Galician → English gl->en
German → English de->en
Greek → English el->en
Hebrew → English he->en
Hindi → English hi->en
Hungarian → English hu->en
Indonesian → English id->en
Irish → English ga->en
Italian → English it->en
Japanese → English ja->en
Korean → English ko->en
Latvian → English lv->en
Lithuanian → English lt->en
Malay → English ms->en
Norwegian → English nb->en
Persian → English fa->en
Polish → English pl->en
Portuguese → English pt->en
Portuguese → Spanish pt->es
Romanian → English ro->en
Russian → English ru->en
Slovak → English sk->en
Slovenian → English sl->en
Spanish → English es->en
Spanish → Portuguese es->pt
Swedish → English sv->en
Tagalog → English tl->en
Thai → English th->en
Turkish → English tr->en
Ukranian → English uk->en
Urdu → English ur->en
"""
