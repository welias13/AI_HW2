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
from ucs import normal_ucs
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

num_of_paths = 500000

#centrality function runs num_of_paths paths from random nodes with probality 0.99 to continue in path
# @tools.timed
def centrality(Roads):
    centrality_dict = {}
    #zeroing all nodes indexes to have 0 visits
    for junc in Roads.junctions():
        centrality_dict[junc.index] = 0
    #search loop that runs for num_of_paths times, each iteration is a path
    for i in range(0,num_of_paths):
        #getting random node to start with
        curr_node_index = random.choice(Roads).index
        try:
            while True:
                #adding +1 visit to this node
                centrality_dict[curr_node_index] += 1
                #probality check if to go on or stop
                if random.randrange(0, 100) == 0:
                    break
                #getting next node to expand to
                curr_node_index = random.choice(Roads[curr_node_index].links).target
        except:
            ""
    #sorting nodes by visits number
    sorted_nodes = sorted(centrality_dict.items(), key=operator.itemgetter(1), reverse=True)
    #writing to file
    with open('centrality.csv', 'w', newline='') as out:
        csv_out = csv.writer(out)
        for row in sorted_nodes:
            csv_out.writerow(row)
    return sorted_nodes

#build abstract search space used for betterwaze
# @tools.timed
def build_abstract_dict(Roads ,k = 0.005, m = 0.1):
    #getting the first k*N nodes to build the space for them
    with open("centrality.csv", 'rt') as c:
        N_tag = math.floor(len(Roads)*k)
        it = itertools.islice(c, N_tag)
        centers = [int(row[0]) for row in csv.reader(it)]
    abstract_dict = {}
    #for each node in the best K*N nodes for centerality file calculate UFS paths+cost to M*K*N closet nodes
    for center in centers:
        #potential neighbors which are M*k*N
        potential_neighbors = [ele for ele in centers if ele != center]
        #run ufs from center to potential_neighbors
        (neighbors,num_developed_nodes)  = normal_ucs(Roads.junctions(), center, potential_neighbors, m)
        #sort the result by distance
        sorted_nodes = sorted(neighbors, key=operator.itemgetter(1))
        #get closet m*k*n nodes
        neighbors = sorted_nodes[0:math.floor((len(potential_neighbors) + 1) * m)]
        abstract_links = []
        #for each neighbor create the abstract linkes list to return in junction
        for neighbor in neighbors:
            abstract_links.append(AbstractLink(neighbor[2],neighbor[0],neighbor[1],-1))
        #store center's junction in the abs space dict
        abstract_dict[center] = Junction(center, Roads[center].lat, Roads[center].lon,abstract_links)
        neighbors = []
        sorted_nodes = []
        abstract_links = []
        potential_neighbors = []
    #dump the dict to .pkl file for future use
    with open("abstractSpace.pkl",'wb') as p:
        pickle.dump(abstract_dict,p)

def comp(list1, list2):
    if len(list1) != len(list2):
        return False

    for val in list1:
        if val not in list2:
            return False

    return True



if __name__ == "__main__":
    logging.info("Main start")
    logging.info("Loading Roads")
    Roads = ways.graph.load_map_from_csv("tlv.csv")
    logging.info("load finished")
    logging.info("Building centrality")
    centrality(Roads)
    logging.info("centrality finished")
    logging.info("Build Abstract")
    build_abstract_dict(Roads, k=0.005, m = 0.1)
    logging.info("Build Abstract finished")
