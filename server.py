import json
from flask import request, Flask, Response
from flask_pymongo import PyMongo  
from bson.json_util import dumps
from utils import *
from time import sleep


class Server:

    def __init__(self):  
        try:
            self.app = Flask(__name__)
            print('Flask initialized successfully.')
        except:
            print('Failed to initialize Flask.')
        
        #self.app.config["MONGO_URI"] = "mongodb://aiegSimulatormockApp:Lo0RSpu5-dF5xsd@192.168.30.215:27037/aiegSimulatormock"
        self.app.config["MONGO_URI"] = self.__initMongoConfig()
        self.db = PyMongo(self.app).db
        self.__testMongoConnection('_selfTest')
        try:
            self.activeTestCase = '-1'
        except Exception as e:
            print("Faild to load AI Engine Config")


    def __testMongoConnection(self, coll):
        try:
            testColl = self.db.get_collection(coll)
            testColl.insert_one({"test":"Success"})
            sleep(1)
            testColl.remove({"test":"Success"})
            testColl.drop()
            print('Database successfully configured and connected.')
        except Exception as e:
            print('Failed to configure MongoDB. Error message: ' + str(e))

    # Initialization of MongoDB Service. 
    def __initMongoConfig(self):
        try:
            from config import mongoConfig
        except:
            base = 'mongoConfig = \'mongodb://'
            ip = input("mongoDB configuration doesn't exist. Starting MongoDB configuration process.\nPlease specify the IP of your mongoDB: ")
            port = input("Please specify the port that mongoDB uses: ")
            user = input("Please specify your user name: ")
            pswd = input("Please enter the password corresponding to this DB: ")
            if len(user) > 0 and len(pswd) > 0:
                base += user + ":" + pswd + "@" 
            db = input("Please specify which database you are authorized to access: ")
            if len(db) == 0:
                print("No name entered; Will use default name 'mydb'")
                db = 'mydb'
            f = open('config.py',mode='a')
            f.write(base + ip + ":" + port + '/' + db + '\'')
            f.close()
            from config import mongoConfig
        return mongoConfig
        

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                                INFRASTRUCTURE
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    # A customized 'jsonify' function that interfaces with the app to avoid the error of regular jsonify being unable to parse ObjectID type in MongoDB documents.
    # The function basically inherits the original jsonify function but uses 'dumps' instead.
    # DON'T CHANGE.
    def jsonify(self, *args, **kwargs):
        indent = None
        separators = (',', ':')
        if self.app.config['JSONIFY_PRETTYPRINT_REGULAR'] or self.app.debug:
            indent = 2
            separators = (', ', ': ')
        if args and kwargs:
            raise TypeError(
                'jsonify() behavior undefined when passed both args and kwargs')
        elif len(args) == 1:  # single args are passed directly to dumps()
            data = args[0]
        else:
            data = args or kwargs
        return self.app.response_class(
            dumps(data, indent=indent, separators=separators) + '\n',
            mimetype=self.app.config['JSONIFY_MIMETYPE']
        )


    def preProcess(self,request):
        try:
            req = request.json
            try:
                coll = self.db.get_collection(req['collection'])
            except Exception as e: print("ERROR: Can't locate target collection. " + str(e))
            return req, coll

        except Exception as e:
            print("Pre-Processing failed: " + str(e))
            return None, None

    def success(self,result):
        return self.jsonify({
                "code": 110400,
                "message": "success",
                "result": result
            })

    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                                    OPERATIONS
    '''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
    '''
    POST
    {
        'id': '12091',
        'collection':'2014910'
        <other data>
    }
    '''
    def writeDocument(self,request):
        try:
            req, coll = self.preProcess(request)
            # Convert the POST request data into JSON format, stored in req.
            # Insert the newly posted data into the database. If there is already a document that has the same 
            if(coll.find({'id':req['id']}).count()):
                coll.replace_one({'id':req['id']}, req)
            else:
                coll.insert_one(req)
            return self.success(coll.find_one({'id':req['id']}))
        except Exception as e: return jsonError(e)

    '''
    POST
    {
        'id': '12091',
        'collection':'2014910'
    }
    '''
    def getDocument(self, request):
        try:
            req, coll = self.preProcess(request)
            return self.success(coll.find_one({'id': req['id']}))
        except Exception as e: return jsonError(e)

    '''
    POST
    {
        'collection':'2014910'
    }
    '''
    def getAllDocuments(self,request):
        try:
            req, coll = self.preProcess(request)
            # Look through the collection and find all documents in the database, put them into a list.
            result = []
            for item in coll.find():
                result.append(item)
            return self.success(result)
        except Exception as e: return jsonError(e)
    
    '''
    POST
    {
        'id': '12091',
        'name':'a'
    }
    '''
    def getAndFilterDocument(self, request):
        try:
            req, coll = self.preProcess(request)
            li = []
            try:
                name = req['name']
            except:
                return ParamNotFoundError("name")
            for this in coll.find():
                if 'name' in this and this['name'].find(name) != -1:
                    li.append(this)
            return self.success(li)
        except Exception as e: return jsonError(e)

    '''
    POST
    {
        'id': '12091',
        'collection':'2014910'
    }
    '''
    def deleteDocuments(self,request):
        try:
            req, coll = self.preProcess(request)
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
                return self.success("These entries have been deleted: " + str(listDeleted) + "; These entries are not found therefore cannot be deleted: " + str(listNotFound))

            else:
                query = {'id':req['id']}
                #If id param is not a list.
                if(coll.find(query).count()):
                    coll.remove(query)
                    return self.success("target entry deleted successfully.")
                else:
                    return noDataFoundError()
        except BaseException as e: return jsonError(e)

    '''
    POST
    {
        'id': '12091',
    }
    '''
    def selectTestCase(self,request):
        try:
            req, coll = self.preProcess(request)
            self.activeTestCase = req["id"]
            print("activeTestCase is now " + str(self.activeTestCase))
            return self.success(coll.find_one({'id': self.activeTestCase}))
        except Exception as e: return jsonError(e)

    '''
    POST
    {
        'collection': 'testcases',
    }
    '''
    def dropCollection(self,request):
        try:
            req, coll = self.preProcess(request)
            try:
                coll.drop()
                return self.success("Collection dropped successfully")
            except:
                return noDataFoundError()
        except Exception as e: return jsonError






    '''
    POST
    {
        'id': '12091',
        'collection':'2014910',
        'key':'rmlkam'
    }
    '''
    def getValueByKey(self, request):
        req, coll = self.preProcess(request)
        dataType = req['key']
        id = req['id']
        if coll.find({'id': id}).count():
            try:
                return self.success({dataType : coll.find_one({'id':id})[dataType]})
            except:
                return noDataFoundError()
        # If no test case data is found that matches the id, return an error message.
        else:
            return noDataFoundError()

    '''
    POST
    {
        'id': '12091',
        'collection':'2014910',
        'key':'rmlkam'
    }
    '''
    def getRawValueByKey(self, request):
        req, coll = self.preProcess(request)
        dataType = req['key']
        id = req['id']
        if coll.find({'id': id}).count():
            try:
                return self.success({dataType : coll.find_one({'id':id})[dataType]})
            except:
                return ParamNotFoundError('dataType')
        # If no test case data is found that matches the id, return an error message.
        else:
            return noDataFoundError()