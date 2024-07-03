from sqlalchemy import Table, Column, Integer,  MetaData, VARCHAR, ForeignKey, func
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
# import enum
from datetime import datetime
from typing import Annotated


metadata_obj = MetaData()

workers_table = Table(  # императивный стиль
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", VARCHAR(20))
)


# конструктор типов для сокращения кода
intpk = Annotated[int, mapped_column(primary_key=True)]
strmy = Annotated[str, mapped_column(VARCHAR(20))]


class WorkersOrm(Base):  # декларативный стиль
    __tablename__ = "workers"

    id: Mapped[intpk]
    username: Mapped[strmy]

# class Workload(enum):
#     parttime = "partitme"
#     fulltime = "fulltime"


class ResumesOrm(Base):
    __tablename__ = "resumes"

    id: Mapped[intpk]
    title: Mapped[strmy]
    compensation: Mapped[int | None]  # либо mapped_column(nullable=True)
    workload: Mapped[strmy] = mapped_column(default="partitme")
    worker_id: Mapped[int] = mapped_column(
        ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(
        default=0,
        server_default=func.current_timestamp()
    )  # первый default - пайтон отправляет в БД,  а во втором БД сама обновляется
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp(),
        onupdate=datetime.now()  # в случае обновления БД
    )
