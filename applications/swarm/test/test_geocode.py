#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from applications.swarm.assistant.Geospatial import GeoSpatial

def main():

    geoSpatial = GeoSpatial()
    #print '8m'
    #lista = geoSpatial.getIntermediatePointsFromTwoDots(tuple([-31.754314,-52.31679]),tuple([-31.7543523,-52.3168628]))
    #print 'lista->',lista

    #print '13m'
    #lista = geoSpatial.getIntermediatePointsFromTwoDots(tuple([-31.754314,-52.31679]),tuple([-31.7543649,-52.3169098]))
    #print 'lista->',lista

    #print '67m'
    #lista = geoSpatial.getIntermediatePointsFromTwoDots(tuple([-31.754314,-52.31679]),tuple([-31.7545088,-52.3174564]))
    #print 'lista->',lista

    print 'Machado de Assis'
    print geoSpatial.calculate_initial_compass_bearing(tuple([-31.7469122,-52.3966362]),tuple([-31.7465021,-52.3954744]))

    print 'Pinheiro Machado'
    print geoSpatial.calculate_initial_compass_bearing(tuple([-31.7560159,-52.3846862]),tuple([-31.7548008,-52.3842713]))

    print 'Rua João Haical'
    print geoSpatial.calculate_initial_compass_bearing(tuple([-31.7478493,-52.3202943]),tuple([-31.7477848,-52.3200818]))

    print 'Marcilio Días'
    print geoSpatial.calculate_initial_compass_bearing(tuple([-31.7458435,-52.344019]),tuple([-31.7445931,-52.344068]))

    print 'Av. Francisco Caruccio'
    print geoSpatial.calculate_initial_compass_bearing(tuple([-31.7411288,-52.3488685]),tuple([-31.7411457,-52.3496638]))

if __name__ == '__main__':
    main()
