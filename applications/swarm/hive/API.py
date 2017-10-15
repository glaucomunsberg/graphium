#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2, os, traceback, json

from osmapi import OsmApi

from system.Graphium import Graphium

class API:

    _instance   = None
    _my_api     = None
    _g          = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(API, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._my_api    = OsmApi(username = u"glaucomunsberg", password = u"********")
        self._g         = Graphium()

    def getWaysByNode(self,NodeId):
        #print 'getWaysByNode... ',NodeId
        results = self._my_api.NodeWays(int(NodeId))
        to_return = []

        for result in results:
            #print 'result: ',result
            the_way = {}
            the_way['id'] = result['id']
            the_way['nodes'] = []
            if 'tag' in result.keys():
                #print 'tags: ', result['tag']
                if 'name' in result['tag'].keys():
                    the_way['name'] = result['tag']['name']
                else:
                    the_way['name'] = None

            if 'nd' in result.keys():
                #print 'nodes: ',result['nd']
                the_way['nodes'] = result['nd']
            to_return.append(the_way)
        return to_return

    def getPanoByPoint(self,lat,lng,heading=0,pitch=0):

        key     = self._g.gmaps['google_key']
        s_width = self._g.gmaps['width']
        s_height= self._g.gmaps['height']

        file_photo_metadata = self.getPanoInfoByPoint(lat,lng)

        file_name   = file_photo_metadata['pano_id']+".jpeg"
        directory   = self._g.path_picture()+"google_street_view/"

        if not os.path.isfile(directory+file_name):
            try:
                url_map             = "https://maps.googleapis.com/maps/api/streetview?size="+str(s_width)+"x"+str(s_height)+"&location="+str(lat)+","+str(lng)+"&pitch="+str(pitch)+"&key="+key+"&heading="+str(heading)
                file_photo          = urllib2.urlopen(url_map)

                with open(directory+file_name,'wb') as output:
                    output.write(file_photo.read())
                return directory+file_name
            except Exception as error:
                print 'ERROR:'
                print traceback.format_exc()
            return None
        else:
            return directory+file_name

    def getPanoInfoByPoint(self,lat,lng):

        key     = self._g.gmaps['google_key']

        url_info = "https://maps.googleapis.com/maps/api/streetview/metadata?key="+key+"&location="+str(lat)+","+str(lng)
        print ""
        print "url_info->",url_info
        response = urllib2.urlopen(url_info)
        data = json.loads(response.read())
        return data
