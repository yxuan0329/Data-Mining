# -*- coding: utf-8 -*-
"""
Homework 2 Sequential Pattern Mining
@author: Yun-Hsuan, Liang
"""
from itertools import combinations

candidate_data = [[]]
candidate_data_count = [[]]
freq_pattern_data = [[]]
freq_pattern_data_count = [[]]
freq_pattern_filter = []


def load_transaction_data(file_name):
    transaction = []
    with open(file_name, 'r') as file:
        for lines in file:
            data_line = lines.split()
            global_set = {}
            classify_data_by_time(global_set, data_line)
            
            tmp = []
            for value in global_set.values():
                tmp.append(value)
            transaction.append(tmp)
    file.close()
    return transaction
    
def classify_data_by_time(global_set, data_line):
    for i in range (1, len(data_line), 2):
        if not data_line[i] in global_set:
            global_set[data_line[i]] = []
        global_set[data_line[i]].append(data_line[i+1])
        

def find_subsets(input_set):
    x = len(input_set)
    subsets = []
    for i in range (1, x+1):
        tmp = combinations(input_set, i)
        for s in tmp:
            subsets.append(list(s))
    return subsets

def find_l1_freq_pattern(transaction, min_supp):
    candidate_data.append([])
    candidate_data_count.append([])
    candidate_dict = {}
    freq_pattern_data.append([])
    freq_pattern_data_count.append([])
    
    for line in transaction:
        length_1_seq_pattern = set()
        for sets in line:
            for data in sets:
                str_data = str(data)
                length_1_seq_pattern.add(str_data)
                
        # candidate_dict = length_1_seq_count(length_1_seq_pattern, candidate_data_count, candidate_dict)
        for str_data in length_1_seq_pattern:
            if str_data in candidate_dict:
                candidate_dict[ str_data ] += 1
            else : # not in the dict, then create
                candidate_dict[ str_data ] = 1

    compare_min_supp(candidate_dict, min_supp)
    return candidate_data_count


def compare_min_supp(candidate_dict, min_supp):
    for key,value in candidate_dict.items():
        if value >= min_supp:
            freq_pattern_data[1].append( [str_to_list(key)] )
            freq_pattern_data_count[1].append(value)
        else : # not larger than min-supp
            freq_pattern_filter.append( [str_to_list(key)] )

    
def str_to_list(string):
    return list(string[2:-2].split("', '"))

def filtered(transaction, candidate_data_count):
    filtered_transaction = []
    for line in transaction:
        exist = False # initialize
        for sets in line:
            for data in sets:
                for fp_data in freq_pattern_data[1]:
                    if data == fp_data[0]:
                        exist = True
                        break
                        # goto end
                if exist == True:
                    break
            if exist == True:
                break
            
        # label: end
        if exist == True:
            filtered_transaction.append(line)
            
    return filtered_transaction

def find_candidate(transaction, dim, candidate_data, candidate_data_count):
    candidate_data.append([])
    candidate_data_count.append([])
  
    for x in freq_pattern_data[dim-1]:
        for y in freq_pattern_data[dim-1]:
            if x[:-1] == y[:-1]:
                tmp = x.copy()
                tmp.append(y[-1])
                candidate_data[dim].append(tmp)
                candidate_data_count[dim].append(0)
    # print( len(candidate_data[dim]), dim )        
    for data in range(0, len(candidate_data[dim])):
        for each_transaction in transaction:
            ret = matched_pattern(each_transaction, candidate_data[dim][data])
            candidate_data_count[dim][data] += ret

def matched_pattern(each_transaction, candidate_pattern_data):
    each_transaction_length = len(each_transaction)
    candidate_pattern_data_length = len(candidate_pattern_data)
    
    # compare data length
    if each_transaction_length >= candidate_pattern_data_length:
        i = 0
        for x in each_transaction :
            if candidate_pattern_data[i] in x:
                i += 1
                if i == candidate_pattern_data_length:
                    return 1
    return 0

def find_freq_pattern(dim, transaction, min_supp, candidate_data, candidate_data_count):
    freq_pattern_data.append([])
    freq_pattern_data_count.append([])

    for i in range (0, len(candidate_data_count[dim]) ):
        if candidate_data_count[dim][i] >= min_supp:
            freq_pattern_data[dim].append(candidate_data[dim][i])
            freq_pattern_data_count[dim].append(candidate_data_count[dim][i])
    
                    
def output(min_supp): # print and write to file
    print("The minimum support you entered is", min_supp)
    print()
    file_output = open("output.txt", "w")
    for i in range(0, len(freq_pattern_data)):
        for j in range(0, len(freq_pattern_data[i])):
            print(str(freq_pattern_data[i][j]),' support=', freq_pattern_data_count[i][j] )
            file_output.write( str(freq_pattern_data[i][j]) + ' support=' + str(freq_pattern_data_count[i][j]) + '\n')
    file_output.close()


if __name__ == '__main__':
    input_file_name = input('Enter the file name(e.g. test.txt):')
    min_supp = int (input('Enter the minimum support:'))
    transaction = load_transaction_data(input_file_name)
    # transaction = load_transaction_data("seqData.dat.txt")
    # min_supp = 200
    
    for row in range (0, len(transaction)):
        for col in range (0,len(transaction[row]) ):
            transaction[row][col] = find_subsets(transaction[row][col])
            
    candidate_data_count = find_l1_freq_pattern(transaction, min_supp) 
    filtered_transaction = filtered(transaction, candidate_data_count) # filtered unexist data
    
    dim = int(1)  
    while not freq_pattern_data[dim] == []:
        find_candidate(transaction, dim, candidate_data, candidate_data_count)
        find_freq_pattern(dim, transaction, min_supp, candidate_data, candidate_data_count)
        dim += 1
        
    output(min_supp)

