# -*- coding: utf-8 -*-

'''
@program: util.py
@descript: 工具方法
@author: 软件学院 1754060 张喆
@create: 2021/01/01 
'''

import csv


def labelMapper(label):
    if label == '年龄段':
        return 'age'
    elif label == '有工作':
        return 'job'
    elif label == '有自己的房子':
        return 'house'
    elif label == '信贷情况':
        return 'loan'
    elif label == '类别(是否给贷款)':
        return 'type'


def dataMapper(item):
    return (0 if item in ['否', '青年', '一般'] else 1 if item in ['是', '中年', '好'] else 2)


def readData(filename):
    '''
    读取数据并进行格式转化
    :param filename: 数据集文件名
    :return: 数据集(格式转化后)，标签名(格式转化后)
    '''
    with open(filename, 'r', encoding='UTF-8-sig') as f:
        reader = csv.reader(f)

        labels, dataset = [], []

        for row in reader:
            if row[0] == 'ID':
                labels = list(map(labelMapper, row[1:]))
            else:
                pass
                rawData = row[1:]
                dataset.append(list(map(dataMapper, rawData)))
        return dataset, labels
