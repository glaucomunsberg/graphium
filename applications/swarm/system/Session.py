from Mongo import Mongo
from Graphium import Graphium
from Logger import Logger


class Session:
    _mongo = None
    _g = None
    _logger = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Session, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, logger=None):

        self._mongo = Mongo()
        self._g = Graphium()

        if logger is None:
            self._logger = Logger('Session')
        else:
            self._logger = logger

        if self._mongo.get_session() is None:
            g_key_data_start = [None] * len(self._g.gmaps['google_console_key'])
            g_key_last_usage = [None] * len(self._g.gmaps['google_console_key'])
            g_key_usage_count = [0] * len(self._g.gmaps['google_console_key'])

            session_data = {'g_key_data_start': g_key_data_start,
                            'g_key_usage_count': g_key_usage_count,
                            'g_key_last_usage': g_key_last_usage}

            self._mongo.create_session(session_data)
            self._logger.info("Session: Creating a Session on database")
        else:
            self._logger.info("Session: Restored session from database")

    def get_info(self):
        return self._mongo.get_session()

    def update_key_data_start(self, position, date_string):
        session = self._mongo.get_session()
        session['g_key_data_start'][position] = date_string
        self._mongo.update_session(session)

    def update_key_last_usage(self, position, date_string):
        session = self._mongo.get_session()
        session['g_key_last_usage'][position] = date_string
        self._mongo.update_session(session)

    def update_key_count_usage(self, position):
        session = self._mongo.get_session()
        session['g_key_usage_count'][position] += 1
        self._mongo.update_session(session)

    def reset_key_count_usage(self, position):
        session = self._mongo.get_session()
        session['g_key_usage_count'][position] = 0
        self._mongo.update_session(session)