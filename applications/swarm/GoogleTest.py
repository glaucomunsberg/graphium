#!/usr/bin/env python
# -*- coding: utf-8 -*-

from assistant.GoogleAPI import GoogleAPI

def main():

    googleAPI = GoogleAPI()
    for index in range(6):
        print 'Gkey:', index
        print googleAPI.get_authorization_key()
        # time.sleep(1)

if __name__ == '__main__':
    main()

from threading import Thread

class Agent(Thread):

    def run(self):

        while get_street_no_visited() != 0:

            street = get_street_no_visited()[0]

            for node in street['nodes']:

                points = break_node_in_points(node)

                street_orientation = get_street_orientation(node)

                heating_left = street_orientation - 90
                heating_right = street_orientation + 90

                for point in points:


                    image_left = get_image_street_view(point['lat'],point['lng'],heating_left)
                    image_right = get_image_street_view(point['lat'],point['lng'],heating_right)

                    if identify_with_model(image_left):
                        create_graffiti_on_map(point, heating_left, image_left)


                    if identify_with_model(image_rigth):
                        create_graffiti_on_map(point, heating_right, image_right)

            set_street_visited(street)