import bson, datetime

from system.Mongo import Mongo
from system.Graphium import Graphium
from assistant.API import API


def main():
    graphium = Graphium()
    mongo = Mongo()
    api = API("?????")

    panos_ids = {}

    total = mongo.get_pano_by_query({"swarm_identifier": "20181103173441", "classification": "FN"}).count()
    consulted = 0
    previews = 0
    current = 0

    for pano in mongo.get_pano_by_query({"swarm_identifier": "20181103173441", "classification": "FN"}):
        print str(current) + "/" + str(total) + " from " + pano['pano_id']

        mongo.insertGraffiti(pano['lat'],pano['lng'],pano['pano_id'],str(pano['heading']), "0", "","","","","[(u'n06596364', u'comic_book', 0.0)]", "20181103173441", "false_negative" )


if __name__ == '__main__':
    main()