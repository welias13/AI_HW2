'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple
import collections

from ways.graph import Roads
from ways.info import TYPE_INDICES
from pandas.core.window import _Rolling_and_Expanding
from sqlalchemy.orm.collections import collection

from ways import load_map_from_csv

import sys

def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    number_of_junctions = len(roads)
    number_of_links = 0
    max_branching_factor = 0
    min_branching_factor = sys.maxsize
    max_distance = 0
    min_distance = sys.maxsize
    total_distance = 0
    lnk_type_list = []
    #for each junc in roads check the its maximal branching factor and update if its bigger that old one,also do the same for minimal branching factor
    for junc in roads.junctions():
        if len(junc.links) > max_branching_factor:
            max_branching_factor = len(junc.links)
        if len(junc.links) < min_branching_factor:
            min_branching_factor = len(junc.links)
    number_of_links = 0
    #for each link check for the maximal and minimal distance and update when there is need
    for lnk in roads.iterlinks():
        number_of_links += 1
        total_distance = total_distance + lnk.distance
        if lnk.distance > max_distance:
            max_distance = lnk.distance
        if lnk.distance < min_distance:
            min_distance = lnk.distance
        lnk_type_list.append(lnk.highway_type)
    #COUNTER used to store all node as 0 links, used for making sure all the nodes are in final returned dict
    sub_dict = collections.Counter({type:0 for type in TYPE_INDICES})
    types_histogram = collections.Counter(lnk_type_list)
    types_histogram.subtract(sub_dict)
    return {
        'Number of junctions' : number_of_junctions,
        'Number of links' : number_of_links,
        'Outgoing branching factor' : Stat(max=max_branching_factor, min=min_branching_factor, avg=float(number_of_links)/number_of_junctions),
        'Link distance' : Stat(max=max_distance, min=min_distance, avg=float(total_distance)/number_of_links),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram' : types_histogram,  # tip: use collections.Counter
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))

        
if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()
