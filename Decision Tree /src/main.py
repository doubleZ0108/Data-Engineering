# -*- coding: utf-8 -*-

'''
@program: main.py
@description: ID3算法演示主函数
@author: 软件学院 1754060 张喆
@create: 2021/01/01 
'''

import ID3 as ID3
import util as util
import TreePlotter as TreePlotter

if __name__ == "__main__":
    ''' 读取数据 '''
    filename = "../data/data.csv"
    dataset, labels = util.readData(filename)

    ''' 构建ID3决策树 '''
    ID3DesicionTree = ID3.createID3DecisionTree(dataset, labels[:])  # 拷贝，createTree会改变labels
    print('ID3DesicionTree:\n', ID3DesicionTree)

    ''' 绘制ID3决策树 '''
    TreePlotter.plotID3DecisionTree(ID3DesicionTree)

    ''' 测试 '''
    # 年龄段 有工作 有自己的房子 信贷情况
    testData = ['中年', '否', '否', '一般']       # 测试结果为: 不给贷款
    # testData = ['老年', '是', '否', '非常好']   # 测试结果为: 给贷款
    # testData = ['中年', '否', '是', '一般']     # 测试结果为: 给贷款
    # testData = ['青年', '是', '是', '好']       # 测试结果为: 给贷款
    testData = list(map(util.dataMapper, testData))
    result = ID3.classify(ID3DesicionTree, labels, testData)
    print("\n测试结果为: %s" % ('不给贷款' if int(result) == 0 else '给贷款'))
