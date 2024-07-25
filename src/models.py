from sqlalchemy import Table, Column, Integer,  MetaData, VARCHAR, ForeignKey, func, TIMESTAMP, Index
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
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

resumes_table = Table(
    "resumes",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("title", VARCHAR(40)),
    Column("compensation", Integer, nullable=True),
    Column("workload", VARCHAR(40)),
    Column("worker_id", ForeignKey("workers.id", ondelete="CASCADE")),
    Column("created_at", TIMESTAMP, server_default=func.current_timestamp()),
    Column("updated_at", TIMESTAMP, server_default=func.current_timestamp(),
           onupdate=datetime.now()),
)

# конструктор типов для сокращения кода
intpk = Annotated[int, mapped_column(primary_key=True)]
strmy = Annotated[str, mapped_column(VARCHAR(40))]


class WorkersOrm(Base):  # декларативный стиль
    __tablename__ = "workers"

    id: Mapped[intpk]
    username: Mapped[strmy]

    resumes: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker", # нужен для того, чтобы были правильные ссылки между relationship
    )

    resumes_parttime: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="worker", # нужен для того, чтобы были правильные ссылки между relationship
        primaryjoin="and_(WorkersOrm.id == ResumesOrm.worker_id, ResumesOrm.workload == 'parttime')" ,# подгрузка только таких резюме
        order_by="ResumesOrm.id.desc()",
        # lazy="" # неявное указание подгрузки (так не делать)
    )

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
        default=datetime.now() ,
        server_default=func.current_timestamp()
    )  # первый default - пайтон отправляет в БД,  а во втором БД сама обновляется
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp(),
        onupdate=datetime.now()  # в случае обновления БД
    )

    worker: Mapped["WorkersOrm"] = relationship(
        back_populates="resumes"
    )

    __table_args__ = (
        Index("title_index", "title") # Можно использовать для добавления  индексов, превичных ключей проверок и прочеее
    )