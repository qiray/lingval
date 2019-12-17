# -*- coding: utf-8 -*-

import tabulate

def print_table(title, headers, data):
    if title:
        print(title)
    print(tabulate.tabulate(data, headers=headers, numalign="right"))
