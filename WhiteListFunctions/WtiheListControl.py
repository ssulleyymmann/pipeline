from multipledispatch import dispatch
from sqlalchemy import or_, and_, func, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

from Model.DatabaseTables import DynamicTable, WhiteList, tableDictVodafone, engine, \
    tableDictRefinitiv
from Model.Model_DML_DDL import session


# White list control table based fullname
@dispatch(list, str)
def whiteListTraccing(whiteList, searchTable):

    excludeWhiteListFirstName = []
    excludeWhiteListLastName = []
    excludeWhiteFullName = []

    externalFirstName = []
    externalLastName = []

    DynamicTable.__table__.name = searchTable

    # Find differences between given table & white list
    for externalQuery in session.query(DynamicTable):
        externalFirstName.append(externalQuery.FIRST_NAME)
        externalLastName.append(externalQuery.LAST_NAME)

    for safeTable in whiteList:
        WhiteList.__table__.name = safeTable

        for exCheckNumber in range(len(externalFirstName)):
            result = session.query(WhiteList).filter(or_(and_(WhiteList.LAST_NAME == externalLastName[exCheckNumber],
                                                              WhiteList.FIRST_NAME == externalFirstName[exCheckNumber]),
                                                         and_(WhiteList.LAST_NAME == externalFirstName[exCheckNumber],
                                                              WhiteList.FIRST_NAME == externalLastName[exCheckNumber])))

            for instance in result:
                excludeWhiteListFirstName.append(instance.FIRST_NAME)
                excludeWhiteListLastName.append(instance.LAST_NAME)
                excludeWhiteFullName.append(instance.NAME)
    return excludeWhiteListFirstName, excludeWhiteListLastName, excludeWhiteFullName


# Vodafone white List Control
def whiteListTraccingVF(whiteList, blacklist):

    Base = declarative_base()
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    inspector = inspect(engine)
    excludeWhiteListName = []
    excludeWhiteListTCKN = []
    excludeWhiteListVKN = []

    externalName = []
    externalTCKN = []
    externalVKN = []

    # Find differences between given table & white list
    for blackResult in blacklist:
        dynamicDict = {}
        dynamicDict = tableDictVodafone(blackResult)

        dynamicTableClass = type(blackResult, (Base,), dynamicDict)
        Base.metadata.create_all(engine)

        for externalQuery in session.query(dynamicTableClass):

            externalName.append(externalQuery.NAME)
            externalTCKN.append(externalQuery.TCKN)
            externalVKN.append(externalQuery.TCKN)

    for safeTable in whiteList:
        dynamicDict = {}
        dynamicDict = tableDictVodafone(safeTable)

        dynamicTableClass = type(safeTable, (Base,), dynamicDict)
        Base.metadata.create_all(engine)

        for exCheckNumber in range(len(externalName)):

            result = session.query(dynamicTableClass).filter(or_(dynamicTableClass.NAME == externalName[exCheckNumber],
                                                                 dynamicTableClass.TCKN == externalTCKN[exCheckNumber],
                                                                 dynamicTableClass.VKN == externalVKN[exCheckNumber]))

            for instance in result:
                excludeWhiteListName.append(instance.NAME)
                excludeWhiteListTCKN.append(instance.TCKN)
                excludeWhiteListVKN.append(instance.VKN)

    return excludeWhiteListName, excludeWhiteListTCKN, excludeWhiteListVKN


def whiteListSingleSearchTraccing(whiteList, fullName):
    excludeWhiteListFullName = []
    Base = declarative_base()
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    inspector = inspect(engine)


    for safeTable in whiteList:
        dynamicDict = {}
        dynamicDict = tableDictRefinitiv(safeTable)
        dynamicTableClass = type(safeTable, (Base,), dynamicDict)
        Base.metadata.create_all(engine)

        for instance in session.query(dynamicTableClass).filter(dynamicTableClass.NAME == fullName):
            excludeWhiteListFullName.append(instance.NAME)
    return excludeWhiteListFullName
