import six
from unittest import TestCase

from crossings.utils import convertLatLong


class TestConvertLatLon(TestCase):
    def testUnrecognizable(self):
        """
        An unrecognizable string must raise value error.
        """
        error = "^Could not split lat/lon string 'hey'$"
        six.assertRaisesRegex(self, ValueError, error, convertLatLong, 'hey')

    def testTwoFloatsCommaSpace(self):
        """
        The convertLatLong must return the expected value when passed two
        floats separated by a comma and a space.
        """
        lat, lon = convertLatLong('27.0, 35.3')
        self.assertAlmostEqual(lat, 27.0)
        self.assertAlmostEqual(lon, 35.3)

    def testTwoFloatsCommaNoSpace(self):
        """
        The convertLatLong must return the expected value when passed two
        floats separated by a comma but with no intervening space.
        """
        lat, lon = convertLatLong('27.0,35.3')
        self.assertAlmostEqual(lat, 27.0)
        self.assertAlmostEqual(lon, 35.3)

    def testTwoFloatsSpace(self):
        """
        The convertLatLong must return the expected value when passed two
        floats separated by a space.
        """
        lat, lon = convertLatLong('27.0 35.3')
        self.assertAlmostEqual(lat, 27.0)
        self.assertAlmostEqual(lon, 35.3)

    def testTwoFloatsLeadingWhitespace(self):
        """
        The convertLatLong must return the expected value when passed two
        floats separated by a space with leading whitespace.
        """
        lat, lon = convertLatLong('  27.0   35.3')
        self.assertAlmostEqual(lat, 27.0)
        self.assertAlmostEqual(lon, 35.3)

    def testTwoFloatsTrailingWhitespace(self):
        """
        The convertLatLong must return the expected value when passed two
        floats separated by a space with trailing whitespace.
        """
        lat, lon = convertLatLong('27.0   35.3  ')
        self.assertAlmostEqual(lat, 27.0)
        self.assertAlmostEqual(lon, 35.3)

    def testTwoFloatsLeadingAndTrailingWhitespace(self):
        """
        The convertLatLong must return the expected value when passed two
        floats separated by a space with leading and trailing whitespace.
        """
        lat, lon = convertLatLong('  27.0   35.3  ')
        self.assertAlmostEqual(lat, 27.0)
        self.assertAlmostEqual(lon, 35.3)

    def testViennaFromDM(self):
        """
        The convertLatLong must return the expected value when passed the
        location of Vienna with only degrees and minutes (no seconds).
        """
        lat, lon = convertLatLong('48°12\'N 16°22\'E')
        self.assertAlmostEqual(lat, 48.2)
        self.assertAlmostEqual(lon, 16.366666666666)

    def testViennaFromDMS(self):
        """
        The convertLatLong must return the expected value when passed the
        location of Vienna with degrees, minutes, and seconds.
        """
        lat, lon = convertLatLong('48°12\'30.0"N 16°6\'15.5"E')
        self.assertAlmostEqual(lat, 48.208333333)
        self.assertAlmostEqual(lon, 16.104305555)

    def testRandom(self):
        """
        Test a random value obtained from
        https://www.fcc.gov/media/radio/dms-decimal
        """
        lat, lon = convertLatLong('22°22\'22"N 33°33\'33"E')
        self.assertAlmostEqual(lat, 22.37277777)
        self.assertAlmostEqual(lon, 33.55916666)
