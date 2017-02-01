from osmapi import OsmApi


def ad_mat(min_lat, max_lat, min_lon, max_lon):
    ad_Matrix = []

    def initialize_twodlist(data):
        new = []
        for i in range(0, 10):
            for j in range(0, 10):
                new.append(data)
            twod_list.append(new)
            new = []

    MyApi = OsmApi()
    # print MyApi.NodeGet(123)
    data = []
    data = MyApi.Map(min_lon, min_lat, max_lon, max_lat)

    node = []
    way = []
    node_size = 0
    way_size = 0
    c = []
    for i in data:
        if (i[u'type'] == "node"):
            if ((i[u'data'][u'lat'] > min_lat) & (i[u'data'][u'lat'] < max_lat) & (i[u'data'][u'lon'] > min_lon) & (
                        i[u'data'][u'lon'] < max_lon)):
                node.append({'number': node_size + 1, 'lat': i[u'data'][u'lat'], 'lon': i[u'data'][u'lon'],
                             'id': i[u'data'][u'id'], 'tag': i[u'data'][u'tag']})
                node_size = node_size + 1
        if (i[u'type'] == "way"):
            way.append(
                {'number': way_size + 1, 'id': i[u'data'][u'id'], 'tag': i[u'data'][u'tag'], 'nd': i[u'data'][u'nd']})
            way_size = way_size + 1

    temp_ar = []
    for i in node:
        for j in way:
            temp = 0;
            for k in j['nd']:
                if (k == i['id']):
                    temp = 1
            if (temp == 1):
                temp_ar.append(1)
            else:
                temp_ar.append(0)
        ad_Matrix.append(temp_ar)
        temp_ar = []

    return node, way, ad_Matrix
