# -*- coding: utf-8 -*-

import glob
import os

def get_output_path(path=None):
    if path:
        return "output/" + path + "/"
    return "output/"

def prepare_output(filename):
    path = get_output_path(filename)
    if not os.path.isdir(path):
        os.makedirs(path)
    files = glob.glob('%s/*' % (path))
    for f in files: # clear output folder
        os.remove(f)

def get_basename(path):
    filename_with_ext = os.path.basename(path)
    filename, _ = os.path.splitext(filename_with_ext)
    return filename

def write_csv(path, name, headers, data):
    f = open(path + "%s.csv" % (name), "w", encoding="utf-8")
    f.write(";".join(headers) + '\n')
    for line in data:
        f.write(";".join(str(x) for x in line) + '\n')
    f.close()

def write_file(path, name, data):
    f = open(path + "%s.txt" % (name), "w", encoding="utf-8")
    f.write(data)
    f.close()
