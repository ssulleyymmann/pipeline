import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from BatchSearchRepository.VodafoneModelSearch import VFCustomerSearch
from BatchSearchRepository.RefinitivModelSearch import tableSearch
from FuzzyFunctions.SingleFuzzyResult import fullNameSearch

app = Flask(__name__)
CORS(app)

signature = os.environ.get('SIGNATURE', 'LOCAL')


@app.route('/fcheck/table/', methods=["POST"])
def checkDynamicTable():
    if request.headers.get('X-SIGNATURE', 'TEST') != signature:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()

    tableName = data["tableName"]
    tableList = data["tableList"]
    threshold = int(data["threshold"])
    tempTable = data["tempTable"]
    whiteList = data["whiteList"]


    return tableSearch(tableName, tableList, threshold, tempTable, whiteList)


@app.route('/fcheck/vfull/', methods=["POST"])
def checkDeltaRefinitiv():
    if request.headers.get('X-SIGNATURE', 'TEST') != signature:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()

    tableName = data["tableName"]
    tableList = data["tableList"]
    threshold = int(data["threshold"])
    tempTable = data["tempTable"]
    whiteList = data["whiteList"]

    return VFCustomerSearch(tableName, tableList, threshold, tempTable, whiteList)


@app.route('/fcheck/nfull/', methods=["POST"])
def fnameSearch():
    if request.headers.get('X-SIGNATURE', 'TEST') != signature:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()

    fullName = data["fullName"]
    threshold = int(data["threshold"])
    tableList = data["tableList"]
    tempTable = data["tempTable"]
    whiteList = data["whiteList"]
    tckn_vkn = -1
    if 'tckn_vkn' in data :
        tckn_vkn = data["tckn_vkn"]
    return fullNameSearch(fullName, tckn_vkn, threshold, tableList, whiteList, tempTable)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
