#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from shutil import copyfile

from system.Mongo import Mongo
from system.Graphium import Graphium


def main():
    graphium = Graphium()
    mongo = Mongo()

    for graffiti in mongo.get_graffiti_by_query({"situation": "false_positive"}):

        for pano in mongo.get_pano_by_query({"pano_id": graffiti['pano_id']}):

            if pano['heading'].split(".")[0] == graffiti['heading']:
                pic_name = pano['pano_id'] + "_h_" + pano['heading'] + "_p_" + str(graffiti['pitch']) + ".jpeg"

                picture_origem_path = graphium.path_picture() + "google_street_view/" + pic_name

                picture_destiny_path = "/Users/glaucomunsberg/Desktop/graffiti_to_train_poa/false_positive/" + pic_name

                copyfile(picture_origem_path, picture_destiny_path)

    for graffiti in mongo.get_graffiti_by_query({"situation": "false_negative"}):

        for pano in mongo.get_pano_by_query({"pano_id": graffiti['pano_id']}):

            if pano['heading'] == graffiti['heading']:
                pic_name = pano['pano_id'] + "_h_" + pano['heading'] + "_p_" + str(graffiti['pitch']) + ".jpeg"

                picture_origem_path = graphium.path_picture() + "google_street_view/" + pic_name

                picture_destiny_path = "/Users/glaucomunsberg/Desktop/graffiti_to_train_poa/false_negative/" + pic_name

                copyfile(picture_origem_path, picture_destiny_path)


if __name__ == '__main__':
    main()
