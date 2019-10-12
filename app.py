import json
from flask_server import Server
from flask import request
from error_handling import badRequestError
from utils import *


# Version: 0.1.0
server = Server()




'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                DB:    Collection Layer
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# MongoDB doesn't allow creation of an empty collection. So when you write a document, its corresponding collectino is automatically generated.

# Drop a collection with all documents inside it.
@server.app.route('/database/drop_collection/', methods=['POST', 'GET'])
def dropCollection(): return server.mongo.dropCollection(request) if request.method == "POST" else badRequestError()

# List all visible collections 
@server.app.route('/database/list_collections/', methods=['POST', 'GET'])
def listCollection(): return server.mongo.listCollections(request) if request.method == "POST" else badRequestError()

@server.app.route('/database/get_statistics/', methods=['POST', 'GET'])
def getStatistics(): return server.mongo.getStatistics(request) if request.method == "POST" else badRequestError()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                DB:    Document Layer
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Write a document, or replace an existing one.
@server.app.route('/database/write_document/', methods=['POST', 'GET'])
def write(): return server.mongo.writeDocument(request) if request.method == "POST" else badRequestError()

# Obtain a document with a specific id in a spcific collection.
@server.app.route('/database/get_one_document/', methods=['POST', 'GET'])
def getOne(): return server.mongo.getDocument(request) if request.method == "POST" else badRequestError()

# Obtain all documents within a collection.
@server.app.route('/database/get_all_documents/', methods=['POST', 'GET'])
def getAll(): return server.mongo.getAllDocuments(request) if request.method == "POST" else badRequestError()

# Obtain all documents within a collection with a filter.
@server.app.route('/database/get_and_filter_documents/', methods=['POST', 'GET'])
def getAndFilter(): return server.mongo.getAndFilterDocument(request) if request.method == "POST" else badRequestError()

# Delete one or multiple documents with a specific id wihtin a collection.
@server.app.route('/database/delete_document/', methods=['POST', 'GET'])
def delete(): return server.mongo.deleteDocuments(request) if request.method == "POST" else badRequestError()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                  DB:  Key-Value Layer
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# Get a value of a specific key of a document in a spcific collection.
@server.app.route('/database/get_value_by_key/', methods=['POST', 'GET'])
def getValueByKey(): return server.mongo.getValueByKey(request) if request.method == "POST" else badRequestError()

# Get raw data of a specific key of a document in a spcific collection.
@server.app.route('/database/get_raw_value_by_key/', methods=['POST', 'GET'])
def getRawValueByKey(): return server.mongo.getRawValueByKey(request) if request.method == "POST" else badRequestError()




'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                        Kafka
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

@server.app.route('/kafka/send_message/',methods=['POST', 'GET'])
def sendKafkaMessage(): return server.kafka.sendMessage(request) if request.method == "POST" else badRequestError()

@server.app.route('/kafka/receive_message/',methods=['POST', 'GET'])
def sendKafkaMessage(): return server.kafka.receiveMessages(request) if request.method == "POST" else badRequestError()









'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                    Legacy Functions
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

@server.app.route('/simulator/add_scenario/', methods=['POST'])
def addScenario(): return server.mongo.writeDocument(newRequest(request,{'collection':'scenarios'})) if request.method == "POST" else badRequestError()

@server.app.route('/simulator/get_all_scenario', methods=['POST'])
def getAllScenario(): return server.mongo.getAllDocuments(newRequest(request,{'collection':'scenarios'})) if request.method == "POST" else badRequestError()

@server.app.route('/simulator/delete_scenario', methods=['POST'])
def deleteScenario(): return server.mongo.deleteDocuments(newRequest(request,{'collection':'scenarios'})) if request.method == "POST" else badRequestError()

@server.app.route('/simulator/get_scenario', methods=['POST'])
def getScenario(): return server.mongo.getDocument(newRequest(request,{'collection':'scenarios'})) if request.method == "POST" else badRequestError()

@server.app.route('/simulator/search_scenario', methods=['POST'])
def searchScenario(): return server.mongo.getAndFilterDocument(newRequest(request,{'collection':'scenarios'})) if request.method == "POST" else badRequestError()

@server.app.route('/simulator/get_all_scenario', methods=['POST','GET'])
def getAllScenarios(): return server.mongo.getAllDocuments(newRequest(request,{'collection':'scenarios'}))

@server.app.route('/v1/aiengine/simulatormockserver/editor', methods=['POST'])
def addTestCase(): return server.mongo.writeDocument(newRequest(request,{'collection':'test_cases'})) if request.method == "POST" else badRequestError()

@server.app.route('/v1/aiengine/simulatormockserver/delete', methods=['POST'])
def deleteTestCase(): return server.mongo.deleteDocuments(newRequest(request,{'collection':'test_cases'})) if request.method == "POST" else badRequestError()

@server.app.route('/v1/aiengine/simulatormockserver/getall', methods=['POST', 'GET'])
def getAllTestCases(): return server.mongo.getAllDocuments(newRequest(request,{'collection':'test_cases'})) 

@server.app.route('/simulator/get_test_case', methods=['POST', 'GET'])
def getTestCase(): return server.mongo.getDocument(newRequest(request,{'collection':'test_cases'}))

@server.app.route('/simulator/search_test_case', methods=['POST'])
def searchTestCase(): return server.mongo.getAndFilterDocument(newRequest(request,{'collection':'test_cases'})) if request.method == "POST" else badRequestError()

@server.app.route('/v1/aiengine/simulatormockserver/select_test_case', methods=['POST'])
def selectTestCase(): return server.mongo.selectTestCase(newRequest(request,{'collection':'test_cases'})) if request.method == "POST" else badRequestError()

@server.app.route('/violation-web/1.0/violation/query', methods=['POST', 'GET'])
def getTrafficRes(): return server.mongo.getRawValueByKey(newRequest(request,{'collection':'test_cases','id':server.activeTestCase,'key':'mockTrafficRes'})) 

@server.app.route('/getTimeSlot', methods=['POST', 'GET'])
def getTimeSlot(): return server.mongo.getRawValueByKey(newRequest(request,{'collection':'test_cases','id':server.activeTestCase,'key':'mockTimeSlot'})) 

@server.app.route('/v1/cms/festival/attribute', methods=['POST', 'GET'])
def getHoliday(): return server.mongo.getRawValueByKey(newRequest(request,{'collection':'test_cases','id':server.activeTestCase,'key':'mockHoliday'}))

@server.app.route('/getData/<dataType>', methods=['POST', 'GET'])
def get_mock_data(dataType): return server.mongo.getValueByKey(newRequest(request,{'key':dataType,'collection':'test_cases','id':server.activeTestCase}))

if __name__ == '__main__':
    server.app.run(host='0.0.0.0', port=5000,debug=True)
