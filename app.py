import json
from server import *
from utils import badRequestError

# Version: 0.1.0

flask = Server()

@flask.app.route('/write/', methods=['POST'])
def write(): return flask.writeDocument(request) if request.method == "POST" else badRequestError()

@flask.app.route('/delete/', methods=['POST'])
def delete(): return flask.deleteDocuments(request) if request.method == "POST" else badRequestError()

@flask.app.route('/get_one/', methods=['POST'])
def getOne(): return flask.getDocument(request) if request.method == "POST" else badRequestError()

@flask.app.route('/get_all_documents/', methods=['POST'])
def getAll(): return flask.getAllDocuments(request) if request.method == "POST" else badRequestError()

#Filtering now only supports 'name'
@flask.app.route('/get_and_filter_documents/', methods=['POST'])
def getAll(): return flask.getAndFilterDocument(request) if request.method == "POST" else badRequestError()



if __name__ == '__main__':
    flask.app.run(host='0.0.0.0', port=5000)
