# -*- coding: utf-8 -*-

'''
@program: ID3.py
@description: ID3核心算法
@author: 软件学院 1754060 张喆
@create: 2021/01/01 
'''

from math import log
import operator


def calcEntropy(dataset):
    '''
    计算信息熵 entropy(S) = -\sum_{i=1}^{n}(p_i * log_2p_i)
    :param dataset: 数据集(子集)
    :return: 信息熵
    '''
    numEntries = len(dataset)
    labelCounts = {}    # 给所有可能分类创建字典
    for featVec in dataset:
        currentlabel = featVec[-1]
        if currentlabel not in labelCounts.keys():
            labelCounts[currentlabel] = 0
        labelCounts[currentlabel] += 1

    Ent = 0.0
    for key in labelCounts:
        p = float(labelCounts[key]) / numEntries
        Ent = Ent - p * log(p, 2)
    return Ent


def splitDataset(dataset, axis, value):
    '''
    划分数据集
    :param dataset: 数据集(子集)
    :param axis: 属性值
    :param value: 特征值
    :return: 划分后的数据集合
    '''
    retdataset = []
    for featVec in dataset:  # 抽取符合划分特征的值
        if featVec[axis] == value:
            reducedfeatVec = featVec[:axis]  # 去掉axis特征
            reducedfeatVec.extend(featVec[axis + 1:])  # 将符合条件的特征添加到返回的数据集列表
            retdataset.append(reducedfeatVec)
    return retdataset


def findGainMostFeature(dataset):
    '''
    寻找信息增益最大的特征
    :param dataset: 数据集(子集)
    :return: 信息增益最大对应的特征
    '''
    numFeatures = len(dataset[0]) - 1
    baseEnt = calcEntropy(dataset)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):  # 遍历所有特征
        featList = [example[i] for example in dataset]
        uniqueVals = set(featList)  # 将特征列表创建成为set集合，元素不可重复。创建唯一的分类标签列表
        newEnt = 0.0
        for value in uniqueVals:  # 计算每种划分方式的信息熵
            subdataset = splitDataset(dataset, i, value)
            p = len(subdataset) / float(len(dataset))
            newEnt += p * calcEntropy(subdataset)
        infoGain = baseEnt - newEnt
        print(u"ID3中第%d个特征的信息增益为: %.3f" % (i, infoGain))
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain  # 计算最好的信息增益
            bestFeature = i
    return bestFeature


def findMajorityFeature(classList):
    '''
    选取出现最多的类型作为叶节点的类型
    没有剩余属性可以用来进一步划分样本，此时该节点作为叶子
    :param classList: 待选取属性
    :return: 出现最多的类型
    '''
    classCont = {}
    for vote in classList:
        if vote not in classCont.keys():
            classCont[vote] = 0
        classCont[vote] += 1
    sortedClassCont = sorted(classCont.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCont[0][0]


def createID3DecisionTree(dataset, labels):
    '''
    构建ID3决策树
    :param dataset: 原始数据列表
    :param labels: 类比标签列表
    :return: 字典表示的ID3决策树
    '''
    classList = [example[-1] for example in dataset]
    if classList.count(classList[0]) == len(classList):
        # 类别完全相同，停止划分
        return classList[0]
    if len(dataset[0]) == 1:
        # 遍历完所有特征时返回出现次数最多的
        return findMajorityFeature(classList)
    bestFeat = findGainMostFeature(dataset)
    bestFeatLabel = labels[bestFeat]
    print(u"此时最优索引为: %s\n" % (bestFeatLabel))
    ID3Tree = {bestFeatLabel: {}}
    del (labels[bestFeat])
    # 得到列表包括节点所有的属性值
    featValues = [example[bestFeat] for example in dataset]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        ID3Tree[bestFeatLabel][value] = createID3DecisionTree(splitDataset(dataset, bestFeat, value), subLabels)
    return ID3Tree


def classify(inputTree, featLabels, testVec):
    '''
    对测试样本进行分类
    :param inputTree: 决策树
    :param featLabels: 分类标签列表
    :param testVec: 测试数据
    :return: 分类结果
    '''
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    classLabel = '0'
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel
