#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import urllib
import time


def mapsearch(name_place):
    lat = []
    lon = []
    lat_temp = []
    lon_temp = []
    result = []
    temp_temp = []
    key = "AIzaSyBOeGVakjKHKZ_QYZAWuu3fjYuIV6Dxomk"
    data_size = 0
    for address in name_place:
        lat_temp_position = []
        lon_temp_position = []
        temp_position = []
        name_place_encoded = urllib.quote_plus(address)
        link = 'https://maps.googleapis.com/maps/api/geocode/xml?key=' + key + '&new_forward_geocoder=true&address=' + name_place_encoded
        f = urllib.urlopen(link)
        c = urllib.urlopen(link)
        ffile = open("fff"+str(data_size)+".txt", "w")
        ffile.write(str(address) + "\r\n")
        for i in c:
            ffile.write(str(i) + "\r\n")
        line = f.readline()
        str_location = '<location>'
        str_lat = '<lat>'
        lat_len = len(str_lat)
        str_lon = '<lng>'
        lon_len = len(str_lon)
        position_location = -1
        cline = 0
        while line != '</GeocodeResponse>':
            cline += 1
            position_location = line.find(str_location)
            if position_location != -1:
                line = f.readline()  # make lat
                position_lat = line.find(str_lat)
                count = 0
                i = line[position_lat + lat_len + count]
                str_temp = ""
                while i != '<':
                    str_temp += i
                    count += 1
                    i = line[position_lat + lat_len + count]
                data_size += 1
                lat.append(float(str_temp))
                lat_temp.append(float(str_temp))
                lat_temp_position.append(float(str_temp))

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
                lon_temp.append(float(str_temp))
                lon_temp_position.append(float(str_temp))
            else:
                line = f.readline()
            position_location = -1
            if cline > 400:
                position_location = -1
                break
        temp_position.append(lat_temp_position)
        temp_position.append(lon_temp_position)
        temp_position.append(address)
        temp_temp.append(temp_position)

    result.append(temp_temp)
    print lat_temp
    print lon_temp
    lat_temp.sort()
    lon_temp.sort()

    if data_size % 2 == 1:
        lat_med = lat_temp[data_size / 2]
        lon_med = lon_temp[data_size / 2]
    else:
        lat_med = (lat_temp[data_size / 2] + lat_temp[(data_size / 2) - 1]) / 2
        lon_med = (lon_temp[data_size / 2] + lon_temp[(data_size / 2) - 1]) / 2

    lat_temp = []
    lon_temp = []
    rangee = 0.05
    if data_size > 2:
        for i in range(0, data_size):
            if ((lat[i] - lat_med < rangee) & (lat_med - lat[i] < rangee)) & (
                        (lon[i] - lon_med < rangee) & (lon_med - lon[i] < rangee)):
                lat_temp.append(lat[i])
                lon_temp.append(lon[i])

    data_size = len(lon_temp)

    lat_temp.sort()
    lon_temp.sort()
    min_lat = lat_temp[0]
    max_lat = lat_temp[data_size - 1]
    min_lon = lon_temp[0]
    max_lon = lon_temp[data_size - 1]

    delta_lat = max_lat - min_lat
    delta_lon = max_lon - min_lon

    min_lat = min_lat - (0.25 * delta_lat)
    max_lat = max_lat + (0.25 * delta_lat)
    min_lon = min_lon - (0.25 * delta_lon)
    max_lon = max_lon + (0.25 * delta_lon)

    temp = []
    temp.append(max_lat)
    temp.append(min_lat)
    temp.append(max_lon)
    temp.append(min_lon)

    result.append(temp)
    print lat_med
    print lon_med
    print min_lat
    print max_lat
    print min_lon
    print max_lon
    return result


if __name__ == '__main__':
    result = mapsearch(
        ['สื่แยกหนองหอย', 'ถนนมหิ่ดล','ตลาดสดหนองหอย'])