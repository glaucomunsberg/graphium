#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, math
sys.path.append('../')

from geopy.distance import great_circle

from system.Graphium import Graphium
from system.Logger import Logger

class GeoSpatial:

    _logger = None

    def __init__(self,logger=None):
        if logger == None:
            self._logger = Logger('Geospatial')
        else:
            self._logger = logger

    #
    # getDistance
    #   calculate the distance between two dots
    def getDistance(self,dot1,dot2):
        return great_circle(dot1, dot2).meters

    #
    # getIntermediatePointsFromTwoDots
    #   between two dots if great that distanceMax slice in a dots
    #   with distance max bewteen new points.
    #
    def getIntermediatePointsFromTwoDots(self,dot1,dot2,distanceMax=13):
        lista_to_return = []
        distanceBetween = self.getDistance(dot1,dot2)
        print "Dots:",dot1,dot2

        if distanceBetween <= 13:
            print 'distanceBetween '+str(distanceBetween)+' <= 13m'
            lista_to_return = [dot1,dot2]
            return lista_to_return
        else:
            print 'distanceBetween '+str(distanceBetween)+' > 13m'

            lat1    = dot1[0]
            lng1    = dot1[1]
            lat2    = dot2[0]
            lng2    = dot2[1]

            if lat2 > lat1:
                lat_diff    = float(lat2-lat1)
            else:
                lat_diff    = float(lat1-lat2)

            if lng2 > lng1:
                lng_diff    = float(lng2-lng1)
            else:
                lng_diff    = float(lng1-lng2)

            divisibleBy    = distanceBetween/float(distanceMax)
            #print 'DivisionBy',divisibleBy
            lat_bit     = lat_diff%float(divisibleBy)
            lng_bit     = lng_diff%float(divisibleBy)

            lista_to_return.append(dot1)
            for i in range(int(divisibleBy)):
                to_append = tuple([lat1+((i+1)*lat_bit),lng1+((i+1)*lng_bit)])
                #print 'Append',to_append
                lista_to_return.append(to_append)

            lista_to_return.append(dot2)
            return lista_to_return


    def getIntermediatePointsFromTwoCoordinates(self,lat1,lng1,lat2,lng2,distanceMax=13):
        lat1 = float(lat1)
        lng1 = float(lng1)
        lat2 = float(lat2)
        lng2 = float(lng2)

        dot1 = (lat1,lng1)
        dot2 = (lat2,lng2)
        return self.getIntermediatePointsFromTwoDots(dot1,dot2)


    def calculateInitialCompassBearing(self,pointA, pointB):
        """
        Calculates the bearing between two points.
        The formulae used is the following:
            θ = atan2( sin(Δlong).cos(lat2),
                       cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
        :Parameters:
          - `pointA: The tuple representing the latitude/longitude for the
            first point. Latitude and longitude must be in decimal degrees
          - `pointB: The tuple representing the latitude/longitude for the
            second point. Latitude and longitude must be in decimal degrees
        :Returns:
          The bearing in degrees
        :Returns Type:
          float
        """
        if (type(pointA) != tuple) or (type(pointB) != tuple):
            raise TypeError("Only tuples are supported as arguments")

        lat1 = math.radians(pointA[0])
        lat2 = math.radians(pointB[0])

        diffLong = math.radians(pointB[1] - pointA[1])

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                * math.cos(lat2) * math.cos(diffLong))

        initial_bearing = math.atan2(x, y)

        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360

        return compass_bearing
