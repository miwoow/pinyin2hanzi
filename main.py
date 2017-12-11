#!/bin/env python
#encoding:utf-8

import io
import sys
import pprint
import json
import mysql.connector

def gen_pai(O, pai, cursor):

    sql = "select A.word as word, B.prob as pai_prob from emission as A left join start as B  ON A.word = B.word where A.pinyin='%s' order by A.id" % (O[0])
    cursor.execute(sql)

    for (word, pai_prob) in cursor:
        if not pai_prob:
            pai_prob = 0
        pai.append((word, int(pai_prob)))

def gen_eprob(pinyin, e_prob):
    sql = "select word, prob from emission where pinyin='%s' order by id" % (pinyin)
    cursor.execute(sql)

    for(word, prob) in cursor:
        if not prob:
            prob = 0
        e_prob.append((word, int(prob)))

def get_tprob(one, two):
    sql = "select id, prob from trans where one='%s' and two='%s'" % (one, two)
    cursor.execute(sql)

#    if len(cursor) > 1:
#        print 'ERROR: trans find two'

    for (id, prob) in cursor:
        if not prob:
            prob = 0
        return int(prob)

    return 0

def vertbi(O, cursor):
    pai = []
    gen_pai(O, pai, cursor)
    last_v = pai

    v_v = []
    v_n = []

    for i in range(0, len(O)):
        v_v.append([])
        v_n.append([])

    for i in pai:
        vb_value = (i[0], i[1], 0)
        v_v[0].append(vb_value)
        v_n[0].append(i[0])


    for i in range(1, len(O)):
        pinyin = O[i]
        e_prob = []
        gen_eprob(pinyin, e_prob)
        for j in range(0, len(e_prob)):
            max_prob = 0
            max_node = ''
            max_index = 0
            for k in range(0, len(v_v[i-1])):
                t_prob = get_tprob(v_v[i-1][k][0], e_prob[j][0])
                prob = v_v[i-1][k][1] * t_prob
                if prob > max_prob:
                    max_prob = prob
                    max_node = e_prob[j][0]
                    max_index = k
            v_v[i].append((e_prob[j][0], max_prob * e_prob[j][1], max_index))
            v_n[i].append(max_node)

#    pprint.pprint(v_v)


    v_v_last_sorted = sorted(v_v[len(O)-1], cmp=lambda x,y:cmp(x[1], y[1]), reverse=True)

#    pprint.pprint(v_v_last_sorted)

    max_prob = 0
    max_node = ''
    max_index = 0
    result = []

    j = 0
    for k in v_v_last_sorted[:6]:
        result.append([])
        result[j].insert(0, k[0])
        max_index = k[2]
        i = len(O) - 2
        while i >= 0:
            try:
                result[j].insert(0, v_n[i][max_index][0])
                max_index = v_v[i][max_index][2]
            except:
#                print max_index
                pass
            i = i -1
        j = j + 1

    for i in result:
        print ''.join(i)

#    for i in v_v[len(O) - 1]:
#        if i[1] > max_prob:
#            max_prob = i[1]
#            max_node = i[0]
#            max_index = i[2]
##    print 'max_node: %s' % (max_node)
#    result.insert(0, max_node)

#    i = len(O) - 2
#    while i >= 0:
#        try:
#            max_node  = v_n[i][max_index][0]
#            max_index = v_v[i][max_index][2]
#            result.insert(0, max_node)
#        except:
#            print max_index
#        i = i - 1
#
#    print ''.join(result)

def split_pinyin(pinyin, py_arr):
    char_dict = json.loads(open('pinyin_prob.txt', 'r').read())
    pre_char = ''
    start_char = 0
    end_char = 0
    for i in pinyin:
        if pre_char == '':
            pre_char = i
            end_char = end_char + 1
            continue
        else:
            mstr = '%s%s' % (pre_char, i)
            pre_char = i
            if float(char_dict[mstr]) == 0.0:
                py_arr.append(pinyin[start_char:end_char])
                start_char = end_char
                end_char = end_char + 1
            else:
                end_char = end_char + 1
    py_arr.append(pinyin[start_char:])

def split_pinyin2(py_word_dict, pinyin, py_arr):
    last_pos = -2
    while abs(last_pos) < len(pinyin):
        last_py = pinyin[last_pos:]
        if py_word_dict.has_key(last_py) and py_word_dict.has_key(pinyin[0:last_pos]):
            py_arr.append(pinyin[0:last_pos])
            py_arr.append(pinyin[last_pos:])
            return
        else:
            last_pos = last_pos - 1
 

    
if __name__ == '__main__':
    cnx = mysql.connector.connect(user='root', password='xd123', database='sinput')
    cursor = cnx.cursor()
    py_word_dict = json.loads(open('pinyin_word.txt', 'r').read())
    while True:
        final_py = []
        pinyin = raw_input('INPUT: ')
        pinyin = pinyin.strip()
        input_pinyin_arr = pinyin.split(' ')
        for pinyin_str in input_pinyin_arr:
            pinyin_arr = []
            split_pinyin(pinyin_str, pinyin_arr)
            for i in pinyin_arr:
                if not py_word_dict.has_key(i):
                    pinyin_arr2 = []
                    split_pinyin2(py_word_dict, i, pinyin_arr2)
                    final_py.extend(pinyin_arr2)
                else:
                    final_py.append(i)
        print final_py
        vertbi(final_py, cursor)
