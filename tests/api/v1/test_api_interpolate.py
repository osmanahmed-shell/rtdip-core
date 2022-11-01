# Copyright 2022 RTDIP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pytest_mock import MockerFixture
import pandas as pd
from datetime import datetime
from tests.sdk.python.rtdip_sdk.odbc.test_db_sql_connector import MockedDBConnection
from tests.sdk.python.rtdip_sdk.functions.test_raw import DATABRICKS_SQL_CONNECT
from tests.api.v1.api_test_objects import INTERPOLATE_MOCKED_PARAMETER_DICT, INTERPOLATE_MOCKED_PARAMETER_ERROR_DICT, INTERPOLATE_POST_MOCKED_PARAMETER_DICT, INTERPOLATE_POST_BODY_MOCKED_PARAMETER_DICT, mocker_setup, TEST_HEADERS
from fastapi.testclient import TestClient
from src.api.v1 import app

MOCK_METHOD = "src.sdk.python.rtdip_sdk.functions.interpolate.get"
MOCK_API_NAME = "/api/v1/events/interpolate"

def test_api_interpolate_get_success(mocker: MockerFixture):   
    client = TestClient(app) 

    test_data = pd.DataFrame({"EventTime": [datetime.utcnow()], "TagName": ["TestTag"], "Value": [1.01]})
    mocker = mocker_setup(mocker, MOCK_METHOD, test_data)
    
    response = client.get(MOCK_API_NAME, headers=TEST_HEADERS, params=INTERPOLATE_MOCKED_PARAMETER_DICT)
    actual = response.text
    expected = test_data.to_json(orient="table", index=False).replace("Z", "000+00:00")    

    assert response.status_code == 200
    assert actual == expected

def test_api_interpolate_get_validation_error(mocker: MockerFixture):
    client = TestClient(app) 

    test_data = pd.DataFrame({"EventTime": [datetime.utcnow()], "TagName": ["TestTag"], "Value": [1.01]})
    mocker = mocker_setup(mocker, MOCK_METHOD, test_data)
    
    response = client.get(MOCK_API_NAME, headers=TEST_HEADERS, params=INTERPOLATE_MOCKED_PARAMETER_ERROR_DICT)
    actual = response.text  

    assert response.status_code == 422
    assert actual == '{"detail":[{"loc":["query","start_date"],"msg":"field required","type":"value_error.missing"}]}'    

def test_api_interpolate_get_error(mocker: MockerFixture):
    client = TestClient(app) 

    test_data = pd.DataFrame({"EventTime": [datetime.utcnow()], "TagName": ["TestTag"], "Value": [1.01]})
    mocker = mocker_setup(mocker, MOCK_METHOD, test_data, Exception("Error Connecting to Database"))
    
    response = client.get(MOCK_API_NAME, headers=TEST_HEADERS, params=INTERPOLATE_MOCKED_PARAMETER_DICT)
    actual = response.text

    assert response.status_code == 400
    assert actual == '{"detail":"Error Connecting to Database"}'

def test_api_interpolate_post_success(mocker: MockerFixture):   
    client = TestClient(app) 

    test_data = pd.DataFrame({"EventTime": [datetime.utcnow()], "TagName": ["TestTag"], "Value": [1.01]})
    mocker = mocker_setup(mocker, MOCK_METHOD, test_data)
    
    response = client.post(MOCK_API_NAME, headers=TEST_HEADERS, params=INTERPOLATE_POST_MOCKED_PARAMETER_DICT, json=INTERPOLATE_POST_BODY_MOCKED_PARAMETER_DICT)
    actual = response.text
    expected = test_data.to_json(orient="table", index=False).replace("Z", "000+00:00")    

    assert response.status_code == 200
    assert actual == expected

def test_api_interpolate_post_validation_error(mocker: MockerFixture):
    client = TestClient(app) 

    test_data = pd.DataFrame({"EventTime": [datetime.utcnow()], "TagName": ["TestTag"], "Value": [1.01]})
    mocker = mocker_setup(mocker, MOCK_METHOD, test_data)
    
    response = client.post(MOCK_API_NAME, headers=TEST_HEADERS, params=INTERPOLATE_MOCKED_PARAMETER_ERROR_DICT, json=INTERPOLATE_POST_BODY_MOCKED_PARAMETER_DICT)
    actual = response.text  

    assert response.status_code == 422
    assert actual == '{"detail":[{"loc":["query","start_date"],"msg":"field required","type":"value_error.missing"}]}'    

def test_api_interpolate_post_error(mocker: MockerFixture):
    client = TestClient(app) 

    test_data = pd.DataFrame({"EventTime": [datetime.utcnow()], "TagName": ["TestTag"], "Value": [1.01]})
    mocker = mocker_setup(mocker, MOCK_METHOD, test_data, Exception("Error Connecting to Database"))
    
    response = client.post(MOCK_API_NAME, headers=TEST_HEADERS, params=INTERPOLATE_MOCKED_PARAMETER_DICT, json=INTERPOLATE_POST_BODY_MOCKED_PARAMETER_DICT)
    actual = response.text

    assert response.status_code == 400
    assert actual == '{"detail":"Error Connecting to Database"}'