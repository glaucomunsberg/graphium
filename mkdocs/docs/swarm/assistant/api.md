# Definition

`API.py` connect to OsmAPI.

## Params

**usermme**: name in API. `type:Stirng`

**password**: password in API. `type:Stirng`


## Methods

**getWaysByNode** : Get the routes that the dot is a bit.

**getPanoByPoint**: Return the image pano form this point. `type:Dic`

**getPanoInfoByPoint**: Return the information of this point (lat,lng). `type:Dic`

**getStreetGeocodeInfoFromMaps**: Get street Geo Code information suchs country,city, address from `Google Maps`.

**getStreetGeoCodeInfoFromOSM**: Get street Geo Code information suchs country,city, address from `Open Street Maps`
