import pandas as pd
r = [0 for n in range(32)]


def get_reg_index(reg_name):
    if reg_name[0] == 'r':
        index = int(reg_name[1:])
        return index
    else:
        return int(reg_name)
    


df = pd.read_csv('input_file.txt', header=None, sep=" ")
s = pd.Series([100,200,300])

for i in range(len(df)):
    if df[0][i] == 'addi':
        r[get_reg_index(df[1][i])] = r[get_reg_index(df[2][i])] + get_reg_index(df[3][i])
    elif df[0][i] == 'add':
        r[get_reg_index(df[1][i])] = r[get_reg_index(df[2][i])] + r[get_reg_index(df[3][i])]
    
    print(r)