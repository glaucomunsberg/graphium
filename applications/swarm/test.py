from system.Mongo import Mongo

from assistant.Geospatial import GeoSpatial
from assistant.API import API

def main():

    #geos = GeoSpatial()
    #dot1 = tuple([-31.780517, -52.3371523])
    #dot2 = tuple([-31.7802525, -52.3380589])
    #dot2 = tuple([-31.780517, -52.3371523])
    #dot1 = tuple([-31.7802525, -52.3380589])
    #dot1 = tuple([-31.781286, -52.337468])
    #dot2 = tuple([-31.7805170, -52.3371523])
    #dot1 = tuple([-31.772288, -52.352641])
    #dot2 = tuple([-31.770481, -52.352595])
    #print 'Dots'
    #print geos.getIntermediatePointsFromTwoDots(dot1,dot2)

    #api = API()
    #api.getStreetGeoCodeInfoFromOSM("155081917")
    mongo = Mongo()
    print mongo.getMapsCounterSwarmByIdentifer("20171203193750")

if __name__ == '__main__':
    main()
