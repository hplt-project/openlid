# author: laurie
from .sentence_split import LANGS_MOSES, split_lang_code_map
from sacremoses import MosesPunctNormalizer

def get_mpn(splitter_lang):
    """Set up Moses Punct normaliser with correct lang, or fall back to English"""
    # check if Lang_Script code can be converted to three-letter then check for Moses
    moses_lang = "en"  # default
    if splitter_lang in split_lang_code_map:
        lang = split_lang_code_map[splitter_lang]
        if lang in LANGS_MOSES:
            moses_lang = LANGS_MOSES[lang]  # get better lang if possible

    mpn = MosesPunctNormalizer(lang=moses_lang)

    return mpn