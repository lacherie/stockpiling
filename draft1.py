#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


class RPD:
    def __init__(self, single_price, no_box, len_box, wid_box, dep_box):
        self.single_price = single_price
        self.no_box = no_box
        self.len_box = len_box
        self.wid_box = wid_box
        self.dep_box = dep_box
        
        
class N95(RPD):
    def __init__(self, single_price, no_box, len_box, wid_box, dep_box):
        super().__init__(single_price, no_box, len_box, wid_box, dep_box)
        
class Elastomeric(RPD):
    def __init__(self, single_price, no_box, len_box, wid_box, dep_box, filter_sets=0, filter_set_cost=0, filter_sets_per_box=0, filter_box_len=0, filter_box_wid=0, filter_box_dep=0):
        super().__init__(single_price, no_box, len_box, wid_box, dep_box)
        self.filter = Filter(filter_sets, filter_set_cost, filter_sets_per_box, filter_box_len, filter_box_wid, filter_box_dep)

class Filter:
    def __init__(self, filter_sets, filter_set_cost, filter_sets_per_box, filter_box_len, filter_box_wid, filter_box_dep):
        self.filter_sets = filter_sets
        self.filter_set_cost = filter_set_cost
        self.filter_sets_per_box = filter_sets_per_box
        self.filter_box_len = filter_box_len
        self.filter_box_wid = filter_box_wid
        self.filter_box_dep = filter_box_dep
    
        
N95_baracco = N95(0.25, 20, 12, 6, 6)
