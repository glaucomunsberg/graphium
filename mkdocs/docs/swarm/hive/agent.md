# Definition

`Agent.py` is a class  in Thread that walk in a street.

## Params

**swarm_identifier**: a identifier. `type:Stirng`


## Methods

**run** : start the executation.

**updateRule** : Update the Street's counter.

**nodeByNode**: calcule the distance between two dots in meters. `type:Int`

**firstNode**: execute only on first node.

**lastNode**: execute only on last node.

**lastNode**: call when we have only one node at street.

**chooseTheFirstStret**: Method to choose the first street to try walk. First choose a way from wishlist else a aleatory way. `type:Street`

**chooseTheFirstStret**: After walk one street new need choose de next this method choose the way with less count and return. If any way cross he then we need get other way how? Go to other agent =]. `type:Street`

**fastChooseTheNextStret**: this method choose the fast way: check the list of wish, if empty choose the fist road that is not busy and count igual 0. `type:Street`

**choosingNewStreetToNavegate**: choose the street with the less weight to navegate. `type:Street`

**appendPathBread**: update the lat and lng of agent set at pathbread of agent.

**appendStreetVisited**: insert the name of the street if agent are not visited yet.

**startAgent**: Set the name, start the mongo information and others actions.

**finish**: Set information about agent at db and close at db.

**getIdentifier**: Return the identifier. `type:Identifier`

**setIdentifier**: set the identifier.

**setAgentName**: Return the agent name.
