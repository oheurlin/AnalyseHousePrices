import time, random, http.client, json, string
from hashlib import sha1

caller_id = 'API_USERNAME'
private_key = 'API_KEY'

offset = 0
total_count = 0
search_area = 'Stockholm'

file = open('ApartmentSearch_' + search_area + '.csv', 'w')
headers = 'Address, Area, Longitude, Latitude, Living area (m2),' \
          ' Rooms, Floor, Rent, Sold date, Listed price, Sold for (SEK)\n'
file.write(headers)

while offset <= total_count or offset == 0:
    timestamp = str(int(time.time()))
    unique = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(16))

    unicode = (caller_id+timestamp+private_key+unique).encode()
    hashstr = sha1(unicode).hexdigest()

    url = ("/sold?q="+search_area+"&limit=35"+"&offset="+str(offset)+"&callerId="+caller_id+"&time="+timestamp+
           "&unique="+unique+"&hash="+hashstr)

    connection = http.client.HTTPConnection("api.booli.se")
    connection.request("GET", url)
    response = connection.getresponse()
    data = response.read()
    connection.close()
    json_data = json.loads(data)

    if response.status != 200:
        print('fail')

    for i in json_data['sold']:
        longitude = '0'
        latitude = '0'
        listed_price = '0'
        floor = '0'
        rent = '0'
        sqm = '0'
        area = '0'
        rooms = '0'
        address = str(i['location']['address']['streetAddress'])
        sold_date = str(i['soldDate'])
        sold_for = str(i['soldPrice'])

        if 'longitude' in i['location']['position']:
            longitude = str(i['location']['position']['longitude'])
        if 'latitude' in i['location']['position']:
            latitude = str(i['location']['position']['latitude'])
        if 'rooms' in i:
            rooms = str(i['rooms'])
        if 'namedAreas' in i['location']:
            area = str(i['location']['namedAreas'][0])
        if 'livingArea' in i:
            sqm = str(i['livingArea'])
        if 'rent' in i:
            rent = str(i['rent'])
        if 'listPrice' in i:
            listed_price = str(i['listPrice'])
        if 'floor' in i:
            floor = str(i['floor'])

        file.write(address + ',' + area +
                   ',' + longitude + ',' + latitude + ',' + sqm +
                   ',' + rooms + ',' + floor + ',' + rent +
                   ',' + sold_date + ',' + listed_price + ',' + sold_for + ',' + '\n')
    offset = offset + json_data['limit']
    total_count = json_data['totalCount']
print('Finished, fetched data from ' + str(total_count) +' sold apartments')
