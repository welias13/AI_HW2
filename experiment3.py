from _ast import operator

from docutils.nodes import target
from numpy.distutils.system_info import openblas_info
from sqlalchemy.sql.functions import current_date
import os
import csv
import ways
import logging
import itertools
import sys

import main2b
import abstract
import dataSet
if __name__ == "__main__":
    pairs_dict = {}
    pairs_list = []
    ucs_base_results_dict = {}
    astar_base_results_dict = {}


    logging.info("starting experiment2 test...")

    Roads = ways.graph.load_map_from_csv()

    with open("dataSet.csv", 'rt') as c:
        it = itertools.islice(c, 20)  # 20 or 19
        for row in csv.reader(it):
            pairs_list.append((int(row[0]), int(row[1])))
    pairs_dict = dict(pairs_list)

    # caculate path on each pair using base func, return dict that maps (index,index) to (number of node explored,cost)
    for start_index in pairs_dict.keys():
        goal_index = pairs_dict[start_index]
        ucs_base_result = main2b.uc_time_exp(Roads, start_index, goal_index)  # store this data
        ucs_base_results_dict[(start_index, goal_index)] = (ucs_base_result[0], ucs_base_result[1])
        astar_base_result = main2b.a_star_time_exp(Roads, start_index, goal_index)
        astar_base_results_dict[(start_index, goal_index)] = (astar_base_result[0], astar_base_result[1])
        # (res[0],res[1])=(number of nodes explored,cost)

    logging.info("starting writing csv file")
    try:
        # write the result to file experiment.csv with format = start,goal,#node,cost,#node,cost,#node,cost..
        with open('experiment3.csv', 'w', newline='') as out:
            csv_out = csv.writer(out)
            for start_index in pairs_dict.keys():
                goal_index = pairs_dict[start_index]
                pair_index = (start_index, goal_index)
                row = [start_index, goal_index, ucs_base_results_dict[pair_index][0],
                       ucs_base_results_dict[pair_index][1], astar_base_results_dict[pair_index][0],
                       astar_base_results_dict[pair_index][1]]
                # logging.info("starting writing csv file by k")
                csv_out.writerow(row)
    except:
        print('Write to experiment3.csv failed!')
logging.info("Done all")
sys.exit(0)
