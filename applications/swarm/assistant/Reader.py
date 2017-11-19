#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob, argparse, os

from pymongo import MongoClient
from osgeo import ogr, osr
from osmread import parse_file, Way, Node,Relation

from system.Graphium import Graphium
from system.Logger import Logger
from system.Helper import Helper

class Reader:

    _g          = None
    _logger     = None
    _helper     = None
    _args       = None
    file_name   = None
    nodes       = None
    city        = None

    def __init__(self,args):

        self._g         = Graphium()
        self._logger    = Logger('Reader')
        self._helper    = Helper()
        self._args      = args

        self.__client		= MongoClient(self._g.mongodb['mongo_host'], self._g.mongodb['mongo_port'])
        self.__db			= self.__client[self._g.mongodb['mongo_db']]
        self.__collection   = self.__db.street

        if args.osm_path[:1] == "/":
            self.file_name  = args.osm_path
        else:
            self.file_name  = self._g.path_dataset()+args.osm_path

        self.nodes      = {}
        self.ways_types = []
        self.num_total_ways = 0
        self._logger.info("Reader: Start at "+self._helper.getTimeNow())


    def start(self):

        if not os.path.exists(self.file_name):
            self._logger.info("Reader: path'{0}' not exist".format(self.file_name))
            raise ValueError('The path is not valid {0}'.format(self.file_name))

        city_exits = False
        # select the subtypes of streets to filter on osm file
        if self._g.osm['use_urban_ways'] == True:
            self.ways_types += self._g.osm['urban_highway_tipes']
        if self._g.osm['use_motorways']  == True:
            self.ways_types += self._g.osm['motorways_highway_tipes']
        if self._g.osm['use_othersways'] == True:
            self.ways_types += self._g.osm['others_highway_tipes']

        self._logger.info("Reader: Types of ways '{0}'.".format(self.ways_types))
        # first is necessary map all nodes to fast acess on dict

        city = None
        for entity in parse_file(self.file_name):
            if isinstance(entity,Node):
                self.nodes[str(entity.id)] = entity

            if isinstance(entity,Node) and 'place' in entity.tags and entity.tags['place'] == "city":

                if city == None:
                    city = {}
                    self._logger.info("Reader: Node {0}.".format(entity))

                    try:
                        city['name'] = entity.tags['name']
                    except:
                        city['name'] = ""

                    try:
                        city['state'] = entity.tags['is_in:state']
                    except:
                        city['state'] = entity.tags['is_in']

                    try:
                        city['country'] = entity.tags['is_in:country']
                    except:
                        city['country'] = ""

                    try:
                        city['population'] = int(entity.tags['population'])
                    except:
                        city['population'] = -1
                    try:
                        city['country_code'] = entity.tags['is_in:country_code']
                    except:
                        city['country_code'] = ""

                    try:
                        city['state_code'] = entity.tags['is_in:state_code']
                    except:
                        city['state_code'] = ""

                    try:
                        city['lat'] = entity.lat
                    except:
                        city['lat'] = ""

                    try:
                        city['lng'] = entity.lon
                    except:
                        city['lng'] = ""

                    try:
                        city['osm_node_id'] = int(entity.id)
                    except:
                        city['osm_node_id'] = 0

                elif city['population'] < int(entity.tags['population']):

                    self._logger.info("Reader: Node {0}.".format(entity))

                    try:
                        city['name'] = entity.tags['name']
                    except:
                        city['name'] = ""

                    try:
                        city['state'] = entity.tags['is_in:state']
                    except:
                        city['state'] = entity.tags['is_in']

                    try:
                        city['country'] = entity.tags['is_in:country']
                    except:
                        city['country'] = ""

                    try:
                        city['population'] = int(entity.tags['population'])
                    except:
                        city['population'] = -1

                    try:
                        city['country_code'] = entity.tags['is_in:country_code']
                    except:
                        city['country_code'] = ""

                    try:
                        city['state_code'] = entity.tags['is_in:state_code']
                    except:
                        city['state_code'] = ""

                    try:
                        city['lat'] = entity.lat
                    except:
                        city['lat'] = ""

                    try:
                        city['lng'] = entity.lon
                    except:
                        city['lng'] = ""

                    try:
                        city['osm_node_id'] = int(entity.id)
                    except:
                        city['osm_node_id'] = 0

        if city == None:
            city = {}
            city['name']   = 'Unnamed'
            city['lat']    = 0.0
            city['lng']    = 0.0
            city['osm_node_id'] = 0
            city['state_code'] = ""
            city['country'] = ""
            city['country_code'] = ""
            city['population'] = 0

        self.city = self.getCityAndCoutry(city['name'],city['country_code'])
        if self.city == None:

            self.insertCityInformationOSM(city)
            self._logger.info("Creating '"+city['name']+"' on system")
            self.city = self.getCityAndCoutry(city['name'],city['country_code'])
            city_id = str(self.city.get('_id'))

            for entity in parse_file(self.file_name):
                if isinstance(entity, Way) and 'highway' in entity.tags:
                    is_to_insert = False
                    for type_way in self.ways_types:
                        if type_way in entity.tags['highway']:
                            is_to_insert = True

                    if is_to_insert:
                        self.num_total_ways+=1
                        way = {}
                        way['cross_streets_osm_id'] = []
                        way['street_count'] = 0
                        way['busy'] = False
                        way['city_id'] = city_id
                        try:
                            way['name_osm'] = entity.tags['name']
                        except:
                            way['name_osm'] = ""
                        try:
                            way['surface_osm'] = entity.tags['surface']
                        except:
                            way['surface_osm'] = ""

                        way['id_osm']      = entity.id
                        if 'highway' in entity.tags.keys():
                            way['type_osm']    = entity.tags['highway']
                        else:
                            way['type_osm'] = ""

                        way['nodes'] = []
                        for node in entity.nodes:
                            node = self.nodes[str(node)]
                            lat = node.lat
                            lng = node.lon
                            identifier = node.id
                            highway = None
                            try:
                                highway = node.tags['highway']
                            except:
                                None
                            way['nodes'].append({"lat": lat,"lng": lng,"id": identifier,"highway":highway})

                        self.insertStreetInformationOSM(way)

        else:
            self._logger.info("OSM: City '"+self.city['name']+"' realy exist on system")
            #print 'City realy exist on system'

        self._logger.info("Total '"+str(self.num_total_ways)+" in "+self.city['name']+"'")
        #print 'Total ',self.num_total_ways


    # insertStreetInformationOSM
    #   insert the strret informatiton
    #   from data collected from osm file
    #
    def insertStreetInformationOSM(self,data):
        self.__collection = self.__db.street
        self.__collection.insert_one(data)

    # insertCityInformationOSM
    #   insert the new city from file osm
    #
    def insertCityInformationOSM(self,data):
        self.__collection = self.__db.city
        self.__collection.insert_one(data)

    # getCityAndCoutry
    #   get the informations from city on mongodb
    #
    def getCityAndCoutry(self,name,country_code):
        self.__collection = self.__db.city
        return self.__collection.find_one({'name':name,'country_code':country_code})

    def readShapeFromOpenStreet(self,shape_file_url=None):
        if shape_file_url != None:
            self.file_name = shape_file_url
        else:
            self.file_name = self._config.shape_city_url

        driver = ogr.GetDriverByName('ESRI Shapefile')
        shp = driver.Open(self.file_name)
        layer = shp.GetLayer(0)
        spatialRef = layer.GetSpatialRef()
        self._logger.info("Reader: spatialRef {0}.".format(spatialRef))
        layerDefinition = layer.GetLayerDefn()

        self._logger.info("Reader: layerDefinition {0}.".format(layerDefinition))

        for i in range(50):
            feature = layer.GetFeature(i)
            print feature.ExportToJson()
