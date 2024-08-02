from models import Base, WorkersOrm, ResumesOrm, VacanciesOrm, Workload
from database import session_factory, sync_engine
from sqlalchemy import select, insert, func, cast, Integer, and_
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager
from schemas import WorkersRelDTO, ResumesRelVacanciesRepliedWithoutVacancyCompensationDTO


class SyncOrm:
    @staticmethod
    def create_tables():
        # sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def insert_data():
        worker_1 = WorkersOrm(username="Василий")
        worker_2 = WorkersOrm(username="Михаил")
        with session_factory() as session:
            session.add(worker_1)  # добавление в сессию unit of work
            session.add(worker_2)
            session.flush()  # отправляет все данные в базу данных, но не обновляет базу данных
            session.commit()

    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            resume_vas_1 = ResumesOrm(
                title="Python Junior Developer", compensation=50000, workload=Workload.parttime, worker_id=1)
            resume_vas_2 = ResumesOrm(
                title="Python Разработчик", compensation=150000, workload=Workload.fulltime, worker_id=1)
            resume_mic_1 = ResumesOrm(
                title="Python Data Engineer", compensation=250000, workload=Workload.fulltime, worker_id=2)
            resume_mic_2 = ResumesOrm(
                title="Data Scientist", compensation=300000, workload=Workload.parttime, worker_id=2)
            session.add_all([resume_vas_1, resume_vas_2,
                             resume_mic_1, resume_mic_2])
            session.commit()

    @staticmethod
    def insert_additional_resumes():
        with session_factory() as session:
            workers = [
                {"username": "Artem"},  # id 3
                {"username": "Roman"},  # id 4
                {"username": "Petr"},   # id 5
            ]
            resumes = [
                {"title": "Python программист", "compensation": 60000,
                    "workload": Workload.parttime, "worker_id": 3},
                {"title": "Machine Learning Engineer", "compensation": 70000,
                    "workload": Workload.fulltime, "worker_id": 3},
                {"title": "Python Data Scientist", "compensation": 80000,
                    "workload": Workload.fulltime, "worker_id": 4},
                {"title": "Python Analyst", "compensation": 90000,
                    "workload": Workload.fulltime, "worker_id": 4},
                {"title": "Python Junior Developer", "compensation": 100000,
                    "workload": Workload.parttime, "worker_id": 5},
            ]
            insert_workers = insert(WorkersOrm).values(workers)
            insert_resumes = insert(ResumesOrm).values(resumes)
            session.execute(insert_workers)
            session.execute(insert_resumes)
            session.commit()

    @staticmethod
    def select_data():
        with session_factory() as session:
            # worker_id = 1
            # worker_jack = session.get(WorkersOrm, worker_id) # один работник те одна сущность
            query = select(WorkersOrm)
            result = session.execute(query)
            print(f"{result.scalars().all()}")

    @staticmethod
    def update_worker(worker_id: int = 2, new_username: str = "Михаил"):
        with session_factory() as session:
            worker_michael = session.get(WorkersOrm, worker_id)
            worker_michael.username = new_username
            # session.expire_all(worker_michael) # сбрасывает все изменения
            # session.refresh(worker_michael) # обновление до состояния, которое находится в базе данных
            session.commit()

    @staticmethod
    def select_resumes_avg():
        with session_factory() as session:
            query = (
                select(ResumesOrm.workload,
                       cast(func.avg(ResumesOrm.compensation), Integer).label("avg_comp"))
                       .select_from(ResumesOrm).filter(and_(
                           ResumesOrm.title.contains("Python"),
                           ResumesOrm.compensation > 40000
                       )).group_by(ResumesOrm.workload)
            )
            # print(query.compile(compile_kwargs={"literal_binds" : True}))
            result = session.execute(query)
            print(result.all())
    
    @staticmethod
    def join_cte_subquery_window_func(like_language : str = "Python"):
        with session_factory() as session:
            r = aliased(ResumesOrm)
            w = aliased(ResumesOrm)
            subq = (
                select(
                    r, 
                    w,
                    func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label("avg_py")
                )
                .select_from(w)
                .join(r, r.worker_id == w.id).subquery("helper1") # full = True - cross, isouter= True - левый
            )
            cte = (
                select(
                    subq.c.worker_id,
                    subq.c.compensation,
                    subq.c.workload,
                    subq.c.avg_py,
                    (subq.c.compensation - subq.c.avg_py).label("comp_diff")
                )
                .subquery("helper2")
            )
            query = (
                select(cte).
                order_by(cte.c.comp_diff.desc())
            )
            # print(query.compile(compile_kwargs={"literal_binds" : True}))
            result = session.execute(query)
            print(result.all())

    @staticmethod
    def select_workers_with_lazy_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm).
                options(joinedload(WorkersOrm.resumes)) #  подходит только для загрузки one to one; many to one
            ) # проблема n+1 запроса(ленивый вид подгрузки) #  ленивая подругзка не используется при  assyn (всегда прописывать options)
            result = session.execute(query)
            result = result.unique().scalars().all() #только уникальные первичные ключи

            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)

    @staticmethod
    def select_workers_with_select_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm).
                options(selectinload(WorkersOrm.resumes)) # меньше гоняется трафика подходит для для one to many; many to many
            ) # проблема n+1 запроса(ленивый вид подгрузки)
            result = session.execute(query)
            result = result.unique().scalars().all() #только уникальные первичные ключи

            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)

    @staticmethod
    def select_workers_with_condition_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm).
                options(selectinload(WorkersOrm.resumes_parttime)) 
            )
            result = session.execute(query)
            result = result.unique().scalars().all() #только уникальные первичные ключи

            print(result)

    @staticmethod
    def select_workers_with_contains_eager_relationship():
        with session_factory() as session:
            query = (
                select(WorkersOrm).
                join(WorkersOrm.resumes).
                options(contains_eager(WorkersOrm.resumes)) #  резюме есть(уже подгрузили), sql их подтянет из таблицы, и сделает структуру вложенной(для указания  limit необходимо создать подзапрос и его уже связать с  contains_eager)
            )
            result = session.execute(query)
            result = result.unique().scalars().all() #только уникальные первичные ключи

            print(result)

    @staticmethod
    def convert_workers_to_dto():
        with session_factory() as session:
            query = (
                select(WorkersOrm)
                .options(selectinload(WorkersOrm.resumes))
                .limit(2)
            )

            res = session.execute(query)
            result_orm = res.scalars().all()
            print(f"{result_orm=}")
            result_dto = [WorkersRelDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto
        
    @staticmethod
    def add_vacancies_and_replices():
        with session_factory() as session:
            new_vacancy = VacanciesOrm(title="Python разработчик", compensation=100000)
            resume_1 = session.get(ResumesOrm, 1)
            resume_2 = session.get(ResumesOrm, 2)
            resume_1.vacancies_replied.append(new_vacancy)
            resume_2.vacancies_replied.append(new_vacancy)
            session.commit()

    @staticmethod
    def select_resumes_with_all_relationship():
        with session_factory() as session:
            query  = (
                select(ResumesOrm)
                .options(joinedload(ResumesOrm.worker))
                .options(selectinload(ResumesOrm.vacancies_replied).load_only(VacanciesOrm.title)) # только название
            )

            res = session.execute(query)
            result_orm = res.scalars().all()
            print(f"{result_orm=}")
            result_dto = [ResumesRelVacanciesRepliedWithoutVacancyCompensationDTO.model_validate(row, from_attributes=True) for row in result_orm]
            print(f"{result_dto=}")
            return result_dto