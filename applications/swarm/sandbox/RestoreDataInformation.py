#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from applications.swarm.assistant.GoogleAPI import GoogleAPI
from applications.swarm.system.Mongo import Mongo
from applications.swarm.system.Graphium import Graphium

def main():

    graphium = Graphium()
    mongo = Mongo()

    panos = []

    for graffiti in mongo.get_graffitis():
        panos.append(graffiti['pano_id'])

    dir_name = graphium.path_picture()
    dir_name += "google_street_view/"
    print dir_name
    test = os.listdir(dir_name)
    count = 0
    for item in test:
        if item.endswith(".jpeg"):

            splited = item.split("_h_")
            pano_id = splited[0]
            splited = splited[1].split("_p_")
            heading = splited[0]
            splited = splited[1].split(".jpeg")[0]


            #print 'File name', item
            #print 'pano_id', pano_id
            #print 'heading', heading
            #print 'splited', splited

            classification = "F"
            if pano_id in panos:
                classification = "T"

            mongo.insert_pano("20181103173441", pano_id, heading, splited, item, classification)
            count += 1
            print "\r"
            print item

    print str(count)+" images."


if __name__ == '__main__':
    main()
