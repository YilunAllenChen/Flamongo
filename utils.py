# dict_to_xml: Helper function that converts a dict object into a xml format string.
# parameter: data -> the dictionary object to be passed in.

from flask import jsonify

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
        "code": 110402,
        "message": str(e)
    })


def badRequestError(e):
    return jsonify({
        "code": 110402,
        "message": str(e)
    })