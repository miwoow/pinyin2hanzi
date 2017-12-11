#!/bin/env python
#encoding:utf-8

import io
import sys
import sqlite3

def load_start(start):
    fh2 = open('start.sql', 'w')
    fh = io.open('start.txt', 'r', encoding='utf-8')
    for line in fh.readlines():
        line = line.strip()
        line_arr = line.split(' ')
        start[line_arr[0]] = line_arr[1]
        sql = "insert into start (word, prob) values('%s', %s);\n" % (line_arr[0], line_arr[1])
        fh2.write(sql.encode('utf-8'))
    fh.close()
    fh2.close()

def load_trans(trans):
    fh = io.open('trans.txt', 'r', encoding='utf-8')
    fh2 = open('trans.sql', 'w')
    for line in fh.readlines():
        line = line.strip()
        line_arr = line.split(' ')
        trans[line_arr[0]] = line_arr[1]
        sql = "insert into trans (one, two, prob) values ('%s', '%s', %s);\n" % (line_arr[0][0], line_arr[0][1], line_arr[1])
        fh2.write(sql.encode('utf-8'))
        
    fh.close()
    fh2.close()


def load_emission(emission):
    fh2 = open('emission.sql', 'w')
    fh = io.open('emission.txt', 'r', encoding='utf-8')
    for line in fh.readlines():
        line = line.strip()
        line_arr = line.split(' ')
        if len(line_arr) < 3:
            print line
            continue
        trans[line_arr[0]] = {}
        trans[line_arr[0]][line_arr[1]] = line_arr[2]
        sql = "insert into emission (word, pinyin, prob) values('%s', '%s', %s);\n" % (line_arr[0], line_arr[1], line_arr[2])
        fh2.write(sql.encode('utf-8'))
    fh.close()
    fh2.close()


if __name__ == '__main__':
    start = {}
    trans = {}
    emission = {}
    load_start(start)
    load_trans(trans)
    load_emission(emission)
    while True:
        pinyin = raw_input('INPUT: ')
        pinyin = pinyin.strip()
        pinyin_arr = pinyin.split(' ')
        print pinyin_arr
