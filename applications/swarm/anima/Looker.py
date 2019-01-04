#!/usr/bin/env python
# -*- coding: utf-8 -*-

from system.Graphium import Graphium
from system.Mongo import Mongo
from system.Helper import Helper
from system.Logger import Logger
from assistant.API import API
from assistant.Geospatial import GeoSpatial
from Oracle import Oracle


class Looker:

    _g = None
    _helper = None
    _logger = None
    _mongo = None
    _api = None
    _oracle = None
    geos = None

    def __init__(self, swarm_identifier, logger=None):

        self._g = Graphium()
        self._helper = Helper()
        self._mongo = Mongo()
        self._swarm_identifier = swarm_identifier

        if logger is None:
            self._logger = Logger()
        else:
            self._logger = logger

        self.geos = GeoSpatial(self._logger)
        self._api = API(self._swarm_identifier, self._logger)
        self._oracle = Oracle(None, self._logger)

    def driveFromPointToPoint(self, dot1, dot2, way_osm_id):
        self._logger.info("Looker: Check dot {0} and {1}".format(dot1,dot2))
        #   slice two points to in two or many points
        #   get the orientation of route
        #   calculate the degrees to look de left and right side
        #   for each point in points:
        #       get paranonamic image
        points = self.geos.getIntermediatePointsFromTwoDots(dot1, dot2)
        street_orientation = self.geos.calculateStreetOrientation(dot1, dot2)
        left_side = street_orientation-90
        right_side = street_orientation+90

        if left_side >= 360.0:
            left_side = left_side - 360.0

        if right_side >= 360.0:
            right_side = right_side - 360.0

        for point in points:
            self._logger.info("Looker: Check point {0}".format(point))
            lat = point[0]
            lng = point[1]

            data_point_left = self._api.getPanoByPoint(lat, lng, left_side)
            data_point_right = self._api.getPanoByPoint(lat, lng, right_side)

            if data_point_left['status'] == "OK":
                self.checkPointToPredict(data_point_left,way_osm_id)
            else:
                self._logger.info("Looker: CheckPoint can't execute to point {0},{1} error '{2}'.".format(data_point_left['lat'], data_point_left['lng'], data_point_left['status']))

            if data_point_right['status'] == "OK":
                self.checkPointToPredict(data_point_right,way_osm_id)
            else:
                self._logger.info("Looker: CheckPoint can't execute to point {0},{1} error '{2}'.".format(data_point_right['lat'], data_point_right['lng'], data_point_right['status']))

    def checkPointToPredict(self, dataPoint, way_osm_id):





        prediction = self._oracle.predictInPano(dataPoint['image_path'])
        if prediction["prediction"]:

            #
            # INFORMATION OF COUNTRY,CITY AND STATE is EMPTY
            #
            self._mongo.insert_pano("20181103173441", dataPoint['pano_id'], dataPoint['heading'], "0", dataPoint['file_name'], "T")
            self._mongo.insertGraffiti(dataPoint['lat'], dataPoint['lng'], dataPoint['pano_id'], dataPoint['heading'], dataPoint['pitch'], "", "", "", "", prediction["probability"], self._swarm_identifier)
            #
            # GOOGLE INFORMATION ABOUT COUNTRY, CITY AND STATE
            #
            #streetMetadata = self._api.getStreetGeoCodeInfoFromOSM(way_osm_id)
            #if streetMetadata['status'] != "OK":
            #    self._mongo.insertGraffiti(dataPoint['lat'],dataPoint['lng'],dataPoint['pano_id'],dataPoint['heading'],dataPoint['pitch'],streetMetadata['country'],streetMetadata['state'],streetMetadata['city'],streetMetadata['address'],prediction["probability"],self._swarm_identifier)
            #else:
            #    streetMetadata = self._api.getStreetGeocodeInfoFromMaps(dataPoint['lat'],dataPoint['lng'])
            #    if streetMetadata['status'] != "OK":
            #        self._mongo.insertGraffiti(streetMetadata['lat'],streetMetadata['lng'],dataPoint['pano_id'],dataPoint['heading'],dataPoint['pitch'],streetMetadata['country'],streetMetadata['state'],streetMetadata['city'],streetMetadata['address'],prediction["probability"],self._swarm_identifier)
            #    else:
            #        print "Looker: CAN'T insert street without metadata in point {0} at way_osm_id {1}".format(dataPoint,way_osm_id)
            #        self._logger.info("Looker: CAN'T insert street without metadata in point {0} at way_osm_id {1}".format(dataPoint,way_osm_id))
            # get the street information suchs city, country and address
            # put it in dataset
        else:
            self._mongo.insert_pano("20181103173441", dataPoint['pano_id'], dataPoint['heading'], "0", dataPoint['file_name'], "F")
            self._logger.info("Looker: It's not a graphiti at {0}".format(dataPoint))
