You can configure parameters from execution on Graphium. All configuration are in `data/configs/` folder. 
Each json file was created to encapsulate a scope of application.

List of configuration files

* [analytics.json](#analytics-configuration)
* [gmaps.json](#gmaps-configuration)
* [graphium.json](#graphium-configuration)
* [mongodb.json](#mongodb-configuration)
* [oracle.json](#oracle-configuration)
* [osm.json](#osm-configuration)
* [scissor.json](#scissor-configuration)
* [swarm.json](#swarm-configuration)


!!!info
    Annotation in configurations files is in JSON format.

!!!warning
    Be careful to customize, when you change configuration, this can change swarm and agent behavior.
    
    
## Graphium Configuration

`graphium.json` have a base information to execution. Such path to model, log level and path to configuration. 

See below a example `graphium.json`

    {
        "path_picture": "data/pictures/", 
        "log_level": "INFO", 
        "path_root": "/Users/.../Projetos/graphium/", 
        "path_dataset": "data/datasets/", 
        "path_model": "data/models/", 
        "version": "0.0.4", 
        "path_log": "data/logs/", 
        "path_config": "data/configs/"
    }
    
## Swarm Configuration

`swarm.json` you find swarm configuration to start and execute the swarm. 
Configure the `swarm_turns` to change number of agents, `swarm_cycles` to define a number of execution on each agents.

See below a example of `swarm.json`

    {
      "swarm_turns": 3,
      "swarm_cycles": -1,
      "swarm_agent_names_API": "http://namey.muffinlabs.com/name.json?with_surname=true&frequency=all",
      "swarm_agent_names": ["Coralina Malaya", ... , "Dulce Barrell"],
      "swarm_agent_colors": ["#E91E63", ... ,"#827717"]
    }
    
## Oracle Configuration

`oracle.json` you configure the model used on oracle function.

!!! info
    Don't forget to put model_name.h5 on folder `data/models/`
    
See below a example of `oracle.json`
    
    
    {
      "model_name": "20170821191051"
    }
    
    
## Scissor Configuration

`scissor.json` you configure the model cut images. Use the `max` and `min` to define the frame of the cut. 
`target_rate` allow you to remove borders on image range 0 to 1. 

!!!warning
    Be careful, the image cut and size need be exactly the model load on Oracle.
    
See below a example of `oracle.json`
    
    
    {
        "target_max_width":224,
        "target_max_height":224,
        "target_min_width":224,
        "target_min_height":224,
        "target_rate":0.8
    }
    
## Gmaps Configuration

`gmaps.json` you configure the **Google Console Keys** and the size of images. The `width` and `height` set size of image get in Google Street View API,
the `google_console_key`,`google_console_secret`,`limit_request_by_key` and `limit_time_by_key` are a list of console access used on API class.

!!!annotation
    Read more about [Google Console Keys](/data/google_api).
    
    
!!!info
    The `limit_time_by_key` is 24h to limit in `limit_request_by_key` requests.
    
!!!warning
    Set `limit_request_by_key` to not exceed the limit of your account.
    
See below a example of `gmaps.json`
    
    
    {
      "width": 640,
      "height": 450,
      "google_console_account": ["<ACCOUNT_NAME>"],
      "google_console_key": ["<ACCOUNT_KEY>"],
      "google_console_secret": ["<ACCOUNT_KEY_SECRET>"],
      "limit_request_by_key": [25000],
      "limit_time_by_key": [86400]
    }
    
## MongoDB Configuration

`mongodb.json` you configure MongoDB connection. See below a example of `mongodb.json`
    
    {
      "mongo_db": "graphium",
      "mongo_host": "localhost",
      "mongo_port": 27017
    }

## OSM Configuration

`osm.json` you configure Open Street Maps (OSM). Each street is labeled with a type, where you can compile what is urban street. Disable types are possible.
    
!!! annotation
    If you disable a street type all street labeled will not load to database.
    
See below a example of `osm.json`
    
    {
      "use_urban_ways": true,
      "use_motorways": true,
      "use_othersways":false,
      "urban_highway_tipes": ["tertiary", "road", "residential", "service", "living_street", "pedestrian", "bus_guideway", "steps","secondary", "trunk", "primary"],
      "motorways_highway_tipes": ["motorway", "escape"],
      "others_highway_tipes": ["track"]
    }
    
    
## Analytics Configuration

`analytics.json` you configure how the system. The `time_between_analises` is set to 120 seconds.
    
!!! warning
    Not set a low limit, it's will affect performance.
    
See below a example of `analytics.json`
    
    {
      "time_between_analises": 120
    }


