# Definition

The Mongo return a unique instance of Mongo. It content a list of methods that help write in mongo DB.

## Methods


### Agents

**getAgentByIdentifier**: Return the agent by Identifer. `type:Object`

**getAgentByName**: Like  `getAgentByIdentifier` but by name. `type:Object`

**updateAgentByName**: Update agente by name. `type:Boolean`

**updateAgentByIdentifier**: update agent by `identifier`. `type:Boolean`

**insertAgent**: Create a new agent in a swarm by your `identifier`. `type:String:Identifier`

**endAgent**: Finish their execution. `type:Boolean`

**getAgentsBySwarmIdentifier**: Get agents in swar my `identifier`. `type:List:Object`

**getAgentQuery**: Generic. `type:List`

**getAgentsActiveBySwarm**: Only active agents in swarm by `identifier`. `type:List`

**getAgentsEndWellBySwarm**: Return a list with agents that end well. `type:List`


### Users

**insertUser**: Create a new user. `type:String:Identifier`

**updateUserInformation**: Updat the email and date of user. `type:Boolean`

**getUsersQuery**: Generic. `type:List`

**removeUsers**: Remove user from mongo db. `type:Boolean`


### Streets

**getStreetByIdOSM**: Return the first street by `identifier`. `type:Object`

**getStreetByName**: Return the first street by `street name`. `type:Object`

**updateStreetById**: Update the street with id `identifier`. `type:Boolean`

**getStreetQuery**: Generic. `type:List`


### WishLists

**insertWishList**: Insert a wish List that is a street that pretend visit. `type:Boolean`

**removeWishList**: Remove a wish List by `query`. `type:Boolean`

**getWishListById**: get wishList by `id`. `type:Object`


### Swarms

**insertSwarm**: Insert a new swart at database . `type:String:Identifier`

**getSwarmByIdentifier**: Return the first object with `identifier` . `type:Object`

**updateSwarmByIdentifier**: update the swarm by `identifier`. `type:Boolean`

### Log

**addLog**: add log in a swarm `id`. `type:Boolean`


### Wish

**updateWishById**: update the wish by `id`. `type:Object`

**getWishListByIdentifier**: update the wish List by `Identifier`. `type:List`

**getWishListNoProccessedByIdentifier**: return only the streets in wishList not processed. `type:List`

**updateWishListById**: Upodat the wish list with `data`. `type:Boolean`


### Graffiti

**insertGraffiti**: Insert a graffiti in mongodb. `type:String:Identifier`
