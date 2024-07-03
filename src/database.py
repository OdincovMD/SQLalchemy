
from sqlalchemy import String, create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from config import settings

sync_engine = create_engine(  # создание синхронного подключения
    url=settings.DATABASE_URL_pymysql,
    # вывод всех запросов в консоль(для понимания, как работает sqlalchemy)
    echo=True,
    # pool_size=5, # пять подклкючений к базе данных максимум
    # max_overflow=10, # дополнительные подключения, если перебор по подключениям
)


session_factory = sessionmaker(sync_engine)  # фабрика сессий


class Base(DeclarativeBase):
    pass
