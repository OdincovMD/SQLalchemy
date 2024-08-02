
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config import settings

sync_engine = create_engine(  # создание синхронного подключения
    url=settings.DATABASE_URL_pymysql,
    # вывод всех запросов в консоль(для понимания, как работает sqlalchemy)
    # echo=True,
    # pool_size=5, # пять подклкючений к базе данных максимум
    # max_overflow=10, # дополнительные подключения, если перебор по подключениям
)


# async_engine = create_async_engine(
#     url=settings.DATABASE_URL_asyncpg,
#     echo=True,
# )


session_factory = sessionmaker(sync_engine)  # фабрика сессий
# async_session_factory = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    def __repr__(self):
        cols = [f"{col}={getattr(self, col)}" for col in self.__table__.columns.keys()]
        return f"<{self.__class__.__name__} {','.join(cols)}>"