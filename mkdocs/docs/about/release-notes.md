# Release Notes


## Version 0.0.7

* `Anima`: `Looker.py` appending Pano on database
* `System`: `Assessor.py` a new tools to seed and change information on datbase
* `System`: `Graphium.py` appending analytics.json information
* `System`: `Mongo.py` suport to pano collection
* `Assistant`: `Analytics` new classe to report use of memory
* `Assistant`: `API.py` improved get Google Pano
* `Assistant`: `GoogleAPI` improved to authorizing_key from Google Console request
* `Assistant`: `GoogleSigning` signing the request on `GoogleAPI`

## Version 0.0.6

* `Anima`: `Oracle.py` fixing google request
* `Anima`: `Looker.py` improved get hostname
* `Anima`: Identifying memory leaks with pympler
* `Webserver`: `Database` sqlite3 to MySQL

## Version 0.0.5    

* `Anima`: `Oracle.py` now whit model params form json file
* `System`: With `Session.py` to control accesses on google API
* `Assistent`: Controller `GoogleAPI.py` to many Google Console Keys
* `Docs`: With Google Material

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
* `System`: Graphium receive the picture folder to not request two time the same pano_image. Google restricts 25.000 requests by day

## Version 0.0.1

* Project start based on old graphium project
