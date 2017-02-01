#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import urllib


def mapsearch(name_place):
    lat = []
    lon = []
    key = "AIzaSyBOeGVakjKHKZ_QYZAWuu3fjYuIV6Dxomk"
    data_size = 0
    for address in name_place:
        data_size += 1
        name_place_encoded = urllib.quote_plus(address)
        link = 'https://maps.googleapis.com/maps/api/geocode/xml?key=' + key + '&new_forward_geocoder=true&address=' + name_place_encoded
        f = urllib.urlopen(link)
        line = f.readline()
        str_location = '<location>'
        str_lat = '<lat>'
        lat_len = len(str_lat)
        str_lon = '<lng>'
        lon_len = len(str_lon)
        while line != '</GeocodeResponse>':
            position_location = line.find(str_location)
            if position_location != -1:
                break
            else:
                line = f.readline()

        line = f.readline()  # make lat
        position_lat = line.find(str_lat)
        count = 0
        i = line[position_lat + lat_len + count]
        str_temp = ""
        while i != '<':
            str_temp += i
            count += 1
            i = line[position_lat + lat_len + count]
        a = float(str_temp)
        lat.append(float(str_temp))

        line = f.readline()  # make lon
        position_lon = line.find(str_lon)
        count = 0
        i = line[position_lon + lon_len + count]
        str_temp = ""
        while i != '<':
            str_temp += i
            count += 1
            i = line[position_lon + lon_len + count]
        lon.append(float(str_temp))

    lat.sort()
    lon.sort()

    min_lat = lat[0]
    max_lat = lat[data_size - 1]
    min_lon = lon[0]
    max_lon = lon[data_size - 1]

    delta_lat = max_lat - min_lat
    delta_lon = max_lon - min_lon

    min_lat = min_lat - (0.25 * delta_lat)
    max_lat = max_lat + (0.25 * delta_lat)
    min_lon = min_lon - (0.25 * delta_lon)
    max_lon = max_lon + (0.25 * delta_lon)
    return min_lat, max_lat, min_lon, max_lon


if __name__ == '__main__':
    min_lat, max_lat, min_lon, max_lon = mapsearch(['ตลาดสดหนองหอย', 'มหาลัยเชียงใหม่'])
