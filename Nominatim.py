#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import urllib
from decimal import Decimal


def nominatim(name_place):
    min_lat_ar = []
    max_lat_ar = []
    min_lon_ar = []
    max_lon_ar = []

    # name_place = ['ddddds']
    data_size = 0
    for i in name_place:
        data_size = data_size + 1
        name_place_encoded = urllib.quote_plus(i)
        link = 'http://nominatim.openstreetmap.org/search?q=' + name_place_encoded + '&format=xml&polygon=1&addressdetails=1'
        f = urllib.urlopen(link)
        str_bdb = "boundingbox"  # bdb = boundingbox
        bdd_len = 13  # boundingbox="
        position_sarch = -1

        line = f.readline()

        while (line != '</searchresults>'):
            position_sarch = line.find(str_bdb)
            if (position_sarch != -1):
                break;
            else:
                line = f.readline()

        if (position_sarch != -1):
            min_lat_t = 0.0
            max_lat_t = 0.0
            min_lon_t = 0.0
            max_lon_t = 0.0

            count = 0
            count_latlon = 0
            i = line[position_sarch + bdd_len + count]
            str_temp = ""
            while (i != '"'):
                if (i != ','):
                    str_temp += i
                else:
                    if (count_latlon == 0):  # get min lat
                        min_lat_t = Decimal(str_temp)
                    else:
                        if (count_latlon == 1):  # get max lat
                            max_lat_t = Decimal(str_temp)
                        else:
                            if (count_latlon == 2):  # get min lon
                                min_lon_t = Decimal(str_temp)
                    count_latlon = count_latlon + 1
                    str_temp = ""
                count = count + 1
                i = line[position_sarch + bdd_len + count]
            max_lon_t = Decimal(str_temp)  # get min lat

            min_lat_ar.append(min_lat_t)
            max_lat_ar.append(max_lat_t)
            min_lon_ar.append(min_lon_t)
            max_lon_ar.append(max_lon_t)

    if (position_sarch != -1):
        min_lat_ar.sort()
        max_lat_ar.sort()
        min_lon_ar.sort()
        max_lon_ar.sort()

        min_lat = min_lat_ar[0]
        max_lat = max_lat_ar[data_size - 1]
        min_lon = min_lon_ar[0]
        max_lon = max_lon_ar[data_size - 1]

        # print min_lat
        # print max_lat
        # print min_lon
        # print max_lon
    else:
        print "Not Found!!"
    return min_lat, max_lat, min_lon, max_lon
