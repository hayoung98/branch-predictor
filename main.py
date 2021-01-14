import pandas as pd
import copy
r = [0 for n in range(32)]  # reg
loop_start_pointer = {}  # 存所有label的起始位置 loop+1

BHT = []
init_entry = []

entry_count = input('Enter entries: ')  #  幾個entry

for i in range(int(entry_count)):
    BHT.append([])
    init_entry.append([['00','SN','SN','SN','SN','N']])
# print(BHT)

BHT_pointer = 0



def get_reg_index(reg_name):
    if reg_name[0] == 'r':
        index = int(reg_name[1:])
        return index
    else:
        return int(reg_name)

def bin(l):
    if l == 'T':
        return '1'
    elif l == 'N':
        return '0'

    if l == '00':
        return 0
    elif l == '01':
        return 1
    elif l == '10':
        return 2
    elif l == '11':
        return 3
    
    if l == '1':
        return 'T'
    elif l == '0':
        return 'N'

def state_change(prev_e, r):
    i = bin(prev_e[0])+1  #  如果前一個的2bit history為00，就修改r[1](第一個2BC)
    if prev_e[6] == 'T':
        if prev_e[i] == 'SN':
            r[i] = 'WN'
        elif prev_e[i] == 'WN':
            r[i] = 'WT'
        elif prev_e[i] == 'WT':
            r[i] = 'ST'
    elif prev_e[6] == 'N':
        if prev_e[i] == 'WN':
            r[i] = 'SN'
        elif prev_e[i] == 'WT':
            r[i] = 'WN'
        elif prev_e[i] == 'ST':
            r[i] = 'WT'
    return r    


def taken_or_not(entry, NorT):
    # entry[-1] = 最後一個狀態
    return_entry = copy.deepcopy(entry[-1])
    '''改2bit history'''
    if len(entry) == 1:
        return_entry[0] = '01'
    else:
        return_entry[0] = (bin(entry[-1][6])+bin(entry[-2][6]))

    '''改2BC'''
    return_entry = state_change(entry[-1], return_entry)

    '''改Pred'''
    return_entry[5] = return_entry[bin(return_entry[0])+1][1]

    '''改E'''
    if NorT == 1:
        return_entry[6] = 'T'
    elif NorT == 0:
        return_entry[6] = 'N'
    return return_entry

def write2BHT(result):
    global BHT_pointer
    BHT[BHT_pointer] = result
    BHT_pointer += 1
    if BHT_pointer == int(entry_count):
        BHT_pointer = 0
    


if __name__ == '__main__':
    df = pd.read_csv('input_file.txt', header=None, sep=" ")
    print(df)
    now_pointer = 0
    
    while now_pointer < len(df):
        if df[0][now_pointer] == 'addi':
            r[get_reg_index(df[1][now_pointer])] = r[get_reg_index(df[2][now_pointer])] + get_reg_index(df[3][now_pointer])
        elif df[0][now_pointer] == 'add':
            r[get_reg_index(df[1][now_pointer])] = r[get_reg_index(df[2][now_pointer])] + r[get_reg_index(df[3][now_pointer])]
        elif df[0][now_pointer] == 'mul':
            r[get_reg_index(df[1][now_pointer])] = r[get_reg_index(df[2][now_pointer])] * r[get_reg_index(df[3][now_pointer])]
        elif df[0][now_pointer] == 'div':
            r[get_reg_index(df[1][now_pointer])] = r[get_reg_index(df[2][now_pointer])] / r[get_reg_index(df[3][now_pointer])]
        
        if df[0][now_pointer] != '-' and df[1][now_pointer] == '-':
            loop_start_pointer[df[0][now_pointer]] = now_pointer + 1
            now_pointer += 1            
            continue
        if df[0][now_pointer] == 'beq':
            if r[get_reg_index(df[1][now_pointer])] == r[get_reg_index(df[2][now_pointer])]:
                now_pointer = loop_start_pointer[df[3][now_pointer]]

                '''寫入BHT'''
                if len(init_entry[BHT_pointer][0]) == 6:
                    init_entry[BHT_pointer][0].append('T')
                else:
                    init_entry[BHT_pointer].append(taken_or_not(init_entry[BHT_pointer], 1))
                write2BHT(init_entry[BHT_pointer][-1])

                continue
            else:
                '''寫入BHT'''
                if len(init_entry[BHT_pointer][0]) == 6:
                    init_entry[BHT_pointer][0].append('T')
                else:
                    init_entry[BHT_pointer].append(taken_or_not(init_entry[BHT_pointer], 0))
                write2BHT(init_entry[BHT_pointer][-1])
                
                now_pointer+=1
                continue
        elif df[0][now_pointer] == 'bne':
            if r[get_reg_index(df[1][now_pointer])] != r[get_reg_index(df[2][now_pointer])]:
                now_pointer = loop_start_pointer[df[3][now_pointer]]

                '''寫入BHT'''
                if len(init_entry[BHT_pointer][0]) == 6:
                    init_entry[BHT_pointer][0].append('T')
                else:
                    init_entry[BHT_pointer].append(taken_or_not(init_entry[BHT_pointer], 1))
                write2BHT(init_entry[BHT_pointer][-1])             

                continue
            else:
                '''寫入BHT'''
                if len(init_entry[BHT_pointer][0]) == 6:
                    init_entry[BHT_pointer][0].append('T')
                else:
                    init_entry[BHT_pointer].append(taken_or_not(init_entry[BHT_pointer], 0))
                write2BHT(init_entry[BHT_pointer][-1])

                now_pointer+=1
                continue
        now_pointer += 1
        # print(r)
        # print(BHT)
        print('------------------------------------')
        print('{:>5}'.format('   '), end = '')
        print('{:>5}'.format('2BC'), end = '')
        print('{:>5}'.format('2BC'), end = '')
        print('{:>5}'.format('2BC'), end = '')
        print('{:>5}'.format('2BC'), end = '')
        print('{:>5}'.format('Pred'), end = '')
        print('{:>5}'.format('Exec'))
        for j in range(int(entry_count)):
            for k in range(6):
                try:
                    print('{:>5}'.format(BHT[j][k]), end = '')
                except IndexError:
                    print('{:>5}'.format('-'), end = '')
            try:
                print('{:>5}'.format(BHT[j][6]))
            except IndexError:
                print('{:>5}'.format('-'))

    print('end')