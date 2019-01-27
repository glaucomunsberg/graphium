#!/usr/bin/env python
# -*- coding: utf-8 -*-


import traceback, argparse, socket

from system.Graphium import Graphium
from system.Mongo import Mongo
from system.Helper import Helper
from system.Logger import Logger
from anima.Looker import Looker

class Marionette:


    _g = None
    _args = None
    _mongo = None
    _helper = None
    _logger = None
    _looker = None
    _swarm_identifier = None
    _swarm_identifier_mirror = None

    def __init__(self, args):

        self._g = Graphium()
        self._mongo = Mongo()
        self._helper = Helper()
        self._logger = Logger('Marionette')
        self._args = args

    def start(self):

        if self._args.model_name is None:
            self._logger.info("Mirror: the model can't be empty")
            raise ValueError("Mirror: the model can't be empty")

        if self._args.swarm_identifier is None:
            self._logger.info("Mirror: the swarm Identifier can't be empty")
            raise ValueError("Mirror: the swarm Identifier can't be empty")

        mirror_swarm = self._mongo.getSwarmByIdentifier(self._args.swarm_identifier)

        if mirror_swarm is None:
            self._logger.info("Mirror: the swarm don't exits. Please, choose a valid swarm.")
            raise ValueError("Mirror: the swarm don't exits. Please, choose a valid swarm.")

        self._swarm_identifier = self._helper.getSerialNow()

        if self._mongo.getSwarmByIdentifier(self._swarm_identifier) is None:
            self._mongo.insertSwarm(self._swarm_identifier, 0, "marionette", self._helper.getTimeNow(), self._helper.getTimeNow(), socket.gethostbyname(""), 0, 0, mirror_swarm['city_id'], self._args.model_name)

        self._looker = Looker(self._swarm_identifier, self._logger)

        for pano in self._mongo.get_pano_by_query({"swarm_identifier":self._args.swarm_identifier}):

            dataPoint = {}
            dataPoint['image_path'] = self._g.path_picture() + "google_street_view/"+pano['imagem_name']
            dataPoint['swarm_identifier'] = self._swarm_identifier
            dataPoint['pano_id'] = pano['pano_id']
            dataPoint['heading'] = pano['heading']
            dataPoint['splited'] = "0"
            dataPoint['file_name'] = pano['imagem_name']

            #dataPoint['classification'] = "?"
            #dataPoint['probability'] = "?"

            dataPoint['lat'] = pano['lat']
            dataPoint['lng'] = pano['lng']
            dataPoint['pitch'] = "0"
            dataPoint['country'] = ""
            dataPoint['state'] = ""
            dataPoint['city'] = ""

            self._looker.checkPointToPredict(dataPoint, None)
