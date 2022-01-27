import sqlalchemy
from multipledispatch import dispatch
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker

from PreSearchFunctions.Global.GlobalFunctions import returnDf
from Model.DatabaseTables import engine, VFCustomer


# Pull data full name from VF customers table
def VFfnameResult(dynamicTableClassVF):
    FIRST_NAME = []
    LAST_NAME = []
    FUL_NAME = []
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    for queryResult in session.query(dynamicTableClassVF):
        FIRST_NAME.append(queryResult.FirstName)
        LAST_NAME.append(queryResult.LastName)
        FUL_NAME.append(queryResult.NAME)

    return FIRST_NAME, LAST_NAME, FUL_NAME


# VF Vustomers Only
@dispatch(sqlalchemy.orm.query.Query,str)
def singleInputResult(sqlQuery,table):
    result = []
    id = []
    try:
        for query in sqlQuery:
            instance = inspect(query)
            id.append(query.id)
            items = instance.attrs.items()
            result.append([x.value for _, x in items])
            column = instance.attrs.keys()
            # vf customers will edit next line
            df = returnDf(column, result, 100, table)

        return df, id
    except:
        return result, id
