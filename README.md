# 介绍
基于论文 SEDANSPOT: Detecting Anomalies in Edge Streams的复现分析  
作者提供了[算法代码](https://github.com/dhivyaeswaran/sedanspot) ，输出结果是对于每一条边的异常分数  
本项目对于[1998 DARPA INTRUSION DETECTION EVALUATION DATASET](http://www.ll.mit.edu/r-d/datasets/1998-darpa-intrusion-detection-evaluation-dataset) 
数据集进行处理得到符合算法的输入，通过作者算法得到输出结果，并对结果进行分析。

# Data文件夹
存放需要处理数据集，这里Data为示例，只放入了一天的数据
# Result文件夹
存放处理数据得到的input和算法输出的output结果
# Evaluate文件夹
存放PR的结果(precision,recall,thresholds)和捕获异常分析结果  
find：实际为异常，算法发现也为异常  
not_find: 实际为异常，算法未发现为异常
# dataProcessMain.py
对于数据处理，输出input.csv
# evaluateMain.py
对于output.csv分析输出PR_result.txt
# analyzeMain.py
根据PR图选择一个合适的threshold进行分析，输出analyze.txt
