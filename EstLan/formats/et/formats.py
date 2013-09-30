GATEME_EVENT = 'l, j F H:i'                         # 'reede, 9 Oktoober 14:30'
GATEME_EVENT_SHORT = 'j N H:i'                      # '9 Okt. 14:30'
GATEME_SHORT_DATE = 'd.m'                           # '09.10'
GATEME_GRAPH_DATE = 'D j.m'                         # 'R 9.10'
GATEME_EVENT_HEADER = 'l j.m'                       # 'reede 9.10'
GATEME_EVENT_POSTER = 'j. N'                        # '9. Okt'

DATETIME_FORMAT = 'j. F Y H:i'                      # '9. Oktoober 2006 14:30'
DATE_FORMAT = 'j. F Y'                              # '9. Oktoober 2006'
DATE_NO_YEAR_FORMAT = 'j. F'                        # '9. Oktoober'
TIME_FORMAT = 'H:i'                                 # '14:30'
#SHORT_DATE_FORMAT = 'd.m.Y'                        # '09.10.2006'
SHORT_DATE_FORMAT_JS = 'dd.mm.yy'                   # '25.10.2006' for javascript
SHORT_DATETIME_FORMAT = 'd.m.Y, H:i'                # '09.10.2006, 14:30'
DATETIME_FORMAT_JS = 'j.m, H:i'                     # '9.10, 14:30'

DATE_INPUT_FORMATS = (
    '%d.%m.%Y', '%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y', # '25.10.2006', '2006-10-25', '10/25/2006', '10/25/06'
)
TIME_INPUT_FORMATS = (
    '%H:%M',                                        # '14:30'
    '%H:%M:%S',                                     # '14:30:59'
)
DATETIME_INPUT_FORMATS = (
    '%d.%m.%Y %H:%M:%S',                            # '25.10.2006 14:30:59'
    '%d.%m.%Y %H:%M',                               # '25.10.2006 14:30'
    '%Y-%m-%d %H:%M:%S',                            # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M',                               # '2006-10-25 14:30'
    '%d/%m/%Y %H:%M:%S',                            # '10/25/2006 14:30:59'
    '%d/%m/%Y %H:%M',                               # '10/25/2006 14:30'
    '%d/%m/%y %H:%M:%S',                            # '10/25/06 14:30:59'
    '%d/%m/%y %H:%M',                               # '10/25/06 14:30'
)

DECIMAL_SEPARATOR = '.'

CSV_DELIMITER = ';'

NUMBER_GROUPING = 3
