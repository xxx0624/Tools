#__author__ = 'xing'
#coding=utf-8

import operator
import time
from math import log

#获取dataset标签
def get_label(dataSet):
    label_list = []
    for data in dataSet:
        label_list.append(data[-1])
    return label_list

#获取dataset的标签以及统计标签的频次
def count_label(dataSet):
    label_count = {}
    for data in dataSet:
        c = data[-1]
        if c not in label_count:
            label_count[c] = 1
        else:
            label_count[c] += 1
    return label_count

#计算香农熵
def calculate_ShannonEntropy(dataSet):
    label_count = count_label(dataSet)
    shannon_entropy = 0.0
    dataSet_size = len(dataSet)
    for label in label_count:
        temp_p = float(label_count[label]) / dataSet_size
        shannon_entropy -= temp_p * log(temp_p, 2)
    return shannon_entropy

#去除某属性数据
def generate_new_dataSet(dataSet, columnID, value):
    new_dataSet = []
    for data in dataSet:
        if data[columnID] == value:
            new_data = data[:columnID] + data[1+columnID:]
            new_dataSet.append(new_data)
    return new_dataSet

#选择最好的属性
def chooseBestFeature(dataSet):
    num_features = len(dataSet[0]) - 1
    base_shannon_entropy = calculate_ShannonEntropy(dataSet)
    #print base_shannon_entropy
    best_info_gain = 0
    best_feature = -1
    for columnID in range(num_features):
        column_feature = [data[columnID] for data in dataSet]
        unique_column_feature = set(column_feature)
        current_entropy = 0.0
        for single_column_feature in unique_column_feature:
            sub_dataSet = generate_new_dataSet(dataSet, columnID, single_column_feature)
            current_entropy += float(len(sub_dataSet)) / float(len(dataSet)) * calculate_ShannonEntropy(sub_dataSet)
        current_info_gain = base_shannon_entropy - current_entropy
        if current_info_gain > best_info_gain:
            best_info_gain = current_info_gain
            best_feature = columnID
    return best_feature

def most_label(label_list):
    label_count = {}
    for c in label_list:
        if c not in label_count.keys():
            label_count[c] = 1
        else:
            label_count[c] += 1
    label_count = sorted(label_count.iteritems(), key=operator.itemgetter(1), reverse=True)
    return label_count[0][0]

def build_decision_tree(dataSet, labels):
    label_list = [data[-1] for data in dataSet]
    if label_list.count(label_list[0]) == len(label_list):
        return label_list[0]
    if len(dataSet[0]) == 1:
        return most_label(label_list)
    best_feature_index = chooseBestFeature(dataSet)
    best_feature_label = labels[best_feature_index]
    result_tree = {best_feature_label:{}}
    del(labels[best_feature_index])
    best_feature_values = [data[best_feature_index] for data in dataSet]
    unique_best_feature_values = set(best_feature_values)
    for v in unique_best_feature_values:
        sub_labels = labels[:]
        result_tree[best_feature_label][v] = build_decision_tree(generate_new_dataSet(dataSet, best_feature_index, v), sub_labels)
    return result_tree

def create_dataSet():
    # dataSet=[[1,1,'yes'],
    #         [1,1,'yes'],
    #         [1,0,'no'],
    #         [0,1,'no'],
    #         [0,1,'no']]
    # labels = ['no surfaceing','flippers']
    dataSet = [
    [1,1,0, 'L1'],
    [1,2,0, 'L1'],
    [3,2,0, 'L1'],
    [1,1,10, 'L2'],
    [1,2,10, 'L2'],
    [3,2,10, 'L2'],
    [-1, -1, 0, 'L3'],
    [-1, -2, 0, 'L3'],
    [-1, -3, 0, 'L3'],
    [-1, -1, 10, 'L4'],
    [-1, -2, 10, 'L4'],
    [-1, -3, 10, 'L4'],
    ]
    labels = ['ha1', 'ha2', 'ha3']
    return dataSet, labels

def run():
    dataSet, labels = create_dataSet()
    result_tree = build_decision_tree(dataSet, labels)
    print result_tree
    print "over..."

if __name__ == "__main__":
    run()