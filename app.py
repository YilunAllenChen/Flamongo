import json
from server import *
from utils import badRequestError




# Version: 0.1.0
flask = Server()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                    Collection Layer
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# MongoDB doesn't allow creation of an empty collection. So when you write a document, its corresponding collectino is automatically generated.

# Drop a collection with all documents inside it.
@flask.app.route('/drop_collection/', methods=['POST'])
def dropCollection(): return flask.dropCollection(request) if request.method == "POST" else badRequestError()


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                    Document Layer
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Write a document, or replace an existing one.
@flask.app.route('/write_document/', methods=['POST'])
def write(): return flask.writeDocument(request) if request.method == "POST" else badRequestError()

# Obtain a document with a specific id in a spcific collection.
@flask.app.route('/get_one_document/', methods=['POST'])
def getOne(): return flask.getDocument(request) if request.method == "POST" else badRequestError()

# Obtain all documents within a collection.
@flask.app.route('/get_all_documents/', methods=['POST'])
def getAll(): return flask.getAllDocuments(request) if request.method == "POST" else badRequestError()

# Obtain all documents within a collection with a filter.
@flask.app.route('/get_and_filter_documents/', methods=['POST'])
def getAndFilter(): return flask.getAndFilterDocument(request) if request.method == "POST" else badRequestError()

# Delete one or multiple documents with a specific id wihtin a collection.
@flask.app.route('/delete_document/', methods=['POST'])
def delete(): return flask.deleteDocuments(request) if request.method == "POST" else badRequestError()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                    Key-Value Layer
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Get a value of a specific key of a document in a spcific collection.
@flask.app.route('/get_value_by_key/', methods=['POST'])
def getValueByKey(): return flask.getValueByKey(request) if request.method == "POST" else badRequestError()

# Get raw data of a specific key of a document in a spcific collection.
@flask.app.route('/get_raw_value_by_key/', methods=['POST'])
def getRawValueByKey(): return flask.getRawValueByKey(request) if request.method == "POST" else badRequestError()








'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                    Legacy Functions
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

@flask.app.route('/simulator/add_scenario/', methods=['POST'])
def addScenario(): return flask.writeDocument(newRequest(request,{'collection':'scenarios'})) if request.method == "POST" else badRequestError()

@flask.app.route('/simulator/get_all_scenario', methods=['POST'])
def getAllScenario(): return flask.getAllDocuments(newRequest(request,{'collection':'scenarios'})) if request.method == "POST" else badRequestError()

@flask.app.route('/simulator/delete_scenario', methods=['POST'])
def deleteScenario(): return flask.deleteDocuments(newRequest(request,{'collection':'scenarios'})) if request.method == "POST" else badRequestError()

@flask.app.route('/simulator/get_scenario', methods=['POST'])
def getScenario(): return flask.getDocument(newRequest(request,{'collection':'scenarios'})) if request.method == "POST" else badRequestError()

@flask.app.route('/simulator/search_scenario', methods=['POST'])
def searchScenario(): return flask.getAndFilterDocument(newRequest(request,{'collection':'scenarios'})) if request.method == "POST" else badRequestError()

@flask.app.route('/simulator/get_all_scenario', methods=['POST'])
def getAllScenarios(): return flask.getAllDocuments(newRequest(request,{'collection':'scenarios'})) if request.method == "POST" else badRequestError()

@flask.app.route('/v1/aiengine/simulatormockserver/editor', methods=['POST'])
def addTestCase(): return flask.writeDocument(newRequest(request,{'collection':'test_cases'})) if request.method == "POST" else badRequestError()

@flask.app.route('/v1/aiengine/simulatormockserver/delete', methods=['POST'])
def deleteTestCase(): return flask.deleteDocuments(newRequest(request,{'collection':'test_cases'})) if request.method == "POST" else badRequestError()

@flask.app.route('/v1/aiengine/simulatormockserver/getall', methods=['POST'])
def getAllTestCases(): return flask.getAllDocuments(newRequest(request,{'collection':'test_cases'})) if request.method == "POST" else badRequestError()

@flask.app.route('/simulator/get_test_case', methods=['POST', 'GET'])
def getTestCase(): return flask.getDocument(newRequest(request,{'collection':'test_cases'}))

@flask.app.route('/simulator/search_test_case', methods=['POST'])
def searchTestCase(): return flask.getAndFilterDocument(newRequest(request,{'collection':'test_cases'})) if request.method == "POST" else badRequestError()

@flask.app.route('/v1/aiengine/simulatormockserver/select_test_case', methods=['POST'])
def selectTestCase(): return flask.selectTestCase(newRequest(request,{'collection':'test_cases'})) if request.method == "POST" else badRequestError()

@flask.app.route('/violation-web/1.0/violation/query', methods=['POST', 'GET'])
def getTrafficRes(): return flask.getRawValueByKey(newRequest(request,{'collection':'test_cases','id':flask.activeTestCase,'key':'mockTrafficRes'})) 

@flask.app.route('/getTimeSlot', methods=['POST', 'GET'])
def getTimeSlot(): return flask.getRawValueByKey(newRequest(request,{'collection':'test_cases','id':flask.activeTestCase,'key':'mockTimeSlot'})) 

@flask.app.route('/v1/cms/festival/attribute', methods=['POST', 'GET'])
def getHoliday(): return flask.getRawValueByKey(newRequest(request,{'collection':'test_cases','id':flask.activeTestCase,'key':'mockHoliday'}))

@flask.app.route('/getData/<dataType>', methods=['POST', 'GET'])
def get_mock_data(dataType): return flask.getValueByKey(newRequest(request,{'key':dataType,'collection':'test_cases','id':flask.activeTestCase}))



if __name__ == '__main__':
    flask.app.run(host='0.0.0.0', port=5000,debug=True)
