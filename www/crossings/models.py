from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class Country(object):

    ALBANIA = 'AL'
    AUSTRIA = 'AU'
    BOSNIA_HERZEGOVINA = 'BH'
    BULGARIA = 'BU'
    CROATIA = 'CR'
    GREECE = 'GR'
    HUNGARY = 'HU'
    ITALY = 'IT'
    KOSOVO = 'KO'
    MACEDONIA = 'MA'
    MONTENEGRO = 'MO'
    ROMANIA = 'RO'
    SERBIA = 'SE'
    SLOVENIA = 'SL'
    TURKEY = 'TU'

    CHOICES = (
        (ALBANIA, 'Albania'),
        (AUSTRIA, 'Austria'),
        (BOSNIA_HERZEGOVINA, 'Bosnia Herzegovina'),
        (BULGARIA, 'Bulgaria'),
        (CROATIA, 'Croatia'),
        (GREECE, 'Greece'),
        (HUNGARY, 'Hungary'),
        (ITALY, 'Italy'),
        (KOSOVO, 'Kosovo'),
        (MACEDONIA, 'Macedonia'),
        (MONTENEGRO, 'Montenegro'),
        (ROMANIA, 'Romania'),
        (SERBIA, 'Serbia'),
        (SLOVENIA, 'Slovenia'),
        (TURKEY, 'Turkey'))


COUNTRY_NAME = {
    'AL': 'Albania',
    'AU': 'Austria',
    'BH': 'Bosnia Herzegovina',
    'BU': 'Bulgaria',
    'CR': 'Croatia',
    'GR': 'Greece',
    'HU': 'Hungary',
    'IT': 'Italy',
    'KO': 'Kosovo',
    'MA': 'Macedonia',
    'MO': 'Montenegro',
    'RO': 'Romania',
    'SE': 'Serbia',
    'SL': 'Slovenia',
    'TU': 'Turkey',
}


@python_2_unicode_compatible
class Crossing(models.Model):
    active = models.NullBooleanField('active?', blank=True)
    bicycleCrossing = models.NullBooleanField('bicycle crossing', blank=True)
    countryTo = models.CharField('country entering', max_length=2,
                                 choices=Country.CHOICES)
    countryFrom = models.CharField('country leaving', max_length=2,
                                   choices=Country.CHOICES)
    countryToPlace = models.CharField('city/town in country being entered',
                                      max_length=200, blank=True,
                                      null=True)
    countryFromPlace = models.CharField('city/town in country being left',
                                        max_length=200, blank=True,
                                        null=True)
    crossingType = models.CharField('type', max_length=200, blank=True)
    lastEditBy = models.CharField('last edit by', max_length=200, blank=True)
    lastUpdate = models.DateTimeField('last update', auto_now=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=200)
    notes = models.CharField(max_length=4000, blank=True)
    openingHours = models.CharField('opening hours', max_length=200,
                                    blank=True)
    otherNames = models.CharField('other names', max_length=2000, blank=True)
    tcr4Survey = models.NullBooleanField('TCR4 survey?', blank=True)
    underEditBy = models.CharField('under edit by', max_length=200, blank=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Comment(models.Model):
    crossing = models.ForeignKey(Crossing, on_delete=models.CASCADE)
    # Note that the max_length below should be the same as we use in
    # www/crossings/templates/crossings/index.html
    text = models.CharField(max_length=4000)
    lastUpdate = models.DateTimeField('last update', auto_now=True)

    def __str__(self):
        return self.text
