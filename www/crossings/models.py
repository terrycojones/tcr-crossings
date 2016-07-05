from django.db import models


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


class Crossing(models.Model):
    active = models.NullBooleanField('active?', blank=True)
    bicycleCrossing = models.NullBooleanField('bicycle crossing', blank=True)
    country1 = models.CharField('country 1', max_length=2,
                                choices=Country.CHOICES)
    country2 = models.CharField('country 2', max_length=2,
                                choices=Country.CHOICES)
    crossingType = models.CharField('type', max_length=200, blank=True)
    lastEditBy = models.CharField('last edit by', max_length=200, blank=True)
    lastUpdate = models.DateTimeField('last update', auto_now=True)
    latitude = models.FloatField(blank=True, null=True)
    location1 = models.CharField('location 1', max_length=200, blank=True,
                                 null=True)
    location2 = models.CharField('location 2', max_length=200, blank=True,
                                 null=True)
    longitude = models.FloatField(blank=True, null=True)
    name = models.CharField(max_length=200, unique=True)
    notes = models.CharField(max_length=4000, blank=True)
    openingHours = models.CharField('opening hours', max_length=200,
                                    blank=True)
    otherNames = models.CharField('other names', max_length=2000, blank=True)
    status = models.TextField(blank=True)
    tcr4Survey = models.NullBooleanField('TCR4 survey?', blank=True)
    underEditBy = models.CharField('under edit by', max_length=200, blank=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    # crossing = models.ForeignKey(Crossing, on_delete=models.CASCADE)
    crossingId = models.IntegerField()
    # Note that the max_length below should be the same as we use in
    # www/crossings/templates/crossings/index.html
    text = models.CharField(max_length=4000)
    lastUpdate = models.DateTimeField('last update', auto_now=True)

    def __str__(self):
        return self.text
