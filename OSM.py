#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from osmapi import OsmApi
from mapsearch_3 import mapsearch
import numpy as np


def find_ind(id, node):
    for i in node:
        if i['id'] == id:
            return int(i['number'] - 1)
    return -1


def osm_mat(min_lat, max_lat, min_lon, max_lon):
    ic_Matrix = []

    MyApi = OsmApi()
    data = MyApi.Map(min_lon, min_lat, max_lon, max_lat)
    node = []
    way = []
    node_size = 0
    way_size = 0
    wat_size_limit = 1
    for i in data:
        if i[u'type'] == "node":
            if ((i[u'data'][u'lat'] > min_lat) & (i[u'data'][u'lat'] < max_lat) & (i[u'data'][u'lon'] > min_lon) & (
                        i[u'data'][u'lon'] < max_lon)):
                # node.append({'number': node_size + 1, 'lat': i[u'data'][u'lat'], 'lon': i[u'data'][u'lon'],
                #              'id': i[u'data'][u'id'], 'tag': i[u'data'][u'tag']})
                node.append({'number': node_size + 1, 'lat': i[u'data'][u'lat'], 'lon': i[u'data'][u'lon'],
                             'id': i[u'data'][u'id']})
                node_size += 1
        if i[u'type'] == "way":
            c = 0
            for j in i[u'data'][u'nd']:
                c += 1
            if c > wat_size_limit:
                if u'highway' in i[u'data'][u'tag']:
                    if (i[u'data'][u'tag'][u'highway'] != 'service') & (
                                i[u'data'][u'tag'][u'highway'] != 'secondary_link') & (
                                i[u'data'][u'tag'][u'highway'] != 'primary_link'):
                        way.append(
                            {'number': way_size + 1, 'id': i[u'data'][u'id'], 'tag': i[u'data'][u'tag'],
                             'nd': i[u'data'][u'nd']})
                        way_size += 1
    temp_ar = []
    for i in node:
        for j in way:
            temp = 0
            for k in j['nd']:
                if k == i['id']:
                    temp = 1
            if temp == 1:
                temp_ar.append(1)
            else:
                temp_ar.append(0)
        ic_Matrix.append(temp_ar)
        temp_ar = []
    ad_Matrix = []
    for i in range(0, node_size):
        temp_ar = []
        for j in range(0, node_size):
            temp_ar.append(0)
        ad_Matrix.append(temp_ar)
    for i in way:
        for j in i['nd']:
            temp = 0
            for k in i['nd']:
                if j == k:
                    temp = 1
                else:
                    if temp == 1:
                        x = find_ind(j, node)
                        y = find_ind(k, node)
                        if (x != -1) & (y != -1):
                            ad_Matrix[x][y] = 1
                            ad_Matrix[y][x] = 1
                        break
    delete_list = []
    for i in range(0, node_size - 1):
        c = 0
        for j in range(0, node_size - 1):
            if ad_Matrix[i][j] == 1:
                c += 1
        if c == 0:
            delete_list.append(i)
    ad_Matrix = np.delete(ad_Matrix, delete_list, axis=0)
    ad_Matrix = np.delete(ad_Matrix, delete_list, axis=1)
    node_size -= len(delete_list)
    cross = []
    for i in ad_Matrix:
        temp = 0
        for j in i:
            temp += j
        cross.append(temp)
    new_cross = [
        [[node[i]['lat'], node[i]['lon']], cross[i]]
        for i in range(node_size) if cross[i] > 2
        ]
    return new_cross, ad_Matrix


if __name__ == '__main__':
    result = mapsearch(
        ['สื่แยกหนองหอย', 'ถนนมหิ่ดล', 'ธัซ์\'gลุงรตนไกอบฟาง', 'การเคหะซุมซนเชียงใหม่', '.Here', 'LeCoqj’Or',
         'ตลาดหนองหอย'])
    osm_mat(result[1][1], result[1][0], result[1][3], result[1][2])
