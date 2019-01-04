# Definition

`Assessor.py` allow commands to read or change data from execution or configuration

## Attributes

**args**: argparse. `type:argparse`

## Methods

**start**: Read --rake args params and execute command.

**list_city**: List all cities was upload after.

**swarm_list**: List all swarms in database.

**swarm_active**: List only swarms active.

**swarm_shutdown**: Command to shutdowm all swarms that is online.

**swarm_erase**: ERASE all information about swarms, agents, logs e graffiti.

**agent_erase**: ERASE all agents information in database.

**list_street**: List all street in database.

**list_config**: List configuration in `/data/configs/*.json` files

**log_erase**: Remove all files *.log in `/data/logs/`

**session_list**: Print information about key usage.

**graffiti_list**: List all graffiti

**graffiti_erase**: ERASE all graffiti in database.