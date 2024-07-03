from models import Base, WorkersOrm
from database import session_factory, sync_engine
from sqlalchemy import select


class SyncOrm:
    @staticmethod
    def create_tables():
        # sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
    
    @staticmethod
    def insert_data():
        worker_bobr = WorkersOrm(username="Bobr")
        worker_volk = WorkersOrm(username="Volk")
        with session_factory() as session:
            session.add(worker_bobr) # добавление в сессию unit of work
            session.add(worker_volk)
            session.flush() # отправляет все данные в базу данных, но не обновляет базу данных
            session.commit()
    
    @staticmethod
    def select_data():
        with session_factory() as session:
            # worker_id = 1
            # worker_jack = session.get(WorkersOrm, worker_id) # один работник те одна сущность
            query = select(WorkersOrm)
            result  = session.execute(query)
            print(f"{result.scalars().all()}")

    @staticmethod
    def update_worker(worker_id : int = 2, new_username : str = "Misha"):
        with session_factory() as session:
            worker_michael = session.get(WorkersOrm, worker_id)
            worker_michael.username = new_username
            # session.expire_all(worker_michael) # сбрасывает все изменения
            # session.refresh(worker_michael) # обновление до состояния, которое находится в базе данных
            session.commit()
            