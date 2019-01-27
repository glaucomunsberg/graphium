
import bson, datetime

from system.Mongo import Mongo
from system.Graphium import Graphium
from assistant.API import API

def main():

    graphium = Graphium()
    mongo = Mongo()
    api = API("?????")

    panos_ids = {}

    total = mongo.get_pano_by_query({"lng": ""}).count()
    consulted = 0
    previews = 0
    current = 0

    for pano in mongo.get_pano_by_query({"lng": ""}):

        print str(current)+"/"+str(total)+" from "+pano['pano_id']

        if pano['pano_id'] in panos_ids:

            pano['lat'] = panos_ids[pano['pano_id']]['lat']
            pano['lng'] = panos_ids[pano['pano_id']]['lng']
            pano['pano_date'] = panos_ids[pano['pano_id']]['pano_date']

            previews += 1

        else:
            consulted += 1
            pano_info = api.get_pano_info(pano['pano_id'])

            pano['lat'] = pano_info['lat']
            pano['lng'] = pano_info['lng']
            pano['pano_date'] = pano_info['pano_date']

            panos_ids[pano['pano_id']] = pano_info

        mongo.update_pano(pano['_id'], pano)
        current += 1

    print "Consulted "+str(consulted)+" previews"+str(previews)

if __name__ == '__main__':
    main()