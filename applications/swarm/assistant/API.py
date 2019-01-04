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
from assistant.GoogleSigning import GoogleSigning

class API:
    _instance = None
    _my_api = None
    _g = None
    _logger = None
    _helper = None
    _mongo = None
    _swarm_identifier = None
    _google_api = None
    _google_signing = None
    _header = None

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
        self._google_signing = GoogleSigning()

        if logger is not None:
            self._logger = logger
        else:
            self._logger = Logger('API')

        self._header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                              'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                              'Accept-Encoding': 'none',
                              'Accept-Language': 'en-US,en;q=0.8',
                              'Connection': 'keep-alive'}

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
            the_way = dict()
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

        s_width = self._g.gmaps['width']
        s_height = self._g.gmaps['height']
        url_map_sign = ""

        g_auth_protocol = self._google_api.get_authorization_key()
        key = g_auth_protocol['key']
        key_secret = g_auth_protocol['key_secret']

        self._logger.info("API: GoogleAPI return key `"+key+"` with `"+key_secret+"`")

        file_photo_metadata = self.getPanoInfoByPoint(lat, lng)
        if file_photo_metadata['status'] == "OK":
            file_name = file_photo_metadata['pano_id'] + "_h_" + str(heading) + "_p_" + str(pitch) + ".jpeg"
            directory = self._g.path_picture() + "google_street_view/"

            if not os.path.isfile(directory + file_name):
                try:
                    url_map = "https://maps.googleapis.com/maps/api/streetview?size=" + str(s_width) + "x" + str(
                        s_height) + "&location=" + str(lat) + "," + str(lng) + "&pitch=" + str(
                        pitch) + "&key=" + key + "&heading=" + str(heading)

                    url_map_sign = self._google_signing.sign_url(url_map, str(key_secret))

                    request = urllib2.Request(url_map_sign, headers=self._header)
                    file_photo = urllib2.urlopen(request)

                    with open(directory + file_name, 'wb') as output:
                        output.write(file_photo.read())
                    return {'status': file_photo_metadata['status'], 'pano_id': file_photo_metadata['pano_id'],
                            "image_path": directory + file_name, "lat": file_photo_metadata['location']['lat'],
                            "lng": file_photo_metadata['location']['lng'], "heading": heading, "pitch": pitch,
                            'file_name': file_name}
                except Exception as error:
                    print 'ERROR! Data json'
                    print 'URL'
                    print url_map
                    print url_map_sign
                    print 'File Photo Metadata'
                    print file_photo_metadata
                    print traceback.format_exc()
                return None
            else:
                return {'status': file_photo_metadata['status'], 'pano_id': file_photo_metadata['pano_id'],
                        "image_path": directory + file_name, "lat": file_photo_metadata['location']['lat'],
                        "lng": file_photo_metadata['location']['lng'], "heading": heading, "pitch": pitch, 'file_name': file_name}
        else:
            self._logger.info("API: Error to get pano by point from point {0},{1} error '{2}'.".format(lat, lng,
                                                                                                       file_photo_metadata[
                                                                                                           'status']))
            return {'status': file_photo_metadata['status'], 'pano_id': "", "image_path": "", "lat": lat, "lng": lng,
                    "heading": heading, "pitch": pitch, "file_name":""}

    # getPanoInfoByPoint
    #   get the information about pano
    #
    def getPanoInfoByPoint(self, lat, lng):

        g_auth_protocol = self._google_api.get_authorization_key()
        key = g_auth_protocol['key']
        key_secret = g_auth_protocol['key_secret']

        url_info = "https://maps.googleapis.com/maps/api/streetview/metadata?key=" + key + "&location=" + str(
            lat) + "," + str(lng)

        data = dict()

        try:
            response = urllib2.urlopen(url_info)
            data = json.loads(response.read())
        except Exception as error:
            self._logger.info(
                "API: Error at Internet to get Geocode from point {0},{1} url '{2}'.".format(lat, lng, url_info))
            data['status'] = "ERROR"
            print "Error"
            print "URL"
            print url_info
            print error
            print traceback.format_exc()

        return data

    # getStreetGeocodeInfo
    #   get street Geo Code information
    #   suchs country,city, address
    def getStreetGeocodeInfoFromMaps(self, lat, lng):

        #  force position 0, only account with Geocoding API with limit > 1 (billing account)
        key = self._google_api.get_key(0)
        key_secret = self._google_api.get_key_secret(0)
        self.force_use_key_position(0)

        url_info = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat) + "," + str(
            lng) + "&key=" + key

        url_map_sign = self._google_signing.sign_url(url_info, key_secret)

        return_json = {
            "address": "",
            "country": "",
            "city": "",
            "state": "",
            "status": ""
        }

        try:
            response = urllib2.urlopen(url_map_sign)
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
