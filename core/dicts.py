'''
Created on Aug 21, 2014

@author: Kristian
'''
from collections import OrderedDict

# Platform codes.
IPHONE  = 1
ANDROID = 2

PLATFORMS = {
    IPHONE: "iPhone",
    ANDROID: "Android",
}

LANGUAGE_CODES = {
    "us": "en",
    "jp": "ja",
}

# Choices for platforms.
PLATFORM_CHOICES = (
    (IPHONE, "iPhone"),
    (ANDROID, "Android"),
)

# Choices for regions.
COUNTRY_CHOICES = OrderedDict((
    ('us', "United States"),
    ('gb', "UK"),
    ('au', "Australia"),
    ('ca', "Canada"),
    ('de', "Germany"),
    ('fr', "France"),
    ('it', "Italy"),
    ('es', "Spain"),
    ('nl', "The Netherlands"),
    ('jp', "Japan"),
    ('ru', "Russia"),
    ('kr', "Korea"),
    ('cn', "China"),
))

CURRENCIES = {
    'us': "USD",
    'gb': "GBP",
    'au': "AUD",
    'ca': "CAD",
    'de': "EUR",
    'fr': "EUR",
    'it': "EUR",
    'es': "EUR",
    'nl': "EUR",
    'jp': "JPY",
    'ru': "RUB",
    'kr': "USD",
    'cn': "CNY",
}

# Choices for ranking types.
TOP_FREE     = 1
TOP_PAID     = 2
TOP_GROSSING = 3
NEW_FREE     = 4
NEW_PAID     = 5
NEW_GROSSING = 6

TYPE_CHOICES = (
    (TOP_FREE, 'Top Free Apps'),
    (TOP_PAID, 'Top Paid Apps'),
    (TOP_GROSSING, 'Top Grossing Apps'),
    (NEW_FREE, 'New Free Apps'),
    (NEW_PAID, 'New Paid Apps'),
    (NEW_GROSSING, 'New Grossing Apps'),
)

ITUNES_TYPESTRINGS = {
    TOP_FREE: 'topfreeapplications',
    TOP_PAID: 'toppaidapplications',
    TOP_GROSSING: 'topgrossingapplications',
    NEW_FREE: 'newfreeapplications',
    NEW_PAID: 'newpaidapplications',
    NEW_GROSSING: 'newgrossingapplications',
}
