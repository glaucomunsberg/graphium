# Swarm

The swarm allow you search in google street map. Try execute the `Main.py` class.

## Commands

Start using a city such `Pelotas`.

    python Main.py --mode swarm --swarm_city 59dd4d7b6a86370cb85d6be7 --model_name 20190120203800


#### Arguments

* **--swarm_identifier**: Identifier of swarm. Empty the instance will be created else get information from db . Default `None`.

* **--swarm_name**: name of swarm. If empty full with datatime

* **--user_email**: Email to identify the user. Default `admin@graphium.com`.

* **--swarm_num_agent**: Number of agents to work

* **--swarm_city**: City to crawler.
