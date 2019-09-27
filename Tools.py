import json
from flask import request, Flask, Response
from bson.json_util import dumps


app = Flask(__name__)

def initFlask():
    return app

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

# getData : Helper function to get data from the database of specified type.
# Parameters:   coll -> database collection object.
#               request -> HTTP request object.
#               dataType -> String, type of data requested.
#               id -> int, id number of the test case.
def getData(coll, request, dataType, id):
    # Parse the request content into a dictionary object, stored in req. Support both POST and GET.
    if request.method == "GET":
        req = request.args.to_dict()
    elif request.method == "POST":
        if request.get_data():
            req = json.loads(request.get_data())
            if 'id' in req:
                id = req['id']
        else:
            req = {}
    # If id not specified (in other words, left at default 0), return a message to remind user to set it.
    if(id == -1):
        return "ERROR: You haven't specified the test case yet as the ID is detected to be -1 (default value)."
    # Obtain the data from the test case data specified by the required ID.
    # If test case is found in the database, return it.
    if coll.find({'id': id}).count():
        result = Response(coll.find_one({'id': id})[dataType])
        result.headers['Content-Type'] = "application/json"
        # Return the data using the requested format. JSON if not specified.
        if "dataType" not in req or req["dataType"] == "JSON":
            return result
        elif req["dataType"] == "XML":
            try:
                return dict_to_xml(result)
            except:
                return "Data requested seems not to be a python-dict object and therefore is not parsable at this moment."
        # If requested data type is specified but neither JSON nor XML, return an error message.
        else:
            return "Only JSON and XML format supported at this moment."
    # If no test case data is found that matches the id, return an error message.
    else:
        return "No test case data exists in the database. Upload and select test case first."


def getJsonData(coll, request, dataType, id):
    # Parse the request content into a dictionary object, stored in req. Support both POST and GET.
    if request.method == "GET":
        req = request.args.to_dict()
    elif request.method == "POST":
        if request.get_data():
            req = json.loads(request.get_data())
            if 'id' in req:
                id = req['id']
        else:
            req = {}
    # If id not specified (in other words, left at default 0), return a message to remind user to set it.
    if(id == -1):
        return jsonify({
            "code": 110401,
            "message": "WARNING: You haven't specified the test case yet as the ID is detected to be -1 (default value)."
            })
    # Obtain the data from the test case data specified by the required ID.
    # If test case is found in the database, return it.
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
                "message": "Target test case doesn't contain key: " + dataType
            })

    # If no test case data is found that matches the id, return an error message.
    else:
        return jsonify({
                    "code": 110403,
                    "message":"No test case data exists in the database. Upload and select test case first.",
                    "result": None
                    })




# dict_to_xml: Helper function that converts a dict object into a xml format string.
# parameter: data -> the dictionary object to be passed in.
def dict_to_xml(data):
    xml = []
    for k in sorted(data.keys()):
        v = data.get(k)
        if k == 'detail' and not v.startswith('<![CDATA['):
            v = '<![CDATA[{}]]>'.format(v)
        xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(xml))


def jsonError(e):
    print(e)
    return jsonify({
        "code": 400,
        "message": str(e)
    })