import pandas as pd
from flask import jsonify
from sqlalchemy.orm import sessionmaker

from FuzzyFunctions.BatchFuzzyResult import findFuzzyTableBase
from PreSearchFunctions.VodafoneCustomerModel.VFCFunctions import VFfnameResult
from Model.DatabaseTables import engine, VFCustomer, MapTables,engine, DynamicTable, tableDictRefinitiv, tableDictVodafone
from Model.Model_DML_DDL import dropTempTable
from WhiteListFunctions.WtiheListControl import whiteListTraccingVF
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import or_, inspect

# vf search
def VFCustomerSearch(tableName, tableList, threshold, tempTable, whiteList):
    Base = declarative_base()
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    dfList = []
    inspector = inspect(engine)
    dynamicDictVF = tableDictVodafone(tableName)
    dynamicTableClassVF = type(tableName, (Base,), dynamicDictVF)

    Base.metadata.create_all(engine)
    # White List Control

    excludeWhiteListFirstName, excludeWhiteListLastName,excludeWhiteListName = whiteListTraccingVF(whiteList)

    # Search every sanction table
    for table in tableList:
        firstName, lastName,fullName = VFfnameResult(dynamicTableClassVF)
        fuzzymatch = findFuzzyTableBase(table, firstName, lastName,fullName, threshold)
        if len(fuzzymatch) > 0 :
            fuzzymatch = fuzzymatch[~fuzzymatch['NAME'].isin(excludeWhiteListName)]

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