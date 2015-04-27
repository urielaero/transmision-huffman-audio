# -*- coding: utf-8 -*-

import numpy as np
np.set_printoptions(threshold=np.nan)

NULL = -1

def get_probability(hist, tam):
    prob = np.zeros_like(hist, dtype=float)

    for i in range(len(hist)):
        if hist[i] > 0:
            prob[i] = hist[i] / float(tam)

    return prob

def return_non_zero(table, length=255):
    for i in range(length):
        if table[1][i] != 0 and table[2][i] == -1:
            return table[1][i], i

    return NULL, NULL

def initialize_table(table):
    for i in range(len(table[0])):
        table[2] = NULL
        table[3] = NULL
        table[4] = NULL

def put_simbols(table):
    for i in range(len(table[0])):
        table[0][i] = i

def put_histogram(dat, table, length=255):
    for i in range(length):
        for j in range(len(dat)):
            if i == dat[j]:
                table[1][i] += 1

def get_min_symbol(table, parent, length=255):
    pivot, index = return_non_zero(table, length)

    if pivot == NULL: return NULL, 0

    for i in range(1, length):
        if table[1][i] and table[1][i] < pivot and table[2][i] == -1: 
            pivot = table[1][i]
            index = i

    table[2][index] = parent

    return index, pivot

def get_node(table):
    total_frequency = sum(table[1][:255])

    for i in range(len(table[0])-1, -1, -1):
        if table[1][i] == total_frequency:
            return table[0][i]

def generate_tree(table):
    total_frequency = sum(table[1][:])

    # children's part
    for i in range(256, 512):
        pos1, val1 = get_min_symbol(table, i)
        pos2, val2 = get_min_symbol(table, i)

        if pos1 == -1 and pos2 == -1: break

        table[1][i] = val1 + val2
        table[3][i] = pos1
        table[4][i] = pos2

    # parent's part
    for j in range(i, 512):
        pos1, val1 = get_min_symbol(table, j, 512)
        pos2, val2 = get_min_symbol(table, j, 512)

        table[1][j] = val1 + val2
        table[3][j] = pos1
        table[4][j] = pos2

        if table[1][j] == total_frequency: break

def generate_table(dat):
    table = np.zeros((5, 512))

    initialize_table(table)

    put_simbols(table)
    put_histogram(dat, table)

    return table, table[1][:]

def codifying_symbols(table, sym, bits):
    if table[1][sym] == sum(table[1][:255]):
        return bits

    parent = table[2][sym]

    if table[3][parent] == sym: bits.append(0) # left
    else: bits.append(1) # right

    return codifying_symbols(table, parent, bits)

def decodifying_symbols(table, bits):
    node = get_node(table)

    for i in bits:
        if int(i) == 0: 
            node = table[3][node]
        else: 
            node = table[4][node]

    return table[0][node]


def decodified_dat(table, bits):
    dat_symbols = []

    for bit in bits:
        dat_symbols.append(decodifying_symbols(table, bit[::-1]))

    return dat_symbols

def codified_dat(table, dat):
    dat_bits = []

    for i in dat:
        dat_bits.append(''.join(str(x) for x in codifying_symbols(table, i, [])))

    return dat_bits

if __name__ == '__main__':
    dat = [1,1,2,3,4,4,4,4,5,6,4,4,8,1,2,3,3]

    table, hist = generate_table(dat)
    generate_tree(table)

    dat_bits = codified_dat(table, dat)
    dat_symbols = decodified_dat(table, dat_bits)

    print dat_symbols

    print table.T
