from sqlalchemy import text, insert, select, delete, update
from database import sync_engine, session_factory
from models import metadata_obj, WorkersOrm, Base, workers_table, resumes_table


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
            stmt = insert(workers_table).values([  # использование query билдера
                {"username": "Bobr"},
                {"username": "Volk"},
            ]
            )
            conn.execute(stmt)
            conn.commit()  # коммит обязательно, чтобы обновить базу данных \

    @staticmethod
    def insert_resumes():
        with sync_engine.connect() as conn:
            resumes = [
                {"title": "Python Junior Developer", "compensation": 50000,
                    "workload": "fulltime", "worker_id": 1},
                {"title": "Python Разработчик", "compensation": 150000,
                    "workload": "fulltime", "worker_id": 1},
                {"title": "Python Data Engineer", "compensation": 250000,
                    "workload": "fulltime", "worker_id": 2},
                {"title": "Data Scientist", "compensation": 300000,
                    "workload": "fulltime", "worker_id": 2},
            ]
            stmt = insert(resumes_table).values(resumes)
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def insert_additional_resumes():
        with sync_engine.connect() as conn:
            workers = [
                {"username": "Artem"},  # id 3
                {"username": "Roman"},  # id 4
                {"username": "Petr"},   # id 5
            ]
            resumes = [
                {"title": "Python программист", "compensation": 60000,
                    "workload": "fulltime", "worker_id": 3},
                {"title": "Machine Learning Engineer", "compensation": 70000,
                    "workload": "parttime", "worker_id": 3},
                {"title": "Python Data Scientist", "compensation": 80000,
                    "workload": "parttime", "worker_id": 4},
                {"title": "Python Analyst", "compensation": 90000,
                    "workload": "fulltime", "worker_id": 4},
                {"title": "Python Junior Developer", "compensation": 100000,
                    "workload": "fulltime", "worker_id": 5},
            ]
            insert_workers = insert(workers_table).values(workers)
            insert_resumes = insert(resumes_table).values(resumes)
            conn.execute(insert_workers)
            conn.execute(insert_resumes)
            conn.commit()

    @staticmethod
    def select_workers():
        with sync_engine.connect() as conn:
            query = select(workers_table)
            result = conn.execute(query)
            print(f"{result.all()}")

    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Misha"):
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
