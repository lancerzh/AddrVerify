#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Apr 7, 2016

@author: lancer
'''
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

if __name__ == '__main__':
    print(fuzz.ratio("ACME Factory", "ACME Factory Inc."))

    print(fuzz.partial_ratio("ACME Factory", "ACME Factory Inc."))
    print(fuzz.partial_ratio("张楠", "张楠"))

    pass