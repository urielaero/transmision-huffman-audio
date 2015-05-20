def get_clear_data(val=-1,y=4,x=512):
    return [ [-1 for j in range(y)]  for i in range(x)]

def set_frequency(table,data):
    for i in range(len(table)):
        table[i][0] = data.count(i)

def get_min(table,nos=-2):
    pivo = -1
    for i in range(len(table)):
        if i != nos:
            if pivo == -1 and table[i][0] != 0 and table[i][1] == -1:
                pivo = i
            elif table[i][0] <= table[pivo][0] and table[i][0]!=0 and table[i][1] == -1:
                pivo = i
    
    return pivo

def get_mins(table):
    r1 = get_min(table)
    r2 = get_min(table,r1)
    return r1,r2

def make_tree(t):
    table = [r[:] for r in t]
    for i in range(256,len(table)):
        if table[i][1] == -1 and table[i][2] == -1 and table[i][3] == -1 and table[i][0] == 0:
            min1,min2 = get_mins(table)
            if min1 != -1 and min2 != -1:
                table[i][2] = min1
                table[min1][1] = i
                table[i][0] = table[min1][0]

                table[i][3] = min2
                table[min2][1] = i
                table[i][0] += table[min2][0]
            else:
                return min1,table

def codifica_s(table,sm,buff):
    p = table[sm][1]

    if p == -1:
        return buff

    if table[p][2] == sm:
        buff += '1'
    else:
        buff += '0'

    return codifica_s(table,p,buff)

def printFrecuency(table):
    for i in range(len(table)):
        if table[i][1] > 0:
            print i,table[i][0]

def codifica(table,data):
    s = []
    for d in data:
        cod = codifica_s(table,d,'')
        s.append(cod)
    return s

def decode_s(table,raiz,byte):
    bs = byte[::-1]
    for i in bs:
        intd = int(i)
        if intd == 0:
            raiz = table[raiz][3]
        else:
            raiz = table[raiz][2]
        if raiz < 255:
            return raiz


def decode(table,data):#data list
    size = len(table)
    raiz = size-1
    for i in range(size-2,-1,-1):
        if table[i][0] > table[raiz][0]:
            raiz = i

    s = []
    for d in data:
        cod = decode_s(table,raiz,d)
        s.append(cod)
    return s

def decode_string(table,raiz,data):#data string

    root = raiz
    res = []
    data = data[::-1]
    val = []
    for i in data:
        intd = int(i)
        if intd == 0:
            raiz = table[raiz][3]
        else:
            raiz = table[raiz][2]
        if raiz <= 255:
            res.append(raiz)
            raiz = root
    
    return res[::-1]

def make_hist(d):
    table = get_clear_data()
    set_frequency(table,d)
    return table    

def codifica_data(d):#no usar este 
    if type(d) == bytearray:
        d = list(d)
    table = make_hist(d)
    raiz,tree = make_tree(table)
    cod = codifica(tree,d)
    #print cod
    return tree,cod

def decodifica_data(table,com):
    return decode(table,com)
       

def compress(tree,data):#se debe llamar antes a make_tree
    if type(data) == bytearray:
        data = list(data)
    #raiz,tree = make_tree(table)
    huff = codifica(tree,data)
    sthuff = ''.join(huff)
    return sthuff

def decompress(tree,raiz,data):#se debe tener antes el tree
    return decode_string(tree,raiz,data)

if __name__ == '__main__':
    data = [0,2,2,1,1,1,5,5,5,5,5,5,5,5]
    #data = bytearray('abcdef')
    #data = [0,255,25,1,1,2,3,4,4,4,4,5,6,4,4,8,1,2,3,3]
    com = compress(data)
    #print data
    #print com
    #print decompress(table,com)
    #decompress(table,com)

