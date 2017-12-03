# Definition

`Looker.py` look to google street view with point received from `Geospatial.py` and get the images of sides (left and right) with a instance of `API.py`.

## Params

**swarm_identifier**: a string with swarm identifier. `type:String`

**logger**: a instance of logger or `None`. `type:Logger`


## Methods

**driveFromPointToPoint**: received two points find the intermediate points, logo to left and right of each point and send the image to Oracle analyze.

**checkPointToPredict**: Check if in point the Oracle identify something if true sabe the informations
