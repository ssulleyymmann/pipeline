from nis import match
from statistics import mean
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from multipledispatch import dispatch
from sqlalchemy import and_, or_, inspect
from sqlalchemy.orm import sessionmaker

from Model.DatabaseTables import engine, MapTables, tableDictRefinitiv, tableDictVodafone
from sqlalchemy import Column, String, BIGINT, VARCHAR, Integer, BLOB, SmallInteger, TEXT, DATETIME, Date
from sqlalchemy.ext.declarative import declarative_base


@dispatch(str, list, list, list, int)
def findFuzzyTableBase(table, firstNameList, lastNameList, fullName, threshold):
    Base = declarative_base()
    result = []
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # Map table name before query
    # MapTables.__table__.name = table

    dynamicDict = {}
    inspector = inspect(engine)
    columns = inspector.get_columns(table)

    if not any(d['name'] == 'TCKN' for d in columns):
        dynamicDict = tableDictRefinitiv(table)
    else:
        dynamicDict = tableDictVodafone(table)

    dynamicTableClass = type(table, (Base,), dynamicDict)

    Base.metadata.create_all(engine)
    dfList = []
    queryList = []
    nameList = []
    reverseNameList = []
    try:
        for raw in range(len(firstNameList)):
            if firstNameList[raw] != None and lastNameList[raw] != None:
                reverseFullName = lastNameList[raw] + " " + firstNameList[raw]
            elif lastNameList[raw] != None and firstNameList[raw] == None:
                reverseFullName = lastNameList[raw]
            elif lastNameList[raw] == None and firstNameList[raw] != None:
                reverseFullName = firstNameList[raw]
            else:
                reverseFullName = ""
            nameList.append(fullName[raw])
            reverseNameList.append(reverseFullName)
            queryList.append(dynamicTableClass.NAME.like("%{}%".format(fullName[raw])))
            queryList.append(dynamicTableClass.NAME.like("%{}%".format(reverseFullName)))
            if not any(d['name'] == 'TCKN' for d in columns):
                queryList.append(dynamicTableClass.ALIASES.like("%{}%".format(fullName[raw])))
                queryList.append(dynamicTableClass.ALIASES.like("%{}%".format(reverseFullName)))
        
        sqlQuery = session.query(dynamicTableClass).filter(or_(query for query in queryList))
        for query in sqlQuery:
            scoreList = []
            for i in range(len(nameList)):
                print(nameList[i])
                scoreList.append(fuzz.token_set_ratio(query.NAME, nameList[i]))
                scoreList.append(fuzz.token_set_ratio(query.NAME, reverseNameList[i]))
                if not any(d['name'] == 'TCKN' for d in columns):
                    scoreList.append(fuzz.token_set_ratio(query.ALIASES, nameList[i]))
                    scoreList.append(fuzz.token_set_ratio(query.ALIASES, reverseNameList[i]))

            matchScore = max(score for score in scoreList)
            print(matchScore)
            if matchScore > threshold:
                instance = inspect(query)
                items = instance.attrs.items()
                result.append(np.append([x.value for _, x in items], [matchScore, table]))
                column = [x.upper() for x in instance.attrs.keys()]
                column.extend(['MATCH_SCORE', 'MATCH_TABLE'])
                dfMatch = pd.DataFrame.from_records(result, columns=column)
                dfList.append(dfMatch)

        resultDf = pd.concat(dfList)
        return resultDf
    except:
        return result
