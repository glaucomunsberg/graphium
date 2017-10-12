import json, traceback, os

class Graphium:

    _instance   = None

    config      = None
    mongodb     = None
    osm         = None
    swarm       = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Helper, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):

        path = os.path.abspath(".")
        path = path.split("/")
        path = path[:-2]
        absolute_path = ""
        for pat in path:
            absolute_path+=pat+"/"

        try:
            with open('../../data/configs/graphium.json', 'r') as f:
                self.config = json.load(f)
        except:
            print "ERROR to load graphium.json"
            print traceback.format_exc()
            return

        if absolute_path != self.config['path_root']:
            self.config['path_root'] = absolute_path
            try:
                with open('../../data/configs/graphium.json', 'w') as f:
                    json.dump(self.config, f)
            except:
                print "ERROR to update config absolute path"
                print traceback.format_exc()

        try:
            with open(self.config['path_root']+self.config['path_config']+'mongodb.json', 'r') as f:
                self.mongodb = json.load(f)
        except:
            print "ERROR to update mongodb absolute path"
            print traceback.format_exc()

        try:
            with open(self.config['path_root']+self.config['path_config']+'osm.json', 'r') as f:
                self.osm = json.load(f)
        except:
            print "ERROR to update osm absolute path"
            print traceback.format_exc()

        try:
            with open(self.config['path_root']+self.config['path_config']+'swarm.json', 'r') as f:
                self.swarm = json.load(f)
        except:
            print "ERROR to update swarm absolute path"
            print traceback.format_exc()

    def path_config(self):
        return self.config['path_root']+self.config['path_config']

    def path_log(self):
        return self.config['path_root']+self.config['path_log']

    def path_dataset(self):
        return self.config['path_root']+self.config['path_dataset']

    def version(self):
        return self.config['version']
