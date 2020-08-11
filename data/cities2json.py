#!/usr/bin/env python

""" Create cities database fixture

Transform the cities database from GeoNames into a fixture to be imported
into our cities database.
"""

import json
import csv
import os
import sys


if not os.path.exists('cities500.txt'):
    sys.exit("""Could not find "cities500.txt". Execute the following command to download it:

        $ wget http://download.geonames.org/export/dump/cities500.zip && unzip cities500.zip
""")


print('[')


with open('cities500.txt') as f:
    for line in csv.reader(f, delimiter='\t'):
        geonameid, name, asciiname, alternatenames, latitude, longitude, *rest = line

        print(json.dumps({
            'model': 'core.city',
            'pk': geonameid,
            'fields': {
                'name': name,
                'lat': float(latitude),
                'lon': float(longitude),
            }
        }) + ',')


print(']')
