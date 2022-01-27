from nis import match
import pandas as pd
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from multipledispatch import dispatch
import numpy as np
from sqlalchemy.ext.declarative import declarative_base
from Model.DatabaseTables import engine, MapTables, tableDictRefinitiv, tableDictVodafone

from Model.DatabaseTables import engine, DynamicTable

# Pull data full name from input table
def fnameResult(extable):
    firstName = []
    lastName = []
    fullName = []
    DBSession = sessionmaker(bind=engine)
    Base = declarative_base()
    session = DBSession()
    dynamicDict = {}
    inspector = inspect(engine)
    columns = inspector.get_columns(extable)
    if not any(d['name'] == 'TCKN' for d in columns):
        dynamicDict = tableDictRefinitiv(extable)
    else:
        dynamicDict = tableDictVodafone(extable)

    dynamicTableClass = type(extable, (Base,), dynamicDict)

    Base.metadata.create_all(engine)
    sqlQuery = session.query(dynamicTableClass)
    for queryResult in sqlQuery:
        if not any(d['name'] == 'TCKN' for d in columns):
            firstName.append(queryResult.FIRST_NAME)
            lastName.append(queryResult.LAST_NAME)
        else : 
            firstName.append(queryResult.FirstName)
            lastName.append(queryResult.LastName)
        fullName.append(queryResult.NAME)
    return firstName, lastName, fullName

def queryToList(sqlQuery):
    result = []
    try:
        for test in sqlQuery:
            instance = inspect(test)
            items = instance.attrs.items()
            result.append([x.value for _, x in items])
        return instance.attrs.keys(), result
    except:
        return []

def queryToList2(sqlQuery, matchScore, table):
    result = []
    try:
        for test in sqlQuery:
            instance = inspect(test)
            items = instance.attrs.items()
            result.append(np.append([x.value for _, x in items], [matchScore, table]))
        return instance.attrs.keys(), result
    except:
        return [], []


def returnDf(column, data, score, table):
    dfMatch = pd.DataFrame.from_records(data, columns=column)
    dfMatch["MATCH_SCORE"] = score
    dfMatch["MATCH_TABLE"] = table

    return dfMatch