# Definition

`Reader.py` allow you convert files `.osm` into a struct used by Graphium system.

## Params

**args**: Receive the params suchs the file to convert. `type:argparse`


## Methods

**start** : transform the file .osm in a mongodb struct.

**insertStreetInformationOSM**: insert the data from street at mongodb

**insertCityInformationOSM**: insert the information about the city at mongodb

**getCityAndCoutry**: Return the city on mongodb. `type:Dic`

**readShapeFromOpenStreet**: Get the shape with the information on ESRI shapefile.
