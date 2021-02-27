import os
import re
import pandas as pd
import json
import requests
import logging
from progress.bar import ShadyBar
from FileUtils import FileUtils as fru
from JSONUtils import JSONUtils as jru
from PandasUtils import PandasUtils as pru
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define logging
# Create logger definition
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create file handler which logs messages in log file
fh = logging.FileHandler(__name__)
fh.setLevel(logging.DEBUG)

# Create console handler with high level log messages in console
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(ch)
# logger.addHandler(fh)

# ALM connector URL
connector_url = 'http://almconnector:8080'
server_url = ''

alm_domain = None
alm_project = None

username = None
password = None

tp_parent_folder_id = '1'

# test plan folder creation params
alm_user_name = None
alm_password = None
test_plan_folder_id = None
test_parent_folder_id = None
test_name = None


def automation_framework_folder_creation(project_dir, project_name, host_name):
    logger.debug('****************************************************************************************************')
    logger.debug('Create automation test suite with default robot test case')
    logger.debug('****************************************************************************************************')

    # Create folders based on standard template
    os.mkdir(project_dir + project_name)
    folder_list = ['/data/Test_Inputs', '/results/actual_results', '/results/expected_results',
                   '/results/comparison_results', '/scripts', '/testcases', '/config']
    logger.info('  Automation Test Folder Creation In Progress ....')

    # Iterate through folder list and create required folders
    for item in folder_list:
        path = project_dir + project_name + item
        try:
            os.makedirs(path)
        except OSError:
            logger.info('Unable to create automation directories')

        # Create the standard robot regression test suite
        if re.search(r'testcases', item):
            file_path = path + '/' + project_name + '_Regression.robot'
            f = open(file_path, 'w+')
            f.write(automation_test_case_creation(project_name))
            f.close()

            file_path = path + '/' + 'Report_HTML_Generation.robot'
            f = open(file_path, 'w+')
            f.write(automation_html_report_generation_test_case_creation())
            f.close()

        # Create the script folder and suite_common_library/global_variables.py files
        if re.search(r'scripts', item):
            file_path = path + '/' + 'suite_common_library.py'
            f = open(file_path, 'w+')
            f.write(automation_suite_common_script_creation(project_name))
            f.close()

            file_path = path + '/' + 'global_variables.py'
            f = open(file_path, 'w+')
            f.write(automation_global_variables_creation(project_name, host_name))
            f.close()

        # Create the script folder and suite_common_library/global_variables.py files
        if re.search(r'config', item):
            file_path = path + '/' + 'alm_py_client.py'
            f = open(file_path, 'w+')
            # f.write(automation_suite_common_script_creation(project_name))
            f.close()

            file_path = path + '/' + 'alm_py_client_lib.py'
            f = open(file_path, 'w+')
            # f.write(automation_global_variables_creation(project_name, host_name))
            f.close()

            file_path = path + '/' + 'config.ini'
            f = open(file_path, 'w+')
            # f.write(automation_global_variables_creation(project_name, host_name))
            f.close()

            file_path = path + '/' + 'report_config.json'
            f = open(file_path, 'w+')
            f.write(automation_report_config_creation())
            f.close()

    # Create the standard execution trigger script
    file_path = project_dir + project_name + '/' + 'results' + '/' + 'Trigger_Execution.bat'
    f = open(file_path, 'w+')
    content = r'robot -d . ' + project_dir + project_name + r'/testcases/' + project_name + '_Regression.robot'
    f.write(content)
    f.close()

    # Create the standard execution trigger script - shell script
    file_path = project_dir + project_name + '/' + 'results' + '/' + 'Trigger_Execution.sh'
    f = open(file_path, 'w+')
    content = r'robot -d . ' + project_dir + project_name + r'/testcases/' + project_name + '_Regression.robot'
    f.write(content)
    f.close()

    logger.info('  Automation Test Folder Created Successfully !!!!')
    logger.debug('****************************************************************************************************')


def automation_test_case_creation(project_name):

    # Standard template robot test case
    content = """*** Settings ***
Suite Setup     Create and execute test cases dynamically using test data sheet    ${test_data_full_path}
Library         Collections
Library         String
Library         RequestsProLibrary/DynamicTestCases.py
Library         RequestsProLibrary
Library         ${CURDIR}${/}..${/}scripts${/}suite_common_library.py
Variables       ${CURDIR}${/}..${/}scripts${/}global_variables.py
Suite Teardown    Delete All Sessions

*** Variables ***
${baseline_env}    UAT
${actual_env}    QA
${test_data_full_path}    ${CURDIR}${/}..${/}data${/}Test_Inputs${/}project_name_api_test_data.csv
${test_data_full_path}    ${CURDIR}${/}..${/}data${/}Test_Inputs${/}project_name_api_test_data_UAT.csv
${test_data_full_path}    ${CURDIR}${/}..${/}data${/}Test_Inputs${/}project_name_api_test_data_QA.csv

${actual_results_path}    ${CURDIR}${/}..${/}results${/}actual_results${/}
${expected_results_path}    ${CURDIR}${/}..${/}results${/}expected_results${/}
${test_input_path}    ${CURDIR}${/}..${/}data${/}Test_Inputs${/}
${comparison_results_path}    ${CURDIR}${/}..${/}results${/}comparison_results${/}

*** Test Cases ***
Placeholder Test
    [Tags]    exclude
    Log    ${test_data_full_path}
    Log    Placeholder test required by Robot Framework

*** Keywords ***
Generate and compare expected/actual results
    [Arguments]    ${test_name}
    Generate Actual Results    ${test_data_full_path}    ${test_name}    ${actual_results_path}    ${test_input_path}    ${actual_env}
    Generate Expected Results    ${test_data_full_path}    ${test_name}    ${expected_results_path}    ${test_input_path}    ${baseline_env}
    Compare Actual and Expected Results    ${test_data_full_path}    ${test_name}    ${comparison_results_path}    ${actual_results_path}${/}${test_name}${/}    ${expected_results_path}${/}${test_name}${/}    ${test_name}_response_data    ${test_name}_response_data
    
Create and execute test cases dynamically using test data sheet
    [Arguments]    ${test_data_full_path}
    Set Log Level    INFO
    Log    ${test_data_full_path}
    Log    Get the list of test cases to be executed
    ${test_cases_list}=    API Test Cases List    ${test_data_full_path}
    ${no_of_test_cases}=    Get Length    ${test_cases_list}
    Log    Iterate through each test case and execute the test case
    FOR    ${i}    IN RANGE    ${no_of_test_cases}
        ${test_name}=    Get From Dictionary    ${test_cases_list}[${i}]    test_name
        ${tags}=    Get From Dictionary    ${test_cases_list}[${i}]    test_tags
        @{test_tags}=    Split String    ${tags}    ,        
        ${doc}=    Get From Dictionary    ${test_cases_list}[${i}]    test_documentation
        Add Test Case    ${test_name}    ${doc}    ${test_tags}    Generate and compare expected/actual results    ${test_name}
    END

Generate Actual Results
    [Arguments]    ${test_data_full_path}    ${test_name}    ${actual_results_path}    ${test_input_path}    ${actual_env}
    Generate API Test Results    ${test_data_full_path}    ${test_name}    ${actual_results_path}    ${test_input_path}    ${actual_env}

Generate Expected Results
    [Arguments]    ${test_data_full_path}    ${test_name}    ${expected_results_path}    ${test_input_path}    ${baseline_env}
    Generate API Test Results    ${test_data_full_path}    ${test_name}    ${expected_results_path}    ${test_input_path}    ${baseline_env}
    
"""
    content = content.replace('project_name', project_name)
    return content


def automation_report_config_creation():
    # Standard template robot test case
    content = """{
"db_engine": "postgresql",
"database": "robot_results",
"host": "localhost",
"port": "5432",
"user": "postgres",
"password": "yourpassword",
"require_ssl": "False"
}
"""
    return content


def automation_html_report_generation_test_case_creation():
    # Standard template robot test case
    content = """*** Settings ***
Documentation     This test case is used to generate html report which can be incorporated in status email
Library         RFUtils/RFUtils.py
*** Variables ***
${output_xml}    ${CURDIR}${/}..${/}results${/}output.xml
${output_csv}    ${CURDIR}${/}..${/}results${/}output.csv
${output_html}    ${CURDIR}${/}..${/}results${/}output.html

*** Test Cases ***
Status Report Generation
    [Tags]    Report_Generation
    email_trigger    ${output_xml}    ${output_csv}    ${output_html}

"""
    return content


def automation_suite_common_script_creation(project_name):

    # Standard template robot test case
    content = """from RequestsProLibrary import RequestsProKeywords
from robot.api.deco import keyword
from FileUtils import FileUtils as fru
from PandasUtils import PandasUtils as pru
import sys
import os
import logging
import json
import pandas as pd
import global_variables as gl
import numpy as np
import requests

# requests.packages.urllib3.disable_warnings(requests.package.urllib3.exceptions.InsecureRequestWarning)

sys.path.append(os.path.pardir + r'/scripts/')

# get logger from automation execution
logger = logging.getLogger('project_name.api_execution_log')


@keyword('Generate API Test Results')
def generate_api_results(test_data_full_path, api_name, results_path, test_input_path, environment):
    logger.info('****************************************************************************************************')
    logger.info('Trigger API and extract response - ' + api_name)
    logger.info('****************************************************************************************************')
    logger.info('Step-01 : Start - Read and filter test data file based on API Name')
    test_cases_df = pd.read_csv(test_data_full_path)
    selected_api_df = test_cases_df.loc[test_cases_df['test_name'] == api_name].copy()
    selected_api_df = selected_api_df.loc[selected_api_df['tbe'] == 'YES'].reset_index()
    logger.info('Step-01 : End   - Read and filter test data file based on API Name')

    logger.info('Step-02 : Start - Based on the selected environment trigger the API')
    expected_env_url = ''

    # condition to check if base_env_url is provided globally to override base_env_url from test data sheet
    logger.debug(environment)
    if not environment:
        execution_env = str(selected_api_df['Base_ENV'][0])
    else:
        execution_env = environment

    # Based on execution_env identify the server details from global variables and assign to expected_env_url
    if execution_env == 'DEV':
        expected_env_url = gl.dev_server_name
    elif execution_env == 'QA':
        expected_env_url = gl.qa_server_name
    elif execution_env == 'UAT':
        expected_env_url = gl.uat_server_name
    elif execution_env == 'PROD':
        expected_env_url = gl.prod_server_name

    # Based on the extract_response flag, API responses will be extracted to specified format
    extract_response = str(selected_api_df['extract_response'][0])
    response_format = str(selected_api_df['response_format'][0])

    # Based on the test type trigger the test, if test_type is API trigger the API to extract the response
    rl = RequestsProKeywords()
    selected_api_df = rl.trigger_api(test_data_full_path, test_input_path, api_name, expected_env_url)
    logger.info('Step-02 : End   - Based on the selected environment trigger the API')

    logger.info('Step-03 : Start - Based on response validation flag generate the results')
    response_validation = str(selected_api_df['response_validation'][0])

    # delete and create new actual results folder for the test
    fru.delete_and_create_dir(results_path + api_name)

    actual_results_df = pd.DataFrame([])
    logger.debug(api_name.lower())
    api_response_df = selected_api_df.filter(
        ['test_name', 'API_Response_Code', 'API_Response_Content']).copy()
    pru.write_df_to_csv(api_response_df, results_path + api_name + '/', api_name + '.csv')

    # if response_validation is YES perform detailed validation else check for 200 status code
    api_response_data = selected_api_df['API_Response_Content'][0]
    if extract_response.upper() == 'YES':
        file_path = results_path + '/' + api_name + '/' + api_name + '.' + response_format
        f = open(file_path, "w+")
        f.write(api_response_data)
        f.close()

    if (response_validation == 'YES') or (response_validation == 'PREDEFINED'):
        logger.debug(api_name.lower())
        extract_data_from_api_response(api_name, api_response_data, results_path)
    else:
        api_response_df_flt = api_response_df.filter(['test_name', 'API_Response_Content'])
        logger.debug(api_response_df_flt)
        pru.write_df_to_csv(api_response_df_flt, results_path + api_name + '/' , api_name + '_response_data.csv') 

    logger.info('Step-03 : End   - Based on response validation flag generate the results')
    logger.info('****************************************************************************************************')
    return api_response_df
    
    
class ExecutionStatus(Exception):
    def __init__(self, data):
        self.data = data
        
    def __str__(self):
        return repr(self.data)


@keyword('Compare Actual and Expected Results')
def compare_actual_expected_results(test_data_full_path, api_name, comparison_file_path, actual_file_path,
                                    expected_file_path, actual_file_name, expected_file_name):
    logger.info('****************************************************************************************************')
    logger.info('Compare expected and actual results - ' + api_name)
    logger.info('****************************************************************************************************')
    logger.info('Step-01 : Start - Read and filter test data file based on API Name')
    test_cases_df = pd.read_csv(test_data_full_path)
    selected_api_df = test_cases_df.loc[test_cases_df['test_name'] == api_name].copy()
    selected_api_df = selected_api_df.loc[selected_api_df['tbe'] == 'YES'].reset_index()
    logger.info('Step-01 : End   - Read and filter test data file based on API Name')

    file_format = 'csv'
    keys = str(selected_api_df['key_columns'][0]).split(',')
    if str(selected_api_df['ignore_columns'][0]) == 'nan':
        ignore_columns = []
    else:
        ignore_columns = str(selected_api_df['ignore_columns'][0]).split(',')
        
    exec_summary_df, dup_cons_df, key_matched_df, key_mismatched_df, cell_comp_df = \
        pru.df_diff(actual_file_path, expected_file_path, actual_file_name, expected_file_name, file_format, keys,
                    ignore_columns)
                    
    # Delete and create new comparison results folder for the test
    fru.delete_and_create_dir(comparison_file_path + api_name)
    
    tc_execution_status = 'PASSED'
    
    # Check if we have mismatch count in exec_summary_df and update the execution status
    if int(exec_summary_df['Mismatch'].sum()) > 0:
        tc_execution_status = 'FAILED'
    
    # Write the exec_summary
    pru.write_df_to_csv(exec_summary_df, comparison_file_path + '/' + api_name + '/', 'executive_summary.csv')
    
    # Write duplicate records based on key values
    if len(dup_cons_df) > 0:
        tc_execution_status = 'FAILED'
        pru.write_df_to_csv(dup_cons_df, comparison_file_path + '/' + api_name + '/', 'duplicate_records.csv', 
                            index=True)
                            
    # Write the matched records based on the key values
    key_matched_df['comparison_status'] = 'PASSED'
    del key_matched_df['source']
    pru.write_df_to_csv(key_matched_df, comparison_file_path + '/' + api_name + '/', 'matched_records.csv', index=True)
    
    # Write the mismatched records based on the key values
    if len(key_mismatched_df) > 0:
        tc_execution_status = 'FAILED'
        
        key_mismatched_df['comparison_status'] = key_mismatched_df['source']
        
        key_mismatched_df['additional_info'] = \
            np.where(key_mismatched_df['comparison_status'] == 'right_only', 'Additional records in actual', '')
            
        key_mismatched_df['additional_info'] = \
            np.where(key_mismatched_df['comparison_status'] == 'left_only', 'Missing records in expected',
                    key_mismatched_df['additional_info'])
            
        key_mismatched_df['comparison_status'] = 'FAILED'
        del key_mismatched_df['source']
    
        pru.write_df_to_csv(key_mismatched_df, comparison_file_path + '/' + api_name + '/', 'mismatched_records.csv', 
                            index=True)
    
    # Write the cell by cell mismatch based on the key values
    if len(cell_comp_df) > 0:
        tc_execution_status = 'FAILED'
        
        pru.write_df_to_csv(cell_comp_df, comparison_file_path + '/' + api_name + '/', 'mismatched_cell_by_cell.csv', 
                        index=True)
        
    if 'FAILED' == tc_execution_status:
        raise ExecutionStatus('Comparison of ' + api_name + ' - ' + tc_execution_status)
    else:
        logger.info('Comparison of ' + api_name + ' - ' + tc_execution_status)

    logger.info('****************************************************************************************************')


def extract_data_from_api_response(api_name, api_response_data, results_path):
    logger.info('****************************************************************************************************')
    logger.info('Extract data from api response and create csv file')
    logger.info('****************************************************************************************************')
    logger.info('Step-01 : Start - Extract specific information from API response json')
    
    # project specific code
    if any(selected_tc in api_name for selected_tc in ['api_name1', 'api_name2']):
        if 'api_name1' in api_name:
            # some code
            logger.info('code')
        else:
            api_response_df = pd.read_json(open(results_path + api_name + '/' + api_name + '.JSON'))
            api_response_df = pd.json_normalize(api_response_df.to_dict('records'))

    else:
    
        json_data = json.load(open(results_path + api_name + '/' + api_name + '.JSON', ), encoding='utf-8')
        
        logger.debug(json_data)
        
        try:
            # api_response_df = pd.DataFrame(json_data)
            api_response_df = pd.json_normalize(json_data['rowData'])
        except:
            api_response_df = pd.DataFrame(json_data, index=[0])
            
    dir_name = results_path + api_name
    logger.info(dir_name)
    if not os.path.exists(dir_name):
        os.mkdir(results_path + api_name)
    pru.write_df_to_csv(api_response_df, results_path + api_name + '/', api_name + '_response_data.csv')

    logger.info('Step-01 : End   - Extract specific information from API response json')
    logger.info('****************************************************************************************************')
    return api_response_df
    
"""
    content = content.replace('project_name', project_name)
    return content


def automation_global_variables_creation(project_name, host_name):

    # Standard template robot test case
    content = """import os
# Assign path variables
root_dir = os.path.split(os.path.abspath(''))[0]

# Environment Variables
dev_server_name = 'host_name'
qa_server_name = 'host_name'
uat_server_name = 'host_name'
prod_server_name = 'host_name'

"""
    content = content.replace('project_name', project_name)
    content = content.replace('host_name', host_name)
    # content = content.replace('port_no', port_no)
    return content


def create_alm_test_folder(**kwargs):
    logger.debug('****************************************************************************************************')
    logger.debug('Create ALM Project Folders')
    logger.debug('****************************************************************************************************')

    logger.info('  ALM Project Folder Creation In Progress ....')
    global test_plan_folder_name

    # test plan folder creation params
    create_tp_folder_request_body = {
        "url": server_url,
        "domain": alm_domain,
        "project": alm_project,
        "username": alm_user_name,
        "password": alm_password,
        "folderid": tp_parent_folder_id,
        "user01": alm_user_name,
        "name": test_plan_folder_name,
    }

    # sending get request and saving the response as response object
    r = requests.post(url=connector_url + 'testfolder/', json=create_tp_folder_request_body)

    # convert the json response to string
    json_string = str(r.content.decode('utf-8'))

    # deserialize json_string to python object
    api_json_response_data = json.loads(json_string)

    api_response_df = jru.convert_json_to_data_frame(api_json_response_data)
    logger.debug(api_response_df)
    logger.debug('****************************************************************************************************')

    return api_json_response_data['id']


def create_alm_tests(**kwargs):

    global test_name

    # test plan folder creation params
    create_tp_tests_request_body = {
        "url": server_url,
        "domain": alm_domain,
        "project": alm_project,
        "username": alm_user_name,
        "password": alm_password,
        "folderid": tp_parent_folder_id,
        "user01": alm_user_name,
        "name": test_name,
        "steps": [
            {"name": "steps", "values":[{"value":"0"}]}],
        "custom": [
            {"name": "user-01", "value": "1 - High"},
            {"name": "user-07", "value": "1 - High"},
            {"name": "user-09", "value": "Automated"},
            {"name": "user-10", "value": "Robot"},
            {"name": "status", "value": "Design"},
            {"name": "owner", "value": alm_user_name},
        ],
    }

    # sending get request and saving the response as response object
    r = requests.post(url=connector_url + 'tests/', json=create_tp_tests_request_body)

    logger.debug(str(r.content))


def generate_api_test_data_using_swagger(url=None, project_dir=None, project_name=None, **kwargs):

    logger.debug('****************************************************************************************************')
    logger.debug('Create automation test data sheet using application swagger url')
    logger.debug('****************************************************************************************************')

    # extract the swagger json definition using the url
    response = requests.get(url, verify=False)
    swagger_json_data = response.json()
    logger.info('  Automation Test Data Creation In Progress ....')

    # define test data df and columns required for test data sheet
    test_data_df = pd.DataFrame(columns=['tbe', 'test_suite_name', 'test_name', 'test_documentation', 'test_tags',
                                         'test_type', 'request_type', 'uri'])

    # define df to hold parameters for each api
    parameter_df = pd.DataFrame([])

    # extract the api definition from the swagger json data

    # extract the base path of the api definition
    base_path = swagger_json_data['basePath']

    # bar1 = ShadyBar(r'Automation Test Data Creation In Progress', suffix='%(percent)d%%')

    # iterate and extract api details
    for (k, v) in swagger_json_data['paths'].items():

        # temp df to store the api details
        test_data_tmp_df = pd.DataFrame(columns=['tbe', 'test_suite_name', 'test_name', 'test_documentation',
                                                 'test_tags', 'test_type', 'request_type', 'uri'])

        # temp df to store the parameter details
        parameter_tmp_df = pd.DataFrame([])

        if type(v) is dict:
            for(k1, v1) in v.items():
                test_data_tmp_df['test_suite_name'] = v1['tags']
                test_data_tmp_df['test_name'] = v1['operationId']

                # check if summary is blank and assign value as test documentation
                if 'summary' in v1:
                    test_data_tmp_df['test_documentation'] = v1['summary']

                test_data_tmp_df['test_tags'] = 'Sanity'
                test_data_tmp_df['tbe'] = 'NO'
                test_data_tmp_df['extract_response'] = 'YES'
                test_data_tmp_df['key_columns'] = ''
                test_data_tmp_df['ignore_columns'] = ''
                test_data_tmp_df['response_format'] = 'JSON'
                test_data_tmp_df['response_validation'] = 'NO'
                test_data_tmp_df['test_type'] = 'API'
                test_data_tmp_df['request_type'] = k1.upper()
                test_data_tmp_df['uri'] = base_path + k
                test_data_tmp_df['data'] = ''
                test_data_tmp_df['auth'] = ''
                test_data_tmp_df['headers'] = ''
                test_data_tmp_df['files'] = ''

                # check parameters and assign values for each api
                if 'parameters' in v1:
                    parameter_tmp_df = pd.DataFrame(v1['parameters'])
                    parameter_tmp_df['test_name'] = v1['operationId']

                    for i, row in parameter_tmp_df.iterrows():
                        parameter_name = row['name'] + '_d'

                        if 'x-example' in parameter_tmp_df.columns:
                            test_data_tmp_df[parameter_name] = row['x-example']
                        else:
                            test_data_tmp_df[parameter_name] = ''

                    if parameter_df.empty:
                        parameter_df = parameter_tmp_df.copy()
                    else:
                        parameter_df = parameter_df.append(parameter_tmp_df, ignore_index=True, sort=False)

        if test_data_df.empty:
            test_data_df = test_data_tmp_df.copy()
        else:
            test_data_df = test_data_df.append(test_data_tmp_df, ignore_index=True, sort=False)

    #     bar1.next()
    #
    # bar1.finish()

    pru.write_df_to_csv(test_data_df, project_dir + project_name + '/data/Test_Inputs/',
                        project_name + '_api_test_data.csv')
    pru.write_df_to_csv(parameter_df, project_dir + project_name + '/data/Test_Inputs/',
                        project_name + '_all_parameters.csv')

    parameter_df = parameter_df[['test_name', 'name', 'description', 'required', 'type']]
    pru.write_df_to_csv(parameter_df, project_dir + project_name + '/data/Test_Inputs/',
                        project_name + '_parameters_key_details.csv')

    logger.info('  Automation Test Data Created Successfully !!!!')
    # logger.info(test_data_df)
    # logger.info(parameter_df)




