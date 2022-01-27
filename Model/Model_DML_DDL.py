from sqlalchemy.orm import sessionmaker
from Model.DatabaseTables import engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Drop before write
def dropTempTable(tempTable):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    session.execute(f"DROP TABLE IF EXISTS {tempTable}")
    session.commit()
    session.close()
