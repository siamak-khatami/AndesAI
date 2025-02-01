from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import BIGINT, INT, SMALLINT, FLOAT, String, BOOLEAN
from sqlalchemy.schema import Sequence, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from General.constants import TableNames as TbNames
from General.constants import FieldNames as FldNames
from General.constants import Consts, OnDelete
from Database.db import Db_Base, Db_engine


class UserTbModel(Db_Base):

    __tablename__ = TbNames.Users

    user_id_init_seq = Sequence(
        '{}_userid_seq'.format(TbNames.Users), start=100000001)
    #
    user_id = Column(FldNames.UserID, BIGINT, user_id_init_seq, primary_key=True, autoincrement=True,
                     nullable=False, server_default=user_id_init_seq.next_value())
    email = Column(FldNames.Email, String, nullable=False, unique=True)
    user_public_id = Column(FldNames.UserPubID, String, nullable=True, unique=True)
    name = Column(FldNames.Name, String, nullable=True)
    family = Column(FldNames.Family, String, nullable=True)
    country_iso = Column(FldNames.CountryIso, String, nullable=True)
    mobile = Column(FldNames.Mobile, String, nullable=True)
    password = Column(FldNames.Password, String, nullable=False)
    # one_time_password = Column(FldNames.OneTimePass, String, nullable=True)
    registration_time = Column(FldNames.RegTime, TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # TODO: add lastchekin db to the system
    is_enabled = Column(FldNames.IsEnabled, BOOLEAN, nullable=False, server_default='True')
    # If email activation, default should be False


class UserTours(Db_Base):
    __tablename__ = TbNames.UserTours
    tour_id = Column(FldNames.TourID, BIGINT, primary_key=True, autoincrement=True, nullable=False)
    tour_name = Column(FldNames.TourName, String, nullable=True, unique=True)


class UserTourVisibility(Db_Base):
    """
    In this table we save whether to show a tour to a specific user or not
    """
    __tablename__ = TbNames.UserTourVisibility
    tour_visibility_id = Column("tour_visibility_id", BIGINT, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(FldNames.UserID, BIGINT,
                     ForeignKey('{}.{}'.format(TbNames.Users, FldNames.UserID),
                                ondelete=OnDelete.CASCADE), nullable=False)
    tour_id = Column(FldNames.TourID, BIGINT,
                     ForeignKey('{}.{}'.format(TbNames.UserTours, FldNames.TourID),
                                ondelete=OnDelete.CASCADE), nullable=False)


Db_Base.metadata.create_all(bind=Db_engine)
