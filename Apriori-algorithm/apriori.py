# -*- coding: utf-8 -*-
"""
homework 1: Association rules with Apriori algo.
@author: Yun-Hsuan N26101892
"""

from itertools import combinations
from collections import defaultdict


item_count = defaultdict()
index_map = dict()
subsets = set([])
new_subsets = set()
all_item_count = defaultdict()
supp_numerator = 0.000 # 分子 = global_set
supp_denumerator = 0.000 # 分母


def load_transaction_data(file_name):
    transaction = []
    with open(file_name, 'r') as file:
        for lines in file:
            transaction.append(set(lines.split()))
    return transaction


def freq_count(transaction, min_supp):
    rules = set()
    global_set = set()
    last_global_set = set()
    for item in transaction:
        global_set = add_to_set(item, global_set) # all item set without duplicate
    iteration = 1
    subsets = generate_combination_set(global_set, 1)
    
    while len(subsets) >= 1:
        check_subset(transaction, subsets) # record the count of every subset
        compare_min_supp(item_count, index_map, min_supp)
        
        # add each item and its count into list(dict)
        j = 0
        for i in subsets:
            i = sorted(i)
            tmp = item_count[j]
            if tmp > 0 and len(i) > 1:
                print(set(i), tmp)
                rules.add(tuple(i))
            j += 1 
            all_item_count.setdefault(tuple(i), tmp) # add into dict
        # =====
        
        global_set = create_new_globalsets(subsets)
        
        # print("global set=", global_set)
        if len(global_set) == 0:
            global_set = tuple(sorted(last_global_set))
            item_count.clear()
            index_map.clear()
            return global_set, rules
        else:
            global_set = tuple(sorted(global_set))
            item_count.clear()
        
            iteration += 1 
            subsets = generate_combination_set(global_set, iteration) # generate the combination-subsets of next iteration
            last_global_set = global_set
        
            
    return global_set, rules
     
   
def add_to_set(subset, superset):
    if not subset.issubset(superset):
        superset = superset | subset
    return superset

# generate all the possible subsets from item set
def generate_combination_set(item_set, length):
    subsets = combinations(item_set, length)
    return set(sorted(subsets))
                    
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

def calc_supp_numerator(freq_set, transaction):
    x = tuple(sorted(freq_set))
    sets = set(freq_set)
    all_item_count[x] = 0
    for each_transaction in transaction:
        if sets.issubset(each_transaction):
            all_item_count[x] += 1
    return all_item_count[x]

def calc_min_confidence(freq_patten_rules, min_conf, file_output):   
    r_subsets = set()
    for r in freq_patten_rules:
        for length in range(1, len(r)):
            tmp = generate_combination_set(r, length)
            r_subsets = r_subsets | tmp

        for subset in r_subsets.copy():
            s = tuple(sorted(subset))
            supp_denumerator = all_item_count[s]
            conf = supp_numerator / supp_denumerator
            diff_subset = tuple(set(r)-set(subset))
            if conf >= min_conf and not diff_subset == ():
                output(file_output, subset, diff_subset, round(conf, 4))
                r_subsets.remove(subset)
    
def output(file_output, subset, diff_subset, conf):
    output = str(subset)+str(' --> ')+ str(diff_subset) +str('  conf= ')+ str(conf)
    print(output)
    file_output.write(output+'\n')
    
     

if __name__ == '__main__':
    input_file_name = input('Enter the file name(e.g. test.txt):')
    min_supp = float(input('Enter the minimum support:'))
    min_conf = float(input('Enter the minimum confidence:'))
    transaction = load_transaction_data(input_file_name)
    # min_supp = 0.08  # 0.08 * 88162 = 7053
    # min_conf = 0.75
    transaction = load_transaction_data("input.txt")
    min_supp = min_supp * len(transaction)
    
    print("The frequent pattern count which is larger than min_support:")
    freq_set, rules = freq_count(transaction, min_supp)
    
    supp_numerator = calc_supp_numerator(freq_set, transaction)

    print("The strong rule:")
    file_output = open("output.txt", "w")
    calc_min_confidence(rules, min_conf, file_output)
    file_output.close()