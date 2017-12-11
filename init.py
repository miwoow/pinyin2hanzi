#!/bin/env python
#encoding:utf-8

import io
import os
import re
from pypinyin import lazy_pinyin

def col_files(files):
    path = './dic'

    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path, i)):
            files.append(os.path.join(path, i))
        else:
            npath = os.path.join(path, i)
            for j in os.listdir(npath):
                files.append(os.path.join(npath, j))


def init_start(files):
    start = {}
    for f in files:
        fh = io.open(f, 'r', encoding='utf-8')
        for line in fh.readlines():
            line = line.strip()
            if line.startswith('#') or line.startswith('-'):
                print line
                continue

            line = re.sub(r'[‘’\s+\.\!\/_,$%^*(+"\']+|[+——《》！，。？、~@#￥%……&*（）：；]+'.decode("utf8"), " ".decode("utf8"), line)
            for char_word in line.split(' '):
                char_word = char_word.strip()
                if len(char_word) > 0:
                    if start.has_key(char_word[0]):
                        start[char_word[0]] = start[char_word[0]] + 1
                    else:
                        start[char_word[0]] = 1
        fh.close()

    fh = open('start.txt', 'w')
    for i in start.keys():
        line = '%s %s\n' % (i, start[i])
        fh.write(line.encode('utf-8'))
    fh.close()

def init_trans(files):
    trans = {}
    for f in files:
        print 'do file %s' % f
        fh = io.open(f, 'r', encoding='utf-8')
        for line in fh.readlines():
            line = line.strip()
            if line.startswith('#') or line.startswith('-'):
                print line
                continue
#            line = re.sub(r'[^u4e00-u9fa5]+', '', line)
            line = re.sub(r'[‘’\s+\.\!\/_,$%^*(+"\']+|[+——《》！，。？、~@#￥%……&*（）：；]+'.decode("utf8"), " ".decode("utf8"), line)
            for char_word in line.split(' '):
                char_word = char_word.strip()
                if len(char_word) > 1:
                    for i in range(0, len(char_word)-1):
                        msg = char_word[i:i+2]
                        if trans.has_key(msg):
                            trans[msg] = trans[msg] + 1
                        else:
                            trans[msg] = 1

        fh.close()

    print 'start output ... '
    fh = open('trans.txt', 'w')
    for i in trans.keys():
        line = '%s %s\n' % (i, trans[i])
        fh.write(line.encode('utf-8'))
    fh.close()
    print 'output end...'

def init_emission(files):
    emission = {}
    for f in files:
        print 'do file %s' % f
        fh = io.open(f, 'r', encoding='utf-8')
        for line in fh.readlines():
            line = line.strip()
            if line.startswith('#') or line.startswith('-'):
                print line
                continue
#            line = re.sub(r'[^u4e00-u9fa5]+', '', line)
            line = re.sub(r'[‘’\s+\.\!\/_,$%^*(+"\']+|[+——《》！，。？、~@#￥%……&*（）：；]+'.decode("utf8"), " ".decode("utf8"), line)
            for char_word in line.split(' '):
                char_word = char_word.strip()
                if len(char_word) > 0:
                    
                    pinyin_arr = lazy_pinyin(char_word)
                    line_len = len(char_word)
                    pinyin_arr_len = len(pinyin_arr)
                    if line_len != pinyin_arr_len:
                        line = re.sub(r'[0-9a-zA-Z]+', '', char_word)
                        pinyin_arr = lazy_pinyin(char_word)
                        line_len = len(char_word)
                        pinyin_arr_len = len(pinyin_arr)
                        if line_len == 0 or line_len != pinyin_arr_len:
                            continue
                    for i in range(0, len(char_word)):
                        if emission.has_key(char_word[i]):
                            if emission[char_word[i]].has_key(pinyin_arr[i]):
                                emission[char_word[i]][pinyin_arr[i]] = emission[char_word[i]][pinyin_arr[i]] + 1
                            else:
                                emission[char_word[i]][pinyin_arr[i]] = 1
                        else:
                            emission[char_word[i]] = {}
                            emission[char_word[i]][pinyin_arr[i]] = 1
        fh.close()

    print 'start output ...'
    fh = open('emission.txt', 'w')
    for i in emission.keys():
        for j in emission[i].keys():
            line = '%s %s %s\n' % (i, j, emission[i][j])
            fh.write(line.encode('utf-8'))
    fh.close()
    print 'end output ...'


if __name__ == '__main__':
    files = []
    col_files(files)
    init_start(files)
    init_trans(files)
    init_emission(files)

