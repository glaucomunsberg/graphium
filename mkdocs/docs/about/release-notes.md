# Release Notes

## Version 0.0.4

* `Anima`: fixing insertGraffiti call
* `Anima`: `Looker.py` receive the swarm_identifier now
* `Assistant`: Into `API.py` the limit of google maps API request
* `Hive`: `Swarm.py` improved to set the date start and number of request from agents in google maps api
* `System`: improved the `Mongo.py` to google maps interactions

## Version 0.0.3

* `Anima`: The `Looker.py` moved into Package and create
* `Anima`: `Oracle.py` class responsible by predictions models
* `Assistant`: Intro `Scissor.py` to cut images. `API.py` moved into this Package
* `Assistant`: `Reader.py` improved to make a place – without city information – a fictional city
* `Hive`: Agents now drive between two dots
* `System`: improved the `Graphium.py` to scissor information

## Version 0.0.2

* `Assistant`: Intro `GeoSpatial.py` to cal distance and intermediate points of system
* `Assistant`: Intro `Looker.py` search the pictures on google street view
* `Hive`: Improved the `Agent.py` and `API.py`
* `System`: Now the `Graphium.py` has the config to download images from Google Street View
* `System`: Graphium receive the picture folder to not request two time the same pano image. Google restricts 25.000 requests by day

## Version 0.0.1

* Project start baseded on old graphium project
