# Definition

The graphium return a instance of Graphium. It is a Dic with many configs what you can see inside the directory `data/configs/`

## Attributes

**config** : the metadata of configuration has default. The file `data/configs/graphium.json` is load to system.`type:Dic`

Keys inside attribute config:

    {
        "path_root": "<PATH>/kootstrap/",
        "path_log":"data/logs/",
        "path_config":"data/configs/",
        "path_dataset":"data/datasets/",

        "log_level":"INFO",
        "version":"0.0.1"
    }

**mongodb** : the metadata of mongoDB used has default. The file `data/configs/mongodb.json` is load to system. `type:Dic`

Keys inside attribute Mongod:

    {
        "mongo_db":"graphium",
        "mongo_host":"localhost",
        "mongo_port":27017
    }

**osm** : the metadata of Open Street Map used has default. The file `data/configs/osm.json` is load to system. `type:Dic`

Keys inside attribute OSM:

    {
      "use_urban_ways": true,
      "use_motorways": true,
      "use_othersways":false,
      "urban_highway_tipes": ["tertiary", "road", "residential", "service", "living_street", "pedestrian", "bus_guideway", "steps","secondary", "trunk", "primary"],
      "motorways_highway_tipes": ["motorway", "escape"],
      "others_highway_tipes": ["track"]
    }

**swarm** : the metadata of Swarm used has default. The file `data/configs/swarm.json` is load to system. `type:Dic`

Keys inside attribute Swarm:

    {
      "swarm_turns": 3,
      "swarm_cycles": -1,
      "swarm_agent_names_API": "http://namey.muffinlabs.com/name.json?with_surname=true&frequency=all",
      "swarm_agent_names": ["Coralina Malaya","Abigail Johnson","Antonietta Marinese","Elisa Rogoff","Serafim Folkerts", "Dulce Barrell"],
      "swarm_agent_colors": ["#E91E63", "#9C27B0", "#F44336", "#673AB7", "#3F51B5", "#2196F3", "#00BCD4", "#009688", "#4CAF50", "#CDDC39", "#FF9800","#795548","#FF5722","#607D8B","#9E9E9E","#827717"]
    }

**gmaps** : the metadata of google street maps used has default. The file `data/configs/gmaps.json` is load to system. `type:Dic`

Keys inside attribute Gmap:

  {
    "width": 640,
    "height": 450,
    "google_key": "AIzaSyB6_XPVntnTJHG9jN9OrO11ou8GEV77qOM",
    "limit_maps_by_day": 25000
  }

**scissor** : the metadata of scissor used has default. The file `data/configs/scissor.json` is load to system. `type:Dic`

Keys inside attribute Scissor:

    {
        "target_max_width":224,
        "target_max_height":224,
        "target_min_width":224,
        "target_min_height":224,
        "target_rate":0.8
    }
    
**oracle** : the metadata of oracle used has default. The file `data/configs/oracle.json` is load to system. `type:Dic`

Keys inside attribute Oracle:

    {
        "model_name": "20170821191051"
    }

**analytics** : the metadata of analytics used has default. The file `data/configs/analytic.json` is load to system. `type:Dic`

Keys inside attribute Analytics:

    {
        "time_between_analises": 120
    }


## Methods

**path_config**: Return absolute path to configurations of koopstrap. `type:String`

**path_log**: Return absolute path to logs of system. `type:String`

**path_dataset**: Return absolute path to all datasets. `type:String`

**path_model**: Return absolute path to all models. `type:String`

**path_picture**: Return absolute path to all images on directory. `type:String`

**version**: Return version of koopstrap. `type:String`
