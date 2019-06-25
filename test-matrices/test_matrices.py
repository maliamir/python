#!flask/bin/python

from flask import Flask, abort, jsonify, make_response, request
from flask_cors import CORS, cross_origin
from cassandra.cluster import Cluster

import json
import re

alphaNumPattern = '^[A-Za-z0-9_-]*$'

cassandraCluster = Cluster(['127.0.0.1'])
cassandraSession = cassandraCluster.connect("performo")

flaskApp = Flask(__name__)
cors = CORS(flaskApp)
@flaskApp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@flaskApp.route('/matrices', methods=['GET'])
@cross_origin()
def load_test_matrices():
    json = ''
    rows = cassandraSession.execute("select * from test_matrices");
    for row in rows:
        json += '{"log_stamp": "' + str(row[0]) + '",\n"matrix": ' + row[1] + '},\n'
    return '[' + json[0:json.__len__() - 2] + ']'

@flaskApp.route('/matrices', methods=['POST'])
def add_test_matrix():

    if not request.json:
        abort(400)

    data = request.json
    matrices = data['matrices']
    dbJsonArray = []
    resJsonArray = []

    for matrix in matrices:

        duration = str(matrix['duration'])
        if duration.isnumeric():
            duration = matrix['duration']
        else:
            duration = -1

        if str(matrix['testUnitName']).isalnum() and re.match(alphaNumPattern, matrix['testUnitName']):
            testUnitName = matrix['testUnitName']
            jsonObject = {
                'testUnitName': testUnitName,
                'duration': duration
            }
            dbJsonArray.append(jsonObject)
        else:
            jsonObject = {
                'error': "Test Unit named '" + matrix['testUnitName'] + "' with duration '" + str(duration) +
                         "' is not alpha-numeric; hence, not persisted."
            }

        resJsonArray.append(jsonObject)

    if len(dbJsonArray) > 0:
        jsonArrayInDb = json.dumps(dbJsonArray)
        cassandraSession.execute("insert into test_matrices (log_stamp, matrix) VALUES ( toTimestamp( now() ), '" + jsonArrayInDb + "')");

    jsonArrayAsResponse = jsonify({'matrices': resJsonArray})
    print(jsonArrayAsResponse)

    return jsonArrayAsResponse, 201


if __name__ == '__main__':
    flaskApp.run(host='0.0.0.0')