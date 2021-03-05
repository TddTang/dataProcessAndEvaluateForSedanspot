import pandas as pd
import glob

# 分析算法发现的异常
# 根据PR曲线，选取一个合理的threshold进行分析
now_threshold = 0.00400733 

def dataloader():
    tcp = pd.DataFrame(index=[], columns=[])
    files = glob.glob('Data/*')
    for file in files:
        tcp1 = pd.read_csv(file, delim_whitespace=True, header=None)
        tcp = tcp.append(tcp1, ignore_index=True)
    tcp = tcp.iloc[:, [1, 2, 10, 9]]
    tcp.columns = ['date', 'time', 'type', 'anomaly']
    tcp = tcp[tcp.date != '07/32/1998']
    tcp['date_time'] = tcp['date'] + '/' + tcp['time']
    tcp = tcp.drop('date', axis=1)
    tcp = tcp.drop('time', axis=1)
    tcp['date_time'] = pd.to_datetime(tcp['date_time'], format='%m/%d/%Y/%H:%M:%S')

    initial_time = tcp['date_time'].min()

    tcp['date_time'] = tcp['date_time'] - initial_time
    tcp['hours_past'] = tcp['date_time'].dt.days * 86400 + tcp['date_time'].dt.seconds  # 换成秒
    tcp = tcp.sort_values('hours_past')
    print("tcp over")
    output = pd.read_csv('Result/output150.csv', delim_whitespace=True, header=None) # 需要分析的结果
    output.columns = ['score']
    print("output over")
    return tcp, output


if __name__ == '__main__':
    tcp, output = dataloader()
    detected_label = []
    for i, row in output.iterrows():
        if i % 10000 == 0:
            print("detected_label: " + str(i))
        if row['score'] >= now_threshold:
            detected_label.append(1)
        else:
            detected_label.append(0)
    find = []
    not_find = []
    id = 0
    for i, row in tcp.iterrows():
        if id % 10000 == 0:
            print("statistic: " + str(id))
        if row['anomaly'] == 1 and detected_label[id] == 1:
            find.append(row['type'])
        if row['anomaly'] == 1 and detected_label[id] == 0:
            not_find.append(row['type'])
        id += 1

    #  Analyze
    find_big_count = {}
    find_small_count = {}
    big_small = {}
    for i in range(len(find)):
        if i % 100000 == 0:
            print('find_count: ' + str(i))
        str_list = find[i].split(',')
        if len(str_list) == 8:
            big_type = str_list[4]
            small_type = str_list[0]
            if big_type in big_small:
                big_small[big_type].add(small_type)
            else:
                big_small[big_type] = set()
                big_small[big_type].add(small_type)

            if big_type in find_big_count.keys():
                find_big_count[big_type] += 1
            else:
                find_big_count[big_type] = 1
            if small_type in find_small_count.keys():
                find_small_count[small_type] += 1
            else:
                find_small_count[small_type] = 1

    not_find_big_count = {}
    not_find_small_count = {}
    for i in range(len(not_find)):
        if i % 100000 == 0:
            print('not_find_count: ' + str(i))
        str_list = not_find[i].split(',')
        if len(str_list) == 8:
            big_type = str_list[4]
            small_type = str_list[0]
            if big_type in not_find_big_count.keys():
                not_find_big_count[big_type] += 1
            else:
                not_find_big_count[big_type] = 1
            if small_type in not_find_small_count.keys():
                not_find_small_count[small_type] += 1
            else:
                not_find_small_count[small_type] = 1
    file_name = "./Evaluate/analyze_150.txt"
    f = open(file_name, "w")
    print('now threshold = ' + str(now_threshold), file=f)
    print('BIG and SMALL TYPE:', file=f)
    for key in big_small:
        print(key, file=f)
        print(big_small[key], file=f)
    print('---------------------------------------------', file=f)
    print('BIG TYPE:', file=f)
    print('FIND:', file=f)
    print(find_big_count, file=f)
    print('NOT FIND:', file=f)
    print(not_find_big_count, file=f)
    print('---------------------------------------------', file=f)
    print('SMALL TYPE:', file=f)
    for key in find_small_count:
        find_num = find_small_count[key]
        not_find_num = 0
        if key in not_find_small_count.keys():
            not_find_num = not_find_small_count[key]
        print(key + ' [find: ' + str(find_num) + ' , not_find: ' + str(not_find_num) + ' ]', file=f)
    f.close()

