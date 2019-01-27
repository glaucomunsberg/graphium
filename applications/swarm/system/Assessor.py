#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse, math, os, datetime

from system.Mongo import Mongo
from system.Graphium import Graphium
from system.Helper import Helper
from system.Logger import Logger


class Assessor:

    _g = None
    _mongo = None
    _helper = None
    _logger = None
    _args = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Assessor, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, args):

        self._g = Graphium()
        self._mongo = Mongo()
        self._helper = Helper()
        self._logger = Logger('Assessor')
        self._args = args

    def start(self):

        if self._args.rake == "city:list":
            self.list_city()
        elif self._args.rake == "street:list":
            self.list_street(None)
        elif self._args.rake == "street:count":
            self.list_street(True)
        elif self._args.rake == "config:list":
            self.list_config()
        elif self._args.rake == "swarm:list":
            self.swarm_list()
        elif self._args.rake == "swarm:active":
            self.swarm_active()
        elif self._args.rake == "swarm:shutdown":
            self.swarm_shutdown()
        elif self._args.rake == "swarms:erase":
            self.swarm_erase()
        elif self._args.rake == "swarm:erase":
            self.swarm_erase_by_id(self._args)
        elif self._args.rake == "agents:erase":
            self.agent_erase()
        elif self._args.rake == "graffitis:list":
            self.graffiti_list()
        elif self._args.rake == "graffiti:erase":
            self.graffiti_erase()
        elif self._args.rake == "session:list":
            self.session_list()
        elif self._args.rake == "logs:erase":
            self.log_erase()
        elif self._args.rake == "model:list":
            self.model_list()
        elif None:
            print 'You need a function on rake'
        else:
            print self._args.rake+" is not a function"

    def list_city(self):

        print 'List of Cities'
        count = 0
        for city in self._mongo.getCities():
            count += 1
            print "Id "+str(city['_id'])+" Name `"+city['name']+"`"

        print str(count)+" cities."
        self._logger.info('Assessor: List cities')

    def swarm_list(self):
        print 'List Swarms'
        count = 0
        for swarm in self._mongo.get_swarms():
            count += 1
            print "Id "+str(swarm['_id'])+" Name `"+swarm['name']+"`"

        print str(count)+" swarms."
        self._logger.info('Assessor: List swarms')

    def swarm_active(self):
        print 'List Active Swarms'
        count = 0
        for swarm in self._mongo.get_swarms():
            if swarm['active'] is True:
                count += 1
                print "Identifier "+swarm['identifier']+" ID "+str(swarm['_id'])+" Name `"+swarm['name']+"`"
                for agent in self._mongo.getAgentQuery({'swarm_identifier':swarm['identifier']}):
                    print "-> Agent Name: "+agent['name']+" Active "+str(agent['active'])

        print str(count)+" active swarms."
        self._logger.info('Assessor: List swarm active')

    def swarm_shutdown(self):
        count_shutdonw = 0
        for swarm in self._mongo.get_swarms():
            if swarm['active'] is True:

                swarm_data = self._mongo.getSwarmByIdentifier(swarm['identifier'])

                streets = self._mongo.getStreetQuery({"city_id": swarm_data['city_id']})

                count = 0
                for street in streets:
                    count += street['street_count']*street['street_count']
                    street['street_count'] = 0
                    street['busy'] = False
                    self._mongo.updateStreetById(street.get('_id'), street)

                self._logger.info('Assessor: I\'m calculating the QMI!')
                if len(streets) != 0:
                    swarm_data['qmi'] = math.sqrt(count/float(len(streets)))
                else:
                    swarm_data['qmi'] = 0.0

                swarm_data['end_at'] = self._helper.getTimeNow()
                swarm_data['active'] = False

                self._mongo.updateSwarmByIdentifier(swarm['identifier'], swarm_data)
                count_shutdonw += 1

        self._logger.info('Assessor: Shutdown '+str(count_shutdonw)+' swarms')
        print 'Shutdown '+str(count_shutdonw)+' swarms'

    def swarm_erase(self):

        try:
            mode_1 = raw_input("It's will stop all swarm. You are sure? Y/N\n")
            if mode_1.lower() == "y" or mode_1.lower() == "yes":
                mode_2 = raw_input("It's will erase all swarms, agents, graffitis and logs saved on Graphium. You are "
                                   "sure? Y/N\n")
                if mode_2.lower() == "y" or mode_2.lower() == "yes":

                    self.swarm_shutdown()

                    count = self._mongo.get_swarms().count()
                    self._mongo.swarm_erase_by_query({})
                    print str(count)+" erased swarms"

                    self.agent_erase()

                    self.graffiti_erase()

                    self.log_erase()
                else:
                    print "Ok, we no change anything."
            else:
                print "Ok, we no change anything."
        except ValueError:
            print "Not a number"

    def swarm_erase_by_id(self, args):

        if self._mongo.getSwarmByIdentifier(args.id) is None:

            print args.id+" is not a swarm identifier."

        else:

            try:
                mode_2 = raw_input("It's will ERASE a swarm, agents, graffitis and panos saved on Graphium. You are "
                                   "sure? Y/N\n")
                if mode_2.lower() == "y" or mode_2.lower() == "yes":

                    self._mongo.pano_erase_by_query({"swarm_identifier": args.id})
                    self._mongo.graffiti_erase_by_query({"swarm_identifier": args.id})
                    self._mongo.agent_erase_by_query({"swarm_identifier": args.id})
                    self._mongo.swarm_erase_by_query({"identifier": args.id})

                else:
                    print "Ok, we no change anything."
            except ValueError:
                print "Not a number"



    def agent_erase(self):
        count = self._mongo.get_agents().count()
        self._mongo.agent_erase_by_query({})
        print str(count)+" erased agents"

    def list_street(self, count):

        if count is None or count == False:
            print 'List of Streets'
            count_street = 0
            for street in self._mongo.getStreets():
                count_street += 1
                print "Name `"+street['name_osm']+"`"

            print str(count_street)+' streets.'

        else:
            print 'Count of Streets'
            print str(len(self._mongo.getStreets()))+" streets"

        self._logger.info('Assessor: List street')

    def list_config(self):
        print "Config list"

        print '\nGraphium'
        for key, value in self._g.config.items():
            print str(key)+": "+str(value)
        print '\nMongoDB'
        for key, value in self._g.mongodb.items():
            print str(key)+": "+str(value)
        print '\nOSM'
        for key, value in self._g.osm.items():
            print str(key)+": "+str(value)
        print '\nSwarm'
        for key, value in self._g.swarm.items():
            print str(key)+": "+str(value)
        print '\nGmaps'
        for key, value in self._g.gmaps.items():
            print str(key)+": "+str(value)
        print '\nScissor'
        for key, value in self._g.scissor.items():
            print str(key)+": "+str(value)
        print '\nOracle'
        for key, value in self._g.oracle.items():
            print str(key)+": "+str(value)
        print '\nAnalytics'
        for key, value in self._g.analytics.items():
            print str(key)+": "+str(value)

        self._logger.info('Assessor: List config')

    def log_erase(self):
        count = 0
        for log_folder in [ "api/", "assessor/", "geospatial/", "googleapi/",
                           "graphium/", "reader/", "session/", "swarm/" ]:
            dir_name = self._g.path_log()+log_folder
            test = os.listdir(dir_name)
            for item in test:
                if item.endswith(".log"):
                    os.remove(os.path.join(dir_name, item))
                    count += 1

        print str(count)+" erased logs."

    def session_list(self):
        print 'Session information'
        session = self._mongo.get_session()
        for row in range(len(session['g_key_usage_count'])):
            print "Key Position: "+str(row)
            print "Count       : "+str(session['g_key_usage_count'][row])
            print "First usage : "+str(datetime.datetime.strptime(session['g_key_data_start'][row], '%Y%m%d%H%M%S'))
            print "Last usage  : "+str(datetime.datetime.strptime(session['g_key_last_usage'][row], '%Y%m%d%H%M%S'))

    def graffiti_list(self):
        count = 0
        for graffiti in self._mongo.get_graffiti_by_query({}):
            count += 1
            print str(graffiti['_id'])+" swarm: "+graffiti['swarm_identifier']
        print str(count)+" graffiti."

    def graffiti_erase(self):
        count = self._mongo.get_graffiti_by_query({}).count()
        self._mongo.graffiti_erase_by_query({})
        print str(count)+" erased graffiti"

    def model_list(self):
        print 'not implemented yet.'

