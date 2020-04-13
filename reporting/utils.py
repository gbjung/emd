import re

def escape_sequence_character(text):
    if not text:
        return ''
    return re.sub('[\x00-\x08\x0B-\x1F]', '', text)
