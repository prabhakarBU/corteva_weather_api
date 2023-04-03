from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask, jsonify, request, abort
from datetime import datetime, timedelta
import pymysql

app = Flask(__name__)

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='cortevaweather')

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "corteva-weather-api"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

# checkWeatherData = [
#   {
#     "date": "01-01-1985",
#     "maxtemp": -22,
#     "mintemp": -128,
#     "precipitation": 94,
#     "stationId": "USC00110072"
#   },
#   {
#     "date": "01-02-1985",
#     "maxtemp": -122,
#     "mintemp": -217,
#     "precipitation": 0,
#     "stationId": "USC00110072"
#   },
#   {
#     "date": "01-03-1985",
#     "maxtemp": -106,
#     "mintemp": -244,
#     "precipitation": 0,
#     "stationId": "USC00110072"
#   },
#   {
#     "date": "01-04-1985",
#     "maxtemp": -56,
#     "mintemp": -189,
#     "precipitation": 0,
#     "stationId": "USC00110072"
#   },
#   {
#     "date": "01-05-1985",
#     "maxtemp": 11,
#     "mintemp": -78,
#     "precipitation": 0,
#     "stationId": "USC00110072"
#   }
# ]


@app.route('/')
def index():
    return "<h2>This is just a basic Flask Application</h2>"


@app.route('/api/weather',defaults={'page':0}, methods=['GET'])
@app.route('/api/weather/<int:page>', methods=['GET'])
def getAllWeatherPaginated(page):
    cursor = connection.cursor()
    # Execute query
    offset = 5
    startat = page*offset
    sql = "SELECT * FROM weatherData limit %s , %s"
    cursor.execute(sql, (startat,offset))
    # Fetch all the records
    results = cursor.fetchall()
    payload = []
    content = {}
    for result in results:
        print(result[1])
        content = {'stationId': result[0], 'date': result[1].strftime("%m-%d-%Y"),
                   'maxtemp': result[2], 'mintemp': result[3], 'precipitation': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)


@app.route('/api/weather/<int:page>/<int:offset>', methods=['GET'])
def getAllWeatherPaginatedOffset(page,offset):
    cursor = connection.cursor()
    # Execute query
    sql = "SELECT * FROM weatherData limit %s , %s"
    cursor.execute(sql, (page,offset))
    # Fetch all the records
    results = cursor.fetchall()
    payload = []
    content = {}
    for result in results:
        print(result[1])
        content = {'stationId': result[0], 'date': result[1].strftime("%m-%d-%Y"),
                   'maxtemp': result[2], 'mintemp': result[3], 'precipitation': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/weather/station/<string:stationId>',defaults={'page':0}, methods=['GET'])
@app.route('/api/weather/station/<string:stationId>/<int:page>', methods=['GET'])
def getWeatherByStationId(stationId,page):
    # if stationId not in weatherData:
    #     abort(404)
    offset = 5
    startat = page*offset
    cursor = connection.cursor()
    # Execute query
    sql = "SELECT * FROM weatherData where origin = %s limit %s,%s"
    cursor.execute(sql,(stationId,startat,offset))
    # Fetch all the records
    results = cursor.fetchall()
    payload = []
    content = {}
    for result in results:
        print(result[1])
        content = {'stationId': result[0], 'date': result[1].strftime("%m-%d-%Y"),
                   'maxtemp': result[2], 'mintemp': result[3], 'precipitation': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)


@app.route('/api/weather/station/<string:stationId>/<int:page>/<int:offset>', methods=['GET'])
def getWeatherByStationIdPaginatedWithOffset(stationId,page,offset):
    # if stationId not in weatherData:
    #     abort(404)
    cursor = connection.cursor()
    # Execute query
    sql = "SELECT * FROM weatherData where origin = %s limit %s,%s"
    cursor.execute(sql,(stationId,page,offset))
    # Fetch all the records
    results = cursor.fetchall()
    payload = []
    content = {}
    for result in results:
        print(result[1])
        content = {'stationId': result[0], 'date': result[1].strftime("%m-%d-%Y"),
                   'maxtemp': result[2], 'mintemp': result[3], 'precipitation': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/weather/date/<string:date>',defaults={'page':0}, methods=['GET'])
@app.route('/api/weather/date/<string:date>/<int:page>', methods=['GET'])
def getWeatherByDate(date,page):
    # if stationId not in weatherData:
    #     abort(404)
    offset = 5
    startat = page*offset
    cursor = connection.cursor()
    # Execute query
    sql = "SELECT * FROM weatherData where weatherdate = %s limit %s,%s"
    cursor.execute(sql,(date,startat,offset))
    # Fetch all the records
    results = cursor.fetchall()
    payload = []
    content = {}
    for result in results:
        print(result[1])
        content = {'stationId': result[0], 'date': result[1].strftime("%m-%d-%Y"),
                   'maxtemp': result[2], 'mintemp': result[3], 'precipitation': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)


@app.route('/api/weather/date/<string:date>/<int:page>/<int:offset>', methods=['GET'])
def getWeatherByDatePaginatedWithOffset(date,page,offset):
    # if stationId not in weatherData:
    #     abort(404)
    cursor = connection.cursor()
    # Execute query
    sql = "SELECT * FROM weatherData where weatherdate = %s limit %s,%s"
    cursor.execute(sql,(date,page,offset))
    # Fetch all the records
    results = cursor.fetchall()
    payload = []
    content = {}
    for result in results:
        print(result[1])
        content = {'stationId': result[0], 'date': result[1].strftime("%m-%d-%Y"),
                   'maxtemp': result[2], 'mintemp': result[3], 'precipitation': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/weather/year/<string:year>',defaults={'page':0}, methods=['GET'])
@app.route('/api/weather/year/<string:year>/<int:page>', methods=['GET'])
def getWeatherByYear(year,page):
    # if stationId not in weatherData:
    #     abort(404)
    offset = 5
    startat = page*offset
    cursor = connection.cursor()
    cursor = connection.cursor()
    # Execute query
    sql = "SELECT * FROM weatherData where year(weatherdate) = %s limit %s,%s"
    cursor.execute(sql,(year,page,offset))
    # Fetch all the records
    results = cursor.fetchall()
    payload = []
    content = {}
    for result in results:
        content = {'stationId': result[0], 'date': result[1].strftime("%m-%d-%Y"),
                   'maxtemp': result[2], 'mintemp': result[3], 'precipitation': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)


@app.route('/api/weather/year/<string:year>/<int:page>/<int:offset>', methods=['GET'])
def getWeatherByYearWithPageOffset(year,page,offset):
    # if stationId not in weatherData:
    #     abort(404)
    cursor = connection.cursor()
    cursor = connection.cursor()
    # Execute query
    sql = "SELECT * FROM weatherData where year(weatherdate) = %s limit %s,%s"
    cursor.execute(sql,(year,page,offset))
    # Fetch all the records
    results = cursor.fetchall()
    payload = []
    content = {}
    for result in results:
        content = {'stationId': result[0], 'date': result[1].strftime("%m-%d-%Y"),
                   'maxtemp': result[2], 'mintemp': result[3], 'precipitation': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)

#try compressing the response and show ?

@app.route('/api/weather/stats',defaults={'page':0}, methods=['GET'])
@app.route('/api/weather/stats/<int:page>', methods=['GET'])
def getAllWeatherSummary(page):
    offset = 5
    startat = page*offset
    cursor = connection.cursor()
    # Execute query
    sql = "SELECT * FROM weatherDataSummary limit %s,%s"
    cursor.execute(sql,(startat,offset))
    # Fetch all the records
    results = cursor.fetchall()
    payload = []
    content = {}
    for result in results:
        content = {'stationId': result[0], 'year': result[1],
                   'avgMaxTemp': result[2], 'avgMintemp': result[3], 'totalPrecipitation': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)


@app.route('/api/weather/stats/<int:page>/<int:offset>', methods=['GET'])
def getAllWeatherSummaryWithPageOffset(page,offset):
    cursor = connection.cursor()
    # Execute query
    sql = "SELECT * FROM weatherDataSummary limit %s,%s"
    cursor.execute(sql,(page,offset))
    # Fetch all the records
    results = cursor.fetchall()
    payload = []
    content = {}
    for result in results:
        content = {'stationId': result[0], 'year': result[1],
                   'avgMaxTemp': result[2], 'avgMintemp': result[3], 'totalPrecipitation': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/weather/stats/station/<string:stationId>',defaults={'page':0}, methods=['GET'])
@app.route('/api/weather/stats/station/<string:stationId>/<int:page>', methods=['GET'])
def getWeatherSummaryByStationId(stationId,page):
    # if stationId not in weatherData:
    #     abort(404)
    offset = 5
    startat = page*offset
    cursor = connection.cursor()
    # Execute query
    sql = "SELECT * FROM weatherDataSummary where stationId = %s limit %s,%s"
    cursor.execute(sql,(stationId,startat,offset))
    # Fetch all the records
    results = cursor.fetchall()
    payload = []
    content = {}
    for result in results:
        content = {'stationId': result[0], 'year': result[1],
                   'avgMaxTemp': result[2], 'avgMintemp': result[3], 'totalPrecipitation': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/weather/stats/station/<string:stationId>/<int:page>/<int:offset>', methods=['GET'])
def getWeatherSummaryByStationIdWithPageOffset(stationId,page,offset):
    cursor = connection.cursor()
    # Execute query
    sql = "SELECT * FROM weatherDataSummary where stationId = %s limit %s,%s"
    cursor.execute(sql,(stationId,page,offset))
    # Fetch all the records
    results = cursor.fetchall()
    payload = []
    content = {}
    for result in results:
        content = {'stationId': result[0], 'year': result[1],
                   'avgMaxTemp': result[2], 'avgMintemp': result[3], 'totalPrecipitation': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/weather/stats/year/<string:year>',defaults={'page':0}, methods=['GET'])
@app.route('/api/weather/stats/year/<string:year>/<int:page>', methods=['GET'])
def getWeatherSummaryByYear(year,page):
    offset = 5
    startat = page*offset
    cursor = connection.cursor()
    # Execute query
    sql = "SELECT * FROM weatherDataSummary where year = %s limit %s,%s"
    cursor.execute(sql,(year,startat,offset))
    # Fetch all the records
    results = cursor.fetchall()
    payload = []
    content = {}
    for result in results:
        content = {'stationId': result[0], 'year': result[1],
                   'avgMaxTemp': result[2], 'avgMintemp': result[3], 'totalPrecipitation': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)

@app.route('/api/weather/stats/year/<string:year>/<int:page>/<int:offset>', methods=['GET'])
def getWeatherSummaryByYearWithPageOffset(year,page,offset):
    cursor = connection.cursor()
    # Execute query
    sql = "SELECT * FROM weatherDataSummary where year = %s limit %s,%s"
    cursor.execute(sql,(year,page,offset))
    # Fetch all the records
    results = cursor.fetchall()
    payload = []
    content = {}
    for result in results:
        content = {'stationId': result[0], 'year': result[1],
                   'avgMaxTemp': result[2], 'avgMintemp': result[3], 'totalPrecipitation': result[4]}
        payload.append(content)
        content = {}
    return jsonify(payload)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
