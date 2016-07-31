from django.core.management.base import BaseCommand, CommandError
from crossings.models import Crossing, Country
from csv import reader

from ._utils import convertLatLong

"""
One-time import of all crossings from CSV to the Django Crossing model.

Note that this script DELETES all pre-existing crossings! You should
only run it if you really know what you're doing. All comments will be
deleted too due to the ON DELETE CASCADE in the model.
"""

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

countries = {
    'Albania': Country.ALBANIA,
    'Austria': Country.AUSTRIA,
    'Bosnia and Herzegovina': Country.BOSNIA_HERZEGOVINA,
    'Bulgaria': Country.BULGARIA,
    'Croatia': Country.CROATIA,
    'Greece': Country.GREECE,
    'Hungary': Country.HUNGARY,
    'Italy': Country.ITALY,
    'Kosovo': Country.KOSOVO,
    'Macedonia': Country.MACEDONIA,
    'Montenegro': Country.MONTENEGRO,
    'Romania': Country.ROMANIA,
    'Serbia': Country.SERBIA,
    'Slovenia': Country.SLOVENIA,
    'Turkey': Country.TURKEY,
}


def strToBool(s, lineNumber):
    origS = s
    s = s.lower()
    if s == 'yes':
        return True
    elif s in {'', 'no', 'n? (motorway?)', 'n ? (motorway?)'}:
        return False
    else:
        raise CommandError(
            'Could not convert string %r found on line %d to Boolean' %
            (origS, lineNumber))


def main(csvfp, command):
    # Delete all pre-existing crossings.
    Crossing.objects.all().delete()

    completeRecords = 0

    for lineNumber, record in enumerate(reader(csvfp), start=1):
        if lineNumber == 1:
            if record != headers:
                raise CommandError(
                    'CSV headers have changed!\nExpected %r\nSaw %r\n' %
                    (headers, record))
            continue

        [name, strId, underEditBy, lastEditBy,
         country1, country1Place, country2, country2Place,
         otherNames, coords, active, openingHours, crossingType,
         bicycleCrossing, tcr4Survey, notes] = record

        if coords:
            try:
                lat, lon = convertLatLong(coords)
            except ValueError:
                command.stderr.write(
                    command.style.ERROR(
                        'Could not convert coords %r on line %d\n' %
                        (coords, lineNumber)))
                lat = lon = -1.0
        else:
            lat = lon = -1.0

        # Round latitude & longitude to 5 decimals. This provides for
        # accuracy down to 1.1 meters. I don't keep all the decimal places
        # for display purposes (we have some coords that have many places
        # and these look odd in the UI).
        lat = round(lat, 5)
        lon = round(lon, 5)

        badCountry = False
        for country in country1, country2:
            if country not in countries:
                command.stderr.write(
                    command.style.ERROR(
                        'Ignoring unknown country %r found on line %d' %
                        (country, lineNumber)))
                badCountry = True

        if badCountry:
            continue

        country1 = countries[country1]
        country2 = countries[country2]

        active = strToBool(active, lineNumber)
        bicycleCrossing = strToBool(bicycleCrossing, lineNumber)
        tcr4Survey = strToBool(tcr4Survey, lineNumber)

        crossing = Crossing(
            active=active,
            bicycleCrossing=bicycleCrossing,
            countryTo=country1,
            countryFrom=country2,
            countryToPlace=country1Place,
            countryFromPlace=country2Place,
            crossingType=crossingType,
            openingHours=openingHours,
            lastEditBy=lastEditBy,
            latitude=lat,
            longitude=lon,
            name=name,
            notes=notes,
            otherNames=otherNames,
            tcr4Survey=tcr4Survey,
            underEditBy=underEditBy)

        crossing.save()
        completeRecords += 1

    return completeRecords


class Command(BaseCommand):
    help = 'Import all crossings from the Google spreadsheet CSV'

    def add_arguments(self, parser):
        parser.add_argument('--csv', required=True)

    def handle(self, *args, **options):
        with open(options['csv']) as fp:
            completeRecords = main(fp, self)

        self.stdout.write(self.style.SUCCESS('Imported %d crossings' %
                                             completeRecords))
