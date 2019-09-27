import json
from flask import request, Flask, Response
from flask_pymongo import PyMongo  
from bson.json_util import dumps
from utils import *


class Server:

    def __init__(self):
        try:
            self.app = Flask(__name__)
            self.collections = {}
            print("Flask initialized successfully.")
        except:
            print("Failed to initialize Flask. ")

        try:
            app.config["MONGO_URI"] = "mongodb://aiegSimulatormockApp:Lo0RSpu5-dF5xsd@192.168.30.215:27037/aiegSimulatormock"
            self.db = PyMongo(app).db
            self.collections = {}
            print("Database successfully configured")
        except Exception as e:
            print("Failed to configure MongoDB. Error message: " + str(e))



    '''
        INFRASTRUCTURE LAYER
    '''

    # A customized 'jsonify' function that interfaces with the app to avoid the error of regular jsonify being unable to parse ObjectID type in MongoDB documents.
    # The function basically inherits the original jsonify function but uses 'dumps' instead.
    # DON'T CHANGE.
    def jsonify(*args, **kwargs):
        indent = None
        separators = (',', ':')
        if app.config['JSONIFY_PRETTYPRINT_REGULAR'] or app.debug:
            indent = 2
            separators = (', ', ': ')
        if args and kwargs:
            raise TypeError(
                'jsonify() behavior undefined when passed both args and kwargs')
        elif len(args) == 1:  # single args are passed directly to dumps()
            data = args[0]
        else:
            data = args or kwargs
        return app.response_class(
            dumps(data, indent=indent, separators=separators) + '\n',
            mimetype=app.config['JSONIFY_MIMETYPE']
        )


    def getCollection(self, coll: str):
        try:
            return self.db.get_collection(coll)
        else:
            print("ERROR: Can't locate target collection.")


    '''
        OPERATION LAYER
    '''
        
    def writeDocument(self,request):
        try:
            # Convert the POST request data into JSON format, stored in req.
            req = json.loads(request.get_data())
            coll = self.getCollection(req['collection'])
            # Insert the newly posted data into the database. If there is already a document that has the same 
            if(coll.find({'id':req['id']}).count()):
                coll.replace_one({'id':req['id']}, req)
            else:
                coll.insert_one(req)
            return jsonify({
                "code": 110400,
                "message": "success",
                "result": req
            })
        except BaseException as e: return jsonError(e)


    def getDocument(self, request):
        try:
            req = json.loads(request.get_data())
            coll = self.getCollection(req['collection'])
            return jsonify({
                "code": 110400,
                "message": "success",
                "result": coll.find_one({'id': req['id']})
            })
        except Exception as e: return jsonError(e)


    def getAndFilterDocument(self, request):
        try:
            req = json.loads(request.get_data())
            coll = self.getCollection(req['collection'])
            return jsonify({
                "code": 110400,
                "message": "success",
                "result": coll.find_one({'id': req['id']})
            })
        except Exception as e: return jsonError(e)


    def deleteDocuments(self,request):
        try:
            req = json.loads(request.get_data())
            coll = self.getCollection(req['collection'])
            ids = req['id']
            if type(ids) is list:
                listDeleted = []
                listNotFound = []
                for thisId in ids:
                    query = {'id':thisId}
                    if(coll.find({'id':thisId}).count()):
                        coll.remove({'id':thisId})
                        listDeleted.append(thisId)
                    else:
                        listNotFound.append(thisId)
                return jsonify({    
                    "code": 110400,
                    "message": "These entries have been deleted: " + str(listDeleted) + "; These entries are not found therefore cannot be deleted: " + str(listNotFound)
                })
            else:
                query = {'id':req['id']}
                #If id param is not a list.
                if(coll.find(query).count()):
                    coll.remove(query)
                    return jsonify({
                        "code": 110400,
                        "message": "target entry deleted successfully."
                    })
                else:
                    return jsonify({
                        "code": 110403,
                        "message": "No entry found with the specified ID."
                    }) 
        except BaseException as e: return jsonError(e)


    '''
    POST
    {
        'id': '12091',
        'collection':'2014910',
        'key':'rmlkam'
    }
    '''

    def getJsonData(self, request):
        req = json.loads(request.get_data())
        coll = self.getCollection(req['collection'])
        dataType = req['key']
        if coll.find({'id': id}).count():
            try:
                result = jsonify({
                    "code": 110400,
                    "message": "Success",
                    "result": {dataType : coll.find_one({'id':id})[dataType]}
                    })
            except:
                result = jsonify({
                    "code": 110403,
                    "message": "Target document doesn't contain key: " + dataType
                })
        # If no test case data is found that matches the id, return an error message.
        else:
            return jsonify({
                        "code": 110403,
                        "message":"No document found in the database. Check your database and your requested id.",
                        "result": None
                        })
