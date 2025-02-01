from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import BIGINT, INT, SMALLINT, FLOAT, String, BOOLEAN
from sqlalchemy.schema import Sequence, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from Database.db import Db_Base, Db_engine
from General.constants import TableNames as TbNames
from General.constants import FieldNames as FldNames
from General.constants import Consts, OnDelete


class Authors(Db_Base):

    __tablename__ = TbNames.Authors

    # author_id_init_seq = Sequence(
    #     '{}_authorid_seq'.format(TbNames.Authors), start=100000001)
    id = Column(FldNames.ID, BIGINT,
                #  _user_id_init_seq,
                primary_key=True, autoincrement=True, nullable=False)
    name = Column(FldNames.Name, String, nullable=True)
    created_at = Column(FldNames.CreatedAt, TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(FldNames.UpdatedAt, TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    deleted_at = Column(FldNames.DeletedAt, TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Books(Db_Base):

    __tablename__ = TbNames.Books
    id = Column(FldNames.ID, BIGINT,
                primary_key=True, autoincrement=True, nullable=False)
    author_id = Column(FldNames.AuthorID, BIGINT, ForeignKey('{}.{}'.format(TbNames.Authors, FldNames.ID),
                                                             ondelete=OnDelete.CASCADE),
                       nullable=False)
    publisher_id = Column(FldNames.PublisherID, BIGINT, ForeignKey('{}.{}'.format(TbNames.Publishers, FldNames.ID),
                                                                   ondelete=OnDelete.NULL),
                          nullable=False)
    title = Column(FldNames.Title, String, nullable=True)
    isbn = Column(FldNames.ISBN, String, nullable=True)
    year = Column(FldNames.Year, SMALLINT, nullable=True)
    created_at = Column(FldNames.CreatedAt, TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(FldNames.UpdatedAt, TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    deleted_at = Column(FldNames.DeletedAt, TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Publishers(Db_Base):

    __tablename__ = TbNames.Publishers

    id = Column(FldNames.ID, BIGINT,
                primary_key=True, autoincrement=True, nullable=False)
    name = Column(FldNames.Name, String, nullable=True)
    created_at = Column(FldNames.CreatedAt, TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(FldNames.UpdatedAt, TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    deleted_at = Column(FldNames.DeletedAt, TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


Db_Base.metadata.create_all(bind=Db_engine)
