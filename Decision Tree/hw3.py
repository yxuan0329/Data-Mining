# -*- coding: utf-8 -*-
"""
Homework 3 Classification
N26101892 Yun-Hsuan, Liang
"""
import math
import operator


data_table = []
member_class_count = {'Basic' :0, 'Normal':0, 'Silver':0, 'Gold':0} # basic, normal, silver, gold

# label_count = {'S':0, 'M':0, 'less than 1':0, 'more than 1': 0, 'less than 40':0, 'more than 40':0, 'less than 60000': 0, 'more than 60000': 0 }
label_count = {0:0, 1:0, 2:0, 3: 0, 4:0, 5:0, 6: 0, 7: 0 }

leaves = [[]]
leaves_info = [[]]

class node():
    def __init__(self):
        self.data = []
        self.flag = [True, True, True, True]
        self.info = [-1, -1, -1, -1] # 0: left(less than), 1: right(larger than)


def get_data_attribute(file_set):
    file = open(file_set, "r")
    data_attribute = set()
    for line in file:
        attribute = line[1:-2].split(',')
        for each in attribute:
            char = each.split()
            data_attribute.add(char[0])
    return sorted(data_attribute)

def create_data_table(file_set):
    file = open(file_set, "r")
    for line in file:
        data = {}
        for attribute in sorted(data_attribute):
            if int(attribute) == 0:
                data[int(attribute)] = 'S'
            elif int(attribute) == 1:
                data[int(attribute)] = 1
            elif int(attribute) == 2:
                data[int(attribute)] = 'Basic'
            elif int(attribute) == 3:
                data[int(attribute)] = 40
            else:
                data[int(attribute)] = 60000
        data_table.append(data)

def fill_data_table(file_set):
    file = open(file_set, "r")
    i = 0 # i-th data in data-table
    for line in file:
        strings = line[1:-2].split(",")
        for string in strings:
            data = string.split(' ', 1 ) # data[0]= attr_id,   data[1]= attr_content 
            id = int(data[0] )
            if id == 0 or id == 2:
                data_table[i][id] = str(data[1])                
            else:
                data_table[i][id] = int(data[1])
        i += 1 # move on to next row of data

def calc_class_member(data_table):
    for index in member_class_count: # init
        member_class_count[index] = 0
    for data in data_table:
        member_class_count[ data[2]] += 1
    return member_class_count


def calc_label_count(data_table):
    for i in range (0, 8) :
        label_count[i] = 0
    
    for line in data_table:
        if line[0] == 'S' :
            label_count[0] += 1
        else:
            label_count[1] += 1
        if line[1] == 1 :
            label_count[2] += 1
        else:
            label_count[3] += 1
        if line[3] <= 40:
            label_count[4] += 1
        else:
            label_count[5] += 1
        if line[4] <= 60000:
            label_count[6] += 1
        else:
            label_count[7] += 1
    

def calc_information_gain(parent_node):
    total_number = len(parent_node.data)
    entropy = [0] * 4
    min_entropy = 100
    min_entropy_label = -1
    for i in range (0, 4):
        p = label_count[2*i] / total_number
        q= label_count[2*i+1] / total_number
        if p != 0 and q != 0 :
            entropy[i] = - p * math.log(p)/math.log(2) - q * math.log(q)/math.log(2)
        else:
            entropy[i] = 0
        if entropy[i] < min_entropy and parent_node.flag[i] == True:
            min_entropy = entropy[i]
            min_entropy_label = i

    # print(min_entropy, min_entropy_label)
    return min_entropy, min_entropy_label

def split_dataset(parent_node, split_attribute):
    splited_left = []
    splited_right = []
    data_table = parent_node.data.copy()
    
    if split_attribute == 0:
        split_value = ord('S')
    elif split_attribute == 1:
        split_value = 1
    elif split_attribute == 2: # 2->3
        split_attribute += 1
        split_value = 40
    else: # attribute = 3->4
        split_attribute += 1
        split_value = 60000
            
    for data in data_table:
        if split_attribute == 0:
            if ord(data[split_attribute]) > split_value:
                splited_right.append(data)
            else:
                splited_left.append(data)
                
        else :
            if int(data[split_attribute]) > split_value:
                splited_right.append(data)
            else:
                splited_left.append(data)
    if split_attribute > 2 :
        split_attribute -= 1
        
    left_node = node()
    left_node.data = splited_left.copy()
    left_node.flag = parent_node.flag.copy()
    left_node.info = parent_node.info.copy()
    left_node.flag[split_attribute] = False
    left_node.info[split_attribute] = 0
    
    right_node = node()
    right_node.data = splited_right.copy()
    right_node.flag = parent_node.flag.copy()
    right_node.info = parent_node.info.copy()
    right_node.flag[split_attribute] = False
    right_node.info[split_attribute] = 1
    
    return left_node, right_node
    
def same_member_class(data_table) :
    for data in data_table :
        for data_2 in data_table :
            if data[2] != data_2[2]:
                return False
    return True
 
    
def no_more_split(root):
    for i in range(0, 4):
        if root.flag[i] == True :
            return False # there can be more than one split
    return True


def decision_tree(root, tree_level) :   
    if not no_more_split(root) :
        
        calc_label_count(root.data)
        min_entropy, split_attribute = calc_information_gain(root)
        left_node, right_node = split_dataset(root, split_attribute)
        
        #print(tree_level, "left node= ", len(left_node.data), left_node.flag, left_node.info)
        #print(tree_level, "right node=", len(right_node.data), right_node.flag, right_node.info )
        
        if tree_level == 3:
            leaves.append(left_node.data)
            leaves_info.append(left_node.info)
            leaves.append(right_node.data)
            leaves_info.append(right_node.info)
        
        tree_level += 1
        decision_tree(left_node, tree_level)
        decision_tree(right_node, tree_level)        
      
        return leaves

def predict_member_class(file_set):
    correct_predict = 0
    
    file = open(file_set, "r")
    file_output = open("output.txt", "w")
    i = 0 # i-th data in data-table
    for line in file:
        predict_card_class = "Basic"
        card_class = ""
        strings = line[1:-2].split(",")
        
        for string in strings:
            data = string.split(' ', 1 ) # data[0]= attr_id,   data[1]= attr_content 
            id = int(data[0] )
            if id == 1 and int(data[1]) == 1 :
                break
            if id == 3 and int(data[1]) <= 40:
                break
            if id == 2:
                card_class = data[1]
            predict_card_class = "Gold"
            
        output(file_output, strings, predict_card_class)            
        if not card_class or predict_card_class == card_class:
            correct_predict += 1
        i += 1 # move on to next row of data
    accuracy = round(correct_predict / i, 4)
    print("accuracy =", accuracy)
    
    
def output(file_output, strings, predict_card_class):
    output_string = str(strings) +" member card = " + predict_card_class
    print(output_string)
    file_output.write(output_string)
            
if __name__ == '__main__':
    file_training_set = input("Enter the training set file name: (e.g. input.txt)")
    file_testing_set = input("Enter the testing set file name: (e.g. input.txt)")
    
    data_attribute = get_data_attribute(file_training_set)
    create_data_table(file_training_set)
    fill_data_table(file_training_set)
    #print(data_table)
    
    
    root = node()
    root.data = data_table.copy()

    mem_count = [0] * 9
    assign_class = ["class"] * 9
    mem_count[0] = calc_class_member(data_table)
    
    tree_level = 1
    leaves = decision_tree(root, tree_level)
    
    print("Training set decision tree:")
    for i in range (1, 9):
        mem_count[i] = calc_class_member(leaves[i])
        assign_class[i] = max(mem_count[i].items(), key=operator.itemgetter(1) )[0] # define which class to assign
        print("leaf", i, mem_count[i], "predict member=", assign_class[i])
    print("\nTesting set prediction: ")
    create_data_table(file_testing_set)
    fill_data_table(file_testing_set)
    predict_member_class(file_testing_set)
    