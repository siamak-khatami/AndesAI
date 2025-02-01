from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import BIGINT, INT, SMALLINT, FLOAT, String, BOOLEAN
from sqlalchemy.schema import Sequence, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from General.constants import TableNames as TbNames
from General.constants import FieldNames as FldNames
from General.constants import Consts, OnDelete
from Database.db import Db_Base, Db_engine


class ProjectsTbModel(Db_Base):
    __tablename__ = TbNames.Projects
    project_id = Column(FldNames.ProjectID, BIGINT, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(FldNames.UserID, BIGINT,
                     ForeignKey('{}.{}'.format(TbNames.Users, FldNames.UserID),
                                ondelete=OnDelete.CASCADE), nullable=False)
    name = Column(FldNames.Name, String, nullable=False)
    registration_time = Column(FldNames.RegTime, TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    is_enabled = Column(FldNames.IsEnabled, BOOLEAN, nullable=True, server_default='True')
    # If email activation, default should be False


class TasksTB(Db_Base):
    __tablename__ = TbNames.TasksTB
    tasks_id = Column(FldNames.TaskID, BIGINT, primary_key=True, autoincrement=True, nullable=False)
    project_id = Column(FldNames.ProjectID, BIGINT,
                        ForeignKey('{}.{}'.format(TbNames.Projects, FldNames.ProjectID),
                                   ondelete=OnDelete.CASCADE), nullable=False)
    task_name = Column(FldNames.TaskName, String, nullable=False, unique=False)
    task_description = Column(FldNames.TaskDescription, String, nullable=False, unique=False)
    task_priority = Column(FldNames.TaskDescription, SMALLINT, nullable=False, default=0)
    task_waiting_times = Column(FldNames.TaskWaitingTime, INT, nullable=False)


class TasksDependencies(Db_Base):
    __tablename__ = TbNames.TasksDependencies
    dependency_id = Column(FldNames.DependencyID, BIGINT, primary_key=True, autoincrement=True, nullable=False)
    dependent_task_id = Column(FldNames.DependentTaskID, BIGINT,
                               ForeignKey('{}.{}'.format(TbNames.TasksTB, FldNames.TaskID),
                                          ondelete=OnDelete.CASCADE), nullable=False)
    independent_task_id = Column(FldNames.InDependentTaskID, BIGINT,
                                 ForeignKey('{}.{}'.format(TbNames.TasksTB, FldNames.TaskID),
                                            ondelete=OnDelete.CASCADE), nullable=False)


class ResourcesTB(Db_Base):
    """
    In this table we save whether to show a tour to a specific user or not
    """
    __tablename__ = TbNames.ResourcesTB
    resource_id = Column(FldNames.ResourceID, BIGINT, primary_key=True, autoincrement=True, nullable=False)
    resource_name = Column(FldNames.ResourceName, String, nullable=False)
    resource_description = Column(FldNames.ResourceDescription, String, nullable=True)
    resource_availability = Column(FldNames.ResourceAvailability, SMALLINT, nullable=False)
    project_id = Column(FldNames.ProjectID, BIGINT,
                        ForeignKey('{}.{}'.format(TbNames.Projects, FldNames.ProjectID),
                                   ondelete=OnDelete.CASCADE), nullable=False)


class TaskResourcesTB(Db_Base):
    __tablename__ = TbNames.TasksResources
    task_resource_id = Column(FldNames.TaskResourceID, BIGINT, primary_key=True, autoincrement=True, nullable=False)
    task_resource_duration = Column(FldNames.TaskResourceDuration, INT, nullable=False)
    task_id = Column(FldNames.TaskID, BIGINT,
                     ForeignKey('{}.{}'.format(TbNames.TasksTB, FldNames.TaskID),
                                ondelete=OnDelete.CASCADE), nullable=False)
    resource_id = Column(FldNames.ResourceID, BIGINT,
                         ForeignKey('{}.{}'.format(TbNames.ResourcesTB, FldNames.ResourceID),
                                    ondelete=OnDelete.NULL), nullable=False)


Db_Base.metadata.create_all(bind=Db_engine)
