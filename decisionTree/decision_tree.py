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

def create_dataSet(file_path):
    # dataSet = [
    # [1,1,0, 'L1'],
    # [1,2,0, 'L1'],
    # [3,2,0, 'L1'],
    # [1,1,10, 'L2'],
    # [1,2,10, 'L2'],
    # [3,2,10, 'L2'],
    # [-1, -1, 0, 'L3'],
    # [-1, -2, 0, 'L3'],
    # [-1, -3, 0, 'L3'],
    # [-1, -1, 10, 'L4'],
    # [-1, -2, 10, 'L4'],
    # [-1, -3, 10, 'L4'],
    # ]
    # labels = ['haa1', 'haa2', 'haa3']
    dataSet = []
    labels = []
    fr = open(file_path, 'r')
    for line in open(file_path):
        line = fr.readline()
        if line.strip() == "label":
            line = fr.readline()
            labels = line.strip().split("\t")
            break
        data = line.strip().split("\t")
        for i in range(len(data) - 1):
            data[i] = float(data[i])
        dataSet.append(data)
    return dataSet, labels

def train_data(file_train_path):
    dataSet, labels = create_dataSet(file_train_path)
    result_tree = build_decision_tree(dataSet, labels[:])
    print "train over..."
    return result_tree, labels

def test_data(file_test_path, decision_tree, label_list):
    dataSet, labels = create_dataSet(file_test_path)
    for data in dataSet:
        temp_tree = decision_tree
        print data
        while True:
            if type(temp_tree) is not dict:
                print temp_tree
                break
            flag = True
            for key in temp_tree.keys():
                #go on find
                for key2 in temp_tree[key].keys():
                    if float(key2) == float(data[getIndex(key, label_list)]):
                        temp_tree = temp_tree[key][key2]
                        flag = False
                        break
            if flag == True:
                print "canot solve..."
                break
    print "test voer..."
def getIndex(label_str, labels):
    for i in range(len(labels)):
        if str(label_str) == str(labels[i]):
            return i
    return -1;



if __name__ == "__main__":
    file_train_path = 'train-decision-tree.txt'
    decision_tree, labels = train_data(file_train_path)
    file_test_path = 'test-decision-tree.txt'
    test_data(file_test_path, decision_tree, labels)