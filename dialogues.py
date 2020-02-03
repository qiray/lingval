# -*- coding: utf-8 -*-

import re
import translations

def get_dialogues_info(text):
    pattern = re.compile(r"\s*-.*")
    lines = text.splitlines()
    dialogues_count = 0
    dialogues_len = 0
    total_len = 0
    total_count = 0
    for line in lines:
        if pattern.match(line):
            dialogues_count += 1
            dialogues_len += len(line)
        if (line and not line.isspace()):
            total_count += 1
            total_len += len(line)
    return [("%s, %%" % translations.get("dialogues"))], [[float(dialogues_len)/total_len*100]]