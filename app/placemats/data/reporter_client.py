import requests
import datetime
import logging
from collections import namedtuple

logger = logging.getLogger(__name__)


URL = 'https://api.federalreporter.nih.gov/v1/projects/search?'
LIMIT = '50'
TOTAL_RECORDS = 1000


BudgetInfo = namedtuple('BudgetInfo', ['reporter_info','grant_count'])


def get_response(term, offset_value):
    search_query = "query=text:"+term
    search_fields = "$textFields:title,abstract,terms"
    offset = "&offset="+str(offset_value)
    retrieval_limit = "&limit="+LIMIT
    response = requests.get(URL+search_query+search_fields+offset+retrieval_limit)
    logger.debug('Connected to RePORTER with status code: {}, starting offset is {}'.format(response.status_code, offset_value))
    return response.json()


def reporter_search(term):
    term = term
    offset_value = 1
    reporter_info = []
    grant_count = ''
    while True:
        # loop body
        info = get_response(term, offset_value)
        if offset_value > TOTAL_RECORDS:
            break
        else:
            grant_count = info['totalCount']
            reporter_info = reporter_info + info['items']
            offset_value += 50
            # Sort by Total Amount; Descending Order
    #reporter_removed = reporter_info.filter(lambda x: x.get('totalCostAmount') not in None, reporter_info )
    reporter_info_sorted = sorted(reporter_info, key=lambda k: k['totalCostAmount'], reverse=True)

    return BudgetInfo(reporter_info_sorted,grant_count)


def time_duration(dateStart,dateEnd):
    ## Takes two date  strings in the format  2014-05-31T00:00:00
    ## Calculate the difference between in terms of years
    if not dateStart:
        return None
    elif not dateEnd:
        return None
    else:
        st = datetime.datetime.strptime(dateStart, '%Y-%m-%dT%H:%M:%S')
        et = datetime.datetime.strptime(dateEnd, '%Y-%m-%dT%H:%M:%S')
        duration = et - st
        return(duration.days/365)





