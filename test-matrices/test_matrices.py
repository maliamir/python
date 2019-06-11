#!flask/bin/python

from flask import Flask, abort, jsonify, make_response, request
from cassandra.cluster import Cluster
import json

cassandraCluster = Cluster(['127.0.0.1'])
cassandraSession = cassandraCluster.connect("performo")

flaskApp = Flask(__name__)

@flaskApp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@flaskApp.route('/matrices', methods=['GET'])
def load_test_matrices():
    json = ''
    rows = cassandraSession.execute("select * from test_matrix");
    for row in rows:
        json += '{"log_stamp": "' + str(row[0]) + '",\n"matrix": ' + row[1] + '},\n'
    return '[' + json[0:json.__len__() - 2] + ']'

@flaskApp.route('/matrices', methods=['POST'])
def add_test_matrix():
    if not request.json:
        abort(400)
    data = request.json
    matrices = data['matrices']
    jsonArray = []
    for matrix in matrices:
        jsonObject = {
            'testUnitName': matrix['testUnitName'],
            'duration': matrix['duration']
        }
        jsonArray.append(jsonObject)

    jsonArrayAsResponse = jsonify({'matrices': jsonArray})
    jsonArrayAsStr = json.dumps(jsonArray)

    cassandraSession.execute("insert into test_matrix (log_stamp, matrix) VALUES ( toTimestamp( now() ), '" + jsonArrayAsStr + "')");

    print(jsonArrayAsStr)

    return jsonArrayAsResponse, 201


if __name__ == '__main__':
    flaskApp.run(host = '10.0.0.110',debug=True)