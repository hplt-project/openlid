import regex

NONWORD_REPLACE_STR = r"[^\p{Word}\p{Zs}]|\d"
NONWORD_REPLACE_PAT = regex.compile(NONWORD_REPLACE_STR)
SPACE_PAT = regex.compile(r"\s\s+")

def clean_line(line):
    """simple language-agnostic cleaning"""
    text = line.strip().replace("\n", " ").lower()  # remove whitespace, apply lowercase
    text = regex.sub(NONWORD_REPLACE_PAT, "", text)  # either (not a word nor a space) or (is digit)
    text = regex.sub(SPACE_PAT, " ", text)  # squeeze whitespace
    return text