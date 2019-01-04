To run the application see below

### Reader
Before you need **load a dataset** from a city. You need populate the database to be processed with a swarm with N agents.
Bellow you can see how upload the city `Pelotas` database:

    cd swarm/
    python Main.py --mode reader --osm_path city_pelotas_full/ex_pelotas.osm


### Swarm
After upload the database – with reader mode – you can execute the a swarm with N agents to find images with a model.

Example: To **run at streets** with `5` agents at `Pelotas` city.

    python Main.py --mode swarm --swarm_city 59dd4d7b6a86370cb85d6be7
    
!!!note
    The `--swarm_city` identifier is unique created at upload moment, you need verify throw command `--rake city:list` the identifier inside your database.

### Assessor
At any time you can consult the system throw the Assessor command. You can consult list agents active, configurations and down swarm execution by command.
See list below:

    python Main.py --mode assessor --rake config:list
    
    python Main.py --mode assessor --rake swarm:list
    python Main.py --mode assessor --rake swarm:active
    python Main.py --mode assessor --rake swarm:shutdown
    python Main.py --mode assessor --rake swarm:erase
    
    python Main.py --mode assessor --rake agent:erase
    
    python Main.py --mode assessor --rake city:list
    
    python Main.py --mode assessor --rake street:list
    python Main.py --mode assessor --rake street:count
    
    python Main.py --mode assessor --rake graffiti:list
    python Main.py --mode assessor --rake graffiti:erase
    
    puthon Main.py --mode assessor --rake session:list
    
    python Main.py --mode assessor --rake log:erase


!!!warning
    `--rake :erase` on assessor **remove permanently**. Be careful about this command.
## Web Server

You can see throw the dashboard on web server at:

	cd ../webserver/app/
	rails s
	
Then, open you browser and go to [http://localhost:3000](http://localhost:3000).