To run the application see below, the first step [Reader](#reader) you load the city geographic data, after that you run [Swarm](#swarm) to check the streets with your model, at last you can use [WebServer](#web-server) to view the swarm running or show results after executation. 

If you want erase an execution, or list elements suchs swarms, agents, cities, streets use [Assessor Commands](#assessor).

### Reader
Before you need **load a dataset** from a city. You need populate the database to be processed with a swarm with N agents.
Bellow you can see how upload the city `Pelotas` database:

    cd swarm/
    python Main.py --mode reader --osm_path city_pelotas_full/ex_pelotas.osm


### Swarm
After upload the database – with reader mode – you can execute the a swarm with N agents to find images with a model.

Example: To **run on streets** with `5` agents at `Pelotas` city with model `20190120203800.h5`.

    python Main.py --mode swarm --swarm_city 59dd4d7b6a86370cb85d6be7 --model_name 20190120203800
    
!!!note
    The `--swarm_city` identifier is unique created at upload moment, you need verify throw command `--rake city:list` the identifier inside your database.

### Assessor
At any time you can consult the system throw the Assessor command. You can consult list agents active, configurations and down swarm execution by command.
See list below:

    python Main.py --mode assessor --rake config:list
    
    python Main.py --mode assessor --rake swarm:list
    python Main.py --mode assessor --rake swarm:active
    python Main.py --mode assessor --rake swarm:shutdown
    python Main.py --mode assessor --rake swarm:erase  --id <SWARM_ID>
    
    python Main.py --mode assessor --rake swarms:erase
    
    python Main.py --mode assessor --rake agents:erase
    
    python Main.py --mode assessor --rake city:list
    
    python Main.py --mode assessor --rake model:list
    
    python Main.py --mode assessor --rake street:list
    python Main.py --mode assessor --rake street:count
    
    python Main.py --mode assessor --rake graffiti:list
    
    python Main.py --mode assessor --rake graffitis:erase
    
    puthon Main.py --mode assessor --rake session:list
    
    python Main.py --mode assessor --rake logs:erase


!!!warning
    `--rake :erase` on assessor **remove permanently**. Be careful about this command.
## Web Server

Go to `applications/web_server` and run the code bellow:

````bash
$ rails s
````

Then, open you browser and go to [http://localhost:3000](http://localhost:3000). To access admin dasboard you need use default user `admin@graphium.com` and password `1234567890`.


!!!info
    Check if you install RoR in [Instalation Section](../about/installation/ubuntu_16.04.md).
    
!!!info
    Check if you [run/running a swarm](../swarm/index.md).
	
