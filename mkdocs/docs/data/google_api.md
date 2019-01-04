## Google Console

Make sure that those APIs are enabled in google account linked in `google.json` file:

* [Geocoding API](https://developers.google.com/maps/documentation/geocoding/start?hl=en_US)
* [Street View Static API](https://developers.google.com/maps/documentation/streetview/intro?hl=en_US)
* [Map Javascript API](https://developers.google.com/maps/documentation/javascript/tutorial?hl=en_US)


### Test APIs

Change `YOUR_KEY` for a valid [API Key/Credential](https://cloud.google.com/docs/authentication/api-keys?hl=en&authuser=0&visit_id=636767679260970986-778433860&rd=1) used in `gmaps.json`

#### Google Geocode API

    https://maps.googleapis.com/maps/api/geocode/json?key=YOUR_KEY&latlng=-31.769016,-52.3347313
    

!!! warning
    Geoocode need a Billing account, try to request more than 2 to get a error.
    
return the result

    {
        "plus_code": {
            "compound_code": "6MJ8+94 Pelotas - Princesa, Pelotas - RS, Brasil",
            "global_code": "48W96MJ8+94"
        },
        "results": [
            {
            "address_components": [
                {
                "long_name": "295",
                "short_name": "295",
                "types": [
                "street_number"
                ]
            },
         },
         ...
    }


#### Google StreetView API (Metadata)


    https://maps.googleapis.com/maps/api/streetview/metadata?key=YOUR_KEY&location=-31.769016,-52.3347313
    
return the result

    {
        "copyright": "© Google, Inc.",
        "date": "2016-05",
        "location": {
            "lat": -31.768969839249,
            "lng": -52.33473672801951
        },
        "pano_id": "LA7XRd3RDyv502bErM79Og",
        "status": "OK"
    }
    
    
#### Google StreetView API (Image)

Make sure that you set the [secret key](https://developers.google.com/maps/documentation/streetview/get-api-key?hl=en_US#get-secret) in gmaps.json
    
    https://maps.googleapis.com/maps/api/streetview?size=600x300&location=-31.71631376649615,-52.35328402555263&heading=33.57544166557756&pitch=0&key=YOUR_KEY&signature=SIGNATURE_KEY
    
return the result, an image like that
   
![StreetImage](https://maps.googleapis.com/maps/api/streetview?size=600x300&location=-31.71631376649615,-52.35328402555263&heading=33.57544166557756&pitch=0&key=AIzaSyB6_XPVntnTJHG9jN9OrO11ou8GEV77qOM&signature=oPRukoq62-EsCayx1S3zTE4tcqI=)