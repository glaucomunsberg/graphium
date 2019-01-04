import json
import traceback
import os


class Graphium:

    _instance = None

    config = None
    mongodb = None
    osm = None
    swarm = None
    gmaps = None
    scissor = None
    oracle = None
    analytics = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Graphium, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):

        path = os.path.abspath(".")
        path = path.split("/")
        path = path[:-2]
        absolute_path = ""
        for pat in path:
            absolute_path += pat+"/"

        try:
            with open('../../data/configs/graphium.json', 'r') as f:
                self.config = json.load(f)
        except Exception, e:
            print "ERROR to upload graphium.json"
            print e
            print traceback.format_exc()
            return

        if absolute_path != self.config['path_root']:
            self.config['path_root'] = absolute_path
            try:
                with open('../../data/configs/graphium.json', 'w') as f:
                    json.dump(self.config, f)
            except Exception, e:
                print "ERROR to upload graphium config"
                print e
                print traceback.format_exc()

        try:
            with open(self.config['path_root']+self.config['path_config']+'mongodb.json', 'r') as f:
                self.mongodb = json.load(f)
        except Exception, e:
            print "ERROR to upload absolute config"
            print e
            print traceback.format_exc()

        try:
            with open(self.config['path_root']+self.config['path_config']+'osm.json', 'r') as f:
                self.osm = json.load(f)
        except Exception, e:
            print "ERROR to upload osm config"
            print e
            print traceback.format_exc()

        try:
            with open(self.config['path_root']+self.config['path_config']+'swarm.json', 'r') as f:
                self.swarm = json.load(f)
        except Exception, e:
            print "ERROR to upload swarm config"
            print e
            print traceback.format_exc()

        try:
            with open(self.config['path_root']+self.config['path_config']+'gmaps.json', 'r') as f:
                self.gmaps = json.load(f)
        except Exception, e:
            print "ERROR to upload gmaps config"
            print e
            print traceback.format_exc()

        try:
            with open(self.config['path_root']+self.config['path_config']+'scissor.json', 'r') as f:
                self.scissor = json.load(f)
        except Exception, e:
            print "ERROR to upload scissor config"
            print e
            print traceback.format_exc()

        try:
            with open(self.config['path_root']+self.config['path_config']+'oracle.json', 'r') as f:
                self.oracle = json.load(f)
        except Exception, e:
            print "ERROR to upload oracle config"
            print e
            print traceback.format_exc()

        try:
            with open(self.config['path_root']+self.config['path_config']+'analytics.json', 'r') as f:
                self.analytics = json.load(f)
        except Exception, e:
            print "ERROR to upload analytics config"
            print e
            print traceback.format_exc()

        if not len(self.gmaps['google_console_key']) == len(self.gmaps['limit_request_by_key']):
            print "WARNING 'google_console_key','limit_request_by_key' and 'limit_second_by_key' is wrong size!"

    def path_config(self):
        return self.config['path_root']+self.config['path_config']

    def path_log(self):
        return self.config['path_root']+self.config['path_log']

    def path_dataset(self):
        return self.config['path_root']+self.config['path_dataset']

    def path_picture(self):
        return self.config['path_root']+self.config['path_picture']

    def path_model(self):
        return self.config['path_root']+self.config['path_model']

    def version(self):
        return self.config['version']
