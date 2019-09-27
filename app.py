import json
from Tools import *
from Mongo import *

# Version: 0.3.1

# Scenario ID as a global. This determines which scenario in the database the server will get its data from
global testCaseID
testCaseID = -1

# Initialize Flask
app = initFlask()

#Initialize mongoDB with Flask
coll_testcases, coll_scenarios = initMongo(app)


# Upload scenario data.N
@app.route('/simulator/add_scenario/', methods=['POST'])
def upload_scenario():
    if request.method == "POST":
        return addOrReplaceById(coll_scenarios,request)

# Remove scenario data.
@app.route('/simulator/delete_scenario', methods=['POST'])
def delete_scenario():
    if request.method == "POST":
        return deleteById(coll_scenarios,request)

# Get a scenario.
@app.route('/simulator/get_scenario', methods=['POST'])
def get_scenario():
    if request.method == "POST":
        return getOne(coll_scenarios,request)

# Search for scenarios:
@app.route('/simulator/search_scenario', methods=['POST'])
def search_scenario():
    if request.method == "POST":
        return searchByName(coll_scenarios, request)









# Get all test case data.
@app.route('/simulator/get_all_scenario', methods=['GET'])
def get_all_scenario():
    if request.method == "GET":
        return getAll(coll_scenarios,request)

# Upload test case data.
@app.route('/v1/aiengine/simulatormockserver/editor', methods=['POST'])
def upload_test_case():
    if request.method == "POST":
        return addOrReplaceById(coll_testcases,request)

# Remove test case data.
@app.route('/v1/aiengine/simulatormockserver/delete', methods=['POST'])
def delete_test_case():
    if request.method == "POST":
        return deleteById(coll_testcases,request)

# Get all test case data.
@app.route('/v1/aiengine/simulatormockserver/getall', methods=['GET'])
def get_all_test_case():
    if request.method == "GET":
        return getAll(coll_testcases,request)

# Get a test case.
@app.route('/simulator/get_test_case', methods=['POST'])
def get_test_case():
    if request.method == "POST":
        return getOne(coll_testcases,request)

# Search test case.
@app.route('/simulator/search_test_case', methods=['POST'])
def search_test_case():     
    if request.method == "POST":
        return searchByName(coll_testcases,request)

# Choose which test case to run, using POST request.
@app.route('/v1/aiengine/simulatormockserver/select_test_case', methods=['POST'])
def select_test_case():
    if request.method == "POST":
        global testCaseID
        testCaseID, result = selectTestCase(coll_testcases,request)
        return result

# Acquire weather data.
@app.route('/dev-onlineservice-weather/weather/qWeatherByLatLng', methods=['GET','POST'])
def get_weather():
    # Body has two params: long and lati.
    return getData(coll_testcases, request, "mockWeather", testCaseID)


# Acquire traffic data.
@app.route('/violation-web/1.0/violation/query', methods=['GET', 'POST'])
def get_traffic_res():
    return getData(coll_testcases, request, "mockTrafficRes", testCaseID)


# Acquire time slot data. #TODO: URL not specified by documentation.
@app.route('/getTimeSlot', methods=['GET', 'POST'])
def get_time_slot():
    return getData(coll_testcases, request, "mockTimeSlot", testCaseID)

# Acquire holiday data.
@app.route('/v1/cms/festival/attribute', methods=['GET', 'POST'])
def get_holiday():
    # Body has two params: startTime and endTime
    return getData(coll_testcases, request, "mockHoliday", testCaseID)

# Run a test case with the current id
@app.route('/simulator/run', methods=['POST'])
def run_test_case():
    if request.method == "POST":
        return runById(coll_testcases, coll_scenarios, request)

# Get all violation data - both history and new.
@app.route('/simulator/get_violation', methods=['GET'])
def get_violation():
    return getViolation(coll_testcases,request, testCaseID)







'''
INTEGRATED APIS
'''


# Integrated getData link.
@app.route('/getData/<dataType>', methods=['GET', 'POST'])
def get_mock_data(dataType):
    return getJsonData(coll_testcases, request, dataType, testCaseID)





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
