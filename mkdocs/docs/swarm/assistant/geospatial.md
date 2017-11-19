# Definition

`Geospatial.py` mensure to you the distance between two points or for example slice two points at many points with the same distance between them.

## Params

**logger**: a instance of logger or `None`. `type:Logger`


## Methods

**getDistance** : Return the distance bewteen two dots. `type:float`

**getIntermediatePointsFromTwoDots**: Return intermediate points between two dots if the distance bewteen them is great that distanceMax. `type:List`

**calculateStreetOrientation**: Return the `bearing` or the direction (degrees) of the points `type:Float`

**getIntermediatePointsFromTwoCoordinates**: the same of `getIntermediatePointsFromTwoDots` but not receive a tuple, but the 4 values (lat1,lng1,lat2,lng2)
