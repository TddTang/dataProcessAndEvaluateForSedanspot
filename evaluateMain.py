import pandas as pd
import glob
from sklearn.metrics import precision_recall_curve, auc
import matplotlib.pyplot as plt


# 评估算法的准确性

def dataloader():
    tcp = pd.DataFrame(index=[], columns=[])
    files = glob.glob('Data/*')
    for file in files:
        tcp1 = pd.read_csv(file, delim_whitespace=True, header=None)
        tcp = tcp.append(tcp1, ignore_index=True)
    tcp = tcp.iloc[:, [1, 2, 7, 8, 9]]
    tcp.columns = ['date', 'time', 'source', 'destination', 'anomaly']
    tcp = tcp[tcp.date != '07/32/1998']
    tcp['date_time'] = tcp['date'] + '/' + tcp['time']
    tcp = tcp.drop('date', axis=1)
    tcp = tcp.drop('time', axis=1)
    tcp['date_time'] = pd.to_datetime(tcp['date_time'], format='%m/%d/%Y/%H:%M:%S')

    # calculate how many hours passed since the initial time
    initial_time = tcp['date_time'].min()

    tcp['date_time'] = tcp['date_time'] - initial_time
    tcp['hours_past'] = tcp['date_time'].dt.days * 86400 + tcp['date_time'].dt.seconds  # 换成秒
    tcp = tcp.sort_values('hours_past')
    df = pd.read_csv('./Result/output150.csv', delim_whitespace=True, header=None)  # 选择需要分析的结果
    df.columns = ['score']
    return tcp, df


if __name__ == '__main__':
    tcp, df = dataloader()
    print(tcp)
    truth = []
    detected = []
    num = 0
    for i, row in tcp.iterrows():
        num += 1
        if num % 10000 == 0:
            print('truth: ' + str(num))
        if row['source'] != '-' and row['destination'] != '-':
            truth.append(int(row['anomaly']))
    #
    # df = pd.read_csv('./Result/output100.csv', delim_whitespace=True, header=None)
    # df.columns = ['score']
    num = 0
    for i, row in df.iterrows():
        num += 1
        if num % 10000 == 0:
            print('detected: ' + str(num))
        detected.append(float(row['score']))

    precision, recall, thresholds = precision_recall_curve(truth, detected)

    # print(len(precision))
    # print(len(recall))
    # print(len(thresholds))
    f = open("./Evaluate/PR_result_150.txt", "w")  # 结果存储的地方
    print('precision' + '            recall              ' + 'thresholds', file=f)
    for i in range(len(thresholds)):
        print(str(precision[i]) + '     ' + str(recall[i]) + '      ' + str(thresholds[i]), file=f)
    f.close()

    print('Area Under Curve:', auc(recall, precision))
    plt.xlabel("recall")
    plt.ylabel("precision")
    plt.figure(1)
    plt.plot(recall, precision)
    plt.show()
