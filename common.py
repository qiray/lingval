# -*- coding: utf-8 -*-

import tabulate

def print_table(title, headers, data, lock=None):
    if lock:
        lock.acquire()
    if title:
        print(title)
    print(tabulate.tabulate(data, headers=headers, numalign="right"))
    if lock:
        lock.release()
