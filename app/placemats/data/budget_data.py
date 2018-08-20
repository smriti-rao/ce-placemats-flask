import logging
from app.placemats.data.reporter_client import *
logger = logging.getLogger(__name__)

PROJECT_ID = 'projectNumber'
PROJECT_TITLE = 'title'
PROJECT_START = 'projectStartDate'
PROJECT_END = 'projectEndDate'
BUDGET = 'totalCostAmount'
ORGANIZATION = 'orgName'
PROJECT_PI = 'contactPi'
DEPT = 'department'
AGENCY = 'agency'

def budget_data_array(info_list: list):

    max_arr_length = 100
    arr_id = 1

    budget_data = []
    for each_record in info_list:

        if not each_record[PROJECT_START]:
            logger.warning('Project Start Date not found for grant, PROJECT_ID: %s',  each_record[PROJECT_ID])
            continue
        if not each_record[PROJECT_END]:
            logger.warning('Project End Date not found for grant, PROJECT_ID: %s', each_record[PROJECT_ID])
            continue
        if not each_record[BUDGET]:
            logger.warning('Project Total Cost not found for grant, PROJECT_ID: %s', each_record[PROJECT_ID])
            continue

        if each_record[AGENCY] == 'NIH':
            grant_type = each_record[PROJECT_ID][1:4]
        else:
            grant_type = each_record[AGENCY]
            if not grant_type:
                grant_type = each_record[DEPT]

        project_duration = time_duration(each_record[PROJECT_START], each_record[PROJECT_END])
        grantee = each_record[ORGANIZATION]+'; '+each_record[PROJECT_PI]
        budget_data.append({'name': each_record[PROJECT_TITLE],
                            'positions': {'total': {'x': 0, 'y': 0}},
                            'id': arr_id,
                            'budget_2013': int(each_record[BUDGET]),
                            'change': project_duration,
                            'department': grantee,
                            'discretion': grant_type})
        arr_id += 1
        if arr_id > max_arr_length:
            break
    return budget_data
