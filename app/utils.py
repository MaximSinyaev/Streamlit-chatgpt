import re

def strip_spaces(text):
    return re.sub(r" +", " ", text).strip()