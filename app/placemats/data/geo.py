import logging
from collections import Counter
from geotext import GeoText
from iso3166 import countries
from collections import namedtuple

logger = logging.getLogger(__name__)

CountryInfo = namedtuple('CountryInfo', ['country_counts', 'code_to_country'])


def get_country_counts(strings):
    country_counts = Counter()
    for s in strings:
        mentions = GeoText(s).country_mentions
        for country in mentions:
            country_counts[country] += 1  # bump per string; ignore freq. of mentions within one string
    code_to_country = {k: countries.get(k) for k in country_counts}
    return country_counts, code_to_country
