# Welcome to Graphium

Graphium help you to walk in google street view and use IA to find elements learned.

## Commands

**Create a dataset** from `Pelotas` data to be processed in a swarm with N agents.

    cd swarm/
    python Main.py --mode reader --osm_path city_pelotas/ex_pelotas.osm


**Run at streets** with `5` agents at `Pelotas` city.

    python Main.py --mode swarm --swarm_city 59dd4d7b6a86370cb85d6be7


## Web Server

You can control everting on web server at:

	cd ../webserver/app/
	rails s

## Project layout

    data/           # folder with all data generate by applications.
        configs/
        datasets/
        logs/
    applications/   # applications suches crawler, analyzers etc
        swarm/
        webserver/
    docs/           # documentation of Graphium
    mkdocs/         # generator of documentation
