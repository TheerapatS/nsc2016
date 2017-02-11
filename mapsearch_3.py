#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import requests


def mapsearch(name_place, scope_area='เชียงใหม่'):
    lat = []
    lon = []
    data_size = 0
    lat_temp = []
    lon_temp = []
    result = []
    temp_temp = []
    key = "AIzaSyBOeGVakjKHKZ_QYZAWuu3fjYuIV6Dxomk"
    url = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}"
    geo = []
    for name in name_place:
        res = requests.get(url.format(name + " " + scope_area , key))
        json = res.json()
        location = []
        if json['status'] == "OK":
            for lo in json['results']:
                location.append(lo['geometry']['location'])
        else:
            res = requests.get(url.format(name, key))
            json = res.json()
            if json['status'] == "OK":
                for lo in json['results']:
                    # print lo['formatted_address'].count(scope_area.decode("utf8"))
                    # if lo['formatted_address'].count(scope_area.decode("utf8"))>0:
                    location.append(lo['geometry']['location'])
        if len(location) > 0:
            geo.append([location, name])
    for r in geo:
        temp_position = []
        for j in r[0]:
            print j[u'lat']
            temp_position.append(j[u'lat'])
            lat.append(j[u'lat'])
            lat_temp.append(j[u'lat'])

            temp_position.append(j[u'lng'])
            lon.append(j[u'lng'])
            lon_temp.append(j[u'lng'])
            data_size += 1
        temp_position.append(r[1])
        temp_temp.append(temp_position)
        result.append(temp_temp)

    #     temp_position.append(lat_temp_position)
    #     temp_position.append(lon_temp_position)
    #     temp_position.append(address)
    #     print lat_temp_position
    #     print lon_temp_position
    #     print address
    #     temp_temp.append(temp_position)
    #
    # if data_size > 0:
    #     result.append(temp_temp)
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
    error_size = 0
    rangee = 0.05
    if data_size > 2:
        for i in range(0, data_size):
            if ((lat[i] - lat_med < rangee) & (lat_med - lat[i] < rangee)) & (
                        (lon[i] - lon_med < rangee) & (lon_med - lon[i] < rangee)):
                lat_temp.append(lat[i])
                lon_temp.append(lon[i])
            else:
                print lat[i]
                print lon[i]
                error_size += 1
    if data_size % 2 == 1:
        temp = data_size + 1
    else:
        temp = data_size
    if error_size < temp / 2:
        data_size = len(lon_temp)

        lat_temp.sort()
        lon_temp.sort()
        min_lat = lat_temp[0]
        max_lat = lat_temp[data_size - 1]
        min_lon = lon_temp[0]
        max_lon = lon_temp[data_size - 1]

        delta_lat = max_lat - min_lat
        delta_lon = max_lon - min_lon

        min_lat -= 0.25 * delta_lat
        max_lat += 0.25 * delta_lat
        min_lon -= 0.25 * delta_lon
        max_lon += 0.25 * delta_lon

        temp = [max_lat, min_lat, max_lon, min_lon]

        result.append(temp)
        print result[1]
        # print lat_med
        # print lon_med
        # print min_lat
        # print max_lat
        # print min_lon
        # print max_lon

        for i in result[0]:
            delete_list = []
            for j in range(len(i[0])):
                if not ((min_lat < i[0][j] < max_lat) & (min_lon < i[1][j] < max_lon)):
                    delete_list.append(j)
            delete_list.sort(reverse=True)
            for k in delete_list:
                i[0].pop(k)
                i[1].pop(k)
        return result
    else:
        print "A"
        return 0
        # raise Exception('Error Message')

if __name__ == '__main__':
    result = mapsearch(
        ['สื่แยกหนองหอย', 'ถนนมหิ่ดล', 'ธัซ์\'gลุงรตนไกอบฟาง', 'การเคหะซุมซนเชียงใหม่', '.Here', 'LeCoqj’Or',
         'ตลาดหนองหอย'],'เชียงใหม่')
    # for r in result:
    #     print r[1]
    #     print r[0]
