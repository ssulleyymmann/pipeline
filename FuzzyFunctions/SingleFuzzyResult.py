from nis import match
from PreSearchFunctions.Global.GlobalFunctions import queryToList, queryToList2
import numpy as np
import pandas as pd
import sqlalchemy
from flask import jsonify
from fuzzywuzzy import fuzz
from multipledispatch import dispatch
from sqlalchemy import or_, inspect
from sqlalchemy.orm import sessionmaker

from PreSearchFunctions.VodafoneCustomerModel.VFCFunctions import singleInputResult
from Model.DatabaseTables import MapTables, engine, DynamicTable, tableDictRefinitiv, tableDictVodafone
from Model.Model_DML_DDL import dropTempTable
from WhiteListFunctions.WtiheListControl import whiteListSingleSearchTraccing, whiteListTraccingVF
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BIGINT, VARCHAR, Integer, BLOB, SmallInteger, TEXT, DATETIME, Date


def fullNameSearch(fullName, tckn_vkn, threshold, tableList, whiteList, tempTable):
    Base = declarative_base()
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    inspector = inspect(engine)

    firstName = fullName.split(" ", maxsplit=2)[0]
    lastName = fullName.split(" ", maxsplit=1)[1]

    firstNameLike = "{}".format(firstName)  # Not used yet
    lastNameLike = "{}".format(lastName)

    fullnameQuery = "%{}%".format(fullName)

    reverseFullName = lastName + " " + firstName

    dfList = []



    for table in tableList:
        dynamicDict = {}
        columns = inspector.get_columns(table)

        if not any(d['name'] == 'TCKN' for d in columns):
            dynamicDict = tableDictRefinitiv(table)
        else:
            dynamicDict = tableDictVodafone(table)
        
        dynamicTableClass = type(table, (Base,), dynamicDict)

        Base.metadata.create_all(engine)

        sqlQuery = session.query(dynamicTableClass)
        aliasesQuery = session.query(dynamicTableClass)
        if not any(d['name'] == 'TCKN' for d in columns):
            excludeWhiteNameRefinitiv = whiteListSingleSearchTraccing(whiteList, fullName)
            sqlQuery = session.query(dynamicTableClass).filter(
                or_(dynamicTableClass.LAST_NAME.like(lastNameLike), dynamicTableClass.FIRST_NAME.like(firstNameLike),
                    dynamicTableClass.LAST_NAME.like(firstNameLike), dynamicTableClass.FIRST_NAME.like(lastNameLike)))
            aliasesQuery = session.query(dynamicTableClass).filter(
                or_(dynamicTableClass.ALIASES.like("%{}%".format(fullName)),
                    dynamicTableClass.ALIASES.like("%{}%".format(reverseFullName))))
        else:

            sqlQuery = session.query(dynamicTableClass).filter(
                or_(dynamicTableClass.LastName.like(lastNameLike), dynamicTableClass.FirstName.like(firstNameLike)))
            tcknQuery = session.query(dynamicTableClass).filter(
                or_(dynamicTableClass.TCKN == tckn_vkn,dynamicTableClass.VKN == tckn_vkn))
            excludeWhiteListName, excludeWhiteListTCKN, excludeWhiteListVKN = whiteListTraccingVF(whiteList,tableList)
            exMatch,vfId = singleInputResult(tcknQuery,table)



            if isinstance(exMatch,pd.DataFrame):
                exMatch = exMatch[~exMatch['NAME'].isin(excludeWhiteListName)]
                exMatch = exMatch[~exMatch['TCKN'].isin(excludeWhiteListTCKN)]
                exMatch = exMatch[~exMatch['VKN'].isin(excludeWhiteListVKN)]
                dfList.append(exMatch)

        fuzzymatch = singleInputResult(sqlQuery, aliasesQuery, fullName, threshold, table)

        # if isinstance(fuzzymatch, pd.DataFrame):
        #     fuzzymatch = fuzzymatch[~fuzzymatch['NAME'].isin(excludeWhiteNameRefinitiv)]
        if len(fuzzymatch) > 0:
            dfList.append(fuzzymatch)

    if tckn_vkn != -1 and any(d['name'] == 'TCKN' for d in columns):
        result = []
        sqlQuery = session.query(dynamicTableClass).filter(
            or_(dynamicTableClass.TCKN == tckn_vkn, dynamicTableClass.VKN == tckn_vkn))
        column, result = queryToList2(sqlQuery, 100, table)
        column.extend(['MATCH_SCORE', 'MATCH_TABLE'])
        dfMatch = pd.DataFrame.from_records(result, columns=column)
        if isinstance(dfMatch, pd.DataFrame):
            dfList.append(dfMatch)


    if not dfList:
        result = {"table": "empty"}
        return jsonify(result)

    result = pd.concat(dfList)
    result = result.drop_duplicates()
    dbConnection = engine.connect()

    # Drop table before create
    dropTempTable(tempTable)

    result.to_sql(tempTable, dbConnection, if_exists='replace', index=False)

    result = {"table": tempTable}
    return jsonify(result)


# Only single search fullname
@dispatch(sqlalchemy.orm.query.Query, sqlalchemy.orm.query.Query, str, int, str)
def singleInputResult(sqlQuery, aliasesQuery, fullName, threshold, table):
    result = []
    dfList = []
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    inspector = inspect(engine)
    columns = inspector.get_columns(table)
    try:
        for query in sqlQuery:
            query.__table__.name = table
            dbFullName = str(query.NAME)
            matchScore = fuzz.token_set_ratio(dbFullName, fullName)
            if matchScore > threshold:
                instance = inspect(query)
                items = instance.attrs.items()
                result.append(np.append([x.value for _, x in items], [matchScore, table]))
                column = instance.attrs.keys()
                column.extend(['MATCH_SCORE', 'MATCH_TABLE'])
                dfMatch = pd.DataFrame.from_records(result, columns=column)
                dfList.append(dfMatch)

        if not any(d['name'] == 'TCKN' for d in columns):
            for queryAl in aliasesQuery:
                matchScoreAliases = fuzz.token_set_ratio(queryAl.ALIASES, fullName)
                if matchScoreAliases > threshold:
                    instance = inspect(queryAl)
                    items = instance.attrs.items()
                    result.append(np.append([x.value for _, x in items], [matchScore, table]))
                    column = instance.attrs.keys()
                    column.extend(['MATCH_SCORE', 'MATCH_TABLE'])
                    dfMatchAliases = pd.DataFrame.from_records(result, columns=column)
                    dfList.append(dfMatchAliases)
        resultDf = pd.concat(dfList)
        return resultDf
    except:
        return result
