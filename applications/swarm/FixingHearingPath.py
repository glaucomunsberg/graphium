#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from assistant.GoogleAPI import GoogleAPI
from system.Mongo import Mongo
from system.Graphium import Graphium

def main():

    graphium = Graphium()
    mongo = Mongo()

    true_positives = 0
    false_positives = 0

    for graffiti in mongo.get_graffitis():

        for pano in mongo.get_pano_by_query({'pano_id':graffiti['pano_id']}):
            if pano['heading'] == str(graffiti['heading']):
                pano['classification'] = "T"
                mongo.update_pano(pano['_id'], pano)
                false_positives += 1
            else:
                pano['classification'] = "F"
                mongo.update_pano(pano['_id'], pano)
                false_positives += 1

    print "True trues ", true_positives
    print "False trues", false_positives


if __name__ == '__main__':
    main()
