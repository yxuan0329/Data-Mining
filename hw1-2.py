# -*- coding: utf-8 -*-
"""
homework 1: Association rules with Apriori algo.
@author: Yun-Hsuan N26101892
"""

from itertools import combinations
from collections import defaultdict

transaction_length = 0
item_count = defaultdict()
index_map = dict()
subsets = set()
new_subsets = set()
all_item_count = defaultdict()
supp_numerator = 0.000 # 分子 = global_set
supp_denumerator = 0.000 # 分母


def load_transaction_data(file_name):
    transaction = []
    with open(file_name, 'r') as file:
        for lines in file:
            transaction.append(set(lines.split()))
        # items = pd.unique(transaction.values.ravel()) # total number of items
    transaction_length = len(transaction)
    return transaction, transaction_length


def freq_count(transaction, min_supp):
    global_set = set()
    for item in transaction:
        global_set = add_to_set(item, global_set) # 扣除重複的數之外，所有item 集合
    iteration = 1
    subsets = generate_combination_set(global_set, 1)
    
    while len(subsets) >= 2:
        check_subset(transaction, subsets) # 每個子集合在transaction中的出現次數，以dict紀錄
        compare_min_supp(item_count, index_map, min_supp)
        # print("item_count=", item_count, type(item_count))
        # print("index_map=",index_map, type(index_map))
        # print("global set=", global_set)
        
        # add each item and its count into list(dict)
        j = 0
        for i in subsets:
            tmp = item_count[j]
            j += 1
            all_item_count.setdefault(i, tmp)
        # =====
        
        
        global_set = create_new_globalsets(subsets)
        item_count.clear()
        
        
        iteration += 1 
        subsets = generate_combination_set(global_set, iteration) # generate the combination-subsets of next iteration
        
        # print(global_set)
    for item in all_item_count:
        if all_item_count[item] > 0:
            print(item, all_item_count[item])
    
    return global_set
     
   
def add_to_set(subset, superset):
    if not subset.issubset(superset):
        superset = superset | subset
    return superset

# generate all the possible subsets from item set
def generate_combination_set(item_set, length):
    subsets = combinations(item_set, length) 
    return set(subsets)
                    
def check_subset(item_set, combination_subsets):
    i = int(0)
    index_map.clear()
    for s in combination_subsets: # create a hashmap
        s_string = "".join(s) # turn s from tuple -> string
        if not index_map.__contains__(s_string):
            index_map.setdefault(s_string, i)
            item_count[i] = 0 # initialize
            i += 1
    for item in item_set:
        for s in combination_subsets:
            if set(s).issubset(item):
                s_string = "".join(s) # turn s from tuple -> string
                x = index_map[s_string]
                item_count[x] = item_count[x] + 1

def compare_min_supp(item_count, index_map, min_supp):
    for index in item_count.copy():
        if item_count[index] < min_supp:
            item_count[index] = -1 # delete from dict
            delete_index_map(index_map, item_count, index)
                
def delete_index_map(index_map, item_count, del_index):
    for i in index_map.copy() :
        if index_map[i] == del_index:
            del index_map[i]
 
def create_new_globalsets(subsets):
    i = 0
    new_subsets = set()
    for s in subsets:
        if item_count[i] > 0:
            new_subsets = new_subsets | set(s)
        i += 1
    return new_subsets

def calc_min_confidence(freq_set, min_conf):
    freq_subset = set()
    for i in range(1, len(freq_set)+1):
        tmp_freq_subset = generate_combination_set(freq_set, i)    
        freq_subset = freq_subset | tmp_freq_subset

    supp_numerator = all_item_count[tuple(freq_set)]
    
    
    for subset in freq_subset:
        # print (subset)
        # print(subset in all_item_count)
        supp_denumerator = all_item_count[subset]
        conf = supp_numerator / supp_denumerator
        diff_subset = tuple(freq_set-set(subset))
        if conf >= min_conf and not diff_subset == ():
            output(subset, diff_subset, round(conf, 3))
        
    
def output(subset, diff_subset, conf):
    file_output = open("output.txt", "a")
    output = str(subset)+str(' --> ')+ str(diff_subset) +str(': ')+ str(conf)
    print(output)
    file_output.write(output+'\n')
    

      

if __name__ == '__main__':
    # input_file_name = input('Enter the file name(e.g. test.txt):')
    # min_supp = input('Enter the minimum support:')
    # min_conf = input('Enter the minimum confidence:')
    # transaction = load_transaction_data(input_file_name)
    min_supp = 2
    min_conf = 0.6
    transaction, transaction_length = load_transaction_data("input1.txt")
    print("The frequent pattern count which is larger than min_support:")
    freq_set = freq_count(transaction, min_supp)
    print()
    
    print("The strong rule:")
    calc_min_confidence(freq_set, min_conf)
    