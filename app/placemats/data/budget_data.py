import logging
from collections import namedtuple
from app.placemats.data.reporter_client import *
logger = logging.getLogger(__name__)

PROJECT_ID = 'projectNumber'
PROJECT_TITLE = 'title'
FY = 'fy'
PROJECT_START = 'projectStartDate'
PROJECT_END = 'projectEndDate'
BUDGET = 'totalCostAmount'
ORGANIZATION = 'orgName'
PROJECT_PI = 'contactPi'
IC = 'ic'
DEPT = 'department'
AGENCY = 'agency'

BudgetDetails = namedtuple('BudgetDetails', ['total_grant_count', 'cumulative_grant_amount', 'budget_data'])
def budget_data_array(info_list: list, total_grant_count = 0):
    total_grant_count = total_grant_count
    cumulative_grant_amount = 0
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
        '''
        if each_record[AGENCY] == 'NIH':
            grant_type = each_record[PROJECT_ID][1:4]
        else:
            grant_type = each_record[AGENCY]
            if not grant_type:
                grant_type = each_record[DEPT]
        '''

        grant_type = ''
        grant_legend = ''

        if each_record[AGENCY] == 'NIH':
            idx = each_record['projectNumber'][1]
            if idx in ['F', 'K', 'P', 'R', 'S', 'D', 'U']:
                grant_type = each_record['projectNumber'][1:4]
                grant_legend = idx
            else:
                grant_type = each_record[IC]
                grant_legend = 'NIH_Oth'
        elif each_record[DEPT] == 'DOD':
            grant_type = 'DOD'
            grant_legend = 'DOD'
        elif each_record[AGENCY] == 'NSF':
            grant_type = 'NSF'
            grant_legend = 'NSF'
        else:
            grant_type = each_record[AGENCY]
            grant_legend = 'Other'
        fiscal_year = each_record[FY]
        project_budget = int(each_record[BUDGET])
        cumulative_grant_amount += project_budget
        project_duration = time_duration(each_record[PROJECT_START], each_record[PROJECT_END])
        grantee = each_record[ORGANIZATION]
        project_pi = each_record[PROJECT_PI]
        budget_data.append({'name': each_record[PROJECT_TITLE],
                            'positions': {'total': {'x': 0, 'y': 0}},
                            'id': arr_id,
                            'fy': fiscal_year,
                            'budget_2013': project_budget,
                            'change': project_duration,
                            'department': grantee,
                            'project_pi': project_pi,
                            'discretion': grant_type,
                            'grant_legend': grant_legend})  # color
        arr_id += 1
        if arr_id > max_arr_length:
            break

    return total_grant_count, cumulative_grant_amount, budget_data
