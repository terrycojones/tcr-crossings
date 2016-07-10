#!/usr/bin/env python

from __future__ import print_function

import sys
from csv import reader
from json import dumps
from time import ctime, gmtime, mktime

from crossings.utils import convertLatLong

headers = [
    'Nominal Name',
    'Nominal ID Number',
    'Under Edit by',
    'Last Edit By',
    'Country 1',
    'Location / Town\nCountry 1',
    'Country 2',
    'Location / Town\nCountry 2',
    'Other Names',
    'Co-ordinates',
    'Active',
    'Opening\nHours',
    'Type\n(road / rail / tunnel /\n motorway / pedestrian etc)',
    'Bicycle Crossing\n(Y/N)',
    'TCR No4 Survey\n(Y/N)',
    'Notes',
]

countries = set((
    'Albania',
    'Austria',
    'Bosnia and Herzegovina',
    'Bulgaria',
    'Croatia',
    'Greece',
    'Hungary',
    'Italy',
    'Kosovo',
    'Macedonia',
    'Montenegro',
    'Romania',
    'Serbia',
    'Slovenia',
    'Turkey'))


def main():
    data = []
    idsSeen = {}  # Key is int id, value is first record
    completeRecords = 0

    for lineNumber, record in enumerate(reader(sys.stdin), start=1):
        if lineNumber == 1:
            if record != headers:
                raise RuntimeError(
                    'CSV headers have changed!\nExpected %r\nSaw %r\n' %
                    (headers, record))
            continue

        [name, strId, editBy, lastEditBy,
         country1, country1Place, country2, country2Place,
         otherNames, coords, active, hours, crossingType, bikeCrossing,
         tcr4Survey, notes] = record

        try:
            intId = int(strId)
        except ValueError:
            raise ValueError(
                'Could not convert id %r to int on line %d.\nRecord %r' %
                (strId, lineNumber, record))

        if intId in idsSeen:
            raise(ValueError,
                  'Place id %r occurs more than once (on lines %d and %d)' %
                  (idsSeen[intId], lineNumber))
        else:
            idsSeen[intId] = lineNumber

        if not coords:
            print('Skipped record %d due to missing coords.' % lineNumber,
                  file=sys.stderr)
            continue

        try:
            lat, lon = convertLatLong(coords)
        except ValueError:
            print('Could not convert coords %r on line %d' %
                  (coords, lineNumber), file=sys.stderr)
            continue

        # Round latitude & longitude to 5 decimals. This provides for
        # accuracy down to 1.1 meters. I don't keep all the decimal places
        # for display purposes (we have some coords that have many places
        # and these look odd in the UI).
        lat = round(lat, 5)
        lon = round(lon, 5)

        if not (country1 and country2):
            print('Skipped record %d due to missing country.' % lineNumber,
                  file=sys.stderr)
            continue

        for country in country1, country2:
            if country not in countries:
                raise ValueError('Unknown country %r found on line %d' %
                                 (country, lineNumber))

        data.append({
            'active': active,
            'bikeCrossing': bikeCrossing,
            'countryTo': country1,
            'countryToPlace': country1Place,
            'countryFrom': country2,
            'countryFromPlace': country2Place,
            'crossingType': crossingType,
            'hours': hours,
            'id': intId,
            'latitude': lat,
            'longitude': lon,
            'name': name,
            'notes': notes,
            'otherNames': otherNames.split() if otherNames else [],
            'tcr4Survey': tcr4Survey,
        })

        completeRecords += 1

    print(dumps({
        'date': ctime(mktime(gmtime())),
        'crossings': data,
    }, indent=4, sort_keys=True))

    print('Found %d complete records in %d lines of input.' %
          (completeRecords, lineNumber), file=sys.stderr)


if __name__ == '__main__':
    main()
