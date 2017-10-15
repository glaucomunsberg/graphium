#!/usr/bin/env python
# -*- coding: utf-8 -*-


from Geospatial import GeoSpatial
from system.Graphium import Graphium
from system.Mongo import Mongo
from system.Helper import Helper
from system.Logger import Logger
from hive.API import API

class Looker:

    _g          = None
    _helper     = None
    _logger     = None
    _mongo      = None
    _api        = None
    geos        = None


    def __init__(self,logger=None):

        self._g         = Graphium()
        self._helper    = Helper()
        self._mongo     = Mongo()
        self.geos       = GeoSpatial()

        if logger == None:
            self._logger    = Logger()
        else:
            self._logger    = logger

        self._api       = API(self._logger)


    def checkPoints(self,dot1,dot2):
        self._logger.info("Looker: Check dots {0} and {1}".format(dot1,dot2))
        #   slice two points to in two or many points
        #   get the orientation of route
        #   calculate the degrees to look de left and right side
        #   for each point in points:
        #       get paranonamic image
        points  = self.geos.getIntermediatePointsFromTwoDots(dot1,dot2)
        street_orientation = self.geos.calculateInitialCompassBearing(dot1,dot2)
        left_side   = street_orientation-90
        right_side  = street_orientation+90
        for point in points:
            self._logger.info("Looker: Check point {0}".format(point))
            lat = point[0]
            lng = point[1]
            self._api.getPanoByPoint(lat,lng,left_side)
            self._api.getPanoByPoint(lat,lng,left_side)
