from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import BIGINT, INT, SMALLINT, FLOAT, String, BOOLEAN
from sqlalchemy.schema import Sequence, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from General.constants import TableNames as TbNames
from General.constants import FieldNames as FldNames
from General.constants import Consts, OnDelete
from Database.db import Db_Base, Db_engine

# Db_Base.metadata.create_all(bind=Db_engine)
