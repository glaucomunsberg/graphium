#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, datetime, traceback, math, argparse
from time import sleep

from system.Graphium import Graphium
from system.Mongo import Logger
from system.Helper import Logger
from system.Logger import Logger
from Agent import Agent

class Swarm:

    _agents         = []
    _identifier     = None
    _config         = None
    _swarm_config   = None
    _mongo          = None
    _helper         = None
    _logger         = None
    _name           = None
    _end_well       = None
    _swarm_at_mongo = None
    _host           = None


    def __init__(self, args):

        self._g        = Graphium()
        self._mongo    = Mongo()
        self._helper   = Helper()
        self._logger   = Logger('Swarm')
        self._args     = args

        self._host     = socket.gethostbyname(socket.gethostname())

        # start basic information about swarm session
        self._logger.debug('Swarm: We are configure my settings...')

        if args.swarm_identifier == None:
            self._identifier        = self._helper.getSerialNow()
        else:
            self._identifier        = args.swarm_identifier

        if args.swarm_name == None:
            self._name = self._helper.getTimeNow()
        else:
            self._name = args.swarm_name

        if args.swarm_city == None:
            self._logger.info("Swarm: the city can't be empty")
            raise ValueError("Swarm: the city can't be empty")

        if self._mongo.getSwarmByIdentifier(self._identifier) == None:
            self._mongo.insertSwarm(self._identifier, args.swarm_num_agent, args.user_email, self._name, self._host, self._g.swarm['swarm_turns'], self._g.swarm['swarm_cycles'], args.swarm_city)

        self.syncFromDB()

    def syncFromDB(self):
        self._swarm_at_mongo    = self._mongo.getSwarmByIdentifier(self._identifier)

    # Start the agents
    def start(self):

        self._logger.debug('Swarm: Let starting agents...')
        try:
            while self._swarm_at_mongo['active']:

                self._logger.info('%s: I\'m checking the agents status!' % ("Swarm"))
                #print 'Swarm are checking the agents'
                num_active_and_end_well = len(self._mongo.getAgentsActiveBySwarm(self._identifier))
                num_active = num_active_and_end_well
                num_active_and_end_well += len(self._mongo.getAgentsEndWellBySwarm(self._identifier))
                self.syncFromDB()
                if num_active_and_end_well < self._swarm_at_mongo['num_agent']:

                    create_agents_number = self._swarm_at_mongo['num_agent'] - num_active_and_end_well
                    print 'Creating', create_agents_number, 'agents'

                    for i in range(create_agents_number):
                            agent = Agent(self._identifier)
                            self._agents.append(agent)
                            agent.start()

                # Sleep x seconds to check again
                #
                sleep(int(self._swarm_at_mongo['seconds_to_check_agents']))
                self.syncFromDB()
                if len(self._mongo.getAgentsActiveBySwarm(self._identifier)) == 0 and len( self._mongo.getStreetQuery({'street_count':0,'city_id': self._swarm_at_mongo['city_id']})) == 0:
                    self._logger.info('Swarm: All streets were coveraged. I\'m done =D')
                    self._swarm_at_mongo['active']      = False


        except Exception as error:
            self._logger.error('Swarm: Swarm die! x(')
            print 'Error:'
            print traceback.format_exc()
            self._logger.critical(str(error))
            self._swarm_at_mongo['end_well'] = False
        finally:
            self.finish()


    def finish(self):
        for agent in self._agents:
            agent.join()

        streets = self._mongo.getStreetQuery({"city_id": self._swarm_at_mongo['city_id']})

        count = 0
        for street in streets:
            count += street['street_count']*street['street_count']
            street['street_count'] = 0
            street['busy'] = False
            self._mongo.updateStreetById(street.get('_id'),street)

        if len(streets) != 0:
            self._logger.info('%s: I\'m calculating the QMI!' % ("Swarm"))
            self._swarm_at_mongo['qmi'] = math.sqrt(count/float(len(streets)))
        else:
            self._swarm_at_mongo['qmi'] = 0.0

        self._swarm_at_mongo['end_at']      = self._helper.getTimeNow()
        self._swarm_at_mongo['active']      = False

        self._mongo.updateSwarmByIdentifier(self._swarm_at_mongo['identifier'],self._swarm_at_mongo)

        self._logger.info('Swarm: Hard work! I finish dude ;)')
