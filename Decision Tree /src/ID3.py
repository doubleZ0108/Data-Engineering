# -*- coding: utf-8 -*-

'''
@program: ID3.py
@description:
@author: 1754060 张喆
@create: 2021/01/01 
'''

from math import log
import operator


def calcEntropy(dataset):
    numEntries=len(dataset)
    labelCounts={}
    #给所有可能分类创建字典
    for featVec in dataset:
        currentlabel=featVec[-1]
        if currentlabel not in labelCounts.keys():
            labelCounts[currentlabel]=0
        labelCounts[currentlabel]+=1
    Ent=0.0
    for key in labelCounts:
        p=float(labelCounts[key])/numEntries
        Ent=Ent-p*log(p,2)#以2为底求对数
    return Ent

def splitDataset(dataset,axis,value):
    retdataset=[]#创建返回的数据集列表
    for featVec in dataset:#抽取符合划分特征的值
        if featVec[axis]==value:
            reducedfeatVec=featVec[:axis] #去掉axis特征
            reducedfeatVec.extend(featVec[axis+1:])#将符合条件的特征添加到返回的数据集列表
            retdataset.append(reducedfeatVec)
    return retdataset


def findGainMostFeature(dataset):
    numFeatures=len(dataset[0])-1
    baseEnt=calcEntropy(dataset)
    bestInfoGain=0.0
    bestFeature=-1
    for i in range(numFeatures): #遍历所有特征
        featList=[example[i]for example in dataset]
        uniqueVals=set(featList) #将特征列表创建成为set集合，元素不可重复。创建唯一的分类标签列表
        newEnt=0.0
        for value in uniqueVals:     #计算每种划分方式的信息熵
            subdataset=splitDataset(dataset,i,value)
            p=len(subdataset)/float(len(dataset))
            newEnt+=p*calcEntropy(subdataset)
        infoGain=baseEnt-newEnt
        print(u"ID3中第%d个特征的信息增益为：%.3f"%(i,infoGain))
        if (infoGain>bestInfoGain):
            bestInfoGain=infoGain    #计算最好的信息增益
            bestFeature=i
    return bestFeature

def findMajorityFeature(classList):
    '''
    数据集已经处理了所有属性，但是类标签依然不是唯一的，
    此时我们需要决定如何定义该叶子节点，在这种情况下，我们通常会采用多数表决的方法决定该叶子节点的分类
    '''
    classCont={}
    for vote in classList:
        if vote not in classCont.keys():
            classCont[vote]=0
        classCont[vote]+=1
    sortedClassCont=sorted(classCont.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCont[0][0]


def createID3DecisionTree(dataset,labels):
    classList=[example[-1] for example in dataset]
    if classList.count(classList[0]) == len(classList):
        # 类别完全相同，停止划分
        return classList[0]
    if len(dataset[0]) == 1:
        # 遍历完所有特征时返回出现次数最多的
        return findMajorityFeature(classList)
    bestFeat = findGainMostFeature(dataset)
    bestFeatLabel = labels[bestFeat]
    print(u"此时最优索引为："+(bestFeatLabel))
    ID3Tree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    # 得到列表包括节点所有的属性值
    featValues = [example[bestFeat] for example in dataset]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        ID3Tree[bestFeatLabel][value] = createID3DecisionTree(splitDataset(dataset, bestFeat, value), subLabels)
    return ID3Tree

def classify(inputTree, featLabels, testVec):
    """
    输入：决策树，分类标签，测试数据
    输出：决策结果
    描述：跑决策树
    """
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
