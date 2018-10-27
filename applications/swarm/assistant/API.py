#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, os, traceback, json, time

from osmapi import OsmApi
from time import sleep
from datetime import datetime

from system.Graphium import Graphium
from system.Logger import Logger
from system.Mongo import Mongo
from system.Helper import Helper
from assistant.GoogleAPI import GoogleAPI

class API:
    _instance = None
    _my_api = None
    _g = None
    _logger = None
    _helper = None
    _mongo = None
    _swarm_identifier = None
    _google_api = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(API, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, swarm_identifier, logger=None):

        self._swarm_identifier = swarm_identifier
        self._my_api = OsmApi(username=u"glaucomunsberg", password=u"********")
        self._g = Graphium()
        self._mongo = Mongo()
        self._helper = Helper()
        self._google_api = GoogleAPI()

        if logger != None:
            self._logger = logger
        else:
            self._logger = Logger('API')

    #
    # getWaysByNode
    #   Check the ways adjacent to Node on OpenStreetMap
    #
    def getWaysByNode(self, NodeId):
        # print 'getWaysByNode... ',NodeId
        results = self._my_api.NodeWays(int(NodeId))
        to_return = []

        for result in results:
            # print 'result: ',result
            the_way = {}
            the_way['id'] = result['id']
            the_way['nodes'] = []
            if 'tag' in result.keys():
                # print 'tags: ', result['tag']
                if 'name' in result['tag'].keys():
                    the_way['name'] = result['tag']['name']
                else:
                    the_way['name'] = None

            if 'nd' in result.keys():
                # print 'nodes: ',result['nd']
                the_way['nodes'] = result['nd']
            to_return.append(the_way)
        return to_return

    #
    # getPanoByPoint
    #   get Pano from Google Street View from lat,lng
    #
    def getPanoByPoint(self, lat, lng, heading=0, pitch=0):

        key = self._g.gmaps['google_key']
        s_width = self._g.gmaps['width']
        s_height = self._g.gmaps['height']

        key = self._google_api.get_authorization_key()['key']

        self._logger.info("API: GoogleAPI return key `"+key+"`")

        file_photo_metadata = self.getPanoInfoByPoint(lat, lng)
        if file_photo_metadata['status'] == "OK":
            file_name = file_photo_metadata['pano_id'] + "_h_" + str(heading) + "_p_" + str(pitch) + ".jpeg"
            directory = self._g.path_picture() + "google_street_view/"

            if not os.path.isfile(directory + file_name):
                try:
                    url_map = "https://maps.googleapis.com/maps/api/streetview?size=" + str(s_width) + "x" + str(
                        s_height) + "&location=" + str(lat) + "," + str(lng) + "&pitch=" + str(
                        pitch) + "&key=" + key + "&heading=" + str(heading)
                    file_photo = urllib2.urlopen(url_map)

                    with open(directory + file_name, 'wb') as output:
                        output.write(file_photo.read())
                    return {'status': file_photo_metadata['status'], 'pano_id': file_photo_metadata['pano_id'],
                            "image_path": directory + file_name, "lat": file_photo_metadata['location']['lat'],
                            "lng": file_photo_metadata['location']['lng'], "heading": heading, "pitch": pitch}
                except Exception as error:
                    print 'ERROR! Data json'
                    print file_photo_metadata
                    print traceback.format_exc()
                return None
            else:
                return {'status': file_photo_metadata['status'], 'pano_id': file_photo_metadata['pano_id'],
                        "image_path": directory + file_name, "lat": file_photo_metadata['location']['lat'],
                        "lng": file_photo_metadata['location']['lng'], "heading": heading, "pitch": pitch}
        else:
            self._logger.info("API: Error to get pano by point from point {0},{1} error '{2}'.".format(lat, lng,
                                                                                                       file_photo_metadata[
                                                                                                           'status']))
            return {'status': file_photo_metadata['status'], 'pano_id': "", "image_path": "", "lat": lat, "lng": lng,
                    "heading": heading, "pitch": pitch}

    # getPanoInfoByPoint
    #   get the information about pano
    #
    def getPanoInfoByPoint(self, lat, lng):

        key = self._google_api.get_authorization_key()['key']

        url_info = "https://maps.googleapis.com/maps/api/streetview/metadata?key=" + key + "&location=" + str(
            lat) + "," + str(lng)
        # print ""
        # print "url_info->",url_info
        response = urllib2.urlopen(url_info)
        data = json.loads(response.read())
        return data

    # getStreetGeocodeInfo
    #   get street Geo Code information
    #   suchs country,city, address
    def getStreetGeocodeInfoFromMaps(self, lat, lng):

        key = self._google_api.get_authorization_key()['key']

        url_info = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat) + "," + str(
            lng) + "&key=" + key

        return_json = {
            "address": "",
            "country": "",
            "city": "",
            "state": "",
            "status": ""
        }
        try:
            response = urllib2.urlopen(url_info)
            data = json.loads(response.read())

            if data['status'] == "OK":
                for result in data['results']:
                    if "street_address" in result['types']:

                        return_json['address'] = result['formatted_address']

                        for address_components in result['address_components']:
                            if 'country' in address_components['types']:
                                return_json['country'] = address_components['long_name']
                            if 'administrative_area_level_1' in address_components['types']:
                                return_json['state'] = address_components['long_name']
                            if 'locality' in address_components['types']:
                                return_json['city'] = address_components['long_name']
                return_json['status'] = "OK"
            else:
                return_json['status'] = "ERROR"
                self._logger.info(
                    "API: Error to get Geocode from point {0},{1} error '{2}'.".format(lat, lng, data['status']))

        except Exception as error:
            self._logger.info(
                "API: Error at Internet to get Geocode from point {0},{1} url '{2}'.".format(lat, lng, url_info))
            return_json['status'] = "ERROR"
        return return_json

    def getStreetGeoCodeInfoFromOSM(self, way_id):

        url_info = "http://nominatim.openstreetmap.org/reverse?format=json&osm_type=W&osm_id=" + str(way_id)

        return_json = {
            "address": "",
            "country": "",
            "city": "",
            "state": "",
            "status": ""
        }

        try:
            response = urllib2.urlopen(url_info)
            data = json.loads(response.read())
            if not "error" in data.keys():
                return_json['address'] = data['address']['road']
                return_json['country'] = data['address']['country']
                return_json['state'] = data['address']['state']
                return_json['city'] = data['address']['city']
                return_json['osm_id'] = data['osm_id']
                return_json['osm_type'] = data['osm_type']
            else:
                return_json['status'] = "ERROR"
                print "API: Error to get nominatim from way_id {0} error '{1}'.".format(way_id, data['error'])
                self._logger.info(
                    "API: Error to get nominatim from way_id {0} error '{1}'.".format(way_id, data['error']))

        except Exception as error:
            self._logger.info("API: Error to get nominatim from way_id {0} url '{1}'.".format(way_id, url_info))
            print "API: Exception!!! Error to get nominatim from way_id {0} url '{1}'.".format(way_id, url_info)
            print traceback.format_exc()
            return_json['status'] = "ERROR"

        return return_json
