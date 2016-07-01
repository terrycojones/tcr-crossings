def dmsToFloat(s):
    """
    """
    # print('got %r' % s)
    s = s.replace('°', ' ').replace("'", ' ').replace('"', ' ')
    direction = s[-1].lower()
    assert direction in ('n', 's', 'e', 'w')
    multiplier = 1 if s[-1].lower() in ('n', 'e') else -1
    # Chop off the direction.
    s = s[:-1]
    # print('converted string is %r.' % s)
    dms = s.split()
    if len(dms) == 2:
        # Assume seconds are missing.
        dms.append(0)

    if len(dms) == 3:
        # print(list(float(x) for x in dms))
        return multiplier * sum(float(x) / 60 ** n for n, x in enumerate(dms))


def convertLatLong(latlong):
    """
    Convert a string of latitude/longitude into a pair of floats.
    """
    # Split, either on comman or whitespace, or fail.
    try:
        origLat, origLon = latlong.split(',')
    except ValueError:
        try:
            origLat, origLon = latlong.split()
        except ValueError:
            raise ValueError('Could not split lat/lon string %r' % latlong)

    # Test to see if we have two floats separated by a comma, in which case
    # we can simply return them.
    try:
        lat = float(origLat)
        lon = float(origLon)
    except ValueError:
        pass
    else:
        return lat, lon

    # Test to see if we can convert DMS strings.
    lat = dmsToFloat(origLat)
    lon = dmsToFloat(origLon)

    if not (lat is None or lon is None):
        return lat, lon

    raise ValueError('Could not convert lat/lon string %r' % latlong)
