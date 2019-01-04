#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo, datetime, bson, time
import system
from unidecode import unidecode
from bson.objectid import ObjectId

from random import randint
from pymongo import MongoClient
from system.Graphium import Graphium


class Mongo:

    _g          = None
    __client	= None
    __db 		= None
    __collection= None

    _instance   = None


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Mongo, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self,db='graphium',address='localhost',port=27017):

        self.__client		= MongoClient(address, port)
        self.__db			= self.__client[db]
        self.__collection   = self.__db.agent
        self._g             = Graphium()


    def disconnect(self):
        self.__client.close()


    ############ Agent ############

    def get_agents(self):
        self.__collection = self.__db.agent
        return self.__collection.find({})

    def agent_erase_by_query(self, query):
        self.__collection = self.__db.agent
        return self.__collection.delete_many(query)

    # getAgentByIdentifier
    #   permit to update informatations at mongodb
    #
    def getAgentByIdentifier(self,identifier):
        self.__collection   = self.__db.agent
        return self.__collection.find_one({'identifier':identifier})

    # getAgent
    #   set the end information about the agent
    #
    def getAgentByName(self,agent_name):
        self.__collection   = sef.__db.agent
        return self.__collection.find_one({'agent_name':agent_name})


    # updateAgentByName
    #   permit to update informatations at mongodb
    #
    def updateAgentByName(self,agent_name,data):
        self.__collection = self.__db.agent
        self.__collection.update({'name':agent_name},{"$set":data},upsert=False)

    # updatePathAgentById
    #   permit to update informatations at mongodb
    #
    def updateAgentByIdentifier(self,identifier,data):
        self.__collection = self.__db.agent
        self.__collection.update({'identifier':identifier},{"$set":data},upsert=False)

    # insertAgent
    #   insert the agent atMongoDB
    #
    def insertAgent(self,name,swarm_identifier,color=None):
        now = datetime.datetime.now()

        identifier = now.strftime("%Y%m%d%H%M%S%f")[:-3]
        if color == None:
            colors = self._g.swarm['swarm_agent_colors']
            active_agents = len(self.getAgentQuery({'active': True}))
            if len(colors) <= active_agents :
                color = colors[active_agents-1]
            else:
                color = colors[randint(0,len(colors)-1)]

        dataToSend = { 'identifier':identifier, 'name':name, 'swarm_identifier':swarm_identifier,'color':color, 'active':True, 'end_at':None, 'last_lat':0.0, 'last_lng':0.0, 'last_street':None,'pathbread':[],'visited_streets':[],'last_street_id_osm':None,'cycles':0}
        self.__collection = self.__db.agent
        the_id = self.__collection.insert(dataToSend)
        return identifier

    # endAgent
    #   set the end information about the agent
    #
    def endAgent(self,identifier,end_at):
        self.__collection = self.__db.agent
        self.__collection.update({'identifier':identifier},{"$set":{'end_at':end_at,'active':False}},upsert=False)

    # getAgentsBySwarmIndentifier
    #   return all agente by swarm identifier
    #
    def getAgentsBySwarmIdentifier(self, swarm_identifier):
        self.__collection = self.__db.agent
        return list(self.__collection.find({'swarm_identifier': swarm_identifier}).short("_id"))

    # getAgentQuery
    #   return the users basead on query passed
    #
    def getAgentQuery(self,query={}):
        self.__collection = self.__db.agent
        return list(self.__collection.find(query))


    def getAgentsActiveBySwarm(self,swarm_identifier):
        returned = []
        self.__collection   = self.__db.agent
        return list(self.__collection.find({'swarm_identifier':swarm_identifier,'active':True}))

    def getAgentsEndWellBySwarm(self,swarm_identifier):
        returned = []
        self.__collection   = self.__db.agent
        return list(self.__collection.find({'swarm_identifier':swarm_identifier,'end_well':True}))

	############ User ############

    # insertUser
    #   insert the user at MongoDB
    #   return the id
    #
    def insertUser(self,email,name,male,facebook_id,google_id,created_at):
        dataToSend = {'email':email, 'name':name, 'male':male, 'facebook_id':facebook_id, 'google_id':google_id, 'created_at': created_at}
        self.__collection = self.__db.user
        return self.__collection.insert_one(dataToSend).inserted_id

    # updateUserInformation
    #
    def updateUserInformation(self,email,data):
        self.__collection = self.__db.user
        self.__collection.update({'email':email},{"$set":data},upsert=False)

    # getUsersQuery
    #   return the users basead on query passed
    #
    def getUsersQuery(self,query={}):
        self.__collection = self.__db.user
        return list(self.__collection.find(query))

    # removeUsers
    #
    def removeUsers(self,query={}):
        self.__collection = self.__db.user
        self.__collection.remove(query)


    ############ Street ############

    # getStreetByIdOSM
    #   get street by id OSM of street
    #
    def getStreetByIdOSM(self,identifier):
        self.__collection   = self.__db.street
        return self.__collection.find_one({'id_osm':identifier})

    # getStreet
    #   set the end information about the street
    #
    def getStreetByName(self,street_name):
        self.__collection   = self.__db.street
        return self.__collection.find_one({'name_osm':street_name})

    # updateStreetById
    #   permit to update informatations at mongodb
    #
    def updateStreetById(self,identifier,data):
        self.__collection = self.__db.street
        self.__collection.update({'_id':identifier},{"$set":data},upsert=False)

    # getStreetsQuery
    #   return the users basead on query passed
    #
    def getStreetQuery(self,query={}):
        self.__collection = self.__db.street
        return list(self.__collection.find(query))

    def getStreets(self):
        self.__collection   = self.__db.street
        return self.__collection.find_one({})


    ############ WishList ############

    # insertWishList
    #   return ID
    #
    def insertWishList(self,lat,lng,dt_required,user_id,busy,processed,priority,street_name,city,country):
        dataToSend = {'lat':lat, 'lng':lng, 'dt_required':dt_required, 'user_id':user_id, 'busy':busy, 'processed': processed, 'priority':priority, 'street_name':street_name, 'city':city, 'country':country}
        self.__collection = self.__db.wish_list
        return self.__collection.insert_one(dataToSend).inserted_id

    # remove WishList
    #
    def removeWishList(self,query={}):
        self.__collection = self.__db.wish_list
        self.__collection.remove(query)

    # getWishListById
    #
    def getWishListById(self,wishListId):
        self.__collection = self.__db.wish_list
        return self.__collection.find_one({'_id':wishListId})



    ############ Swarm ############

    # insertSwarm
    #   create a Swarm of swarm and send the basic information
    #   return Swarm ID
    #
    def insertSwarm(self, identifier, num_agent,user_email="admin@graphium.com", name='default', start_at="", host='0.0.0.0',  seconds_to_check_agents=3, cycles_number=-1, city_id=None, active=True):
        self.__collection = self.__db.swarm
        dataToSend = {'identifier':identifier, 'name':name, 'num_agent':num_agent, 'user_email':user_email, 'host':host, 'active':active, 'start_at':start_at, 'end_at':None, 'end_well':True, 'qmi':0.0, 'seconds_to_check_agents': seconds_to_check_agents, 'city_id':city_id, 'cycles_number':cycles_number, 'num_map_api_request':0 }
        return self.__collection.insert_one(dataToSend).inserted_id

    def get_swarms(self):
        self.__collection = self.__db.swarm
        return self.__collection.find({})

    # getSwarmByIdentifier
    #   get the swarm Swarm by identifier
    #
    def getSwarmByIdentifier(self,identifier):
        self.__collection   = self.__db.swarm
        return self.__collection.find_one({'identifier':identifier})

    # updateSwarmByIdentifier
    #   permit to update informatations at mongodb
    #
    def updateSwarmByIdentifier(self,identifier,data):
        self.__collection = self.__db.swarm
        self.__collection.update({'identifier': identifier}, {"$set": data}, upsert=False)

    def get_session(self):
        self.__collection = self.__db.session
        return self.__collection.find_one({})

    def update_session(self, data):
        self.__collection = self.__db.session
        self.__collection.update({}, {"$set": data}, upsert=False)

    def create_session(self, data):
        self.__collection = self.__db.session
        self.__collection.insert_one(data)

    # countOneToMapsSwarmByIdentifer
    #   count plus one at num_map_api_request field in swarm
    #
    def countOneToMapsSwarmByIdentifer(self,identifier):
        self.__collection = self.__db.swarm
        self.__collection.update({'identifier':identifier}, {'$inc': {'num_map_api_request': 1}})

    # getMapsCounterSwarmByIdentifer
    #   return the num_map_api_request number
    #
    def getMapsCounterSwarmByIdentifer(self,identifier):
        self.__collection = self.__db.swarm
        return self.__collection.find_one({'identifier':identifier})['num_map_api_request']

    # setMapsCounterSwarmByIdentifer
    #   set at num_map_api_request the value
    #
    def setMapsCounterSwarmByIdentifer(self,identifier,value=0):
        self.__collection = self.__db.swarm
        self.__collection.update({'identifier':identifier}, {'$set': {'num_map_api_request': value}})

    def swarm_erase_by_query(self, query):
        self.__collection = self.__db.swarm
        return self.__collection.delete_many(query)

    ############ Wish List ############

    # updateWishById
    #   update a document from wish list by id
    #
    def updateWishById(self, mongo_id, data):
        self.__collection = self.__db.wish_list
        self.__collection.update({'_id': mongo_id}, {"$set": data}, upsert=False)

    # getWishListByIdentifier
    #   return the list of wishs by swarm
    #   short from priority
    #
    def getWishListByIdentifier(self, swarm_session):
        self.__collection = self.__db.wish_list
        return list(self.__collection.find({'swarm_identifier': swarm_session}).short("priority"))

    # getWishListByIdentifier
    #   return the list of wishs by swarm
    #
    def getWishListNoProccessedByIdentifier(self, swarm_session):
        self.__collection = self.__db.wish_list
        return list(self.__collection.find({'swarm_identifier': swarm_session, 'processed': False}))

    # updateStreetById
    #   permit to update informatations at mongodb
    #
    def updateWishListById(self, identifier, data):
        self.__collection = self.__db.wish_list
        self.__collection.update({'_id': identifier}, {"$set": data}, upsert=False)


    ############ Graffiti ############

    # insertGraffiti
    #   insert the graffiti at MongoDB
    #   return the id
    #
    def insertGraffiti(self, lat, lng, pano_id, heading, pitch, country, state, city, address, probability, swarm_identifier):
        dataToSend = {'lat':lat, 'lng':lng, 'pano_id':pano_id, 'heading':heading, 'pitch':pitch, 'country': country, 'state':state, 'city':city, 'address':address, 'probability':str(probability), 'swarm_identifier':swarm_identifier}
        self.__collection = self.__db.graffiti
        return self.__collection.insert_one(dataToSend).inserted_id

    def get_graffiti_by_query(self, query):
        self.__collection = self.__db.graffiti
        return self.__collection.find(query)

    def graffiti_erase_by_query(self,query):
        self.__collection = self.__db.graffiti
        return self.__collection.delete_many(query)

    def get_graffitis(self):
        self.__collection = self.__db.graffiti
        return self.__collection.find({})

    def insert_pano(self, swarm_identifier, pano_id, heading, splited, imagem_name, classification):
        dataToSend = {'swarm_identifier': swarm_identifier, 'pano_id': pano_id, 'heading': heading, 'splited': splited, 'imagem_name': imagem_name, 'classification':classification}
        self.__collection = self.__db.pano
        return self.__collection.insert_one(dataToSend).inserted_id

    def getCities(self):
        self.__collection = self.__db.city
        return self.__collection.find({})


    ############ PANO ############
    #
    def get_panos(self):
        self.__collection = self.__db.pano
        return self.__collection.find({})

    def get_pano_by_query(self, query):
        self.__collection = self.__db.pano
        return self.__collection.find(query)

    def update_pano(self, identifier, data):
        self.__collection = self.__db.pano
        self.__collection.update({'_id': identifier}, {"$set": data}, upsert=False)
