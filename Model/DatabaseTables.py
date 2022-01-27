# import cx_Oracle

from sqlalchemy import Column, String, BIGINT, VARCHAR, Integer, BLOB, SmallInteger, TEXT, DATETIME, Date
from sqlalchemy.dialects.oracle import NUMBER, VARCHAR2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from os import environ as env
from dotenv import load_dotenv
import pymysql

load_dotenv()
CONNECTION = env["DB_URI"]

# engine = create_engine(f'oracle+cx_oracle://{user}:{pwd}@{dsn}', echo=True)

# engine.current_schema = "SYSTEM"
engine = create_engine(CONNECTION)
Base = declarative_base()
Base.metadata.create_all(engine)


class DynamicTable(Base):
    __tablename__ = ""
    UID = Column(Integer, primary_key=True)
    LAST_NAME = Column(VARCHAR(255))
    FIRST_NAME = Column(VARCHAR(255))
    ALIASES = Column(TEXT)
    LOW_QUALITY_ALIASES = Column(TEXT)
    ALTERNATIVE_SPELLING = Column(TEXT)
    CATEGORY = Column(TEXT)
    TITLE = Column(TEXT)
    SUB_CATEGORY = Column(TEXT)
    POSITION = Column(TEXT)
    AGE = Column(SmallInteger)
    DOB = Column(VARCHAR(12))
    PLACE_OF_BIRTH = Column(TEXT)
    DECEASED = Column(TEXT)
    PASSPORTS = Column(TEXT)
    SSN = Column(TEXT)
    LOCATIONS = Column(TEXT)
    COUNTRIES = Column(TEXT)
    COMPANIES = Column(TEXT)
    E_I = Column(TEXT)
    LINKED_TO = Column(TEXT)
    FURTHER_INFORMATION = Column(TEXT)
    KEYWORDS = Column(TEXT)
    EXTERNAL_SOURCES = Column(TEXT)
    UPDATE_CATEGORY = Column(TEXT)
    ENTERED = Column(TEXT)
    UPDATED = Column(TEXT)
    EDITOR = Column(TEXT)
    AGE_DATE_AS_OF_DATE = Column(TEXT)
    PEP_ROLES = Column(TEXT)
    PEP_STATUS = Column(TEXT)
    NOTE = Column(TEXT)
    NAME = Column(TEXT)


class MapTables(Base):
    __tablename__ = "MapTableName"
    UID = Column(Integer, primary_key=True)
    LAST_NAME = Column(VARCHAR(255))
    FIRST_NAME = Column(VARCHAR(255))
    ALIASES = Column(TEXT)
    LOW_QUALITY_ALIASES = Column(TEXT)
    ALTERNATIVE_SPELLING = Column(TEXT)
    CATEGORY = Column(TEXT)
    TITLE = Column(TEXT)
    SUB_CATEGORY = Column(TEXT)
    POSITION = Column(TEXT)
    AGE = Column(SmallInteger)
    DOB = Column(VARCHAR(12))
    PLACE_OF_BIRTH = Column(TEXT)
    DECEASED = Column(TEXT)
    PASSPORTS = Column(TEXT)
    SSN = Column(TEXT)
    LOCATIONS = Column(TEXT)
    COUNTRIES = Column(TEXT)
    COMPANIES = Column(TEXT)
    E_I = Column(TEXT)
    LINKED_TO = Column(TEXT)
    FURTHER_INFORMATION = Column(TEXT)
    KEYWORDS = Column(TEXT)
    EXTERNAL_SOURCES = Column(TEXT)
    UPDATE_CATEGORY = Column(TEXT)
    ENTERED = Column(TEXT)
    UPDATED = Column(DATETIME)
    EDITOR = Column(TEXT)
    AGE_DATE_AS_OF_DATE = Column(TEXT)
    PEP_ROLES = Column(TEXT)
    PEP_STATUS = Column(TEXT)
    NOTE = Column(TEXT)
    NAME = Column(TEXT)


class WhiteList(Base):
    __tablename__ = "WHITE_LIST"
    UID = Column(Integer, primary_key=True)
    LAST_NAME = Column(VARCHAR(255))
    FIRST_NAME = Column(VARCHAR(255))
    ALIASES = Column(TEXT)
    LOW_QUALITY_ALIASES = Column(TEXT)
    ALTERNATIVE_SPELLING = Column(TEXT)
    CATEGORY = Column(TEXT)
    TITLE = Column(TEXT)
    SUB_CATEGORY = Column(TEXT)
    POSITION = Column(TEXT)
    AGE = Column(SmallInteger)
    DOB = Column(VARCHAR(12))
    PLACE_OF_BIRTH = Column(TEXT)
    DECEASED = Column(TEXT)
    PASSPORTS = Column(TEXT)
    SSN = Column(TEXT)
    LOCATIONS = Column(TEXT)
    COUNTRIES = Column(TEXT)
    COMPANIES = Column(TEXT)
    E_I = Column(TEXT)
    LINKED_TO = Column(TEXT)
    FURTHER_INFORMATION = Column(TEXT)
    KEYWORDS = Column(TEXT)
    EXTERNAL_SOURCES = Column(TEXT)
    UPDATE_CATEGORY = Column(TEXT)
    ENTERED = Column(TEXT)
    UPDATED = Column(TEXT)
    EDITOR = Column(TEXT)
    AGE_DATE_AS_OF_DATE = Column(TEXT)
    PEP_ROLES = Column(TEXT)
    PEP_STATUS = Column(TEXT)
    NOTE = Column(TEXT)
    NAME = Column(TEXT)


class VFCustomer(Base):
    __tablename__ = "vf_customers"

    id = Column(BIGINT, primary_key=True)
    TCKN = Column(BIGINT)
    FirstName = Column(VARCHAR(55))
    LastName = Column(VARCHAR(55))
    City = Column(VARCHAR(255))
    Birth_City = Column(VARCHAR(255))
    Country = Column(VARCHAR(255))
    DOB = Column(Date)
    Current_Country = Column(VARCHAR(255))
    Address = Column(VARCHAR(255))
    Occupation = Column(VARCHAR(255))
    POC = Column(VARCHAR(255))
    createdAt = Column(DATETIME)
    VKN = Column(BIGINT)
    NOTE = Column(TEXT)
    NAME = Column(TEXT)


def tableDictRefinitiv(tableName):
    dynamicDict = {'__tablename__': tableName,
                   'UID': Column(Integer, primary_key=True),
                   'LAST_NAME': Column(VARCHAR(255)),
                   'FIRST_NAME': Column(VARCHAR(255)),
                   'ALIASES': Column(TEXT),
                   'LOW_QUALITY_ALIASES': Column(TEXT),
                   'ALTERNATIVE_SPELLING': Column(TEXT),
                   'CATEGORY': Column(TEXT),
                   'TITLE': Column(TEXT),
                   'SUB_CATEGORY': Column(TEXT),
                   'POSITION': Column(TEXT),
                   'AGE': Column(SmallInteger),
                   'DOB': Column(VARCHAR(12)),
                   'PLACE_OF_BIRTH': Column(TEXT),
                   'DECEASED': Column(TEXT),
                   'PASSPORTS': Column(TEXT),
                   'SSN': Column(TEXT),
                   'LOCATIONS': Column(TEXT),
                   'COUNTRIES': Column(TEXT),
                   'COMPANIES': Column(TEXT),
                   'E_I': Column(TEXT),
                   'LINKED_TO': Column(TEXT),
                   'FURTHER_INFORMATION': Column(TEXT),
                   'KEYWORDS': Column(TEXT),
                   'EXTERNAL_SOURCES': Column(TEXT),
                   'UPDATE_CATEGORY': Column(TEXT),
                   'ENTERED': Column(TEXT),
                   'UPDATED': Column(TEXT),
                   'EDITOR': Column(TEXT),
                   'AGE_DATE_AS_OF_DATE': Column(TEXT),
                   'PEP_ROLES': Column(TEXT),
                   'PEP_STATUS': Column(TEXT),
                   'NOTE': Column(TEXT),
                   'NAME': Column(TEXT),
                   }
    return dynamicDict


def tableDictVodafone(tableName):
    dynamicDict = {'__tablename__': tableName,
                   'id': Column(BIGINT, primary_key=True),
                   'TCKN': Column(BIGINT),
                   'FirstName': Column(VARCHAR(55)),
                   'LastName': Column(VARCHAR(55)),
                   'City': Column(VARCHAR(255)),
                   'Birth_City': Column(VARCHAR(255)),
                   'Country': Column(VARCHAR(255)),
                   'DOB': Column(Date),
                   'Current_Country': Column(VARCHAR(255)),
                   'Address': Column(VARCHAR(255)),
                   'Occupation': Column(VARCHAR(255)),
                   'POC': Column(VARCHAR(255)),
                   'createdAt': Column(DATETIME),
                   'VKN': Column(BIGINT),
                   'NOTE': Column(TEXT),
                   'NAME': Column(TEXT),
                   }
    return dynamicDict
