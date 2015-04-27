def get_clear_data():
    return [ [-1 for j in range(4)]  for i in range(512)]

def set_frequency(table,data):
    for i in range(len(table)):
        table[i][0] = data.count(i)
        #if table[i][1] > 0:
            #print i,table[i][1]
    #print '--------'

def get_pivote(table,pivo=-1):
    for i in range(len(table)):
        if table[i][0] != 0 and i != pivo and table[i][1] == -1:
            return i

    return -1

def get_mins(table):
    indexMin = get_pivote(table)
    indexMin2 = get_pivote(table,indexMin)
    #print 'puvos', indexMin,indexMin2
    for i in range(len(table)):
        if indexMin!=i and table[i][0] != 0 and table[i][1] == -1 and table[i][0] <= table[indexMin][0]:
            #print 'asdasd'
            indexMin2 = indexMin
            indexMin = i

        """
        if table[i][2] == -1 and table[i][1] != 0:

            if table[indexMin][1] == 0 or table[i][1] <= table[indexMin][1]:
                print '-->',indexMin,indexMin2,i
                indexMin2 = indexMin
                indexMin = i 

            elif indexMin2 == -1:
                indexMin2 = i
        """
    #print '------'
    #printFrecuency(table)
    #print indexMin,indexMin2
    return indexMin,indexMin2


def make_tree(table):
    for i in range(256,len(table)):
        if table[i][1] == -1 and table[i][2] == -1 and table[i][3] == -1 and table[i][0] == 0:
            min1,min2 = get_mins(table)
            if min1 != -1 and min2 != -1:
                table[i][2] = min1
                table[min1][1] = i
                table[i][0] = table[min1][0]

                #min2,min1 = get_mins(table)
                #if min2 != -1:
                table[i][3] = min2
                table[min2][1] = i
                table[i][0] += table[min2][0]

def codifica_s(table,sm,buff):
    p = table[sm][1]

    if p == -1:
        return buff[::-1]

    if table[p][2] == sm:
        #0 hijo
        buff += '0'
    else:
        buff += '1'

    return codifica_s(table,p,buff)

def printFrecuency(table):
    for i in range(len(table)):
        if table[i][1] > 0:
            print i,table[i][0]

def codifica(table,data):
    s = []
    for d in data:
        cod = codifica_s(table,d,'')
        #print 'c',cod
        s.append(cod)
    return s

def decodifying_b(raiz,table,b,index):
    if index > -1:
        intd = int(b[index])
    else:
        intd = 0

    #print 'raiz',raiz,'b',b,'index',index,'intd',intd

    if intd == 1:
        raiz = table[raiz][3]
    else:
        raiz = table[raiz][2]

    if raiz < 256:
        return raiz

    return decodifying_b(raiz,table,b,index-1)

def decodifying_b2(raiz,table,bs,index):
    #bs = str(b)[::-1]
    #print 'bs',bs,'raiz',raiz
    for i in bs:
        intd = int(i)
        if intd == 0:
            #print 'pasoo'
            raiz = table[raiz][2]
        else:
            raiz = table[raiz][3]

    return raiz

def compress(d):
    if type(d) == bytearray:
        d = list(d)
    table = get_clear_data()
    set_frequency(table,d)
    #print 't',table
    make_tree(table)

    #print table
    return table,codifica(table,d)


def decompress(table,com):
    #raiz
    size = len(table)
    piv = size-1
    for i in range(size-2,-1,-1):
        if table[i][0] > table[piv][0]:
            piv = i

    raiz = piv
    s = []
    for b in com:
        bs = str(b)
        sm = decodifying_b2(raiz,table,bs,len(bs)-1)
        s.append(sm)

    #print s
    return s
    #for i in com:
        

if __name__ == '__main__':
    data = [0,2,2,1,1,1,5,5,5,5,5,5,5,5]
    #data = [0,255,25,1,1,2,3,4,4,4,4,5,6,4,4,8,1,2,3,3]
    table,com = compress(data)
    print data
    print com
    decompress(table,com)

