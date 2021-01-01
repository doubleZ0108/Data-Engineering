# -*- coding: utf-8 -*-

'''
@program: main.py
@description:
@author: 1754060 张喆
@create: 2021/01/01 
'''

import src.ID3 as ID3
import src.util as util
import src.TreePlotter as TreePlotter

if __name__ == "__main__":
    filename = "../data/data.csv"
    dataset, labels = util.readData(filename)

    entropy = ID3.calcEntropy(dataset)

    ID3DesicionTree = ID3.createID3DecisionTree(dataset, labels[:])    # 拷贝，createTree会改变labels
    print('ID3DesicionTree:\n', ID3DesicionTree)

    TreePlotter.plotID3DecisionTree(ID3DesicionTree)

    testData = ['中年', '否', '否', '一般']
    result = ID3.classify(ID3DesicionTree, labels, testData)
    print(result)