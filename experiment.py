import abstract
import ucs
import main

from _ast import operator

from docutils.nodes import target
from numpy.distutils.system_info import openblas_info
from sqlalchemy.sql.functions import current_date

from ways.graph import *
import csv
import random
import operator
import datetime
import ways
import ways.tools as tools
import logging
import math
import itertools
import pickle
import collections
from ucs import normal_ucs
import sys
import pickle as pkl
import abstract
import dataSet
import os

if __name__ == "__main__":
    pairs_dict = {}
    pairs_list = []
    base_results_dict = {}
    abs_results_dict = {}
    abs_results_by_k = {}

    logging.info("starting experiment test...")

    Roads = ways.graph.load_map_from_csv()
    abstract.centrality(Roads)
    dataSet.generate_data_set(Roads)
    k_list = [0.0025, 0.005, 0.01, 0.05]

    for k in k_list:
        abstract.build_abstract_dict(Roads, k, m=0.1)
        os.rename("abstractSpace.pkl",'abstractSpace' + str(k) + '.pkl')

    # loading the pairs to run the experiment on,a sum of 20 pairs as a dict
    with open("dataSet.csv", 'rt') as c:
        it = itertools.islice(c, 20)  #  20 or 19
        for row in csv.reader(it):
            pairs_list.append((int(row[0]), int(row[1])))
    pairs_dict = dict(pairs_list)


    # caculate path on each pair using base func, return dict that maps (index,index) to (number of node explored,cost)
    for start_index in pairs_dict.keys():
        goal_index = pairs_dict[start_index]
        base_result = main.base_exp(Roads,start_index, goal_index)  #  store this data
        base_results_dict[(start_index, goal_index)] = (base_result[0], base_result[1])
        #  (res[0],res[1])=(number of nodes explored,cost)


    # caculate path on each pair using betterWaze func, return dict that maps (index,index) to (number of node explored,cost)
    for k in k_list:
        abs_results_dict = {}
        file_name = 'abstractSpace' + str(k) + '.pkl'
        logging.info('starting load of file: ' + file_name)
        with open(file_name, 'rb') as pk:
            abstractMap = pkl.load(pk)
            for start_index in pairs_dict.keys():
                goal_index = pairs_dict[start_index]
                abs_result = main.betterWaze_exp(Roads,start_index, goal_index, abstractMap)
                abs_results_dict[(start_index, goal_index)] = (abs_result[0], abs_result[1])  #  store this data
            abs_results_by_k[k] = abs_results_dict  #  for each k store its abs_results

    logging.info("starting writing csv file")
    try:
        # write the result to file experiment.csv with format = start,goal,# node,cost,# node,cost,# node,cost..
        with open('experiment.csv', 'w', newline='') as out:
            csv_out = csv.writer(out)
            for start_index in pairs_dict.keys():
                goal_index = pairs_dict[start_index]
                pair_index = (start_index, goal_index)
                row = [start_index, goal_index, base_results_dict[pair_index][0],
                       base_results_dict[pair_index][1]]
                #  logging.info("starting writing csv file by k")
                for k in k_list:
                    #  logging.info("k file = " + str(k))
                    current_k_dict=abs_results_by_k[k]
                    row =  row + [current_k_dict[pair_index][0] , current_k_dict[pair_index][1]]

                csv_out.writerow(row)
    except:
        print('EXCEPTION')
    logging.info("Done all")
    sys.exit(0)
