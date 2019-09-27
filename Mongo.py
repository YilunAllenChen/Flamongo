from flask_pymongo import PyMongo  
from Tools import * 

def initMongo(app):
    # Configure and initialize MongoDB connection with Flask
    '''   CHOOSE MONGODB CONFIG! ONE IS FOR SIT ENV AND THE OTHER IS FOR DEV!!!! '''

    # SIT Environment
    # app.config["MONGO_URI"] = "mongodb://aiegSimulatormockApp:Lo0RSpu5-dF5xsd@192.168.30.132:27037/aiegSimulatormock"
    # DEV Environment
    app.config["MONGO_URI"] = "mongodb://aiegSimulatormockApp:Lo0RSpu5-dF5xsd@192.168.30.215:27037/aiegSimulatormock"


    try:
        coll_testcases = PyMongo(app).db.get_collection("test_cases")
        coll_scenarios = PyMongo(app).db.get_collection("scenarios")
        print("Database connection successful")
    except Exception as e:
        print("Failed to connect to MongoDB database. Error message: " + str(e))

    return coll_testcases, coll_scenarios

def addOrReplaceById(coll,request):
    try:
        # Convert the POST request data into JSON format, stored in result.
        result = json.loads(request.get_data())
        # Insert the newly posted data into the database. If there is already a document that has the same 
        if(coll.find({'id':result['id']}).count()):
            coll.replace_one({'id':result['id']}, result)
        else:
            coll.insert_one(result)
        return jsonify({
            "code": 110400,
            "message": "success",
            "result": result
        })
    except BaseException as e: return jsonError(e)

def selectTestCase(coll,request):
    try:
        result = json.loads(request.get_data())
        global testCaseID
        testCaseID = result["id"]
        print("testCaseID is now " + str(testCaseID))
        return testCaseID, jsonify({
            "code": 110400,
            "message": "success",
            "result": coll.find_one({'id': testCaseID})
        })
    except Exception as e: return -1, jsonError(e)

def getAll(coll,request):
    try:
        # Look through the collection and find all documents in the database, put them into a list.
        result = []
        for item in coll.find():
            result.append(item)
        return jsonify({
            "code": 110400,
            "message": "success",
            "result": result
        })
    except Exception as e: return jsonError(e)


def deleteById(coll,request):
    try:
        # Convert the POST request data into JSON format, stored in result.
        result = json.loads(request.get_data())
        ids = result['id']
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
            query = {'id':result['id']}
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

def runById(coll_testcases, coll_scenarios, request):
    try:
        req = json.loads(request.get_data())
        global testCaseID
        testCaseID = req["id"]
        print("testCaseID is now " + str(testCaseID))
        try:
            testCase = coll_testcases.find_one({'id':testCaseID})
        except:
            return jsonify({
                "code": 110403,
                "message": "This test case does not exist in the database."
            })
        try:
            crspdngScenario = coll_scenarios.find_one({'id':testCase['scenario']})
        except:
            return jsonify({
                "code": 110403,
                "message": "Can't locate the corresponding scenario of this test case. Attempted id: " + str(testCase['scenario'])
            })
        res = {}
        for elmt in crspdngScenario['keys']:
            res[elmt] = testCase[elmt]
        return jsonify({
            "code": 110400,
            "message": "Success",
            "result" : res
        })
    except Exception as e: return jsonError(e)


def getOne(coll, request):
    try:
        result = json.loads(request.get_data())
        return jsonify({
            "code": 110400,
            "message": "success",
            "result": coll.find_one({'id': result['id']})
        })
    except Exception as e: return jsonError(e)




def searchByName(coll, request):
    try:
        li = []
        result = json.loads(request.get_data())
        try:
            name = result['name']
        except:
            return jsonify({
                "code": 110402,
                "message": "Your request does not contain 'name' key."
            })


        for this in coll.find():
            if 'name' in this and this['name'].find(name) != -1:
                li.append(this)

        return jsonify({
            "code": 110400,
            "message": "success",
            "result": li
        })
    except Exception as e: return jsonError(e)


def getViolation(coll, request, testCaseID):
    if request.method == "GET":
        res = coll.find_one({'id':testCaseID})
        try:
            oldVio = res['hisViolationCount']
            newVio = res['newViolationCount']
            return jsonify({
                "code": 110400,
                "message": "success",
                "data": {
                    'oldVioCount':oldVio,
                    'newVioCount':newVio
                }
            })
        except:
            return jsonify({
                "code": 110403,
                "message:":"Active test case has no keys 'hisViolationCount' and/or 'newViolaionCount'. Check your active test case."
            })
    return jsonify({
        "code": 110409,
        "message:":"Failure."
    })