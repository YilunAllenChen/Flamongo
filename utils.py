
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
                                    Convenient Tools
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def newRequest(request, query):
    if request.json == None:
        object.__setattr__(request,'json', {})
    for key in query:
        request.json[key] = query[key]
    return request