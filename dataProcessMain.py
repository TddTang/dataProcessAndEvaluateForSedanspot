import pandas as pd
import numpy as np
import glob

# 处理数据符合算法的输入
if __name__ == '__main__':
    tcp = pd.DataFrame(index=[], columns=[])
    files = glob.glob('Data/*')
    for file in files:
        tcp1 = pd.read_csv(file, delim_whitespace=True, header=None)
        tcp = tcp.append(tcp1, ignore_index=True)
    tcp = tcp.iloc[:, [1, 2, 7, 8]]
    tcp.columns = ['date', 'time', 'source', 'destination']
    tcp = tcp[tcp.date != '07/32/1998']
    tcp['date_time'] = tcp['date'] + '/' + tcp['time']
    tcp = tcp.drop('date', axis=1)
    tcp = tcp.drop('time', axis=1)
    tcp['date_time'] = pd.to_datetime(tcp['date_time'], format='%m/%d/%Y/%H:%M:%S')

    initial_time = tcp['date_time'].min()

    tcp['date_time'] = tcp['date_time'] - initial_time
    tcp['hours_past'] = tcp['date_time'].dt.days * 86400 + tcp['date_time'].dt.seconds  # 换成秒
    tcp = tcp.sort_values('hours_past')

    graphs = tcp.loc[:, ['hours_past', 'source', 'destination']]
    graphs['weight'] = 1
    graphs['label'] = '-'
    print(graphs)
    num = 0
    for i, row in graphs.iterrows():
        num += 1
        if num % 10000 == 0:
            print('num: ' + str(num))
        if row['source'] == '-' or row['destination'] == '-':
            row['weight'] = 0
            num -= 1
    print("result: " + str(num))
    graphs.to_csv('./Result/input.csv', sep=',', header=0, index=0)
