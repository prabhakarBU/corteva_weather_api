import pytest
import json
from app import app

def test_index_route():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data.decode('utf-8') == '<h2>This is just a basic Flask Application</h2>'

@pytest.mark.get_request
def testGetAllWeatherDataPaginated():
    response = app.test_client().get('/api/weather')
    res = json.loads(response.data.decode('utf-8'))
    assert type(res[0]) is dict
    assert res[0]['stationId'] == 'USC00110072'
    assert response.status_code == 200
    assert type(res) is list

@pytest.mark.get_request
def testGetAllWeatherDataByStationId():
    response = app.test_client().get('/api/weather/station/USC00110072')
    res = json.loads(response.data.decode('utf-8'))
    assert type(res[0]) is dict
    assert res[0]['stationId'] == 'USC00110072'
    assert len(res) == 5
    assert response.status_code == 200
    assert type(res) is list

@pytest.mark.get_request
def testGetAllWeatherDataByDate():
    response = app.test_client().get('/api/weather/date/1985-01-01')
    res = json.loads(response.data.decode('utf-8'))
    assert type(res[0]) is dict
    assert res[0]['date'] == '01-01-1985'
    assert len(res) == 5
    assert response.status_code == 200
    assert type(res) is list

@pytest.mark.get_request
def testGetAllWeatherStatsData():
    response = app.test_client().get('/api/weather/stats')
    res = json.loads(response.data.decode('utf-8'))
    assert type(res[0]) is dict
    assert res[0]['year'] == 1985
    assert len(res) == 5
    assert response.status_code == 200
    assert type(res) is list

@pytest.mark.get_request
def testGetAllWeatherStatsDataByStationId():
    response = app.test_client().get('/api/weather/stats/station/USC00110072')
    res = json.loads(response.data.decode('utf-8'))
    assert type(res[0]) is dict
    assert res[0]['stationId'] == 'USC00110072'
    assert len(res) == 5
    assert response.status_code == 200
    assert type(res) is list

@pytest.mark.get_request
def testGetAllWeatherStatsDataByStationIdPaginatedWithOffset():
    response = app.test_client().get('/api/weather/stats/station/USC00110072/0/5')
    res = json.loads(response.data.decode('utf-8'))
    assert type(res[0]) is dict
    assert res[0]['stationId'] == 'USC00110072'
    assert len(res) == 5
    assert response.status_code == 200
    assert type(res) is list

@pytest.mark.get_request
def testGetAllWeatherStatsDataByYear():
    response = app.test_client().get('/api/weather/stats/year/1985')
    res = json.loads(response.data.decode('utf-8'))
    assert type(res[0]) is dict
    assert res[0]['year'] == 1985
    assert len(res) == 5
    assert response.status_code == 200
    assert type(res) is list

@pytest.mark.get_request
def testGetAllWeatherStatsDataByYearPaginatedWithOffset():
    response = app.test_client().get('/api/weather/stats/year/1985/0/5')
    res = json.loads(response.data.decode('utf-8'))
    assert type(res[0]) is dict
    assert res[0]['year'] == 1985
    assert len(res) == 5
    assert response.status_code == 200
    assert type(res) is list