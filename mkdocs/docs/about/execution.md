## Commands

Before you need **load a dataset** from a city. You need populate the database to be processed with a swarm with N agents.
Bellow you can see how upload the city `Pelotas` database:

    cd swarm/
    python Main.py --mode reader --osm_path city_pelotas_full/ex_pelotas.osm


After upload the database – with reader mode – you can execute the a swarm with N agents to find images with a model.

Example: To **run at streets** with `5` agents at `Pelotas` city.

    python Main.py --mode swarm --swarm_city 59dd4d7b6a86370cb85d6be7


## Web Server

You can see throw the dashboard on web server at:

	cd ../webserver/app/
	rails s
	
Then, open you browser and go to [http://localhost:3000](http://localhost:3000).