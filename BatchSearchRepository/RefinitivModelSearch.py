import pandas as pd
from flask import jsonify
from sqlalchemy.orm import sessionmaker

from FuzzyFunctions.BatchFuzzyResult import findFuzzyTableBase
from PreSearchFunctions.Global.GlobalFunctions import fnameResult
from Model.DatabaseTables import engine, DynamicTable, MapTables
from Model.Model_DML_DDL import dropTempTable
from WhiteListFunctions.WtiheListControl import whiteListTraccing


def tableSearch(tableName, tableList, threshold, tempTable, whiteList):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    dfList = []

    # Dynamically rename input table
    #DynamicTable.__table__.name = tableName

    # White List Control
    #excludeWhiteListName, excludeWhiteListLastName, excludeWhiteFullName = whiteListTraccing(whiteList, tableName)

    # Search every sanction table
    for table in tableList:
        firstName, lastName, fullName = fnameResult(tableName)
        fuzzymatch = findFuzzyTableBase(table, firstName, lastName, fullName, threshold)
        # if len(fuzzymatch) > 0 :
        #     fuzzymatch = fuzzymatch[~fuzzymatch['NAME'].isin(excludeWhiteFullName)]

    if isinstance(fuzzymatch, pd.DataFrame):
        dfList.append(fuzzymatch)
    if not dfList:
        result = {"table": "empty"}
        return jsonify(result)

    result = pd.concat(dfList)
    result = result.drop_duplicates()
    dbConnection = engine.connect()

    # Drop table before create
    dropTempTable(tempTable)

    # Dataframe to Mysql table
    result.to_sql(tempTable, dbConnection, if_exists='replace', index=False)

    result = {"table": tempTable}
    return jsonify(result)