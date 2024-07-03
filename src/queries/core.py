from sqlalchemy import text, insert, select, delete, update
from database import sync_engine, session_factory
from models import metadata_obj, WorkersOrm, Base, workers_table


class SyncCore:
    @staticmethod
    def create_tables():
        sync_engine.echo = False
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)

    @staticmethod
    def insert_data():
        with sync_engine.connect() as conn:
    #         stmt = """INSERT INTO workers (username) VALUES плохой стиль написания запросов (сырой запрос)
    # ('Jack'),
    # ('Michael');
    # """
            stmt = insert(workers_table).values([ # использование query билдера
                {"username": "Bobr"},
                {"username": "Volk"},
            ]
            )
            conn.execute(stmt)
            conn.commit() # коммит обязательно, чтобы обновить базу данных \
    
    @staticmethod
    def select_workers():
        with sync_engine.connect() as conn:
            query = select(workers_table)
            result  = conn.execute(query)
            print(f"{result.all()}")

    @staticmethod
    def update_worker(worker_id : int = 2, new_username : str = "Misha"):
        with sync_engine.connect() as conn:
            # stmt = text("UPDATE workers SET username=:username WHERE id=:id")
            # stmt = stmt.bindparams(username=new_username, id=worker_id) # такой синтакисис с маржовым оператором позвоялет биндить пармаетры
            stmt = (
                update(workers_table)
                .values(username=new_username)
                # .where(workers_table.c.id==worker_id)
                .filter_by(id=worker_id)
            )
            conn.execute(stmt)
            conn.commit()


