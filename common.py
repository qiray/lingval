# -*- coding: utf-8 -*-

import tabulate

def accuire_lock(lock):
    if lock:
        lock.acquire()

def release_lock(lock):
    if lock:
        lock.release()

def print_table(title, headers, data, lock=None):
    accuire_lock(lock)
    if title:
        print(title)
    print(tabulate.tabulate(data, headers=headers, numalign="right"))
    release_lock(lock)
