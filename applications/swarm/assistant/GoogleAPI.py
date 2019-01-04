#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
import time

sys.path.append('../')

from system.Graphium import Graphium
from system.Logger import Logger
from system.Session import Session
from system.Helper import Helper
from system.Mongo import Mongo


class GoogleAPI:
    _instance = None
    _g = None
    _helper = None
    _mongo = None
    _logger = None
    _session = None
    _keys = []
    _logger = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GoogleAPI, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, logger=None):

        if logger is None:
            self._logger = Logger('GoogleAPI')
        else:
            self._logger = logger

        self._g = Graphium()
        self._mongo = Mongo()
        self._session = Session()
        self._helper = Helper()

        self._g_keys = self._g.gmaps['google_console_key']
        self._g_keys_secrets = self._g.gmaps['google_console_secret']
        self._g_limit_request = self._g.gmaps['limit_request_by_key']
        self._g_limit_time = self._g.gmaps['limit_time_by_key']

        self._logger.info('%s: Let start the job! =D' % ("GoogleAPI"))

    def get_authorization_key(self):

        authorized = True

        while authorized is True:

            authorized_google_api_protocol = self.authorizing_key()
            authorized = authorized_google_api_protocol['authorized']
            key_position = authorized_google_api_protocol['key_position']

            if authorized is True:
                return authorized_google_api_protocol
            else:
                sleep_time = self.time_do_sleep_by_key(key_position)
                print "I'll sleep for "+str(sleep_time)+" seconds! Google need a break now"

                time_start = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                elapsed = 0
                while elapsed < sleep_time:

                    elapsed = self._helper.get_time_elapsed(time_start, datetime.datetime.now().strftime("%Y%m%d%H%M%S"))

                    sleep_seconds = sleep_time*.10
                    if sleep_seconds <= 1:
                        # last request sleep to 1 minute or 60 seconds
                        sleep_seconds == 60
                        self._logger.info("GoogleAPI: Last sleep for this request")

                    self._logger.info("GoogleAPI: Need sleep for "+str(sleep_seconds)+" seconds")
                    time.sleep(sleep_seconds)

                # time.sleep(sleep_time)

    def get_best_key_position(self):

        session_info = self._session.get_info()
        keys_counts = session_info['g_key_usage_count']
        position = keys_counts.index(min(keys_counts))
        self._logger.info('GoogleAPI: Best position %s' % (str(position)))

        return position

    def authorizing_key(self):

        session_info = self._session.get_info()

        position = self.get_best_key_position()

        authorized_protocol = dict()
        authorized_protocol['authorized'] = False
        authorized_protocol['key_position'] = position
        authorized_protocol['key'] = ""
        authorized_protocol['key_secret'] = ""
        authorized_protocol['key_message'] = "Empty action"

        time_now_string = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        # get authorized key
        # if the key is last used to limit
        # then limit of time is ok
        if session_info['g_key_data_start'][position] is None:
            self._logger.info("GoogleAPI: Position %s is None" % (str(position)))

            session_info['g_key_data_start'][position] = time_now_string
            session_info['g_key_last_usage'][position] = time_now_string

            self._session.update_key_data_start(position, time_now_string)
            self._session.update_key_last_usage(position, time_now_string)

            authorized_protocol['authorized'] = True
            authorized_protocol['key'] = self._g_keys[position]
            authorized_protocol['key_secret'] = self._g_keys_secrets[position]
            authorized_protocol['key_position'] = position
            authorized_protocol['key_message'] = "Valid key, restarted"

        time_elapsed = self.time_elapsed_by_key(position)

        if time_elapsed > self._g_limit_time[position]: # time elapsed
            self._logger.info("GoogleAPI: Position %s need be restart" % (str(position)))

            session_info['g_key_data_start'][position] = time_now_string
            session_info['g_key_last_usage'][position] = time_now_string
            session_info['g_key_usage_count'][position] = 0

            self._session.update_key_data_start(position, time_now_string)
            self._session.update_key_last_usage(position, time_now_string)
            self._session.reset_key_count_usage(position)

            authorized_protocol['authorized'] = True
            authorized_protocol['key'] = self._g_keys[position]
            authorized_protocol['key_secret'] = self._g_keys_secrets[position]
            authorized_protocol['key_position'] = position
            authorized_protocol['key_message'] = "Valid key, under limit"

        if session_info['g_key_usage_count'][position] < self._g_limit_request[position]:
            self._logger.info("GoogleAPI: Position %s counter is OK" % (str(position)))

            session_info['g_key_last_usage'][position] = time_now_string
            session_info['g_key_usage_count'][position] = session_info['g_key_usage_count'][position]+1

            self._session.update_key_last_usage(position, time_now_string)
            self._session.update_key_count_usage(position)

            self._logger.info('Authorized %s position' % (str(position)))

            authorized_protocol['authorized'] = True
            authorized_protocol['key'] = self._g_keys[position]
            authorized_protocol['key_position'] = position
            authorized_protocol['key_secret'] = self._g_keys_secrets[position]
            authorized_protocol['key_message'] = "Valid key, under limit"

            return authorized_protocol

        else:
            self._logger.info("GoogleAPI: Cant authorize %s position" % (str(position)))

            authorized_protocol['authorized'] = False
            authorized_protocol['key'] = ""
            authorized_protocol['key_position'] = position
            authorized_protocol['key_secret'] = ""
            authorized_protocol['key_message'] = "Invalid key, on limit!"

            return authorized_protocol

    def time_elapsed_by_key(self, position):
        session_info = self._session.get_info()
        time_now_string = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        time_elapsed = self._helper.get_time_elapsed(session_info['g_key_data_start'][position], time_now_string)

        self._logger.info("GoogleAPI: Time elapsed "+str(time_elapsed)+" to position "+str(position))
        return time_elapsed

    def time_elapsed_usage_by_key(self, position):
        session_info = self._session.get_info()
        time_elapsed = self._helper.get_time_elapsed(session_info['g_key_data_start'][position], session_info['g_key_last_usage'][position])

        self._logger.info("GoogleAPI: Time usage elapsed "+str(time_elapsed)+" to position "+str(position))
        return time_elapsed

    def time_do_sleep_by_key(self, position):
        return self._g_limit_time[position] - self.time_elapsed_by_key(position)

    def get_key(self, position):
        return self._g_keys[position]

    def get_key_secret(self, position):
        return self._g_keys_secrets[position]

    # Use only if you really need use a position out of `get_authorization_key()` function
    def force_use_key_position(self, position):
        time_now_string = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        if self._session.get_info()['g_key_data_start'][position] is None:
            self._session.update_key_data_start(position, time_now_string)

        self._session.update_key_last_usage(position, time_now_string)
        self._session.reset_key_count_usage(position)
