# Definition

`API.py` connect to OsmAPI.

## Params

**swarm_identifier**: swarm identifier. `type:Stirng`

**logger**: Logger to use in API. `type:Logger`


## Methods

**getWaysByNode** : Get the routes that the dot is a bit.

**getPanoByPoint**: Return the image pano form this point. `type:Dic`

**getPanoInfoByPoint**: Return the information of this point (lat,lng). `type:Dic`

**getStreetGeocodeInfoFromMaps**: Get street Geo Code information suchs country,city, address from `Google Maps`.

**getStreetGeoCodeInfoFromOSM**: Get street Geo Code information suchs country,city, address from `Open Street Maps`
