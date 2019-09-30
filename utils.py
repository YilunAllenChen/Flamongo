from flask import jsonify

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                    Error Handling
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def jsonError(e):
    print(e)
    return jsonify({
        "code": 110402,
        "message": "Error: There is a problem with : " + str(e)
    })

def ParamNotFoundError(e):
    return jsonify({
        "code": 110402,
        "message": "Error: Parameter " + str(e) + " is needed for this request but not found in the request."
    })

def badRequestError():
    return jsonify({
        "code": 110402,
        "message": "Error: METHOD NOT ALLOWED"
    })

def noDataFoundError():
    return jsonify({
        "code": 110403,
        "message": "No data could be found with your requirements."
    })




'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                    Convenient Tools
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



def newRequest(request, query):
    if request.json == None:
        object.__setattr__(request,'json', {})
    for key in query:
        request.json[key] = query[key]
    return request